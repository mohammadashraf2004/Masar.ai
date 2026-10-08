"""Real-runner security probe suite.

NOT a unit test and not shipped in the runner image: it drives a running
project-runner container through its Unix socket with adversarial learner
jobs and checks that each one is contained. Run it with
backend/scripts/project_runner_security_check.sh, which starts the runner
from the real docker-compose.yml definition (no network, custom seccomp,
SETUID/SETGID only), real PostgreSQL and Redis plus API/frontend/proxy
stand-ins on the compose network, and first runs a positive control proving
those services ARE reachable — by name and by IP — from an ordinary
container. "Unreachable from the runner" is then a real result, not a typo
in a hostname.

    python security_probe.py --socket /run/project-runner/runner.sock \
        --token TOKEN --targets api:8000,db:5432,redis:6379,web:3000
"""
from __future__ import annotations

import argparse
import http.client
import json
import socket
import sys
import time


class UnixHTTPConnection(http.client.HTTPConnection):
    def __init__(self, path: str, timeout: float = 120):
        super().__init__("localhost", timeout=timeout)
        self.path = path

    def connect(self) -> None:
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.settimeout(self.timeout)
        self.sock.connect(self.path)


class Runner:
    def __init__(self, path: str, token: str):
        self.path, self.token = path, token

    def request(self, method: str, url: str, body: dict | None = None) -> tuple[int, dict]:
        conn = UnixHTTPConnection(self.path)
        data = json.dumps(body).encode() if body is not None else None
        headers = {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}
        conn.request(method, url, body=data, headers=headers)
        response = conn.getresponse()
        payload = response.read()
        conn.close()
        return response.status, (json.loads(payload) if payload else {})

    def job(self, mode: str, source: str, *, entry: str | None = None, **extra) -> dict:
        entry = entry or ("analysis/probe.py" if mode == "python" else "sql/probe.sql")
        status, out = self.request("POST", "/v1/jobs", {"job": dict(
            mode=mode, entry=entry, files={entry: source}, template_key="masar-commerce-analysis",
            dirs=["charts"], **extra)})
        if status != 200:
            raise RuntimeError(f"runner HTTP {status}: {out}")
        return out


RESULTS: list[tuple[str, bool, str]] = []


def check(name: str, ok: bool, detail: object = "") -> None:
    RESULTS.append((name, bool(ok), "" if ok else str(detail)[:400]))
    print(("PASS " if ok else "FAIL ") + name + ("" if ok else f"  -- {str(detail)[:400]}"), flush=True)


def contained(out: dict) -> bool:
    """The job did not succeed at the forbidden thing (an error, or a timeout)."""
    return out["status"] in {"error", "timeout"}


def connect_src(host: str, port: int) -> str:
    return (
        "import socket\n"
        f"s = socket.create_connection(({host!r}, {port}), timeout=3)\n"
        "print('CONNECTED')\n"
    )


SYSCALL_PROBE = r'''
import ctypes, errno, json, os
libc = ctypes.CDLL(None, use_errno=True)
results = {}
def call(name, nr, *args):
    ctypes.set_errno(0)
    ret = libc.syscall(nr, *[ctypes.c_long(a) for a in args])
    results[name] = (ret, errno.errorcode.get(ctypes.get_errno(), ctypes.get_errno()))
# x86_64 syscall numbers
call("ptrace_traceme", 101, 0, 0, 0, 0)
call("ptrace_attach_pid1", 101, 16, 1, 0, 0)
call("unshare_user", 272, 0x10000000)
call("unshare_net", 272, 0x40000000)
call("mount", 165, 0, 0, 0, 0, 0)
call("keyctl", 250, 0, 0, 0, 0, 0)
call("add_key", 248, 0, 0, 0, 0, 0)
call("bpf", 321, 0, 0, 0)
call("perf_event_open", 298, 0, 0, -1, -1, 0)
call("io_uring_setup", 425, 1, 0)
call("userfaultfd", 323, 0)
call("personality", 135, 0x0400000)
call("kexec_load", 246, 0, 0, 0, 0)
call("init_module", 175, 0, 0, 0)
call("socket_inet", 41, 2, 1, 0)
call("socket_inet6", 41, 10, 1, 0)
call("socket_netlink", 41, 16, 3, 0)
call("socket_packet", 41, 17, 3, 0)
call("chroot", 161, 0)
call("setns", 308, 0, 0)
print(json.dumps(results))
'''


def run_suite(runner: Runner, targets: list[tuple[str, int]], only: str | None, runtime: str = "runc") -> None:
    def want(section: str) -> bool:
        return only is None or only == section

    if want("network"):
        for host, port in targets:
            out = runner.job("python", connect_src(host, port))
            check(f"network: cannot reach {host}:{port}", contained(out) and "CONNECTED" not in out["stdout"], out)
        for host, port, label in (
            ("169.254.169.254", 80, "cloud metadata (IPv4)"), ("fd00:ec2::254", 80, "cloud metadata (IPv6)"),
            ("1.1.1.1", 443, "internet by IP"), ("8.8.8.8", 53, "public DNS by IP"),
            ("172.17.0.1", 2375, "Docker bridge gateway"), ("host.docker.internal", 80, "Docker host"),
            ("example.com", 443, "internet by name"),
        ):
            out = runner.job("python", connect_src(host, port))
            check(f"network: cannot reach {label}", contained(out) and "CONNECTED" not in out["stdout"], out)
        out = runner.job("python", "import socket\nprint(socket.getaddrinfo('example.com', 443))\n")
        check("network: external DNS does not resolve", contained(out), out)
        out = runner.job("python", "import socket\ns = socket.socket(socket.AF_UNIX)\ns.connect('/run/project-runner/runner.sock')\nprint('CONNECTED')\n")
        check("network: learner cannot reach the runner control socket", contained(out) and "CONNECTED" not in out["stdout"], out)
        out = runner.job("python", "lines = open('/proc/net/dev').read().splitlines()[2:]\n"
                                   "print(sorted(l.split(':')[0].strip() for l in lines))\n")
        check("network: only the loopback interface exists",
              out["status"] == "success" and out["stdout"].strip() in ("['lo']", "[]"), out)

    if want("filesystem"):
        for path, label in (
            ("/proc/1/environ", "runner process environment"), ("/proc/1/root/etc/hostname", "PID 1 root via /proc"),
            ("/run/project-runner/runner.sock", "control socket"),
        ):
            out = runner.job("python", f"print(open({path!r}, 'rb').read()[:50])\n")
            check(f"filesystem: cannot read {label}", contained(out), out)
        out = runner.job("python", "import os\nprint(os.listdir('/jobs'))\n")
        check("filesystem: cannot list other job directories", contained(out), out)
        for target in ("/tmp/x", "/opt/runner/x", "/templates/x", "/etc/x", "/x"):
            out = runner.job("python", f"open({target!r}, 'w').write('x')\n")
            check(f"filesystem: cannot write {target}", contained(out), out)
        out = runner.job("python", "open('data/orders.csv', 'a').write('x')\n")
        check("filesystem: dataset copy is read-only", contained(out), out)
        out = runner.job("python", "open('../../../etc/hostname-copy', 'w').write('x')\n")
        check("filesystem: cannot write outside the workspace via ..", contained(out), out)
        out = runner.job("python", "import os, shutil\nshutil.copy('/bin/true', 'charts/t')\nos.chmod('charts/t', 0o755)\n"
                                   "import subprocess\nsubprocess.run(['./charts/t'], check=True)\nprint('EXECUTED')\n")
        check("filesystem: a binary written to the workspace cannot be executed (noexec)",
              contained(out) and "EXECUTED" not in out["stdout"], out)
        out = runner.job("python", "import os\nprint(os.path.exists('/var/run/docker.sock'), os.path.exists('/run/docker.sock'))\n")
        check("filesystem: no Docker socket", out["status"] == "success" and out["stdout"].strip() == "False False", out)
        out = runner.job("python", "print(open('/proc/self/mountinfo').read())\n")
        # mountinfo field 5 is the mount point, field 6 its per-mount options.
        options = [line.split()[5].split(",") for line in out["stdout"].splitlines()
                   if len(line.split()) > 5 and line.split()[4] == "/templates"]
        check("filesystem: templates mounted read-only",
              out["status"] == "success" and options and all("ro" in o for o in options), options or out)

    if want("identity"):
        out = runner.job("python", "import os\nprint(os.getuid(), os.geteuid(), os.getgid(), os.getgroups())\n")
        check("identity: job runs as uid 10001, no groups", out["status"] == "success" and out["stdout"].strip() == "10001 10001 10001 []", out)
        out = runner.job("python", "print([l for l in open('/proc/self/status') if l.startswith(('CapEff','CapPrm','CapInh','CapAmb','NoNewPrivs','Seccomp:'))])\n")
        text = out["stdout"]
        check("identity: no effective/permitted capabilities",
              "CapEff:\\t0000000000000000" in text and "CapPrm:\\t0000000000000000" in text, out)
        check("identity: no_new_privs set", "NoNewPrivs:\\t1" in text, out)
        out = runner.job("python", "import os\nprint(sorted(k for k in os.environ))\n")
        leaked = [k for k in ("RUNNER_TOKEN", "DATABASE_URL", "SECRET_KEY", "REDIS_URL", "OPENAI_API_KEY", "ANTHROPIC_API_KEY")
                  if k in out["stdout"]]
        check("identity: no application secrets in the environment", out["status"] == "success" and not leaked, out)
        out = runner.job("python", "import os, signal\nos.kill(1, signal.SIGKILL)\n")
        check("identity: cannot signal the runner (PID 1)", contained(out), out)

    if want("seccomp"):
        out = runner.job("python", SYSCALL_PROBE)
        try:
            results = json.loads(out["stdout"].strip())  # untrusted sandbox output: parse, never evaluate
        except ValueError:
            results = {}
        check("seccomp: syscall probe ran", out["status"] == "success" and bool(results), out)
        for name, (ret, err) in sorted(results.items()):
            check(f"seccomp/caps: {name} refused", ret == -1, (ret, err))

    if want("resources"):
        out = runner.job("python", "while True:\n    pass\n")
        check("resources: busy loop stopped (timeout)", out["status"] == "timeout", out)
        out = runner.job("python", "import threading\n"
                         "def spin():\n    while True: pass\n"
                         "[threading.Thread(target=spin, daemon=True).start() for _ in range(8)]\n"
                         "spin()\n")
        check("resources: multi-threaded spin stopped", out["status"] == "timeout", out)
        out = runner.job("python", "import time\ntime.sleep(600)\n")
        check("resources: sleeping job stopped by the wall clock", out["status"] == "timeout", out)
        out = runner.job("python", "x = bytearray(6 * 1024 ** 3)\n")
        check("resources: 6 GB allocation refused", contained(out), out)
        out = runner.job("python", "chunks = []\nwhile True:\n    chunks.append(bytearray(64 * 1024 * 1024))\n")
        check("resources: incremental memory exhaustion contained", contained(out), out)
        out = runner.job("python", "import os\nwhile True:\n    os.fork()\n")
        check("resources: fork bomb contained", contained(out), out)
        out = runner.job("python", "import subprocess\nps = [subprocess.Popen(['sleep', '60']) for _ in range(200)]\n")
        check("resources: process count limited", contained(out), out)
        out = runner.job("python", "for i in range(10**7):\n    print('x' * 200)\n")
        check("resources: stdout flood truncated", out["stdout_truncated"] is True and len(out["stdout"]) < 70_000, {k: out[k] for k in ("status", "stdout_truncated")})
        out = runner.job("python", "import sys\nfor i in range(10**6):\n    sys.stderr.write('e' * 200)\n")
        check("resources: stderr flood truncated", out["stderr_truncated"] is True and len(out["stderr"]) < 70_000, {k: out[k] for k in ("status", "stderr_truncated")})
        out = runner.job("python", "import os\nos.write(1, b'x' * (64 * 1024 * 1024))\nprint('done')\n")
        check("resources: raw fd flood cannot corrupt the result", out["status"] == "success", out["status"])
        out = runner.job("python", "open('charts/big.bin', 'wb').write(b'x' * (64 * 1024 * 1024))\n")
        check("resources: single file size capped", contained(out), out)
        out = runner.job("python", "import os\nfor i in range(64):\n    open(f'charts/f{i}.bin', 'wb').write(b'x' * (6 * 1024 * 1024))\n")
        check("resources: workspace size capped", contained(out), out)
        out = runner.job("python", "for i in range(40000):\n    open(f'charts/e{i}', 'w').close()\n")
        if runtime == "gvisor":
            # gVisor's in-sandbox tmpfs ignores nr_inodes: the file count is
            # bounded only by the sandbox memory cap, the wall clock and the
            # per-job cleanup. Check that cleanup leaves the next job unaffected.
            after = runner.job("python", "import os\nprint(len(os.listdir('.')))\n")
            check("resources: mass file creation is cleaned up before the next job (gVisor: no inode cap)",
                  after["status"] == "success" and int(after["stdout"].strip() or 99) <= 8, after)
        else:
            check("resources: file count capped by the filesystem (inodes)", contained(out),
                  {k: out[k] for k in ("status", "stderr")})
        out = runner.job("python", "for i in range(40):\n    open(f'charts/c{i}.txt', 'w').write('x')\n")
        check("resources: generated-file count capped",
              out["status"] == "success" and len(out["generated_files"]) <= 10 and out["artifacts_truncated"] is True, out)
        out = runner.job("python", "print('alive')\n")
        check("resources: runner healthy after abuse", out["status"] == "success" and out["stdout"].strip() == "alive", out)
        out = runner.job("python", "import os\nprint(sum(1 for p in os.listdir('/proc') if p.isdigit() and 'State:\\tZ' in open(f'/proc/{p}/status').read()))\n")
        check("resources: no zombies left behind", out["status"] == "success" and out["stdout"].strip() == "0", out)

    if want("duckdb"):
        for sql, label in (
            ("SELECT * FROM read_csv('/etc/passwd')", "read_csv outside the workspace"),
            ("SELECT * FROM read_text('/etc/hostname')", "read_text"),
            ("SELECT * FROM glob('/**')", "glob the filesystem"),
            ("COPY orders TO 'charts/out.csv'", "COPY TO a file"),
            ("INSTALL httpfs", "INSTALL an extension"),
            ("LOAD httpfs", "LOAD an extension"),
            ("SET enable_external_access = true", "re-enable external access"),
            ("ATTACH 'charts/x.db' AS x", "ATTACH a database file"),
            ("SELECT * FROM read_csv('https://example.com/x.csv')", "read over HTTP"),
            ("SET lock_configuration = false", "unlock the configuration"),
            ("SELECT * FROM read_blob('data/../../../../etc/passwd')", "read_blob traversal"),
            ("SELECT * FROM read_parquet('/etc/hostname')", "read_parquet outside the workspace"),
            ("SET allowed_directories = ['/']", "widen allowed directories"),
            ("SET memory_limit = '64GB'", "raise the memory limit"),
        ):
            out = runner.job("sql", sql)
            check(f"duckdb: {label} refused", out["status"] == "error", out)
        out = runner.job("sql", "SELECT COUNT(*) AS n FROM orders")
        check("duckdb: normal queries still work", out["status"] == "success" and out["table"]["rows"][0][0] > 0, out)
        out = runner.job("sql", "SELECT * FROM range(100000)")
        check("duckdb: result rows limited", out["status"] == "success" and out["table"]["truncated"] is True
              and len(out["table"]["rows"]) == 500, {k: out.get(k) for k in ("status",)})

    if want("workload"):
        workload = (
            "import pandas as pd, numpy as np, duckdb, matplotlib.pyplot as plt\n"
            "orders = pd.read_csv('data/orders.csv', parse_dates=['order_date'])\n"
            "items = pd.read_csv('data/order_items.csv')\n"
            "m = items.merge(orders, on='order_id').drop_duplicates()\n"
            "monthly = m.groupby(m.order_date.dt.to_period('M'))['quantity'].sum()\n"
            "print(np.linalg.norm(np.arange(10.0)), duckdb.sql(\"select count(*) from 'data/orders.csv'\").fetchall())\n"
            "plt.plot(monthly.index.astype(str), monthly.values); plt.savefig('charts/m.png')\n"
            "print(len(monthly))\n"
        )
        out = runner.job("python", workload)
        check("workload: pandas/numpy/duckdb/matplotlib work under the profile",
              out["status"] == "success" and any(f["path"] == "charts/m.png" for f in out["generated_files"]), out)
        out = runner.job("sql", "WITH c AS (SELECT DISTINCT * FROM orders) SELECT strftime(order_date::DATE, '%Y-%m') m, "
                         "COUNT(*) n, RANK() OVER (ORDER BY COUNT(*) DESC) r FROM c GROUP BY 1 ORDER BY 1")
        check("workload: SQL with CTE/window/date functions works", out["status"] == "success" and len(out["table"]["rows"]) >= 12, out)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--socket", default="/run/project-runner/runner.sock")
    parser.add_argument("--token", required=True)
    parser.add_argument("--targets", default="", help="host:port,... services that must be unreachable")
    parser.add_argument("--only", default=None)
    parser.add_argument("--expect-runtime", default=None)
    args = parser.parse_args()
    runner = Runner(args.socket, args.token)

    for _ in range(60):
        try:
            status, health = runner.request("GET", "/healthz")
            if status == 200:
                break
        except OSError:
            time.sleep(1)
    else:
        print("runner did not become healthy")
        return 2
    print(f"runner runtime: {health.get('runtime')}")
    if args.expect_runtime:
        check(f"runtime is {args.expect_runtime}", health.get("runtime") == args.expect_runtime, health)

    bad = Runner(args.socket, "wrong-token")
    status, _ = bad.request("POST", "/v1/jobs", {"job": {}})
    check("control: a wrong token is refused", status == 401, status)

    targets = []
    for item in filter(None, args.targets.split(",")):
        host, port = item.rsplit(":", 1)
        targets.append((host, int(port)))
    run_suite(runner, targets, args.only, health.get("runtime", "runc"))

    failed = [name for name, ok, _ in RESULTS if not ok]
    print(f"\n{len(RESULTS) - len(failed)}/{len(RESULTS)} passed")
    for name in failed:
        print(f"  failed: {name}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
