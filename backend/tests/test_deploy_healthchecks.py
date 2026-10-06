"""The Caddy container's healthcheck must probe the address Caddy's admin API really listens on.

`deploy/Caddyfile` sets `admin localhost:2019`, which Caddy binds on 127.0.0.1 only. The caddy:alpine image resolves
`localhost` to ::1 first and busybox `wget` tries only the first address, so a probe of `http://localhost:2019/...`
was refused on every attempt and the container reported `unhealthy` while it was serving HTTPS normally.
This reads the two repository files (skipped where they are not present, e.g. in the API image's test run).
"""
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
COMPOSE = ROOT / "docker-compose.prod.yml"
CADDYFILE = ROOT / "deploy" / "Caddyfile"

pytestmark = pytest.mark.skipif(not (COMPOSE.is_file() and CADDYFILE.is_file()), reason="deploy files not present")


def _caddy_probe() -> str:
    text = COMPOSE.read_text(encoding="utf-8")
    service = re.search(r"^  caddy:\n(.*?)(?=^  \S|\Z)", text, re.S | re.M).group(1)
    check = re.search(r"healthcheck:\s*(?:#.*\n\s*)*test:\s*(\[.*\])", service)
    assert check, "the caddy service has a healthcheck"
    return check.group(1)


def test_the_caddy_healthcheck_probes_the_admin_api_by_ip_address_not_by_a_name_that_resolves_to_ipv6_first():
    probe = _caddy_probe()
    assert '"wget"' in probe, "the caddy:alpine image has busybox wget and no curl"
    url = re.search(r"http://([^/\"]+)(/[^\"]*)", probe)
    host, path = url.group(1), url.group(2)
    assert host.startswith("127.0.0.1:"), f"probe host {host!r}: use the IPv4 loopback Caddy's admin API binds"
    assert path == "/config/", "still the admin API, which answers 200 once a config is loaded"


def test_the_probe_port_is_the_admin_port_the_caddyfile_declares():
    declared = re.search(r"^\s*admin\s+(\S+):(\d+)\s*$", CADDYFILE.read_text(encoding="utf-8"), re.M)
    assert declared, "the Caddyfile pins the admin address"
    assert declared.group(1) in ("localhost", "127.0.0.1"), "the admin API stays on loopback, never published"
    assert _caddy_probe().count(f":{declared.group(2)}/") == 1
