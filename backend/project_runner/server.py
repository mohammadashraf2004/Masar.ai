"""Project Lab runner service.

A deliberately small HTTP-over-Unix-socket service (stdlib only) that executes
Project Lab jobs for the API. Its container (`project-runner` in
docker-compose.yml) has NO network at all (`network_mode: none`): the only
interface is loopback, so neither this service nor any learner job can open a
connection to the Masar API, PostgreSQL, Redis, the frontend, the proxy, the
Docker host, cloud metadata endpoints or the internet. The API reaches it
through a Unix domain socket on a shared volume.

The socket directory is owned by root and the API's group with mode 2750 (set
up in the image, see Dockerfile). The API (group member) can connect; the
`sandbox` user that runs learner code cannot even traverse the directory, so
learner code cannot reach this control channel either.

Jobs run ONE AT A TIME per replica, each as the unprivileged `sandbox` user.
That is what keeps one learner's job from seeing another's files; scale with
replicas, not threads.

    POST /v1/jobs   {"job": {...}}  -> JobOutcome JSON
    GET  /healthz                   -> {"ok": true, "runtime": "..."}

Environment:
  RUNNER_TOKEN            shared bearer token (defence in depth on top of the
                          socket permissions); required unless
                          RUNNER_ALLOW_NO_TOKEN=1 (local development only)
  RUNNER_SOCKET           socket path (default /run/project-runner/runner.sock)
  RUNNER_TEMPLATES_ROOT   read-only project templates (default /templates)
  RUNNER_JOBS_ROOT        tmpfs for job directories (default /jobs)
  RUNNER_SANDBOX_USER     uid that runs learner code (default sandbox)
  RUNNER_REQUIRE_GVISOR   "1": refuse to start unless running under gVisor
  RUNNER_TIMEOUT_SECONDS, RUNNER_CPU_SECONDS, RUNNER_MEMORY_MB,
  RUNNER_MAX_PROCESSES, RUNNER_QUEUE_WAIT_SECONDS
"""
from __future__ import annotations

import hmac
import json
import logging
import os
import socketserver
import stat
import sys
import threading
from http.server import BaseHTTPRequestHandler

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from project_runner.executor import Limits, execute_job  # noqa: E402
from project_runner.runtime import detect_runtime  # noqa: E402

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("project-runner")

TOKEN = os.environ.get("RUNNER_TOKEN", "")
ALLOW_NO_TOKEN = os.environ.get("RUNNER_ALLOW_NO_TOKEN") == "1"
SOCKET_PATH = os.environ.get("RUNNER_SOCKET", "/run/project-runner/runner.sock")
TEMPLATES_ROOT = os.environ.get("RUNNER_TEMPLATES_ROOT", "/templates")
JOBS_ROOT = os.environ.get("RUNNER_JOBS_ROOT", "/jobs")
SANDBOX_USER = os.environ.get("RUNNER_SANDBOX_USER", "sandbox")
REQUIRE_GVISOR = os.environ.get("RUNNER_REQUIRE_GVISOR") == "1"
QUEUE_WAIT = float(os.environ.get("RUNNER_QUEUE_WAIT_SECONDS", "20"))
MAX_BODY = 8 * 1024 * 1024
LIMITS = Limits(
    timeout_seconds=float(os.environ.get("RUNNER_TIMEOUT_SECONDS", "15")),
    cpu_seconds=int(os.environ.get("RUNNER_CPU_SECONDS", "12")),
    memory_mb=int(os.environ.get("RUNNER_MEMORY_MB", "1024")),
    max_processes=int(os.environ.get("RUNNER_MAX_PROCESSES", "32")),
)
RUNTIME = detect_runtime()
_ONE_JOB = threading.Lock()


class Handler(BaseHTTPRequestHandler):
    server_version = "masar-project-runner"
    sys_version = ""

    def address_string(self) -> str:  # a Unix socket peer has no address
        return "uds"

    def _send(self, status: int, body: dict) -> None:
        data = json.dumps(body, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, fmt, *args):  # never echo request bodies
        log.info("%s", fmt % args)

    def _authorized(self) -> bool:
        if not TOKEN:
            return ALLOW_NO_TOKEN
        header = self.headers.get("Authorization", "")
        return hmac.compare_digest(header.encode(), f"Bearer {TOKEN}".encode())

    def do_GET(self):  # noqa: N802
        if self.path == "/healthz":
            self._send(200, {"ok": True, "runtime": RUNTIME})
        else:
            self._send(404, {"error": "not_found"})

    def do_POST(self):  # noqa: N802
        if self.path != "/v1/jobs":
            self._send(404, {"error": "not_found"})
            return
        if not self._authorized():
            self._send(401, {"error": "unauthorized"})
            return
        length = int(self.headers.get("Content-Length") or 0)
        if length <= 0 or length > MAX_BODY:
            self._send(413, {"error": "body_size"})
            return
        try:
            body = json.loads(self.rfile.read(length).decode("utf-8"))
            job = body["job"]
        except (ValueError, KeyError, TypeError):
            self._send(400, {"error": "bad_request"})
            return
        if not _ONE_JOB.acquire(timeout=QUEUE_WAIT):
            log.warning(json.dumps({"event": "job_rejected", "reason": "busy"}))
            self._send(503, {"error": "busy"})
            return
        try:
            outcome = execute_job(
                job, templates_root=TEMPLATES_ROOT, jobs_root=JOBS_ROOT,
                sandbox_user=SANDBOX_USER, limits=LIMITS,
            )
        except Exception:  # noqa: BLE001 - report, never drop the connection
            log.exception("job failed inside the runner")
            self._send(500, {"error": "runner_failure"})
            return
        finally:
            _ONE_JOB.release()
        # Structured and content-free: never the learner's files or output.
        log.info(json.dumps({
            "event": "job", "mode": job.get("mode") if isinstance(job, dict) else None,
            "status": outcome.status, "ms": outcome.execution_ms,
            "stdout_truncated": outcome.stdout_truncated, "stderr_truncated": outcome.stderr_truncated,
        }))
        self._send(200, outcome.to_dict())


class UnixHTTPServer(socketserver.ThreadingMixIn, socketserver.UnixStreamServer):
    daemon_threads = True

    def server_bind(self) -> None:
        directory = os.path.dirname(self.server_address)
        info = os.stat(directory)
        if info.st_mode & stat.S_IRWXO:
            # Learner code runs as an "other" user here: it must not be able to
            # reach this socket. Refuse rather than serve on an open directory.
            raise SystemExit(f"{directory} must not be accessible to other users (mode {oct(info.st_mode)})")
        try:
            os.unlink(self.server_address)
        except FileNotFoundError:
            pass
        super().server_bind()
        # The DIRECTORY is the gate (root:API-gid, 2750, checked above): only
        # root and the API's group can resolve this path at all. The socket
        # itself is world-connectable because under gVisor (--host-uds=create)
        # the host-side socket file is created root:root, so group ownership
        # cannot be relied on.
        os.chmod(self.server_address, 0o666)


def main() -> None:
    if not TOKEN and not ALLOW_NO_TOKEN:
        raise SystemExit("RUNNER_TOKEN must be set (or RUNNER_ALLOW_NO_TOKEN=1 for local development)")
    if os.geteuid() != 0:
        raise SystemExit("the runner must start as root so each job can be dropped to the sandbox user")
    if REQUIRE_GVISOR and RUNTIME != "gvisor":
        raise SystemExit(
            f"RUNNER_REQUIRE_GVISOR=1 but this container runs under {RUNTIME!r}, not gVisor. "
            "Install runsc on the host and set PROJECT_RUNNER_RUNTIME=runsc (see docs/project-lab.md)."
        )
    log.info(json.dumps({"event": "start", "runtime": RUNTIME, "socket": SOCKET_PATH}))
    UnixHTTPServer(SOCKET_PATH, Handler).serve_forever()


if __name__ == "__main__":
    main()
