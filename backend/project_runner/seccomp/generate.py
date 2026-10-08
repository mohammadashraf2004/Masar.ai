"""Generate the project-runner seccomp profiles. Run after changing the lists:

    python backend/project_runner/seccomp/generate.py

Writes runner-seccomp.json (runc) and runner-seccomp-gvisor.json (runsc with
--oci-seccomp). See README.md for how observed-syscalls.txt was produced.
"""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

# Calls that appeared in the trace only because the adversarial probes made
# them on purpose, or that nothing legitimate here needs. Refused (EPERM).
REFUSED = {
    "add_key", "bpf", "chroot", "init_module", "io_uring_setup", "kexec_load", "keyctl", "mount",
    "perf_event_open", "personality", "ptrace", "setns", "syslog", "unshare", "userfaultfd",
}

# Needed by CPython/glibc/NumPy/pandas/matplotlib/DuckDB on paths the trace
# did not happen to hit. Each is an ordinary process/file/thread primitive.
REVIEWED_EXTRA = {
    # signals: returning from a handler, signalling own threads, alt stacks
    "rt_sigreturn", "tgkill", "tkill", "sigaltstack", "rt_sigpending", "rt_sigsuspend", "alarm",
    # scheduling, time and identity queries
    "sched_yield", "nanosleep", "clock_gettime", "clock_getres", "gettimeofday", "getppid", "getegid",
    "getresuid", "getresgid", "getpgid", "getsid", "getrusage", "times", "getcpu", "sched_getparam",
    "sched_getscheduler", "getpriority", "get_robust_list", "membarrier",
    # file I/O and metadata on the job's own files
    "readv", "writev", "pwrite64", "preadv", "pwritev", "ftruncate", "fsync", "fdatasync", "flock",
    "fadvise64", "rename", "renameat", "renameat2", "mkdirat", "fchdir", "fchmod", "fchmodat", "fchown",
    "statx", "fstatfs", "statfs", "lstat", "newfstatat", "getxattr", "lgetxattr", "fgetxattr", "llistxattr",
    "flistxattr", "copy_file_range", "msync",
    # pipes, polling and waiting (subprocess, threads, DuckDB's thread pool)
    "dup", "dup3", "pipe", "eventfd2", "epoll_ctl", "epoll_wait", "epoll_pwait", "select", "pselect6",
    "ppoll", "waitid", "getsockopt", "futex_waitv",
    # memory policy/locking used by allocators (no effect on other processes)
    "get_mempolicy", "set_mempolicy", "mlock", "munlock",
}

# Allowed only with argument filters (rules below).
FILTERED = {"clone", "clone3", "socket", "socketpair"}

CLONE_NAMESPACE_FLAGS = 0x7E020000  # CLONE_NEWNS|NEWCGROUP|NEWUTS|NEWIPC|NEWUSER|NEWPID|NEWNET
AF_UNIX = 1


def allowlist() -> list[str]:
    observed = set((HERE / "observed-syscalls.txt").read_text().split())
    names = (observed - REFUSED - FILTERED) | REVIEWED_EXTRA
    assert not names & REFUSED and not names & FILTERED
    return sorted(names)


def profile(*, gvisor: bool) -> dict:
    rules = [
        {"names": allowlist(), "action": "SCMP_ACT_ALLOW",
         "comment": "observed under the runner, the security probes and an analysis workload, "
                    "minus REFUSED, plus REVIEWED_EXTRA (generate.py)"},
        {"names": ["clone"], "action": "SCMP_ACT_ALLOW",
         "args": [{"index": 0, "value": CLONE_NAMESPACE_FLAGS, "valueTwo": 0, "op": "SCMP_CMP_MASKED_EQ"}],
         "comment": "threads and processes only: any CLONE_NEW* namespace flag is refused"},
        {"names": ["socket", "socketpair"], "action": "SCMP_ACT_ALLOW",
         "args": [{"index": 0, "value": AF_UNIX, "valueTwo": 0, "op": "SCMP_CMP_EQ"}],
         "comment": "AF_UNIX only: no IPv4/IPv6/netlink/packet sockets"},
    ]
    if gvisor:
        rules.append({
            "names": ["clone3"], "action": "SCMP_ACT_ALLOW",
            "comment": "gVisor does not honour errnoRet for clone3, so glibc never falls back to clone "
                       "and no thread can start. Namespaces created this way exist only inside gVisor's "
                       "user-space kernel; unshare/setns stay refused.",
        })
    else:
        rules.append({
            "names": ["clone3"], "action": "SCMP_ACT_ERRNO", "errnoRet": 38,
            "comment": "ENOSYS: clone3 flags live in memory and cannot be filtered; glibc falls back to clone",
        })
    return {
        "defaultAction": "SCMP_ACT_ERRNO",
        "defaultErrnoRet": 1,
        "architectures": ["SCMP_ARCH_X86_64"],
        "syscalls": rules,
    }


def main() -> None:
    for name, gvisor in (("runner-seccomp.json", False), ("runner-seccomp-gvisor.json", True)):
        (HERE / name).write_text(json.dumps(profile(gvisor=gvisor), indent=1) + "\n", encoding="utf-8")
        print(f"{name}: {len(allowlist())} unconditional + filtered clone/socket rules")


if __name__ == "__main__":
    main()
