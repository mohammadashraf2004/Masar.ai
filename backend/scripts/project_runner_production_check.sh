#!/bin/sh
# Production-host verification for the Project Lab runner under gVisor.
#
# Run ON THE PRODUCTION LINUX HOST, from the repository checkout the stack
# was deployed from, after `runsc` is installed and registered (see
# docs/project-lab.md, "Production host runbook"):
#
#   backend/scripts/project_runner_production_check.sh /etc/masar/production.env
#
# Checks, in order, and stops at the first failure:
#   1. Docker lists the runsc runtime, and a container under it really is gVisor;
#   2. the env file asks for gVisor everywhere (runtime, seccomp profile, both
#      REQUIRE flags, runner backend);
#   3. the compose config gives project-runner `runtime: runsc`;
#   4. the DEPLOYED project-runner container uses runsc and is healthy;
#   5. the API, through the real socket, sees the runner report gVisor;
#   6. the full security probe suite passes under gVisor (throwaway compose
#      project — production containers are not touched);
#   7. a representative capstone slice passes through the deployed API and
#      runner (scripts/project_lab_smoke.py inside the api container).
#
# Read-only for the production stack: it starts nothing in it and changes no
# setting. Exit status 0 only when every step passes.
set -eu

ENV_FILE=${1:?usage: project_runner_production_check.sh /path/to/production.env}
ROOT=$(cd "$(dirname "$0")/../.." && pwd)
COMPOSE="docker compose --env-file $ENV_FILE -f $ROOT/docker-compose.yml -f $ROOT/docker-compose.prod.yml"
step=0
pass() { echo "PASS  $1"; }
fail() { echo "FAIL  $1"; echo; echo "Production-host gVisor verification FAILED at step $step."; exit 1; }
next() { step=$((step + 1)); echo; echo "== $step. $1"; }
env_value() { sed -n "s/^$1=//p" "$ENV_FILE" | tail -1 | tr -d '"'"'"; }

next "Docker knows the runsc runtime"
docker info --format '{{range $name, $_ := .Runtimes}}{{$name}} {{end}}' | grep -qw runsc \
  || fail "runsc is not registered with Docker (/etc/docker/daemon.json, then restart Docker)"
pass "runsc registered"
# gVisor reports a fixed kernel in /proc/version ("...-gvisor ... Sun Jan 10 15:06:54 PST 2016").
# Not dmesg: Docker drops CAP_SYSLOG, so it fails under gVisor too.
docker run --rm --runtime=runsc alpine:3.20 cat /proc/version 2>/dev/null | grep -q "Sun Jan 10 15:06:54 PST 2016" \
  || fail "a container started with --runtime=runsc does not run under gVisor"
pass "a runsc container really is gVisor"

next "The env file requires gVisor everywhere"
[ "$(env_value PROJECT_RUNNER_RUNTIME)" = "runsc" ] || fail "PROJECT_RUNNER_RUNTIME must be runsc"
[ "$(env_value PROJECT_RUNNER_SECCOMP)" = "runner-seccomp-gvisor.json" ] || fail "PROJECT_RUNNER_SECCOMP must be runner-seccomp-gvisor.json"
[ "$(env_value PROJECT_RUNNER_REQUIRE_GVISOR)" = "1" ] || fail "PROJECT_RUNNER_REQUIRE_GVISOR must be 1"
[ "$(env_value PROJECT_LAB_REQUIRE_GVISOR)" = "true" ] || fail "PROJECT_LAB_REQUIRE_GVISOR must be true"
[ "$(env_value PROJECT_RUNNER_PIDS_LIMIT)" -ge 512 ] 2>/dev/null \
  || fail "PROJECT_RUNNER_PIDS_LIMIT must be at least 512 under gVisor (a lower host pid cap lets a fork bomb crash the gVisor sentry)"
backend=$(env_value PROJECT_LAB_EXECUTION_BACKEND)
[ -z "$backend" ] || [ "$backend" = "runner" ] || fail "PROJECT_LAB_EXECUTION_BACKEND must be runner (or unset: compose defaults to runner)"
pass "runtime, seccomp profile, both REQUIRE flags and the pid cap are set"

next "The compose configuration runs project-runner under runsc"
$COMPOSE config --format json | grep -q '"runtime": "runsc"' || fail "compose config has no runtime: runsc for project-runner"
pass "compose config uses runsc"

next "The deployed project-runner container"
cid=$($COMPOSE ps -q project-runner)
[ -n "$cid" ] || fail "project-runner is not running (docker compose up -d project-runner)"
[ "$(docker inspect --format '{{.HostConfig.Runtime}}' "$cid")" = "runsc" ] || fail "the running project-runner container is not using runsc (recreate it)"
[ "$(docker inspect --format '{{.State.Health.Status}}' "$cid")" = "healthy" ] || fail "project-runner is not healthy (docker compose logs project-runner)"
pass "running under runsc and healthy"

next "The API sees a gVisor runner through the socket"
runtime=$($COMPOSE exec -T api python -c '
import http.client, json, os, socket
class C(http.client.HTTPConnection):
    def connect(self):
        self.sock = socket.socket(socket.AF_UNIX); self.sock.settimeout(5)
        self.sock.connect(os.environ["PROJECT_LAB_RUNNER_SOCKET"])
c = C("localhost"); c.request("GET", "/healthz"); print(json.loads(c.getresponse().read())["runtime"])
') || fail "the api container cannot reach the runner socket"
[ "$runtime" = "gvisor" ] || fail "the runner reports runtime '$runtime', not gvisor"
pass "runner reports gvisor to the API"

next "Security probes under gVisor (throwaway compose project)"
sh "$ROOT/backend/scripts/project_runner_security_check.sh" --gvisor || fail "security probes failed under gVisor"
pass "security probes"

next "Representative capstone execution through the deployed API and runner"
$COMPOSE exec -T api python scripts/project_lab_smoke.py || fail "capstone smoke test failed"
pass "capstone smoke test"

echo
echo "Production-host gVisor verification PASSED ($step steps)."
