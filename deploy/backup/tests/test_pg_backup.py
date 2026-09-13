"""
deploy/backup/tests/test_pg_backup.py

Unit tests for deploy/backup/pg-backup.sh's control flow: local backup,
the off-host upload it now performs, and the failure/skip paths for each.

Deliberately independent of backend/tests/ — this exercises a POSIX shell
script, not the FastAPI app, and must not need a running Postgres test
database just to check that a mocked "S3 put-object failed" is handled
correctly. Run on its own:

    pytest deploy/backup/tests/

Real `pg_dump`/`pg_restore`/`aws` are never invoked — see mock_bin/ for
why, and for what each mock actually does. `openssl` IS the real binary:
the encrypt/verify round trip (including the wrong-passphrase case) is
worth proving for real rather than mocking away the one part of this
script that is actual cryptography.

No AWS credentials are used anywhere in this file — the mock `aws` in
mock_bin/ never makes a network call.
"""
import os
import shutil
import stat
import subprocess
import sys
import textwrap
from pathlib import Path

import pytest

HERE = Path(__file__).parent
SCRIPT = HERE.parent / "pg-backup.sh"
MOCK_BIN = HERE / "mock_bin"

# Locate a POSIX shell capable of running the script. Prefer `sh` (what the
# Dockerfile's ENTRYPOINT actually uses); `bash` is an acceptable fallback
# for a host with no standalone `sh` on PATH, since bash runs POSIX sh
# scripts too.
SHELL = shutil.which("sh") or shutil.which("bash")


def _skip_reason():
    if SHELL is None:
        return "no POSIX shell (sh/bash) found on PATH"
    if shutil.which("openssl", path=os.environ.get("PATH")) is None:
        return "openssl not found on PATH"
    return None


pytestmark = pytest.mark.skipif(_skip_reason() is not None, reason=_skip_reason() or "")


@pytest.fixture()
def backup_dir(tmp_path):
    d = tmp_path / "backups"
    d.mkdir()
    return d


@pytest.fixture()
def state_dir(tmp_path):
    d = tmp_path / "mock-aws-state"
    d.mkdir()
    return d


@pytest.fixture()
def call_log(tmp_path):
    return tmp_path / "aws-calls.log"


def run_backup_once(backup_dir, state_dir, call_log, env_overrides=None, expect_success=True):
    """Invoke pg-backup.sh for exactly one cycle (BACKUP_RUN_ONCE=true)."""
    env = dict(os.environ)
    # Start from a clean slate: only what the script itself declares as
    # inputs, not whatever ambient AWS_*/PG* the host happens to have.
    for leak in ("AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_DEFAULT_REGION",
                 "PGHOST", "PGUSER", "PGPASSWORD", "PGDATABASE"):
        env.pop(leak, None)

    env["PATH"] = f"{MOCK_BIN}{os.pathsep}{env['PATH']}"
    env["BACKUP_DIR"] = str(backup_dir)
    env["BACKUP_ENCRYPTION_PASSPHRASE"] = "test-passphrase-not-a-real-secret"
    env["PGDATABASE"] = "testdb"
    env["BACKUP_RUN_ONCE"] = "true"
    env["MOCK_AWS_STATE_DIR"] = str(state_dir)
    env["MOCK_AWS_CALL_LOG"] = str(call_log)
    if env_overrides:
        env.update(env_overrides)

    proc = subprocess.run(
        [SHELL, str(SCRIPT)],
        env=env,
        capture_output=True,
        text=True,
        timeout=30,
    )
    if expect_success:
        assert proc.returncode == 0, (
            f"expected success, got exit {proc.returncode}\n"
            f"stdout:\n{proc.stdout}\nstderr:\n{proc.stderr}"
        )
    return proc


def _daily_dumps(backup_dir):
    return list((backup_dir / "daily").glob("*.dump.enc"))


# ─────────────────────────────────────────────────────────────────────────
# Local backup success (no remote configured — the pre-existing behavior
# must be completely unaffected by this feature existing)
# ─────────────────────────────────────────────────────────────────────────

def test_local_backup_succeeds_with_remote_unset(backup_dir, state_dir, call_log):
    proc = run_backup_once(backup_dir, state_dir, call_log)

    dumps = _daily_dumps(backup_dir)
    assert len(dumps) == 1, dumps
    assert (backup_dir / "last_success").exists()
    assert (backup_dir / "backup_last_success.prom").exists()
    assert "masar_backup_last_success_timestamp_seconds" in (
        backup_dir / "backup_last_success.prom"
    ).read_text()

    # The artifact is real ciphertext, not the plaintext marker — the
    # local backup's own encryption must still be genuinely happening.
    assert b"FAKE_PG_DUMP_CONTENT" not in dumps[0].read_bytes()


def test_remote_disabled_explicitly_skips_upload_and_still_succeeds(backup_dir, state_dir, call_log):
    proc = run_backup_once(backup_dir, state_dir, call_log, {"BACKUP_REMOTE_ENABLED": "false"})

    assert "remote_upload_skipped" in proc.stdout
    assert not (backup_dir / "last_remote_key").exists()
    assert not (backup_dir / "backup_remote_last_success.prom").exists()
    assert not call_log.exists() or call_log.read_text() == ""


def test_local_backup_survives_a_pg_dump_failure_report(backup_dir, state_dir, call_log):
    """pg_dump failing must be reported (non-zero exit, no artifact left
    behind) — this is pre-existing behavior, re-checked here because the
    return-code plumbing changed (run_backup now also folds in the remote
    result) and must not have broken this path."""
    proc = run_backup_once(
        backup_dir, state_dir, call_log,
        {"MOCK_PG_DUMP_FAIL": "1"},
        expect_success=False,
    )
    assert proc.returncode != 0
    assert not _daily_dumps(backup_dir)
    assert not (backup_dir / "last_success").exists()


# ─────────────────────────────────────────────────────────────────────────
# Remote upload success
# ─────────────────────────────────────────────────────────────────────────

def test_remote_upload_success_is_verified_and_recorded(backup_dir, state_dir, call_log):
    proc = run_backup_once(backup_dir, state_dir, call_log, {
        "BACKUP_REMOTE_ENABLED": "true",
        "BACKUP_S3_BUCKET": "masar-backups-test",
        "BACKUP_S3_PREFIX": "masar/postgres",
        "AWS_ACCESS_KEY_ID": "AKIA_TEST_NOT_REAL",
        "AWS_SECRET_ACCESS_KEY": "test-secret-not-real",
    })

    assert "remote_upload_started" in proc.stdout
    assert "remote_upload_succeeded" in proc.stdout

    remote_key_file = backup_dir / "last_remote_key"
    assert remote_key_file.exists()
    key = remote_key_file.read_text().strip()
    # Date-partitioned, matches the documented convention, includes the
    # same filename the local artifact was written under.
    assert key.startswith("masar/postgres/")
    dumps = _daily_dumps(backup_dir)
    assert key.endswith(dumps[0].name)

    assert (backup_dir / "backup_remote_last_success.prom").exists()
    assert "masar_backup_remote_last_success_timestamp_seconds" in (
        backup_dir / "backup_remote_last_success.prom"
    ).read_text()

    # The object that reached "S3" is the already-encrypted artifact,
    # never plaintext — checked against the mock's own recorded state,
    # not just trusted from the log line.
    state_files = list(state_dir.glob("*.size"))
    assert len(state_files) == 1
    uploaded_size = int(state_files[0].read_text().strip())
    assert uploaded_size == dumps[0].stat().st_size

    calls = call_log.read_text()
    assert "put-object" in calls
    assert "head-object" in calls
    assert "--checksum-algorithm SHA256" in calls
    # Default SSE-S3 applied when the caller didn't ask for anything else.
    assert "--server-side-encryption AES256" in calls


def test_remote_upload_uses_endpoint_url_when_set(backup_dir, state_dir, call_log):
    """The one deliberate extension beyond real AWS S3: an S3-compatible
    endpoint, so the exact same script can be pointed at a local emulator
    for a disaster-recovery drill without a second code path."""
    run_backup_once(backup_dir, state_dir, call_log, {
        "BACKUP_REMOTE_ENABLED": "true",
        "BACKUP_S3_BUCKET": "masar-backups-test",
        "AWS_ACCESS_KEY_ID": "AKIA_TEST_NOT_REAL",
        "AWS_SECRET_ACCESS_KEY": "test-secret-not-real",
        "BACKUP_S3_ENDPOINT_URL": "http://minio.test:9000",
    })
    assert "--endpoint-url http://minio.test:9000" in call_log.read_text()


# ─────────────────────────────────────────────────────────────────────────
# Remote upload failure — local backup must be untouched, exit non-zero
# ─────────────────────────────────────────────────────────────────────────

def test_remote_put_failure_preserves_local_artifact_and_fails_the_cycle(backup_dir, state_dir, call_log):
    proc = run_backup_once(backup_dir, state_dir, call_log, {
        "BACKUP_REMOTE_ENABLED": "true",
        "BACKUP_S3_BUCKET": "masar-backups-test",
        "AWS_ACCESS_KEY_ID": "AKIA_TEST_NOT_REAL",
        "AWS_SECRET_ACCESS_KEY": "test-secret-not-real",
        "MOCK_AWS_FAIL_PUT": "1",
    }, expect_success=False)

    assert proc.returncode != 0
    assert "remote_upload_failed" in proc.stdout
    # Local artifact must survive a remote failure untouched.
    dumps = _daily_dumps(backup_dir)
    assert len(dumps) == 1
    # Local heartbeat still reflects the (successful) local half.
    assert (backup_dir / "last_success").exists()
    assert not (backup_dir / "last_remote_key").exists()
    assert not (backup_dir / "backup_remote_last_success.prom").exists()


def test_remote_head_check_failure_fails_the_cycle(backup_dir, state_dir, call_log):
    proc = run_backup_once(backup_dir, state_dir, call_log, {
        "BACKUP_REMOTE_ENABLED": "true",
        "BACKUP_S3_BUCKET": "masar-backups-test",
        "AWS_ACCESS_KEY_ID": "AKIA_TEST_NOT_REAL",
        "AWS_SECRET_ACCESS_KEY": "test-secret-not-real",
        "MOCK_AWS_FAIL_HEAD": "1",
    }, expect_success=False)

    assert proc.returncode != 0
    assert "remote_verify_failed" in proc.stdout
    assert _daily_dumps(backup_dir)
    assert not (backup_dir / "backup_remote_last_success.prom").exists()


def test_remote_size_mismatch_is_treated_as_verification_failure(backup_dir, state_dir, call_log):
    """Exit 0 from put-object is never trusted alone — a size mismatch on
    the HeadObject re-read must fail the cycle even though the upload
    command itself reported success."""
    proc = run_backup_once(backup_dir, state_dir, call_log, {
        "BACKUP_REMOTE_ENABLED": "true",
        "BACKUP_S3_BUCKET": "masar-backups-test",
        "AWS_ACCESS_KEY_ID": "AKIA_TEST_NOT_REAL",
        "AWS_SECRET_ACCESS_KEY": "test-secret-not-real",
        "MOCK_AWS_SIZE_MISMATCH": "1",
    }, expect_success=False)

    assert proc.returncode != 0
    assert "remote_verify_size_mismatch" in proc.stdout
    assert not (backup_dir / "backup_remote_last_success.prom").exists()


def test_remote_checksum_mismatch_is_treated_as_verification_failure(backup_dir, state_dir, call_log):
    proc = run_backup_once(backup_dir, state_dir, call_log, {
        "BACKUP_REMOTE_ENABLED": "true",
        "BACKUP_S3_BUCKET": "masar-backups-test",
        "AWS_ACCESS_KEY_ID": "AKIA_TEST_NOT_REAL",
        "AWS_SECRET_ACCESS_KEY": "test-secret-not-real",
        "MOCK_AWS_CHECKSUM_MISMATCH": "1",
    }, expect_success=False)

    assert proc.returncode != 0
    assert "remote_verify_checksum_mismatch" in proc.stdout
    assert not (backup_dir / "backup_remote_last_success.prom").exists()


# ─────────────────────────────────────────────────────────────────────────
# Missing remote configuration while enabled — must fail clearly, never
# claim success
# ─────────────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("missing", ["BACKUP_S3_BUCKET", "AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"])
def test_enabled_but_missing_required_setting_fails_clearly(backup_dir, state_dir, call_log, missing):
    full = {
        "BACKUP_REMOTE_ENABLED": "true",
        "BACKUP_S3_BUCKET": "masar-backups-test",
        "AWS_ACCESS_KEY_ID": "AKIA_TEST_NOT_REAL",
        "AWS_SECRET_ACCESS_KEY": "test-secret-not-real",
    }
    del full[missing]

    proc = run_backup_once(backup_dir, state_dir, call_log, full, expect_success=False)

    assert proc.returncode != 0
    assert missing in proc.stderr
    assert "is required when BACKUP_REMOTE_ENABLED=true" in proc.stderr
    # Must not claim the remote copy exists when it never even attempted.
    assert not (backup_dir / "last_remote_key").exists()
    assert not (backup_dir / "backup_remote_last_success.prom").exists()
    # And the local backup this cycle would otherwise have made must not
    # be silently skipped either — pg_dump/encrypt/verify all still ran
    # before upload_remote's guard was reached.
    assert _daily_dumps(backup_dir)


# ─────────────────────────────────────────────────────────────────────────
# Secret safety — never in stdout/stderr
# ─────────────────────────────────────────────────────────────────────────

def test_secrets_never_appear_in_output_or_logs(backup_dir, state_dir, call_log):
    passphrase = "test-passphrase-not-a-real-secret"
    secret_key = "test-secret-not-real-SENTINEL"
    proc = run_backup_once(backup_dir, state_dir, call_log, {
        "BACKUP_REMOTE_ENABLED": "true",
        "BACKUP_S3_BUCKET": "masar-backups-test",
        "AWS_ACCESS_KEY_ID": "AKIA_TEST_NOT_REAL",
        "AWS_SECRET_ACCESS_KEY": secret_key,
    })
    combined = proc.stdout + proc.stderr
    assert passphrase not in combined
    assert secret_key not in combined
    for f in [backup_dir / "last_success", backup_dir / "backup_last_success.prom",
              backup_dir / "backup_remote_last_success.prom"]:
        if f.exists():
            text = f.read_text()
            assert passphrase not in text
            assert secret_key not in text
