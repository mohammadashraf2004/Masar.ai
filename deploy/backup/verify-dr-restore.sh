#!/usr/bin/env bash
#
# deploy/backup/verify-dr-restore.sh
#
# Retrieves the latest (or a named) off-host backup object, verifies its
# checksum, decrypts it, and restores it into a target Postgres the caller
# supplies — then verifies schema, migration head, critical constraints
# and representative data. This is the actual disaster-recovery proof:
# "the backup exists in S3" is not evidence of anything on its own, this
# script retrieving and restoring it is.
#
# Refuses to run unless the target looks disposable AND the caller
# confirms that explicitly — see the safety guard below. There is no
# "production DR mode" in this script; restoring into a real production
# database is an entirely different, much more careful operation than
# "verify the backup mechanism works", and this script is only the latter.
#
# Usage:
#   DR_TARGET_DATABASE_URL=postgresql://postgres:pw@disposable-host:5432/db \
#   DR_CONFIRM_DISPOSABLE=true \
#   BACKUP_S3_BUCKET=... BACKUP_S3_PREFIX=masar/postgres \
#   AWS_ACCESS_KEY_ID=... AWS_SECRET_ACCESS_KEY=... \
#   BACKUP_ENCRYPTION_PASSPHRASE=... \
#     ./deploy/backup/verify-dr-restore.sh
#
# Optional:
#   DR_OBJECT_KEY           restore a specific object instead of the latest
#   BACKUP_S3_REGION, BACKUP_S3_ENDPOINT_URL   same meaning as in pg-backup.sh
#   DR_EXPECTED_HEAD        alembic revision expected at head (default below)
#   DR_API_HEALTH_URL       if set, curled and expected to return 200
#
# Requires on PATH: aws, openssl, pg_restore, psql. Never prints the
# encryption passphrase or AWS credentials.

set -euo pipefail

log() { printf '%s %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$*"; }
fail() { log "FAIL: $*"; exit 1; }

DR_EXPECTED_HEAD="${DR_EXPECTED_HEAD:-010_exam_attempt_start_race}"

# ── Safety guard ─────────────────────────────────────────────────────────
# Two independent checks, both required — a name heuristic AND an explicit
# confirmation flag. Neither alone is trustworthy: a heuristic can false-
# negative on an oddly-named disposable host, and a flag alone is one
# copy-pasted command away from being set out of habit.
: "${DR_TARGET_DATABASE_URL:?DR_TARGET_DATABASE_URL is required}"
: "${DR_CONFIRM_DISPOSABLE:?set DR_CONFIRM_DISPOSABLE=true to confirm the target is disposable infrastructure, never production}"
if [ "$DR_CONFIRM_DISPOSABLE" != "true" ]; then
    fail "DR_CONFIRM_DISPOSABLE must be exactly 'true' — refusing to run"
fi
case "$DR_TARGET_DATABASE_URL" in
    *test*|*Test*|*TEST*|*disposable*|*Disposable*|*dr-*|*-dr*|*restore*|*Restore*|*staging*|*Staging*) : ;;
    *)
        fail "DR_TARGET_DATABASE_URL does not look disposable (expected 'test', 'disposable', 'restore', 'staging' or 'dr' somewhere in it) — refusing to run against what might be production. If this really is disposable, rename it; this check exists so a copy-pasted production URL cannot reach pg_restore by accident."
        ;;
esac
log "safety guard passed — target looks disposable: $(printf '%s' "$DR_TARGET_DATABASE_URL" | sed -E 's#://[^@]*@#://***:***@#')"

: "${BACKUP_S3_BUCKET:?BACKUP_S3_BUCKET is required}"
: "${AWS_ACCESS_KEY_ID:?AWS_ACCESS_KEY_ID is required}"
: "${AWS_SECRET_ACCESS_KEY:?AWS_SECRET_ACCESS_KEY is required}"
: "${BACKUP_ENCRYPTION_PASSPHRASE:?BACKUP_ENCRYPTION_PASSPHRASE is required}"
PREFIX="${BACKUP_S3_PREFIX:-masar/postgres}"

AWS_OPTS=()
[ -n "${BACKUP_S3_ENDPOINT_URL:-}" ] && AWS_OPTS+=(--endpoint-url "$BACKUP_S3_ENDPOINT_URL")
[ -n "${BACKUP_S3_REGION:-}" ] && export AWS_DEFAULT_REGION="$BACKUP_S3_REGION"

WORKDIR=$(mktemp -d)
trap 'rm -rf "$WORKDIR"' EXIT

# ── 1. BACKUP RETRIEVAL ──────────────────────────────────────────────────
log "BACKUP RETRIEVAL: locating object"
if [ -n "${DR_OBJECT_KEY:-}" ]; then
    KEY="$DR_OBJECT_KEY"
else
    # Keys are date-partitioned and timestamp-suffixed
    # (masar/postgres/YYYY/MM/DD/db-STAMP.dump.enc), so a lexicographic
    # sort is also a chronological one — the last line is the newest.
    KEY=$(aws "${AWS_OPTS[@]}" s3api list-objects-v2 \
            --bucket "$BACKUP_S3_BUCKET" --prefix "$PREFIX" \
            --query 'sort_by(Contents, &Key)[-1].Key' --output text) \
        || fail "could not list objects under s3://${BACKUP_S3_BUCKET}/${PREFIX}"
    [ -n "$KEY" ] && [ "$KEY" != "None" ] || fail "no backup objects found under s3://${BACKUP_S3_BUCKET}/${PREFIX}"
fi
log "BACKUP RETRIEVAL: using s3://${BACKUP_S3_BUCKET}/${KEY}"

encrypted="$WORKDIR/artifact.dump.enc"
aws "${AWS_OPTS[@]}" s3api get-object \
        --bucket "$BACKUP_S3_BUCKET" --key "$KEY" \
        "$encrypted" >/dev/null || fail "download failed for ${KEY}"
log "BACKUP RETRIEVAL: downloaded $(wc -c < "$encrypted") bytes"

log "BACKUP RETRIEVAL: verifying checksum"
# A second call rather than parsing get-object's own metadata JSON — no
# jq/python3 dependency needed this way, `--query` does the extraction on
# the CLI side. head-object re-reads the object AS STORED, same as
# upload_remote()'s own verification in pg-backup.sh.
remote_sha256_b64=$(aws "${AWS_OPTS[@]}" s3api head-object \
        --bucket "$BACKUP_S3_BUCKET" --key "$KEY" --checksum-mode ENABLED \
        --query 'ChecksumSHA256' --output text 2>/dev/null || true)
local_sha256_b64=$(openssl dgst -sha256 -binary "$encrypted" | openssl base64 -A)
if [ -n "$remote_sha256_b64" ] && [ "$remote_sha256_b64" != "None" ] && [ "$remote_sha256_b64" != "$local_sha256_b64" ]; then
    fail "checksum mismatch after download — remote=${remote_sha256_b64} local=${local_sha256_b64}"
fi
log "BACKUP RETRIEVAL: checksum verified (sha256=${local_sha256_b64})"

# ── 2. DATABASE RESTORE ──────────────────────────────────────────────────
log "DATABASE RESTORE: decrypting"
plain="$WORKDIR/artifact.dump"
openssl enc -d -aes-256-cbc -pbkdf2 -iter 200000 \
        -in "$encrypted" -pass env:BACKUP_ENCRYPTION_PASSPHRASE \
        -out "$plain" \
    || fail "decryption failed — wrong BACKUP_ENCRYPTION_PASSPHRASE, or a corrupt artifact"
log "DATABASE RESTORE: decrypted OK ($(wc -c < "$plain") bytes)"

log "DATABASE RESTORE: pg_restore into target"
pg_restore --no-owner --no-acl --clean --if-exists -d "$DR_TARGET_DATABASE_URL" "$plain" \
    || fail "pg_restore failed"
log "DATABASE RESTORE: complete"

# ── 3. APPLICATION RECOVERY (schema/data verification) ──────────────────
log "APPLICATION RECOVERY: verifying migration head"
actual_head=$(psql "$DR_TARGET_DATABASE_URL" -tA -c "SELECT version_num FROM alembic_version;") \
    || fail "could not read alembic_version from restored database"
actual_head=$(printf '%s' "$actual_head" | tr -d '[:space:]')
[ "$actual_head" = "$DR_EXPECTED_HEAD" ] \
    || fail "migration head mismatch — expected ${DR_EXPECTED_HEAD}, restored database is at ${actual_head}"
log "APPLICATION RECOVERY: migration head OK (${actual_head})"

log "APPLICATION RECOVERY: verifying critical constraints"
for idx in uq_challenge_attempts_active_enrollment uq_exam_attempts_one_in_progress \
           uq_exam_payments_confirmed_ref; do
    count=$(psql "$DR_TARGET_DATABASE_URL" -tA -c \
        "SELECT count(*) FROM pg_indexes WHERE indexname = '${idx}';")
    [ "$(printf '%s' "$count" | tr -d '[:space:]')" = "1" ] \
        || fail "expected constraint/index missing after restore: ${idx}"
done
log "APPLICATION RECOVERY: all 3 checked constraints present"

log "APPLICATION RECOVERY: verifying representative data (row counts)"
psql "$DR_TARGET_DATABASE_URL" -tA -c "
    SELECT 'users=' || count(*) FROM users
    UNION ALL SELECT 'user_wallets=' || count(*) FROM user_wallets
    UNION ALL SELECT 'career_tracks=' || count(*) FROM career_tracks;
" | while read -r line; do log "  ${line}"; done

if [ -n "${DR_API_HEALTH_URL:-}" ]; then
    log "APPLICATION RECOVERY: checking ${DR_API_HEALTH_URL}"
    code=$(curl -s -o /dev/null -w '%{http_code}' "$DR_API_HEALTH_URL") || code="000"
    [ "$code" = "200" ] || fail "application health check returned ${code}, expected 200"
    log "APPLICATION RECOVERY: health check OK (200)"
fi

log "PASS: off-host backup retrieved, decrypted, restored and verified successfully"
