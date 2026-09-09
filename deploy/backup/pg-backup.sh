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
# ── What this does NOT do ───────────────────────────────────────────────
# It does not ship backups off-host. The volume it writes to lives on the
# same machine as the database, which means it survives a dropped table but
# not a lost server. Replicating /backups to object storage (restic, rclone,
# aws s3 sync) is a required, separate step — see LAUNCH_CHECKLIST Phase 5.
# It is left out here deliberately rather than half-implemented, because a
# backup script that appears to be doing off-host replication but is not is
# worse than one that plainly does not.

set -eu

BACKUP_DIR="${BACKUP_DIR:-/backups}"
INTERVAL="${BACKUP_INTERVAL_SECONDS:-86400}"
KEEP_DAILY="${BACKUP_RETENTION_DAILY:-7}"
KEEP_WEEKLY="${BACKUP_RETENTION_WEEKLY:-4}"
KEEP_MONTHLY="${BACKUP_RETENTION_MONTHLY:-6}"

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
    {
        echo "# HELP masar_backup_last_success_timestamp_seconds Unix time of the last verified database backup."
        echo "# TYPE masar_backup_last_success_timestamp_seconds gauge"
        echo "masar_backup_last_success_timestamp_seconds $(date -u +%s)"
    } > "$BACKUP_DIR/backup_last_success.prom.$$"
    mv "$BACKUP_DIR/backup_last_success.prom.$$" "$BACKUP_DIR/backup_last_success.prom"

    log "cycle complete"
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
if ! run_backup; then
    log "initial backup FAILED"
fi

while true; do
    sleep "$INTERVAL"
    if ! run_backup; then
        log "scheduled backup FAILED — /backups/last_success is now stale"
    fi
done
