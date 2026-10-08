"""Container healthcheck: GET /healthz over the runner's Unix socket.

The runner has no network interface but loopback and listens on no TCP port,
so the usual `urlopen('http://127.0.0.1:...')` healthcheck cannot work.
Exit 0 when the service answers 200, 1 otherwise.
"""
import http.client
import os
import socket
import sys

SOCKET_PATH = os.environ.get("RUNNER_SOCKET", "/run/project-runner/runner.sock")


class _UnixConnection(http.client.HTTPConnection):
    def connect(self) -> None:
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.settimeout(self.timeout)
        self.sock.connect(SOCKET_PATH)


def main() -> int:
    try:
        conn = _UnixConnection("localhost", timeout=4)
        conn.request("GET", "/healthz")
        return 0 if conn.getresponse().status == 200 else 1
    except OSError:
        return 1


if __name__ == "__main__":
    sys.exit(main())
