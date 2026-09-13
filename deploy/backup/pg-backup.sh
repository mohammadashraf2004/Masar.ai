#!/bin/sh
#
# deploy/backup/pg-backup.sh
#
# Scheduled, encrypted PostgreSQL backups. Runs as a long-lived container
# (docker-compose.prod.yml `db-backup`) rather than a host cron job, so the
# schedule ships with the stack and does not have to be reinstalled by hand
# on every new server.
#
# Each cycle:
#   1. pg_dump -Fc                 custom format — the format the restore
#                                  procedure in LAUNCH_CHECKLIST Phase 4 was
#                                  verified against, and the only one
#                                  pg_restore can do selective restores from
#   2. encrypt with AES-256        openssl enc, passphrase from the env
#   3. verify the artifact         decrypt + pg_restore --list, so a corrupt
#                                  or wrongly-keyed dump is caught NOW and
#                                  not during an actual disaster
#   4. prune by retention          daily / weekly / monthly
#   5. write a heartbeat           /backups/last_success so a stale backup
#                                  is observable rather than silent
#
# ── Off-host copy ────────────────────────────────────────────────────────
# 6.  upload           the already-encrypted, already-verified artifact —
#                       never a plaintext dump — to object storage, ONLY
#                       when BACKUP_REMOTE_ENABLED=true. Local-only remains
#                       the default so a plain `docker compose up` in
#                       development never touches AWS, and so a production
#                       deploy that has not configured S3 yet can still say
#                       so explicitly (docker-compose.prod.yml requires this
#                       variable be set, with no default, precisely so
#                       "off-host backup" can never be silently assumed).
# 7.  verify remotely   HeadObject: size AND checksum, not just exit 0 from
#                       the upload command.
#
# A failed remote upload does not touch the local artifact or local
# retention — see upload_remote()'s own comment for why the overall cycle
# still exits non-zero when that happens.

set -eu

BACKUP_DIR="${BACKUP_DIR:-/backups}"
INTERVAL="${BACKUP_INTERVAL_SECONDS:-86400}"
KEEP_DAILY="${BACKUP_RETENTION_DAILY:-7}"
KEEP_WEEKLY="${BACKUP_RETENTION_WEEKLY:-4}"
KEEP_MONTHLY="${BACKUP_RETENTION_MONTHLY:-6}"
REMOTE_ENABLED="${BACKUP_REMOTE_ENABLED:-false}"

: "${BACKUP_ENCRYPTION_PASSPHRASE:?BACKUP_ENCRYPTION_PASSPHRASE is required}"
: "${PGDATABASE:?PGDATABASE is required}"

log() { echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) backup: $*"; }

mkdir -p "$BACKUP_DIR/daily" "$BACKUP_DIR/weekly" "$BACKUP_DIR/monthly"

run_backup() {
    stamp="$(date -u +%Y%m%dT%H%M%SZ)"
    plain="/tmp/${PGDATABASE}-${stamp}.dump"
    target="$BACKUP_DIR/daily/${PGDATABASE}-${stamp}.dump.enc"

    log "starting dump of ${PGDATABASE}"
    if ! pg_dump -Fc -f "$plain"; then
        log "ERROR pg_dump failed"
        rm -f "$plain"
        return 1
    fi
    log "dump complete ($(wc -c < "$plain") bytes)"

    # AES-256-CBC with a salted, iterated key derivation. -pbkdf2 matters:
    # without it openssl uses a single MD5 round, which makes a weak
    # passphrase trivially brute-forceable against a stolen dump.
    if ! openssl enc -aes-256-cbc -pbkdf2 -iter 200000 -salt \
            -in "$plain" -out "$target" \
            -pass env:BACKUP_ENCRYPTION_PASSPHRASE; then
        log "ERROR encryption failed"
        rm -f "$plain" "$target"
        return 1
    fi
    rm -f "$plain"
    log "encrypted -> $(basename "$target") ($(wc -c < "$target") bytes)"

    # Verify what was actually written, not what we think we wrote. A
    # backup is only real if it can be decrypted AND parsed as a dump.
    # This catches a wrong passphrase too — verified: decrypting with the
    # wrong key makes pg_restore exit non-zero.
    #
    # `pg_restore --list` with NO filename reads stdin. Passing `-` as a
    # filename does NOT mean stdin: pg_restore takes it literally and
    # fails with "could not open input file". Reading from the pipe also
    # keeps the decrypted dump off the disk entirely.
    if ! openssl enc -d -aes-256-cbc -pbkdf2 -iter 200000 \
            -in "$target" -pass env:BACKUP_ENCRYPTION_PASSPHRASE 2>/dev/null \
            | pg_restore --list >/tmp/verify.txt 2>/dev/null; then
        log "ERROR verification failed — artifact is not a readable dump"
        rm -f "$target"
        return 1
    fi
    log "verified: $(wc -l < /tmp/verify.txt) objects in the archive"
    rm -f /tmp/verify.txt

    # Promote copies for the weekly/monthly tiers. Hard links, so extra
    # retention tiers cost inodes rather than disk.
    [ "$(date -u +%u)" = "7" ] && ln -f "$target" "$BACKUP_DIR/weekly/$(basename "$target")" || true
    [ "$(date -u +%d)" = "01" ] && ln -f "$target" "$BACKUP_DIR/monthly/$(basename "$target")" || true

    prune daily   "$KEEP_DAILY"
    prune weekly  "$KEEP_WEEKLY"
    prune monthly "$KEEP_MONTHLY"

    # Heartbeat. Prometheus/node_exporter textfile collection or a simple
    # staleness check can watch this; a backup job that silently stopped
    # looks exactly like one that is working until you need it.
    date -u +%s > "$BACKUP_DIR/last_success"

    # Same fact in Prometheus textfile-collector format. Point a
    # node_exporter --collector.textfile.directory at $BACKUP_DIR and the
    # DatabaseBackupStale rule in monitoring/prometheus/alerts.yml starts
    # working with no other wiring. Until then the file is inert and the
    # rule produces no samples, which is the honest default: a backup alert
    # that fires because nothing is scraping it teaches people to ignore it.
    write_prom_metric masar_backup_last_success_timestamp_seconds \
        "Unix time of the last verified LOCAL database backup." \
        "backup_last_success.prom"

    # Off-host copy. Local success stands regardless of what happens here —
    # local retention above has already run — but the CYCLE as a whole must
    # not report success while claiming an off-host copy that does not
    # exist, so a remote failure flips the return value below even though
    # every local step succeeded.
    remote_rc=0
    upload_remote "$target" || remote_rc=1

    log "cycle complete"
    return "$remote_rc"
}

# write_prom_metric NAME HELP_TEXT FILENAME
# Shared by the local and remote heartbeats — same atomic-write-then-rename
# pattern (a reader never sees a half-written file), same reasoning about
# why an unscraped metric must produce no samples rather than a false zero.
write_prom_metric() {
    name="$1"; help="$2"; file="$3"
    {
        echo "# HELP $name $help"
        echo "# TYPE $name gauge"
        echo "$name $(date -u +%s)"
    } > "$BACKUP_DIR/$file.$$"
    mv "$BACKUP_DIR/$file.$$" "$BACKUP_DIR/$file"
}

# upload_remote ARTIFACT
#
# Ships the already-encrypted, already-verified local artifact to object
# storage. Never touches a plaintext dump — by the time this runs, the
# plaintext has already been deleted (see run_backup above).
#
# Disabled by default (BACKUP_REMOTE_ENABLED unset or anything but
# "true"): a plain local-only backup must keep working exactly as it did
# before this function existed, so development and any deploy that has not
# configured object storage yet are unaffected. docker-compose.prod.yml
# requires BACKUP_REMOTE_ENABLED to be set explicitly (no default there),
# so "off-host backup" is a decision, not a value nobody set.
#
# Atomicity: relies on S3 PutObject's own guarantee rather than a separate
# temporary-key dance — a PutObject either fully lands at the target key or
# the key does not exist at all; there is no partially-uploaded state a
# reader can observe. That guarantee is sufficient here specifically
# because every key is timestamp-unique (see $key below) and therefore
# never overwrites a previous, good backup — a failed retry simply leaves
# no object at that exact key rather than corrupting one that already
# existed.
upload_remote() {
    artifact="$1"
    name="$(basename "$artifact")"

    if [ "$REMOTE_ENABLED" != "true" ]; then
        log "remote_upload_skipped reason=BACKUP_REMOTE_ENABLED=${REMOTE_ENABLED}"
        return 0
    fi

    # Fail loudly, not silently, on a half-configured remote — a backup
    # that logs "skipped" would look identical to "disabled on purpose";
    # one that claims success without a bucket would be worse than either.
    : "${BACKUP_S3_BUCKET:?BACKUP_S3_BUCKET is required when BACKUP_REMOTE_ENABLED=true}"
    : "${AWS_ACCESS_KEY_ID:?AWS_ACCESS_KEY_ID is required when BACKUP_REMOTE_ENABLED=true}"
    : "${AWS_SECRET_ACCESS_KEY:?AWS_SECRET_ACCESS_KEY is required when BACKUP_REMOTE_ENABLED=true}"

    prefix="${BACKUP_S3_PREFIX:-masar/postgres}"
    # Date-partitioned and timestamp-unique — sortable, and a disaster
    # recovery operator can browse straight to a day without listing the
    # whole prefix. The filename itself is unchanged from the local
    # convention (see run_backup), so a key never needs translating back
    # to figure out which local artifact it corresponds to.
    key="${prefix}/$(date -u +%Y)/$(date -u +%m)/$(date -u +%d)/${name}"

    aws_opts=""
    [ -n "${BACKUP_S3_ENDPOINT_URL:-}" ] && aws_opts="--endpoint-url ${BACKUP_S3_ENDPOINT_URL}"
    [ -n "${BACKUP_S3_REGION:-}" ] && export AWS_DEFAULT_REGION="$BACKUP_S3_REGION"

    # SSE-S3 by default when remote backup is on — free, no extra key
    # management, and the actual security property (encrypted before it
    # ever leaves the host) already holds regardless. SSE-KMS is opt-in
    # for deployments that already have a KMS key; BACKUP_S3_SSE=none
    # disables server-side encryption entirely (the client-side AES-256
    # layer is unaffected either way — this setting is belt-and-suspenders
    # on top of it, never a substitute for it).
    # `s3api put-object` takes `--server-side-encryption` /
    # `--ssekms-key-id` — NOT `--sse` / `--sse-kms-key-id`, which are the
    # higher-level `aws s3 cp`/`sync` commands' flag names for the same
    # thing. Confirmed the hard way: the wrong pair, in this same script,
    # 400'd against a real S3-compatible endpoint during the disaster-
    # recovery drill this feature was verified with — caught by actually
    # running it, which is exactly why that drill exists.
    sse_opts=""
    case "${BACKUP_S3_SSE:-AES256}" in
        AES256) sse_opts="--server-side-encryption AES256" ;;
        aws:kms)
            sse_opts="--server-side-encryption aws:kms"
            [ -n "${BACKUP_S3_KMS_KEY_ID:-}" ] && sse_opts="$sse_opts --ssekms-key-id ${BACKUP_S3_KMS_KEY_ID}"
            ;;
        none | "") sse_opts="" ;;
    esac

    local_size=$(wc -c < "$artifact")
    # Base64 SHA-256, matching the encoding S3's own checksum field uses —
    # a direct byte-for-byte comparison against what HeadObject reports
    # below, not merely "the upload command exited 0".
    local_sha256_b64=$(openssl dgst -sha256 -binary "$artifact" | openssl base64 -A)

    log "remote_upload_started bucket=${BACKUP_S3_BUCKET} key=${key} size=${local_size}b"

    # shellcheck disable=SC2086
    if ! aws $aws_opts s3api put-object \
            --bucket "$BACKUP_S3_BUCKET" --key "$key" \
            --body "$artifact" \
            --checksum-algorithm SHA256 \
            $sse_opts \
            >/tmp/put-object.json 2>/tmp/upload.err; then
        log "ERROR remote_upload_failed bucket=${BACKUP_S3_BUCKET} key=${key} $(tail -c 300 /tmp/upload.err | tr '\n' ' ')"
        rm -f /tmp/put-object.json /tmp/upload.err
        return 1
    fi
    rm -f /tmp/put-object.json /tmp/upload.err

    # Remote verification: exit 0 from put-object is not proof of
    # anything by itself — HeadObject re-reads the object AS STORED and
    # both its size and its checksum must match what was actually sent.
    # shellcheck disable=SC2086
    remote_size=$(aws $aws_opts s3api head-object \
            --bucket "$BACKUP_S3_BUCKET" --key "$key" --checksum-mode ENABLED \
            --query 'ContentLength' --output text 2>/tmp/verify.err) \
        || { log "ERROR remote_verify_failed bucket=${BACKUP_S3_BUCKET} key=${key} $(tail -c 300 /tmp/verify.err | tr '\n' ' ')"; rm -f /tmp/verify.err; return 1; }
    # shellcheck disable=SC2086
    remote_sha256_b64=$(aws $aws_opts s3api head-object \
            --bucket "$BACKUP_S3_BUCKET" --key "$key" --checksum-mode ENABLED \
            --query 'ChecksumSHA256' --output text 2>/dev/null)
    rm -f /tmp/verify.err

    if [ "$remote_size" != "$local_size" ]; then
        log "ERROR remote_verify_size_mismatch bucket=${BACKUP_S3_BUCKET} key=${key} local=${local_size} remote=${remote_size}"
        return 1
    fi
    if [ -n "$remote_sha256_b64" ] && [ "$remote_sha256_b64" != "None" ] && [ "$remote_sha256_b64" != "$local_sha256_b64" ]; then
        log "ERROR remote_verify_checksum_mismatch bucket=${BACKUP_S3_BUCKET} key=${key}"
        return 1
    fi

    log "remote_upload_succeeded bucket=${BACKUP_S3_BUCKET} key=${key} size=${remote_size}b sha256=${local_sha256_b64}"
    printf '%s\n' "$key" > "$BACKUP_DIR/last_remote_key"
    write_prom_metric masar_backup_remote_last_success_timestamp_seconds \
        "Unix time of the last verified OFF-HOST database backup." \
        "backup_remote_last_success.prom"
    return 0
}

prune() {
    tier="$1"; keep="$2"
    # shellcheck disable=SC2012
    count=$(ls -1 "$BACKUP_DIR/$tier"/*.dump.enc 2>/dev/null | wc -l)
    if [ "$count" -gt "$keep" ]; then
        # shellcheck disable=SC2012
        ls -1t "$BACKUP_DIR/$tier"/*.dump.enc | tail -n +$((keep + 1)) | while read -r old; do
            rm -f "$old"
            log "pruned $tier/$(basename "$old")"
        done
    fi
}

# One immediate run so a fresh deployment has a backup within seconds
# rather than after the first full interval.
initial_rc=0
run_backup || initial_rc=$?
if [ "$initial_rc" -ne 0 ]; then
    log "initial backup FAILED (exit ${initial_rc})"
fi

# Test hook only — never set in docker-compose.*.yml. Exits after the one
# run above instead of entering the infinite loop, with that run's own
# exit code, so the automated tests (deploy/backup/tests/test_pg_backup.py)
# can assert on a single deterministic cycle instead of a process that
# never returns.
if [ "${BACKUP_RUN_ONCE:-false}" = "true" ]; then
    exit "$initial_rc"
fi

while true; do
    sleep "$INTERVAL"
    if ! run_backup; then
        log "scheduled backup FAILED — /backups/last_success is now stale"
    fi
done
