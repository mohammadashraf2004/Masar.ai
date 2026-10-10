"""A frontend build must never fall back to the retired first mentor chat.

POST /mentor/chat answers 410. The screen that still calls it is the pre-v2 one, and the mentor page
renders it unless the build says the v2 message/quiz endpoints are live (NEXT_PUBLIC_MENTOR_V2_LIVE).
docker-compose.yml used to default that build argument to empty, so a build made without it shipped a
mentor that could only fail. The default is now the live endpoints, in the base file that the
production overlay inherits, and the env template says the same.

This reads the repository files (skipped where they are not present, e.g. in the API image's test run),
like test_deploy_execution_default.py.
"""
import re
from pathlib import Path

import pytest

from app.controllers import mentor_controller

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "docker-compose.yml"
PROD = ROOT / "docker-compose.prod.yml"
ENV_TEMPLATE = ROOT / "deploy" / "production.env.example"

pytestmark = pytest.mark.skipif(
    not all(p.is_file() for p in (BASE, PROD, ENV_TEMPLATE)), reason="deploy files not present"
)


def _frontend_build_args(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    service = re.search(r"^  frontend:\n(.*?)(?=^  \S|\Z)", text, re.S | re.M)
    assert service, f"{path.name} defines frontend"
    return "\n".join(line for line in service.group(1).splitlines() if not line.lstrip().startswith("#"))


def test_the_retired_chat_endpoint_still_answers_gone():
    # The reason the build default matters: nothing behind the old screen works any more.
    routes = {(route.path, tuple(sorted(route.methods))): route.status_code for route in mentor_controller.router.routes}
    assert routes[("/mentor/chat", ("POST",))] == 410


def test_the_base_compose_file_builds_the_live_mentor_by_default():
    args = _frontend_build_args(BASE)
    assert "NEXT_PUBLIC_MENTOR_V2_LIVE: ${NEXT_PUBLIC_MENTOR_V2_LIVE:-message,quiz}" in args


def test_the_production_overlay_does_not_override_it_with_an_empty_default():
    # It inherits the base file's build args; redefining the variable here must not reintroduce `:-}`.
    assert not re.search(r"NEXT_PUBLIC_MENTOR_V2_LIVE:\s*\$\{NEXT_PUBLIC_MENTOR_V2_LIVE:-\}", _frontend_build_args(PROD))


def test_the_env_template_turns_the_live_endpoints_on():
    template = ENV_TEMPLATE.read_text(encoding="utf-8")
    assert re.search(r"^NEXT_PUBLIC_MENTOR_V2_LIVE=message,quiz$", template, re.M)
