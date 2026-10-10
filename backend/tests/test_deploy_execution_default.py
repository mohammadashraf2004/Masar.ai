"""Production keeps learner code execution off unless an operator turns it on.

docker-compose.yml falls back to PROJECT_LAB_EXECUTION_BACKEND=runner for local development.
In production that fallback was a trap: an env file without the variable selected the runner,
and the API's gVisor startup gate then refused to boot, taking the whole site down. The
production overlay therefore defaults it to `disabled`, keeps the runner behind an explicit
Compose profile, and the env template says `disabled` too.

This reads the repository files (skipped where they are not present, e.g. in the API image's
test run), like test_deploy_healthchecks.py.
"""
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "docker-compose.yml"
PROD = ROOT / "docker-compose.prod.yml"
ENV_TEMPLATE = ROOT / "deploy" / "production.env.example"
CHECK = ROOT / "backend" / "scripts" / "project_runner_production_check.sh"

pytestmark = pytest.mark.skipif(
    not all(p.is_file() for p in (BASE, PROD, ENV_TEMPLATE, CHECK)), reason="deploy files not present"
)


def _service(path: Path, name: str) -> str:
    text = path.read_text(encoding="utf-8")
    found = re.search(rf"^  {re.escape(name)}:\n(.*?)(?=^  \S|\Z)", text, re.S | re.M)
    assert found, f"{path.name} defines {name}"
    return found.group(1)


def _uncommented(block: str) -> str:
    return "\n".join(line for line in block.splitlines() if not line.lstrip().startswith("#"))


def test_the_production_overlay_defaults_learner_execution_to_disabled():
    api = _uncommented(_service(PROD, "api"))
    assert "- PROJECT_LAB_EXECUTION_BACKEND=${PROJECT_LAB_EXECUTION_BACKEND:-disabled}" in api
    # The base file's development fallback is what the overlay overrides.
    assert "PROJECT_LAB_EXECUTION_BACKEND=${PROJECT_LAB_EXECUTION_BACKEND:-runner}" in _service(BASE, "api")


def test_the_production_overlay_starts_the_runner_only_through_its_profile():
    runner = _uncommented(_service(PROD, "project-runner"))
    assert re.search(r'^\s+profiles:\s*\["project-lab"\]\s*$', runner, re.M)


def test_the_env_template_and_the_host_check_agree_that_unset_means_disabled():
    template = ENV_TEMPLATE.read_text(encoding="utf-8")
    assert re.search(r"^PROJECT_LAB_EXECUTION_BACKEND=disabled$", template, re.M)
    check = CHECK.read_text(encoding="utf-8")
    # Enabling must be explicit: the gVisor host check never treats a missing value as `runner`.
    assert '[ "$backend" = "runner" ] || fail' in check
    assert '[ -z "$backend" ]' not in check
