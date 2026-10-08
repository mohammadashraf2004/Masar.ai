# project-runner seccomp profiles

`runner-seccomp.json` (runc) and `runner-seccomp-gvisor.json` (runsc) are the
syscall allowlists applied to the whole project-runner container — the runner
service and every learner job. Default action: `EPERM`.

Both are **generated**: edit the lists in `generate.py`, then

    python backend/project_runner/seccomp/generate.py

## How the allowlist was derived

1. `docker build --target trace -t masar-project-runner:trace backend/project_runner`
   (the shipped image plus `strace`; never deployed).
2. Ran the runner under `strace -f` with `seccomp=unconfined` and `SYS_PTRACE`,
   and drove it with (a) the full adversarial `security_probe.py` suite and
   (b) a legitimate analysis workload: pandas `read_csv`/merge/groupby/
   `to_period`, NumPy linear algebra, matplotlib `savefig`, DuckDB queries
   from Python and from SQL files (CTE, window, date functions, errors).
3. `observed-syscalls.txt` is the set of syscall names seen (102).
4. `generate.py` removes `REFUSED` (calls that appeared only because the
   probes made them on purpose: `ptrace`, `unshare`, `setns`, `mount`, `bpf`,
   `keyctl`, `perf_event_open`, `io_uring_setup`, `userfaultfd`,
   `personality`, `kexec_load`, `init_module`, `chroot`, `syslog`, `add_key`)
   and adds `REVIEWED_EXTRA`: ordinary file/thread/signal/time primitives that
   CPython, glibc, NumPy, pandas, matplotlib or DuckDB use on code paths the
   trace did not happen to hit (each listed with its reason in the file).

It is 156 unconditional names plus the three filtered rules below, against roughly 370 names in Docker's default profile.

## Argument-filtered calls

* `clone` — allowed only with **no** `CLONE_NEW*` namespace flag.
* `clone3` — its flags live in user memory and cannot be inspected by
  seccomp, so under runc it returns `ENOSYS` and glibc falls back to `clone`
  (filtered above). gVisor does not honour that `errnoRet`, so no thread could
  start; the gVisor profile allows `clone3`. Namespaces created that way exist
  only inside gVisor's user-space kernel, and `unshare`/`setns` stay refused.
* `socket`, `socketpair` — `AF_UNIX` only. No IPv4/IPv6/netlink/packet
  sockets, on top of the container having no network interface.

## Verifying

`backend/scripts/project_runner_security_check.sh` (and `--gvisor`) starts
the runner from `docker-compose.yml` with this profile and runs the probes:
every refused call is checked to fail, and the analysis workload is checked
to still work.
