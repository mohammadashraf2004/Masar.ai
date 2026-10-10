# Masar Project Lab

Guided multi-file projects inside **Challenges**. A learner gets a small
workspace, edits allowed files, runs Python or SQL, and completes tasks only
when a deterministic, server-side **Check Step** passes. No AI runs or grades
anything, and nothing costs credits.

The first project is the Data Analyst capstone, *Masar Commerce — Business
Performance Analysis*: 10 milestones, 29 tasks, 12–18 hours (see
[The Data Analyst capstone](#the-data-analyst-capstone)). Projects for other
tracks reuse everything here.

## Pieces

| Concern | Where |
| --- | --- |
| Content (project → milestones → tasks) | `backend/app/services/project_lab/definitions/`, synced to `lab_projects`, `lab_milestones`, `lab_tasks` by `python -m seeds.seed_project_lab` |
| Starter workspace and datasets | `backend/project_templates/<template_key>/workspace/` |
| Dataset generator | `backend/scripts/generate_masar_commerce_data.py` (deterministic) |
| Learner state | `lab_attempts`, `lab_workspace_files` (editable files only), `lab_task_progress`, `lab_runs`, `lab_submissions`, `lab_artifacts` (generated charts), `lab_execution_leases` |
| Private validators | `backend/app/services/project_lab/validators/` (`masar_commerce_facts.py` computes expected results) |
| Execution | `ProjectExecutionService` (`app/services/project_lab/execution.py`) → `runner`, `local` or `disabled` backend |
| Isolated runner | `backend/project_runner/` (own image; `project-runner` service in `docker-compose.yml`) |
| Seccomp profiles | `backend/project_runner/seccomp/` (generated; see its README) |
| Security probes | `backend/project_runner/security_probe.py`, run by `backend/scripts/project_runner_security_check.sh` |
| API | `/api/v1/project-lab/...` (`app/controllers/project_lab_controller.py`) |
| UI | `/challenges` (Guided projects), `/challenges/projects/[slug]` (`frontend/src/features/project-lab/`) |
| Metrics, alerts, dashboard | `app/core/metrics.py` (`project_lab_*`), `monitoring/prometheus/alerts.yml` (`project_lab` group), Grafana "Project Lab" row |

Tests: `backend/tests/test_project_lab.py` (platform), `test_project_lab_capstone.py`
(every milestone's validators, leases, artifacts, submission), the reference
solution in `backend/tests/project_lab_solutions/` (never in the template),
and `frontend/src/features/project-lab/ProjectLab.test.tsx`.

---

## Security boundary

Learner code is untrusted and never runs in the API process. Read this whole
section before changing `project-runner` in `docker-compose.yml`.

### What the audit found (before this hardening)

The first runner listened on TCP on an internal `lab` network shared with the
API. Probing it with a learner job showed:

* **learner code could reach the Masar API** (`urllib.request.urlopen('http://api:8000/')`
  returned 200) and resolve it by name — the API's network path back into
  Masar was open to every learner;
* the runner kept four capabilities (CHOWN, SETUID, SETGID, KILL);
* only Docker's default seccomp profile applied;
* no per-learner concurrency limit, no runner metrics.

### The boundary now

```
 ┌──────────── api container (appuser, gid 1000) ───────────┐
 │  ProjectExecutionService ── RunnerServiceBackend          │
 │        │ HTTP over a Unix socket + bearer token           │
 └────────┼──────────────────────────────────────────────────┘
          │  named volume project_runner_socket
          │  /run/project-runner  root:1000  mode 2750
 ┌────────┼──────── project-runner container ──────────────┐
 │  network_mode: none  (loopback only — no route anywhere) │
 │  read-only rootfs · seccomp allowlist · SETUID/SETGID    │
 │  no-new-privileges · pids/memory/CPU caps · tini         │
 │  server.py (root) ──► harness.py as uid 10001 "sandbox"  │
 │    one job at a time · rlimits · wall clock · cleanup    │
 └──────────────────────────────────────────────────────────┘
```

* **No network at all.** `network_mode: none` gives the runner only a
  loopback interface, so neither the service nor learner code can open a
  connection to the API, PostgreSQL, Redis, the frontend, Caddy, the Docker
  host, cloud metadata (169.254.169.254 / fd00:ec2::254) or the internet. This
  is enforced by the kernel's network namespace, not by application code; the
  seccomp profile additionally refuses every non-`AF_UNIX` socket.
* **API → runner over a Unix socket** on a shared volume. The directory is
  `root:<api gid>` with mode 2750 (seeded from the runner image), so the API's
  group can connect and the `sandbox` uid cannot even traverse it. The server
  refuses to start if the directory is accessible to "other". A bearer token
  is checked as well (defence in depth); production refuses the compose
  default token.
* **No secrets in the runner.** Its environment is the token and the gVisor
  flag; no database URL, API keys or app settings. The image is built from
  `backend/project_runner/` alone, so it contains no application code.
* **Filesystem.** Read-only root. Templates mounted read-only. Jobs live on a
  tmpfs (`/jobs`, 256 MB, `nr_inodes=16384`, `noexec,nosuid,nodev`, mode 1733:
  each job creates its own directory as `sandbox`; nobody can list the root).
  Datasets are *copied* into each job (read-only), never linked to the template.
* **Identity.** The service starts as root and hands every job to uid 10001
  with no supplementary groups; the job cannot signal the service (PID 1 is
  `tini`) or read `/proc/1/environ`. After each job a cleanup step running as
  `sandbox` deletes its files (including `/dev/shm`) and kills every remaining
  `sandbox` process.

### Linux capabilities

`cap_drop: ALL`, then exactly two added back:

| Capability | Why it is required |
| --- | --- |
| `SETUID` | the root service must switch each job to uid 10001 (`subprocess.Popen(user=...)` → `setresuid`) |
| `SETGID` | the same for the job's gid 10001 and to clear supplementary groups (`setgroups([])`) |

Removed: **CHOWN** (each job directory is now created by the harness itself,
already running as `sandbox`, inside the sticky 1733 jobs root) and **KILL**
(on timeout the cleanup step runs *as* `sandbox` and kills that uid's processes,
so the root service never needs to signal another uid). The `sandbox`
processes have no effective, permitted, inheritable or ambient capabilities and
`no_new_privs` is set (all probed).

### Seccomp

`backend/project_runner/seccomp/runner-seccomp.json` (runc) and
`runner-seccomp-gvisor.json` (runsc): a default-deny (`EPERM`) allowlist of
156 syscalls derived from `strace` of the real runner under the adversarial
probes and a pandas/NumPy/matplotlib/DuckDB workload, plus argument filters:
`clone` without any `CLONE_NEW*` flag, `socket`/`socketpair` for `AF_UNIX`
only, `clone3` → `ENOSYS` under runc (glibc falls back to the filtered
`clone`). Refused and probed: `ptrace`, `unshare`, `setns`, `mount`, `bpf`,
`keyctl`, `add_key`, `perf_event_open`, `io_uring_setup`, `userfaultfd`,
`personality`, `kexec_load`, `init_module`, `chroot`, IPv4/IPv6/netlink/packet
sockets. Derivation and regeneration: `seccomp/README.md`.

### gVisor

**Status: supported and verified locally, not yet verified on the production
host. Learner Python execution must remain disabled there until the host
runbook passes.** The base Compose default stays `runc` for local development,
but production configuration accepts only `disabled`, or `runner` with the
complete gVisor contract.

Verified: gVisor `release-20260928.0` in Docker-in-Docker on Docker Desktop
(WSL2 kernel 6.6): the runner started from `docker-compose.yml` under
`runsc` passes all 96 security probes, and the complete capstone (every task
through the real runner, plus hidden-variant reruns) passes with the API
requiring gVisor. Runs are about 1.5× slower than under runc.

Enabling it on a real host: follow the **Production host runbook** below.
Docker Desktop, WSL2 or Docker-in-Docker results are evidence that the
configuration works, not that a given production host is safe — the runbook's
check script must pass on the host itself.

Production validation fails clearly at four levels: static API configuration
rejects an enabled runner unless it names `runsc`, the gVisor seccomp profile,
both require flags, and at least 512 host PIDs; Docker refuses to start the
runner with an unknown runtime; the runner exits at start-up with
`RUNNER_REQUIRE_GVISOR=1` unless it detects gVisor (`project_runner/runtime.py`);
and the API refuses to finish startup unless the live runner reports gVisor.
It re-checks `/healthz` every minute before jobs and refuses execution
(learners see "unavailable", and `ProjectLabRunnerFailing` fires) if that
attestation later changes. There is no production path from `runsc` to `runc`.

Known differences under gVisor: the gVisor seccomp profile must allow `clone3`
(gVisor ignores the `ENOSYS` return, so threads could not start); namespaces
created that way exist only inside gVisor's user-space kernel, and
`unshare`/`setns` stay refused. gVisor's in-sandbox tmpfs ignores
`nr_inodes`, so under gVisor the file count per job is bounded by the sandbox
memory cap, the wall clock and the per-job cleanup instead (probed).

### Resource and abuse controls

| Limit | Value | Enforced by | Probed / tested |
| --- | --- | --- | --- |
| Wall clock | 15 s per job (runner), 45 s per API request incl. queueing | runner `proc.wait(timeout)` + cleanup kill; httpx timeout | busy loop, multi-thread spin, `sleep(600)` |
| CPU | 12 s CPU per job; 1 CPU per runner container | `RLIMIT_CPU`; compose `cpus` | ✓ |
| Memory | 1 GB address space per job; 1.5 GB per container | `RLIMIT_AS`; compose `mem_limit` | 6 GB alloc, incremental exhaustion |
| Processes | 32 per job uid; 128 per local runc container, at least 512 for production gVisor host headroom | `RLIMIT_NPROC`; compose `pids_limit`; `tini` reaps | fork bomb, 200 `sleep`s, no zombies after |
| Output | 65,536 chars each of stdout/stderr; result stream 24 MB | harness `BoundedBuffer`; raw fds 1/2 → `/dev/null` | flood + raw-fd flood; API returns `stdout_truncated`/`stderr_truncated` |
| File size | 8 MB per file | `RLIMIT_FSIZE` | 64 MB write refused |
| Generated files | 10 returned per run (`artifacts_truncated`); 2 MB per image; 30 kept per attempt | harness, execution service, `save_artifacts` | 40 files → 10 + flag |
| Files per job | 16,384 inodes (runc) | tmpfs `nr_inodes` | 40,000 files refused |
| Job storage | 256 MB tmpfs | compose `tmpfs` size | 384 MB refused |
| Workspace | 1 MB of editable files per attempt; 200,000 chars per file | API (`PROJECT_LAB_MAX_WORKSPACE_BYTES`) | 413 `WORKSPACE_TOO_LARGE` |
| SQL rows | 500 returned (`truncated`) | harness `fetchmany` | 100,000-row query |
| DuckDB | no file access, no extension install/load, settings locked after the datasets load | `enable_external_access=false`, `autoinstall/autoload=false`, `lock_configuration=true` | 14 file/extension/settings escapes refused |

### Concurrency

* **One execution per learner** (Run or Check Step, any attempt, any tab, any
  API worker): `lab_execution_leases` holds one row per user, taken with an
  atomic `INSERT … ON CONFLICT DO UPDATE … WHERE expires_at < now()`. A second
  request is refused with **409 `EXECUTION_IN_PROGRESS`** (counted in
  `project_lab_rejected_total`), so one account occupies at most one runner
  slot. The lease is released in a `finally`; a worker that dies leaves a lease
  that expires after `PROJECT_LAB_EXECUTION_LEASE_SECONDS` (180 s, longer than
  any execution), so state recovers by itself.
* **One job per runner replica.** Jobs queue for the slot up to 20 s
  (`RUNNER_QUEUE_WAIT_SECONDS`), then the runner answers 503 and the learner
  sees "busy, try again". Throughput scales with replicas.
* IP rate limits remain (30 runs, 20 checks, 10 submissions per minute).
* `service.ExecutionGate` is the only lease code: a Redis `SET NX PX` lock or a
  queue can replace it without changing the API or the frontend.

### Observability

* Metrics (fixed label sets, no learner data): `project_lab_executions_total{action,kind,status}`,
  `project_lab_execution_seconds{action}`, `project_lab_checks_total{outcome,error_kind}`,
  `project_lab_validator_failures_total{reason}`, `project_lab_rejected_total{reason}`.
  `status=timeout` counts timeouts, `error` learner runtime errors,
  `infrastructure_error` platform failures.
* Grafana: "Project Lab" row (executions by status, p95 duration, checks and refusals).
* Alerts: `ProjectLabRunnerFailing` (>20% infrastructure errors for 10 min),
  `ProjectLabValidatorBroken` (any validator exception).
* Logs: the API logs `project_lab.execution` with purpose, kind, backend,
  status, duration and truncation flags; the runner logs one JSON line per job
  (mode, status, ms). Neither ever logs file contents, output or captured
  values (tested).

### Security probes

```sh
backend/scripts/project_runner_security_check.sh            # runc
backend/scripts/project_runner_security_check.sh --gvisor   # host with runsc registered
```

The script starts `db`, `redis` and `project-runner` from `docker-compose.yml`
(exact shipped settings) under a throwaway compose project, adds stand-ins
listening as `api`, `frontend` and `caddy`, proves with a positive control
that an ordinary container reaches all five by name and IP, then drives the
runner through its socket as uid 1000 with 96 adversarial probes: reaching
the API/DB/Redis/frontend/proxy by name and IP, cloud metadata (IPv4/IPv6),
the internet by IP and name, external DNS, the Docker gateway and host, the
control socket; reading `/proc/1/environ`, PID 1's root, other jobs, the
host filesystem; writing outside the workspace, executing a dropped binary,
the Docker socket; capabilities, `no_new_privs`, environment secrets,
signalling PID 1; 20 dangerous syscalls; busy loops, sleeps, memory bombs,
fork bombs, process floods, stdout/stderr/raw-fd floods, file size/count/
storage; 14 DuckDB escapes; and a real pandas/NumPy/DuckDB/matplotlib
workload that must still work.

Last results (2026-10-06): **96/96 under runc, 96/96 under gVisor.**

### Remaining production risks

1. **gVisor is not enabled on a real production host** (none is provisioned).
   Until it is, a kernel vulnerability reachable through the 156 allowed
   syscalls would escape the container. Do not represent the Project Lab as
   hardened for large-scale anonymous untrusted execution before gVisor (or a
   microVM) runs in production and the probe script passes there.
2. Jobs of one replica share uid 10001, which is safe because jobs are
   serialized per replica; per-job uids or per-job containers would remove
   that dependency.
3. Throughput is one job per replica with a short queue; a Redis-backed queue
   is the next step before heavy use (the lease interface is ready for it).
4. Lesson **code exercises** run here too: `IsolatedPythonRunner`
   (`app/services/code_execution/`) sends each Run and Check Answer to this
   runner through the same execution service, so they inherit every limit
   and the isolation above. Outside production `PROJECT_LAB_EXECUTION_BACKEND=local`
   runs them in a resource-limited API subprocess instead; production never
   does (`build_backend`: runner, or disabled). Exercises whose libraries the
   runner does not install (PyTorch, FastAPI, ...) and the YAML/Dockerfile/
   shell ones are graded without executing learner code. SQL exercises run
   the learner's query in the API process, in an in-memory SQLite database
   that is query-only, with ATTACH/PRAGMA/transactions denied by an
   authorizer, a heap limit, a progress-handler time limit and a 500-row cap
   (`code_grading/sql_grader.py`). Live Python execution therefore waits on
   the same production-host runbook below.
5. If the host loses `runsc` while the env file still names it (a manual
   uninstall, a Docker reinstall that drops the `runtimes` entry), every full
   `docker compose up` aborts until the env file is switched as in rollback
   step 10; containers already running keep running. Re-run
   `project_runner_production_check.sh` after any Docker or kernel upgrade.
   An API configured with `runner` also refuses application startup when the
   runner is absent. Set `PROJECT_LAB_EXECUTION_BACKEND=disabled` to restore
   the rest of Masar; never substitute `runc` while execution remains enabled.
6. The host firewall, TLS proxy and the rest of `DEPLOYMENT.md` still apply.

### Production host runbook (gVisor)

**Status: not yet performed — no production host exists.** Until every step
below passes on the real host, report the Project Lab as *"Production-host
gVisor verification still required."*

Prerequisites: an x86_64 or arm64 Linux host with Docker Engine and Compose
≥ v2.24, the repository checked out at the deployed commit, and the production
env file (`/etc/masar/production.env`, see `DEPLOYMENT.md`). Commands run as
root. **Step 3 restarts Docker, which restarts every container on the host:
do it in a maintenance window** (or with `"live-restore": true` already in
`daemon.json`).

1. **Install a pinned `runsc`** from the release tarball (no "latest" URL is
   published; the standalone `runsc` download is not enough — this release
   refuses to start without its `gvisor-bin/` sidecars):

   ```sh
   V=20260928.0                            # the release verified in testing
   URL=https://storage.googleapis.com/gvisor/releases/release/$V/$(uname -m)
   cd "$(mktemp -d)"
   wget -q $URL/gvisor.tar.bz2 $URL/gvisor.tar.bz2.sha512 && sha512sum -c gvisor.tar.bz2.sha512
   mkdir gv && tar -xjf gvisor.tar.bz2 -C gv
   install -m 0755 "$(find gv -name runsc -type f)" "$(find gv -name containerd-shim-runsc-v1 -type f)" /usr/local/bin/
   rm -rf /usr/local/bin/gvisor-bin && cp -r "$(find gv -name gvisor-bin -type d)" /usr/local/bin/gvisor-bin
   chmod -R a+rX /usr/local/bin/gvisor-bin
   runsc --version
   ```

2. **Register it with Docker** — merge, never overwrite, and keep a backup for
   rollback:

   ```sh
   cp -a /etc/docker/daemon.json /etc/docker/daemon.json.pre-gvisor 2>/dev/null || echo '{}' > /etc/docker/daemon.json.pre-gvisor
   jq '.runtimes.runsc = {"path": "/usr/local/bin/runsc", "runtimeArgs": ["--oci-seccomp", "--host-uds=create"]}' \
     /etc/docker/daemon.json.pre-gvisor > /etc/docker/daemon.json
   ```

   `--oci-seccomp` makes gVisor apply the container's seccomp profile inside
   the sandbox (otherwise it is ignored); `--host-uds=create` lets the runner
   create its socket on the shared volume. Both are required.

3. **Restart Docker** (maintenance window): `systemctl restart docker`.

4. **Verify Docker sees the runtime** — both must succeed:

   ```sh
   docker info --format '{{json .Runtimes}}' | grep -q runsc
   docker run --rm --runtime=runsc alpine:3.20 cat /proc/version   # "... -gvisor ... Sun Jan 10 15:06:54 PST 2016"
   ```

   (`dmesg` is not a usable check: Docker drops `CAP_SYSLOG`, so it fails with
   "klogctl: Operation not permitted" even under gVisor. The runner detects
   gVisor from `/proc/version` the same way.)

5. **Configure the Project Lab** in `/etc/masar/production.env`. Start from
   `PROJECT_LAB_EXECUTION_BACKEND=disabled`; change it to `runner` only after
   steps 1–4 pass:

   ```sh
   PROJECT_LAB_EXECUTION_BACKEND=runner
   PROJECT_LAB_RUNNER_TOKEN=<32+ random characters>      # openssl rand -hex 32
   PROJECT_RUNNER_RUNTIME=runsc
   PROJECT_RUNNER_SECCOMP=runner-seccomp-gvisor.json
   PROJECT_RUNNER_REQUIRE_GVISOR=1                      # runner exits unless it is under gVisor
   PROJECT_LAB_REQUIRE_GVISOR=true                      # API refuses a runner that is not
   PROJECT_RUNNER_PIDS_LIMIT=512                        # host pid headroom gVisor needs
   ```

   The pid cap matters: under gVisor each learner process also costs host
   stub processes/threads, and with the runc value (128) a learner's fork
   bomb intermittently exhausted it, making the gVisor sentry panic
   (`createSysmsgThread: failed to get clone`) and the runner restart
   (reproduced 2026-10-07). Learner processes stay capped at 32 per job by
   `RLIMIT_NPROC` inside the sandbox.

6. **Start the runner, then recreate the API** so both read the new values.
   The API receives the runtime/profile/require settings for validation, but
   never receives the Docker socket. Each API worker waits briefly for the
   runner and then refuses startup unless `/healthz` attests `runtime=gvisor`:

   ```sh
   C="docker compose --env-file /etc/masar/production.env -f docker-compose.yml -f docker-compose.prod.yml"
   $C --profile project-lab up -d --build project-runner
   $C up -d --force-recreate api
   ```

   The production overlay places `project-runner` behind the `project-lab`
   profile. A normal production `$C up -d` therefore cannot accidentally
   create a local-runc runner while execution is disabled. Explicitly targeting
   the profiled service above is part of the controlled activation.

7. **Check runner and API health**: `$C ps project-runner api` shows both as
   `healthy`, and
   `docker inspect --format '{{.HostConfig.Runtime}}' $($C ps -q project-runner)`
   prints `runsc`. If the runner keeps restarting, `$C logs project-runner`
   shows `RUNNER_REQUIRE_GVISOR=1 but the runner is not running under gVisor`
   — the fail-closed path, go to step 10. If the runner is healthy but the API
   repeatedly exits, inspect `$C logs api`; a non-gVisor or unavailable-runner
   startup error means the execution backend must be disabled until the host
   configuration is repaired.

8. **Run the full security probe suite under gVisor**:
   `backend/scripts/project_runner_security_check.sh --gvisor` (a throwaway
   compose project; production containers are not touched). Expect
   `96/96 passed`.

9. **Run the verification script** — it repeats 4, 7 and 8 and adds the
   API-side checks and a representative capstone execution (Python, pandas
   joins, DuckDB SQL, a matplotlib chart, a learner error, a hard-coded answer
   caught by the hidden variant) through the deployed API and runner:

   ```sh
   backend/scripts/project_runner_production_check.sh /etc/masar/production.env
   ```

   Exit status 0 and `Production-host gVisor verification PASSED` are the
   evidence. Record the output with the deployed commit; only then may the
   Project Lab be described as production-verified under gVisor.

10. **Rollback** if any step fails. Choose the first option that applies:
    * **Fail closed (default).** Turn learner execution off; the rest of Masar
      keeps working and learners see "Project execution is not available
      right now" (an infrastructure error, never a fallback):
      `PROJECT_LAB_EXECUTION_BACKEND=disabled`, then
      `$C up -d --force-recreate api && $C stop project-runner`.
    * **Remove the runtime** (if `runsc` itself breaks Docker). First, in the
      env file, set `PROJECT_LAB_EXECUTION_BACKEND=disabled` **and**
      `PROJECT_RUNNER_RUNTIME=runc`. Then restore
      `/etc/docker/daemon.json.pre-gvisor`, `systemctl restart docker`
      (maintenance window), and run `$C up -d`. The production profile omits
      the runner entirely, while the disabled API and the rest of Masar start
      normally.
    * **Do not return production learner execution to runc.** `runc` remains a
      local-development runtime only. If gVisor cannot be restored, keep
      `PROJECT_LAB_EXECUTION_BACKEND=disabled`; rendering, static grading,
      SQL grading, and the rest of Masar remain available.

### gVisor troubleshooting checklist

* `unknown or invalid runtime name: runsc`: registration is absent or Docker
  was not restarted. Re-check `/etc/docker/daemon.json`, `runsc --version`, and
  `docker info --format '{{json .Runtimes}}'`.
* Runner restart loop with `runs under 'runc'`: Compose did not receive the
  intended env file or the container was not recreated. Confirm
  `docker inspect ...HostConfig.Runtime` is `runsc`.
* API startup failure saying the runner is unavailable: wait for runner health,
  verify the shared socket volume and token, then recreate the API. Do not
  weaken either require flag to make it boot.
* gVisor worker failures around `clone3`: use
  `runner-seccomp-gvisor.json`, not the runc profile.
* gVisor sentry crashes under process-abuse probes: verify
  `PROJECT_RUNNER_PIDS_LIMIT` is at least 512. The learner's in-sandbox limit
  remains 32 processes.
* Any unresolved failure: set the backend to `disabled`, recreate the API,
  stop the runner, and keep the release blocker open.

### `local` backend: development and tests only, not a sandbox

The same harness and rlimits, run as the API's own user with that user's
filesystem and network. `app/core/config.py` refuses it in production; a blank
backend setting resolves to `disabled` in production.

---

## Run, Check Step and progress

* **Run** executes the *saved* file. `status`: `success`, `error` (learner
  code; traceback limited to their frames), `timeout`, or
  `infrastructure_error` (the platform, not the learner). Charts a run
  generates are kept as artifacts. A Run never changes progress.
* **Check Step** runs the task's private validator: `pass`, `fail`, or
  `error` (`execution`: the file did not run; `infrastructure`: the platform).
  A check that depends on earlier checks is returned as `pending`, not failed.
* Only a passing check completes a task; the progress row is locked, so a
  repeated pass changes only the counter (idempotent). Milestone and project
  progress derive from tasks.
* **Final submission** (`POST /attempts/{id}/submit`) is accepted only when
  every task has passed; it records `submitted_at` once and returns the
  summary: completed milestones, overall completion, validated skills
  (`lab_milestones.skills`) and generated artifacts. Portfolio publishing and
  certificates would extend `submitted_at`; they are not built.

## Validators

Validators compare **outputs**, never source text, so any correct pandas or
SQL approach passes. The runner returns *observations* (named variables, or
the SQL result table). The API computes expected values itself from the
canonical datasets (`masar_commerce_facts.analyze`, standard library only).
Expected values and validator code never enter the sandbox or any response.

* **Diagnosis without answers.** The facts module also computes the result of
  each typical mistake (every status counted, duplicates kept, `list_price`
  used). A wrong value that equals a mistake's result gets that mistake named —
  e.g. "Cancelled, returned or pending orders appear to be included" — and
  never the expected number. Tests assert that no expected value appears in
  any failing response.
* **Hidden variant.** Every data task reruns the learner's file on a
  deterministic variant dataset (`facts.variant`): orders numbered 0 mod 3, the
  top region's orders 1 mod 3, the best month's even orders, the top product's
  lines and the first/last day's orders are removed. Every count, total and
  ranking a learner could type in moves; every intentional data issue remains.
  Typed-in answers fail `computed_from_data`.
* SQL row order is checked only where the task asks for it (calendar months,
  top-N ranking). Column names are matched case-insensitively.
* Learner code shares the harness's interpreter and could forge observations;
  forging a passing one requires knowing the expected values, which the learner
  can only get by computing them.

---

## The Data Analyst capstone

**Scenario.** The learner joins Masar Commerce, an online retailer in Egypt,
the Gulf, the Levant and North Africa, as a junior Data Analyst. Management
sees sales changing but cannot say why; the CEO, Head of Sales and Head of
Marketing need an executive report. The project starts from their questions,
not from code.

### Dataset (`DATASET_VERSION` 2026.10.2, seed 20261002)

Generated by `backend/scripts/generate_masar_commerce_data.py`: no clock, no
randomness outside the fixed seed — re-running reproduces the committed CSVs
byte for byte, and the generator asserts the invariants the validators rely
on (no ties among top customers/products, exactly the documented issues).

| File | Rows | Columns |
| --- | --- | --- |
| `customers.csv` | 1,500 | customer_id, city, country, region (Egypt, Gulf, Levant, North Africa), segment (consumer, business), signup_date |
| `orders.csv` | 4,224 (4,200 distinct) | order_id, customer_id, order_date (2025), status (completed, cancelled, returned, pending), payment_method, channel |
| `order_items.csv` | 8,568 (8,527 distinct) | order_item_id, order_id, product_id, quantity, unit_price (after discount) |
| `products.csv` | 40 | product_id, product_name, category (6), list_price |

Intentional, documented quality issues (the learner discovers them in M2 and
fixes them in M3):

1. 24 exact duplicate rows in `orders.csv` (joining to them double-counts);
2. 41 exact duplicate rows in `order_items.csv`;
3. 84 country values with stray spaces or wrong case (strip + title case fixes all);
4. 58 customers with no city (must be kept, not dropped);
5. mixed order statuses — only `completed` is recognised revenue.

Analytical structure: growth through 2025 (H2 ≈ +23% over H1), a Ramadan lift
in March, a summer dip, a November peak; Egypt largest by revenue, the Gulf
with the highest AOV; ~54% repeat buyers, 138 registered customers who never
ordered; Electronics ~41% of revenue; two products that never sold; category-
specific discounting. Recognised revenue is 11,470,825.50 EGP from 3,357
completed orders (counting every status gives 14.28 M, keeping duplicates 11.64 M).

### Workspace

`README.md` and `README.ar.md` (brief, data dictionary, business rules —
read-only), `data/` (read-only), `analysis_plan.md`, `findings.md` (the
learner's running analysis log), `sql/` (revenue_by_category,
monthly_revenue, top_customers, product_performance, regional_performance,
price_bands), `analysis/` (inspect_data, clean_data, kpis, customers,
products, trends, visualize), `charts/`, `report.md`. Every later script
imports `load_clean_data()` from `analysis/clean_data.py`, so cleaning
happens once. Starter comments state only contracts (columns, shapes);
the instructions live in the task panel in both languages. Every markdown
placeholder line has an Arabic line under it; both are template lines, which
the markdown validator never counts as the learner's words.

### Milestones and tasks (29)

Guidance tapers by milestone; difficulty comes from analytical independence,
not obscure syntax.

| Milestone | Guidance | Tasks (validator) | What is validated |
| --- | --- | --- | --- |
| M1 Business Brief | guided: numbered steps | frame-the-brief, plan-questions-and-kpis (`common.markdown_sections`) | Objective and Stakeholders written (≥3 items), ≥4 questions, KPI definitions cover the completed-only rule, line revenue and AOV (EN or AR); template lines never count |
| M2 Understand the Data | guided | profile-the-tables, find-quality-issues, understand-orders-and-customers | raw row counts and date range; duplicate rows, missing cities, malformed countries; distinct orders per status, customers who never ordered; findings §Data quality |
| M3 Prepare and Clean | moderate: goal + output, method open | remove-duplicates, standardise-customers, build-sales-table | one row per order/line, no real row lost; every customer kept, one spelling per country, no missing city; the sales table = exactly the completed lines (fan-out and status mistakes named) |
| M4 SQL Business Analysis | moderate | sql-revenue-by-category, sql-monthly-revenue, sql-top-customers, sql-product-performance, sql-regional-performance | result tables (never query text): category revenue; months in calendar order with distinct orders; top 10 ranked by revenue; all products with 0 not NULL; regional customers/orders/revenue/AOV; findings §SQL findings |
| M5 Core KPIs | reduced: question + output contract | headline-kpis, revenue-at-risk | revenue, completed orders, AOV, purchasing customers, items sold; value of cancelled/returned/pending lines, cancellation rate |
| M6 Customer Analysis | reduced | customer-concentration, repeat-purchase-behaviour, customer-segments | revenue per customer and top-decile share; repeat rate, one-time buyers, orders per customer; segment revenue and AOV; findings §Customers |
| M7 Product Analysis | reduced | category-mix, product-concentration, sql-price-bands | category shares and discount depth; top-5/top-10 product share; `CASE` price bands including unsold products; findings §Products |
| M8 Time and Regional | independent: "choose your approach" | growth, regional-value | month-over-month growth, best month, H2 vs H1; region share and revenue per purchasing customer; findings §Trends and regions |
| M9 Data Visualization | independent | chart-monthly-revenue, chart-revenue-by-category, chart-regional-performance (`masar_commerce.chart`) | each task states the business question and the decision it supports; the PNG exists and is ≥400×250; the plotted data equals the data (and the variant's); no pixel grading; findings §Chart takeaways |
| M10 Executive Report | synthesis: requirements only | write-the-report, support-with-numbers, embed-the-charts | seven sections (EN or AR headings), ≥2 risks and ≥3 recommendations as lists; revenue, orders, AOV, repeat rate, top category, top region and best month stated in the right sections (rounding and Arabic digits accepted); three charts embedded and generated |

Phase-3 review (32 → 29 tasks): the objective and stakeholder tasks became
one; five tasks that recomputed an SQL result in pandas (top-10 customers,
category revenue, best/unsold products, monthly trend, regional revenue) were
replaced by analyses SQL makes awkward — concentration, discount depth,
growth, value per customer — so no metric is computed twice as a task. A
`findings.md` log asks for an interpretation after each analytical block, so
the sequence is never query → query → query; the report is synthesised from
it.

Every task has three authored hints (concept → fields and relationships →
implementation direction, never a finished query, script or number) in
English and Arabic, revealed one at a time, free. Instructions, hints, check
messages and starter files are scanned by
`test_learner_facing_text_reveals_no_expected_value`: no example may equal a
real answer at report rounding.

No AI grades the report: the checks are deterministic structure and
fact-reference checks. Qualitative AI feedback could be added later as an
optional extra; completion never depends on it.

### Project Overview and completion

* `lab_projects.overview` (migration 032) holds the overview content: role,
  scenario, duration range, skills and deliverables, in English and Arabic.
  `/challenges/projects/<slug>` shows it before anything else — role,
  difficulty, duration, structure, scenario, deliverables, skills, how the lab
  works and the ten milestones (titles and summaries only) — with **Start
  Project**, **Continue Project** or **View Completed Project**. Visiting it
  never creates an attempt; the lab itself is `/challenges/projects/<slug>/workspace`.
* After final submission the overview shows **Project Completed**: the
  task count, submission date, role, the validated skill areas (from completed
  milestones), the milestones and the learner's artifacts by path.
* `GET /attempts/{id}/completion` returns the portfolio-ready summary
  (`schema_version` 1): project title/description/role/difficulty/track,
  status, task and milestone completion, skills, deliverables, dates and
  artifacts (path, kind, size — never contents, never validator data, only
  files the learner changed plus generated charts). It is frozen into
  `lab_attempts.completion` at submission, so a later Portfolio or
  certificate feature reads exactly what the learner submitted. Nothing is
  public; no portfolio or certificate is built.

### Arabic

All learner-facing content has Arabic: titles, summaries, overview,
instructions, hints, every check label and message, UI strings, the
completion summary and the markdown placeholders. Technical terms stay in
English where useful (SQL, DataFrame, KPI, AOV, JOIN, CTE); code, file names,
SQL, output and result tables stay LTR inside the RTL layout; the report
preview sets each block's direction from its own text. The brief, data
dictionary and business rules are in `README.ar.md`. Learners may write the
plan, findings and report in Arabic, with Arabic headings accepted. Counts in
Arabic UI strings use the "label: number" form (`المهام: 29`), which stays
grammatical for every number.

### Rules for the next capstone (copy these)

1. Start from a business scenario with named stakeholders and their decisions.
2. Taper guidance by milestone: steps → goal + output contract → question +
   contract → "choose your approach" → requirements only.
3. Each task is one meaningful unit of analysis that answers a business
   question; course exercises teach syntax, projects apply it.
4. Never compute the same metric twice as separate tasks; use each tool where
   it is natural (SQL for querying and aggregation, Python for cleaning,
   deeper manipulation and charts).
5. Interleave interpretation (`findings.md`) with computation; the final
   deliverable is synthesised from it.
6. Validators compare results, rerun on a hidden variant, name known mistakes
   and never reveal expected values; the leak test must cover the new project.
7. Write English and Arabic together, and review the Arabic by reading it.

---

## Adding a project

1. Create `backend/project_templates/<key>/workspace/` — no answers in it (the
   runner mounts this folder).
2. Add `definitions/<project>.py` and list it in `definitions/__init__.py`.
3. Reuse `validators/common.py` or add `validators/<project>.py` (import it in
   `validators/__init__.py`).
4. `python -m seeds.seed_project_lab` after `seed.py`. The sync is idempotent,
   refuses unknown validators/tracks/files, never deletes on its own, and
   deletes a task or milestone only when the definition lists its slug in
   `retired_task_slugs` / `retired_milestone_slugs` (that deletes learner
   progress on it). Attempts finished before new tasks were added become active
   again.

## Product decisions (easy to change)

* Starting is free and idempotent (one attempt per learner per project).
* Tasks can be checked in any order; the "current task" is the first incomplete one.
* Explicit save (Ctrl/Cmd+S, prompt on leaving); Run and Check save first.
* The editor is Masar's existing `react-simple-code-editor` + Prism (Monaco's
  CDN workers are blocked by the CSP).
* Learners cannot create files; generated charts are kept per attempt (latest
  version per path, 30 max) for the report and the submission.
* Milestones collapse in the task panel; the one holding the selected task is open.
* Projects are not gated by track enrolment.
