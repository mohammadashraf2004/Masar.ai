from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # ─── App ──────────────────────────────────────────────────────────────
    APP_NAME: str = "Masar"
    APP_VERSION: str = "1.0.0"
    APP_ENV: str = "development"

    # ─── Security ─────────────────────────────────────────────────────────
    SECRET_KEY: str = "change-me-in-production"
    ALGORITHM: str = "HS256"
    # 12 hours. Was 7 days — far too long for a bearer token the browser
    # keeps in localStorage, where any XSS turns into a week-long account
    # takeover. Short enough to bound that window, long enough that a
    # normal study session never gets interrupted.
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 720
    # Bound into every token as `iss`/`aud` and required at verification,
    # so a token minted by some *other* service that happens to share this
    # secret can't be replayed against this API.
    JWT_ISSUER: str = "ai-career-platform"
    JWT_AUDIENCE: str = "ai-career-platform-api"

    # Failed-login lockout (per email+IP pair, see app.core.login_guard).
    LOGIN_MAX_FAILURES: int = 8
    LOGIN_LOCKOUT_MINUTES: int = 15

    # ─── Launch promotion ─────────────────────────────────────────────────
    # A larger signup grant while the platform is finding its first users.
    # Credits only — the certification exam fee is a separate, EGP-only
    # paywall (exam_controller._require_paid_exam) and is NOT affected.
    #
    # LAUNCH_PROMO_UNTIL bounds the OFFER: accounts created after it get
    # the ordinary STARTER_CREDITS. Empty disables the promo entirely, so
    # a missing/typo'd value fails closed rather than granting forever.
    # Format: YYYY-MM-DD (interpreted as end-of-day UTC).
    LAUNCH_PROMO_UNTIL: str = ""
    # Credits granted to accounts created during the window.
    LAUNCH_PROMO_CREDITS: int = 500
    # How long a user keeps them. Unspent promo credits are removed this
    # many days after that user signed up, so the giveaway does not become
    # an open-ended liability. 0 disables expiry.
    LAUNCH_PROMO_DAYS: int = 30

    # ─── Database ─────────────────────────────────────────────────────────
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/ai_career_platform"

    # ─── Rate limiting ────────────────────────────────────────────────────
    # slowapi defaults to per-process in-memory counters, which means each
    # gunicorn worker (and each replica) enforces its own separate budget.
    # REQUIRED in production — the startup check below refuses to boot
    # without it rather than silently degrading to per-process limits.
    REDIS_URL: Optional[str] = None

    # ─── Metrics ──────────────────────────────────────────────────────────
    # /metrics is served by the same app on the same port, which is
    # published to the host — so in production it needs a credential.
    # Prometheus sends it as a bearer token (see monitoring/prometheus.yml).
    METRICS_ENABLED: bool = True
    METRICS_TOKEN: str = ""

    # How many reverse proxies sit between the internet and this app.
    #
    # 0 (the default) means "none" — X-Forwarded-For is IGNORED entirely
    # and the TCP peer address is used. That is the only safe default:
    # X-Forwarded-For is an ordinary request header that any client can
    # set, so honouring it without a proxy in front lets anyone mint a
    # fresh rate-limit bucket per request by rotating the value, which
    # defeats both the login rate limit and the per-account lockout.
    #
    # Set this to the number of proxies you actually run (1 for a single
    # nginx/ALB/Cloudflare in front, 2 for CDN + load balancer, ...).
    # Getting it too HIGH is the dangerous direction: it makes the app
    # read further left in the header, into attacker-controlled entries.
    # See app.core.limiter.client_key for the exact indexing.
    TRUSTED_PROXY_COUNT: int = 0

    # Comma-separated IPs/CIDRs of the proxies above, e.g.
    # "10.0.0.0/8" or "172.31.4.7,172.31.4.8".
    #
    # Counting proxies is not enough on its own: if an attacker can reach
    # this app's port WITHOUT going through the proxy, they can send a
    # one-entry X-Forwarded-For that satisfies the count and lands in the
    # position we read. Checking the socket peer against this list closes
    # that, because a direct connection comes from an untrusted address
    # and its header is then ignored entirely. REQUIRED in production
    # whenever TRUSTED_PROXY_COUNT > 0 (enforced below).
    TRUSTED_PROXY_IPS: str = ""

    # ─── AI provider ──────────────────────────────────────────────────────
    GENERATION_BACKEND: str = "anthropic"
    GENERATION_MODEL_ID: str = "claude-sonnet-4-20250514"
    GENERATION_DEFAULT_MAX_TOKENS: int = 1000
    GENERATION_DEFAULT_TEMPERATURE: float = 0.7
    INPUT_DEFAULT_MAX_CHARACTERS: int = 10000

    # ─── API keys ─────────────────────────────────────────────────────────
    ANTHROPIC_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_API_URL: Optional[str] = None

    # ─── Embedding / Vector DB (future) ───────────────────────────────────
    EMBEDDING_BACKEND: Optional[str] = None
    EMBEDDING_MODEL_ID: Optional[str] = None
    EMBEDDING_MODEL_SIZE: Optional[int] = None
    VECTOR_DB_BACKEND: Optional[str] = None
    VECTOR_DB_PATH: Optional[str] = None
    VECTOR_DB_DISTANCE_METHOD: Optional[str] = None

    # ─── Localisation ─────────────────────────────────────────────────────
    PRIMARY_LANG: str = "en"
    DEFAULT_LANG: str = "en"

    # ─── Track availability ───────────────────────────────────────────────
    # Career tracks open for enrolment, by slug. Everything else in the
    # catalogue is a shell — levels seeded with no topics under them — so
    # enrolling in one buys a dashboard card that opens onto nothing.
    #
    # This is the authoritative rule. The frontend keeps its own copy
    # (frontend/src/lib/tracks.ts) to decide what the UI offers, but that is
    # presentation: POST /tracks/enroll takes a track id, so a client that
    # skips the UI is stopped here instead. Publishing a track is a content
    # seed plus one entry here, not a code change; empty closes enrolment on
    # every track.
    AVAILABLE_TRACK_SLUGS: str = "ai-developer"

    # ─── CORS ─────────────────────────────────────────────────────────────
    FRONTEND_URL: str = "http://localhost:3000"
    # Comma-separated list of extra allowed origins for production
    # (staging domains, custom domains, etc.), e.g. "https://app.example.com,https://staging.example.com"
    EXTRA_CORS_ORIGINS: str = ""

    # ─── Email (Resend) ──────────────────────────────────────────────────────
    RESEND_API_KEY: Optional[str] = None
    EMAIL_FROM: str = "Masar <noreply@example.com>"

    # ─── Payments (Paymob) ─────────────────────────────────────────────────
    PAYMOB_API_KEY: Optional[str] = None
    PAYMOB_INTEGRATION_ID_CARD: Optional[str] = None
    PAYMOB_INTEGRATION_ID_WALLET: Optional[str] = None
    PAYMOB_IFRAME_ID: Optional[str] = None
    PAYMOB_HMAC_SECRET: Optional[str] = None
    PAYMOB_BASE_URL: str = "https://accept.paymob.com/api"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    @property
    def is_production(self) -> bool:
        """Anything that isn't explicitly a local/test environment is
        treated as production. Defaulting the *other* way means a typo in
        APP_ENV ("prod", "Production", "prd") silently disables every
        production safeguard below, which is exactly the failure mode
        these checks exist to prevent."""
        return self.APP_ENV.strip().lower() not in {"development", "dev", "local", "test", "testing"}

    @property
    def launch_promo_until(self):
        """Parsed LAUNCH_PROMO_UNTIL, or None when the promo is off.
        A malformed value returns None — the promo simply does not apply,
        rather than being treated as 'always on'."""
        from datetime import datetime, time, timezone

        raw = self.LAUNCH_PROMO_UNTIL.strip()
        if not raw:
            return None
        try:
            day = datetime.strptime(raw, "%Y-%m-%d").date()
        except ValueError:
            return None
        return datetime.combine(day, time.max, tzinfo=timezone.utc)

    def promo_is_open(self) -> bool:
        from datetime import datetime, timezone

        until = self.launch_promo_until
        return until is not None and datetime.now(timezone.utc) <= until

    @property
    def trusted_proxy_networks(self) -> list:
        """Parsed TRUSTED_PROXY_IPS. Malformed entries are dropped rather
        than silently widening the trust boundary."""
        import ipaddress

        nets = []
        for raw in self.TRUSTED_PROXY_IPS.split(","):
            raw = raw.strip()
            if not raw:
                continue
            try:
                nets.append(ipaddress.ip_network(raw, strict=False))
            except ValueError:
                continue
        return nets

    @property
    def cors_origins(self) -> list[str]:
        """In production ONLY the explicitly configured origins are
        allowed. The localhost entries below are a development
        convenience: with allow_credentials=True, leaving them on in
        production lets any page an attacker can get to run on
        http://localhost:3000 (a malicious local dev server, a desktop
        app's embedded browser) read authenticated responses from the
        production API."""
        origins = {self.FRONTEND_URL}
        if not self.is_production:
            origins.update({
                "http://localhost:3000",
                "http://127.0.0.1:3000",
                "http://localhost:3001",
            })
        origins.update(o.strip() for o in self.EXTRA_CORS_ORIGINS.split(",") if o.strip())
        return sorted(o for o in origins if o)

    @property
    def available_track_slugs(self) -> set[str]:
        """Parsed AVAILABLE_TRACK_SLUGS.

        Compared casefolded and stripped so a stray space or capital in the
        env var can't quietly close enrolment on a published track.
        """
        return {s.strip().casefold() for s in self.AVAILABLE_TRACK_SLUGS.split(",") if s.strip()}


settings = Settings()

# ─── Fail fast on unsafe production config ─────────────────────────────────
if settings.is_production:
    _problems = []
    if settings.SECRET_KEY == "change-me-in-production" or len(settings.SECRET_KEY) < 32:
        _problems.append("SECRET_KEY must be set to a random value of at least 32 characters")
    if len(set(settings.SECRET_KEY)) < 8:
        _problems.append("SECRET_KEY has too little variation to be a real random value")
    if "localhost" in settings.DATABASE_URL or "password@" in settings.DATABASE_URL:
        _problems.append("DATABASE_URL still points at the local dev database/credentials")
    if not settings.FRONTEND_URL.startswith("https://"):
        _problems.append("FRONTEND_URL must be an https:// origin in production")
    if any(o.startswith("http://") for o in settings.cors_origins):
        _problems.append("CORS origins must all be https:// in production")
    if not settings.REDIS_URL:
        # Without shared storage every gunicorn worker and every replica
        # keeps its own counters, so a documented "10/minute" login limit
        # is really 10/minute *per worker*. Failing to boot is the honest
        # outcome: a rate limit that silently enforces 4x what it claims
        # is worse than an obvious startup failure.
        _problems.append(
            "REDIS_URL must be set in production so rate limits and login "
            "lockouts are shared across workers/replicas"
        )
    if settings.METRICS_ENABLED and not settings.METRICS_TOKEN:
        # Unauthenticated /metrics hands anyone route-level traffic,
        # latency, credit burn and auth-failure counts — a free map of the
        # platform's shape and load. Set METRICS_TOKEN, or turn the
        # endpoint off with METRICS_ENABLED=false.
        _problems.append(
            "METRICS_TOKEN must be set when METRICS_ENABLED is true, "
            "otherwise /metrics is public"
        )
    if settings.TRUSTED_PROXY_COUNT < 0:
        _problems.append("TRUSTED_PROXY_COUNT cannot be negative")
    if settings.TRUSTED_PROXY_COUNT > 0 and not settings.trusted_proxy_networks:
        _problems.append(
            "TRUSTED_PROXY_IPS must list the proxy addresses/CIDRs when "
            "TRUSTED_PROXY_COUNT > 0, otherwise a client that reaches this "
            "port directly can forge X-Forwarded-For"
        )
    if _problems:
        raise RuntimeError(
            "Refusing to start with APP_ENV=production due to unsafe configuration:\n  - "
            + "\n  - ".join(_problems)
        )
