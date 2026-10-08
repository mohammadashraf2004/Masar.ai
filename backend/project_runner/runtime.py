"""Which container runtime the runner is executing under.

gVisor (runsc) implements the Linux kernel interface in a user-space kernel,
and identifies itself in two places that runc containers never show:

* the kernel log (syslog(2) READ_ALL), which gVisor fills with its own boot
  messages starting "Starting gVisor..." and which an unprivileged runc
  container cannot read at all;
* /proc/version, which gVisor fixes to "Linux version 4.4.0 #1 SMP Sun Jan 10
  15:06:54 PST 2016" regardless of the host kernel.

Either signal is enough. This is used to *refuse to start* when gVisor is
required and missing; it is not a security control by itself.
"""
from __future__ import annotations

import ctypes
import ctypes.util

_GVISOR_PROC_VERSION = "Sun Jan 10 15:06:54 PST 2016"
_SYSLOG_ACTION_READ_ALL = 3


def _kernel_log() -> str:
    try:
        libc = ctypes.CDLL(ctypes.util.find_library("c") or "libc.so.6", use_errno=True)
        buffer = ctypes.create_string_buffer(64 * 1024)
        size = libc.klogctl(_SYSLOG_ACTION_READ_ALL, buffer, len(buffer))
        return buffer.raw[:size].decode("utf-8", "replace") if size > 0 else ""
    except (OSError, AttributeError):
        return ""


def detect_runtime() -> str:
    """"gvisor" or "runc" (meaning: an ordinary namespaced container)."""
    try:
        with open("/proc/version", encoding="utf-8") as handle:
            if _GVISOR_PROC_VERSION in handle.read():
                return "gvisor"
    except OSError:
        pass
    if "gVisor" in _kernel_log():
        return "gvisor"
    return "runc"
