#!/bin/sh
# Real-runner security check for the Project Lab project-runner.
#
# Starts the runner FROM docker-compose.yml (so the exact shipped settings —
# network_mode: none, seccomp profile, SETUID/SETGID only, read-only root,
# tmpfs limits, pids/memory/CPU caps — are what gets tested), next to the
# real PostgreSQL and Redis services and stand-ins listening as the api,
# frontend and caddy on the compose network. Then:
#
#   1. positive control: an ordinary container on that network CAN reach
#      every one of those services, by name and by IP;
#   2. backend/project_runner/security_probe.py drives the runner over its
#      Unix socket (as uid/gid 1000, like the api) with adversarial learner
#      jobs, including connections to those same names and IPs.
#
# Everything runs under a throwaway compose project (masarsec) and is
# removed afterwards. Needs Docker with Compose v2; no Python on the host.
#
#   backend/scripts/project_runner_security_check.sh            # runc
#   backend/scripts/project_runner_security_check.sh --gvisor   # runsc must be registered with Docker
#
# Exit status: 0 when every probe passes.
set -eu

ROOT=$(cd "$(dirname "$0")/../.." && pwd)
# Docker on Windows (Git Bash) needs a Windows path for bind mounts.
HOST_ROOT=$( (cd "$ROOT" && pwd -W) 2>/dev/null || echo "$ROOT")
PROJECT=masarsec
TOKEN=security-check-token-$(od -An -N12 -tx1 /dev/urandom | tr -d ' \n')
EXPECT=runc
if [ "${1:-}" = "--gvisor" ]; then
  export PROJECT_RUNNER_RUNTIME=runsc PROJECT_RUNNER_SECCOMP=runner-seccomp-gvisor.json PROJECT_RUNNER_REQUIRE_GVISOR=1 \
    PROJECT_RUNNER_PIDS_LIMIT=512
  EXPECT=gvisor
fi
export PROJECT_LAB_RUNNER_TOKEN="$TOKEN" MSYS_NO_PATHCONV=1
COMPOSE="docker compose -p $PROJECT -f $HOST_ROOT/docker-compose.yml"
NET=${PROJECT}_default
SOCK=${PROJECT}_project_runner_socket

cleanup() {
  docker rm -f ${PROJECT}-api ${PROJECT}-frontend ${PROJECT}-caddy >/dev/null 2>&1 || true
  $COMPOSE down -v --remove-orphans >/dev/null 2>&1 || true
}
trap cleanup EXIT INT TERM
cleanup

echo "== starting db, redis and project-runner from docker-compose.yml (runtime: $EXPECT)"
$COMPOSE up -d --build --wait db redis project-runner

for svc in api:8000 frontend:3000 caddy:80; do
  name=${svc%%:*}; port=${svc##*:}
  docker run -d --name ${PROJECT}-$name --network "$NET" --network-alias "$name" \
    python:3.11-slim python -m http.server "$port" >/dev/null
done
sleep 2

echo "== positive control: an ordinary container on $NET reaches every service"
TARGETS=$(docker run --rm --network "$NET" python:3.11-slim python -c '
import socket, sys, time
out = []
for host, port in [("api", 8000), ("db", 5432), ("redis", 6379), ("frontend", 3000), ("caddy", 80)]:
    for _ in range(20):
        try:
            ip = socket.gethostbyname(host)
            socket.create_connection((ip, port), timeout=3).close()
            break
        except OSError:
            time.sleep(1)
    else:
        sys.exit(f"positive control failed: {host}:{port} is not reachable")
    out += [f"{host}:{port}", f"{ip}:{port}"]
print(",".join(out))
')
echo "reachable: $TARGETS"

echo "== probes (as the api's uid/gid, through the socket volume only)"
docker run --rm --network none --user 1000:1000 \
  -v "$SOCK:/run/project-runner" -v "$HOST_ROOT/backend/project_runner:/probe:ro" \
  python:3.11-slim python -I /probe/security_probe.py \
  --token "$TOKEN" --targets "$TARGETS" --expect-runtime "$EXPECT"
