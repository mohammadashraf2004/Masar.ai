#!/usr/bin/env bash
#
# deploy/verify-secrets.sh
#
# Pre-flight check: is every production secret/configuration value present?
#
# Reports PRESENCE ONLY. It never prints a value, never echoes an
# environment variable, and never writes one to a log — running it with
# `set -x`, piping it into a report, or pasting its output into a ticket is
# safe by construction.
#
# It deliberately does NOT validate that a value is *correct* — only that it
# exists and is non-empty, plus a few shape checks that need no secret
# material (length, an https:// prefix, a known-bad default). Correctness is
# proved by the application's own fail-fast guards at boot
# (backend/app/core/config.py) and by the smoke test.
#
# Usage:
#   ./deploy/verify-secrets.sh                    # check the current environment
#   ./deploy/verify-secrets.sh /path/to/prod.env  # check an env file
#
# Exit code 0 = every REQUIRED value present. 1 = at least one missing.

set -uo pipefail

ENV_FILE="${1:-}"

if [[ -n "$ENV_FILE" ]]; then
    if [[ ! -f "$ENV_FILE" ]]; then
        echo "error: env file not found: $ENV_FILE" >&2
        exit 2
    fi
    # Load without echoing. `set -a` exports everything the file defines.
    set -a
    # shellcheck disable=SC1090
    source "$ENV_FILE"
    set +a
    echo "Source: $ENV_FILE"
else
    echo "Source: current environment"
fi
echo

PASS=0
FAIL=0

# present NAME LABEL [required|optional] [note]
present() {
    local name="$1" label="$2" req="${3:-required}" note="${4:-}"
    local value="${!name-}"
    local status
    if [[ -n "$value" ]]; then
        status="configured"
        PASS=$((PASS + 1))
    else
        if [[ "$req" == "required" ]]; then
            status="MISSING"
            FAIL=$((FAIL + 1))
        else
            status="not set (optional)"
        fi
    fi
    printf '  %-28s %-22s %s\n' "$name" "$status" "$note"
}

# check_len NAME MIN — length only; the value itself is never shown.
check_len() {
    local name="$1" min="$2"
    local value="${!name-}"
    if [[ -n "$value" && ${#value} -lt $min ]]; then
        printf '  %-28s %-22s %s\n' "$name" "TOO SHORT" "needs >= $min chars (has ${#value})"
        FAIL=$((FAIL + 1))
    fi
}

# check_not NAME BADVALUE — catches known-bad defaults without printing.
check_not() {
    local name="$1" bad="$2"
    local value="${!name-}"
    if [[ "$value" == "$bad" ]]; then
        printf '  %-28s %-22s %s\n' "$name" "UNSAFE DEFAULT" "still the placeholder value"
        FAIL=$((FAIL + 1))
    fi
}

# check_https NAME
check_https() {
    local name="$1"
    local value="${!name-}"
    if [[ -n "$value" && "$value" != https://* ]]; then
        printf '  %-28s %-22s %s\n' "$name" "NOT HTTPS" "must be an https:// origin in production"
        FAIL=$((FAIL + 1))
    fi
}

echo "── Core (application refuses to boot without these) ──────────────────"
present APP_ENV              "environment"   required "must be 'production'"
present SECRET_KEY           "JWT signing"   required
check_len SECRET_KEY 32
check_not SECRET_KEY "change-me-in-production"
# docker-compose.yml BUILDS DATABASE_URL from the POSTGRES_* values below
# (it must point at the compose-internal host `db`, not whatever a
# developer has locally), so it is normally absent from the env file and
# that is correct. It is only required here if you are running the API
# outside the bundled compose stack.
if [[ -n "${DATABASE_URL-}" ]]; then
    present DATABASE_URL     "database DSN"  required "least-privilege role + ?sslmode=require"
elif [[ -n "${POSTGRES_USER-}" && -n "${POSTGRES_PASSWORD-}" && -n "${POSTGRES_DB-}" ]]; then
    printf '  %-28s %-22s %s\n' "DATABASE_URL" "derived by compose" "from POSTGRES_USER/PASSWORD/DB"
    PASS=$((PASS + 1))
else
    present DATABASE_URL     "database DSN"  required "or set POSTGRES_USER/PASSWORD/DB"
fi
present REDIS_URL            "rate limits"   required "boot probes reachability"
present FRONTEND_URL         "CORS origin"   required
check_https FRONTEND_URL
present RESEND_API_KEY       "email"         required "verification gate depends on it"
present METRICS_TOKEN        "metrics auth"  required "or set METRICS_ENABLED=false"
check_len METRICS_TOKEN 16

echo
echo "── Database ─────────────────────────────────────────────────────────"
present POSTGRES_USER        "db user"       required
present POSTGRES_PASSWORD    "db password"   required "see F-4: does NOT change an existing volume"
check_not POSTGRES_PASSWORD "password"
present POSTGRES_DB          "db name"       required

echo
echo "── AI provider ──────────────────────────────────────────────────────"
backend_name="${GENERATION_BACKEND:-anthropic}"
printf '  %-28s %-22s %s\n' "GENERATION_BACKEND" "${backend_name}" "selects which key is required"
if [[ "$backend_name" == "openai" ]]; then
    present OPENAI_API_KEY    "LLM key"      required "MUST be the rotated key (F-1)"
    present ANTHROPIC_API_KEY "LLM key"      optional
else
    present ANTHROPIC_API_KEY "LLM key"      required
    present OPENAI_API_KEY    "LLM key"      optional "MUST be the rotated key if set (F-1)"
fi

echo
echo "── Payments (Paymob) ────────────────────────────────────────────────"
present PAYMOB_API_KEY               "paymob"  required
present PAYMOB_INTEGRATION_ID_CARD   "paymob"  required
present PAYMOB_INTEGRATION_ID_WALLET "paymob"  required
present PAYMOB_IFRAME_ID             "paymob"  required
present PAYMOB_HMAC_SECRET           "paymob"  required "without it NO payment is ever confirmed"

echo
echo "── Reverse proxy / CORS ─────────────────────────────────────────────"
present TRUSTED_PROXY_COUNT  "proxy hops"    required "0 is only correct with no proxy"
if [[ "${TRUSTED_PROXY_COUNT:-0}" != "0" ]]; then
    present TRUSTED_PROXY_IPS "proxy allowlist" required "fail-fast if count > 0 and this is empty"
else
    printf '  %-28s %-22s %s\n' "TRUSTED_PROXY_IPS" "n/a" "not needed while count = 0"
fi
present EXTRA_CORS_ORIGINS   "extra origins" optional

echo
echo "── Monitoring / ops ─────────────────────────────────────────────────"
present GRAFANA_PASSWORD     "grafana admin" required "ships as admin/admin otherwise"
present ALERT_RECEIVER_URL   "alert sink"    optional "Slack/Discord webhook, if used"
present BACKUP_ENCRYPTION_PASSPHRASE "backup encryption" required "deploy/backup/pg-backup.sh"

echo
echo "── Build arguments (baked into the image, not runtime) ──────────────"
present NEXT_PUBLIC_API_URL  "frontend->API" required "rebuild required to change"
check_https NEXT_PUBLIC_API_URL

echo
echo "─────────────────────────────────────────────────────────────────────"
printf '  %d configured, %d problem(s)\n' "$PASS" "$FAIL"
if [[ $FAIL -gt 0 ]]; then
    echo "  RESULT: NOT READY — resolve the items above before deploying."
    exit 1
fi
echo "  RESULT: all required values present."
echo "  (Presence is not correctness — the app's own fail-fast guards and the"
echo "   smoke test are what prove the values actually work.)"
exit 0
