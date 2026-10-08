from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


# GENERATION_BACKEND value -> the setting that holds that backend's API key.
# Mirrors LLMEnum, which cannot be imported here: app.services imports this
# module, so importing it back would be circular.
_LLM_KEY_SETTING = {
    "anthropic": "ANTHROPIC_API_KEY",
    "openai": "OPENAI_API_KEY",
}


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
    # Clock-skew tolerance, in seconds, for the exp / nbf / iat checks.
    # Tokens are issued and verified by different processes (and, behind a
    # load balancer, different hosts), and a wall clock can step backwards
    # when NTP or a VM time-sync corrects it. Without any tolerance a token
    # issued a moment before such a step has an `iat` "in the future" and is
    # refused with a 401 on a perfectly valid session. Kept to seconds so it
    # does not meaningfully extend a token's 12-hour life.
    JWT_LEEWAY_SECONDS: int = 10

    # Failed-login lockout (per email+IP pair, see app.core.login_guard).
    LOGIN_MAX_FAILURES: int = 8
    LOGIN_LOCKOUT_MINUTES: int = 15

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
    # Wall-clock budget for one provider call, and how often the SDK may
    # re-send it. Sized against the two limits on either side: the browser
    # abandons any API call at 30 s (frontend/src/lib/api.ts) and gunicorn
    # kills a worker at 60 s (--timeout in docker-compose.yml). The SDK
    # defaults — 10 minutes, 2 retries — overshoot both, so a slow provider
    # meant a student staring at a spinner for a request the server was
    # still busy paying for. Applied by LLMProviderFactory (the web app);
    # offline scripts that build a provider themselves keep their own.
    GENERATION_TIMEOUT_SECONDS: float = 25.0
    GENERATION_MAX_RETRIES: int = 0
    # Mentor replies that fail validation fall back to a safe answer and are
    # refunded - this many times per account per 24 h. Beyond it the send is
    # charged: each one already cost up to three provider calls.
    MENTOR_VALIDATION_REFUNDS_PER_DAY: int = 3
    # AI-reviewed project submissions (/tracks/projects/{id}/submit) per account
    # in any rolling 24 hours, on top of that route's per-IP limit.
    PROJECT_REVIEW_LIMIT_PER_DAY: int = 10
    # Largest request body the API accepts (the largest legitimate one is a
    # 200k-character Project Lab file). Caddy enforces the same at the edge.
    MAX_REQUEST_BODY_BYTES: int = 4 * 1024 * 1024

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

    # Learners' weekly study time, used only to turn a path's remaining hours
    # into a "weeks" estimate for display. An assumption, not a promise — it is
    # a setting so the estimate can follow what learners actually do.
    LEARNING_HOURS_PER_WEEK: int = 6

    # ─── Project Lab execution ────────────────────────────────────────────
    # Where learner Python/SQL from the Project Lab runs. Never in this
    # process: see app/services/project_lab/execution.py.
    #   runner   — the isolated project-runner service (docker-compose.yml),
    #              reached over a Unix socket; it has no network at all. The
    #              only backend that is a security boundary.
    #   local    — a restricted subprocess of the API (development and
    #              tests only; NOT a sandbox — refused in production below).
    #   disabled — Run / Check Step report "unavailable".
    # Blank means "local" in development and "disabled" in production, so a
    # production deploy never silently falls back to the unsafe adapter.
    PROJECT_LAB_EXECUTION_BACKEND: str = ""
    PROJECT_LAB_RUNNER_SOCKET: str = ""
    PROJECT_LAB_RUNNER_TOKEN: str = ""
    # true: refuse to send jobs to a runner that does not report gVisor
    # (checked against the runner's /healthz). Set it when the runner is
    # deployed with runtime: runsc, so a misconfigured host fails loudly.
    PROJECT_LAB_REQUIRE_GVISOR: bool = False
    # One execution at a time per learner. A lease older than this is treated
    # as abandoned (a crashed worker), so a learner is never locked out.
    PROJECT_LAB_EXECUTION_LEASE_SECONDS: int = 180
    # Total size of a learner's editable files.
    PROJECT_LAB_MAX_WORKSPACE_BYTES: int = 1_000_000
    # Client-side ceiling for one runner request, including time queued behind
    # other jobs (the runner executes one job at a time per replica).
    PROJECT_LAB_RUNNER_TIMEOUT_SECONDS: float = 45.0
    # Limits applied by the local adapter. The runner service has its own.
    PROJECT_LAB_LOCAL_TIMEOUT_SECONDS: float = 15.0
    PROJECT_LAB_LOCAL_MEMORY_MB: int = 1024
    # Fair share of the shared runner per account (Project Lab and Python code
    # exercises together): runner seconds allowed per rolling window. The
    # default caps any one account at a fifth of one replica's time.
    RUNNER_USER_SECONDS: int = 120
    RUNNER_USER_WINDOW_SECONDS: int = 600

    # ─── Pro plan: included AI usage ──────────────────────────────────────
    # A Pro subscriber's AI actions draw on an allowance instead of the
    # wallet: this many credits (the same per-action prices as the wallet)
    # per rolling window, counted from each request's reservation time.
    PRO_AI_CREDITS_PER_WINDOW: int = 50
    PRO_AI_WINDOW_SECONDS: int = 14400
    # The seven-day trial opens every course but its AI actions are paid from
    # the wallet: the allowance starts with the first payment (decision
    # 2026-10-08).
    PRO_AI_INCLUDE_TRIAL: bool = False
    # A reservation neither finalized nor released after this long belongs to
    # a request that never answered (a worker killed mid-request): it is
    # released, not counted - nothing was delivered. Well above the longest
    # request (gunicorn --timeout 60).
    PRO_AI_RESERVATION_TTL_SECONDS: int = 300

    # ─── CORS ─────────────────────────────────────────────────────────────
    FRONTEND_URL: str = "http://localhost:3000"
    # Comma-separated list of extra allowed origins for production
    # (staging domains, custom domains, etc.), e.g. "https://app.example.com,https://staging.example.com"
    EXTRA_CORS_ORIGINS: str = ""

    # ─── Email (Resend) ──────────────────────────────────────────────────────
    RESEND_API_KEY: Optional[str] = None
    EMAIL_FROM: str = "Masar <noreply@example.com>"

    # ─── Payments (Kashier) ────────────────────────────────────────────────
    # Every new checkout - Pro subscriptions, course purchases, wallet top-ups
    # and exam fees - is a Kashier hosted payment session. "test" talks to
    # test-api.kashier.io with the test keys, "live" to api.kashier.io with the
    # live keys; production refuses "test". All four blank: payments are off
    # (checkout answers 503) and nothing else is affected.
    KASHIER_MODE: str = "test"
    KASHIER_MERCHANT_ID: Optional[str] = None
    # The Payment API key: signs webhooks (x-kashier-signature) - the HMAC secret.
    KASHIER_API_KEY: Optional[str] = None
    # The secret key: the Authorization header of server-to-server calls.
    KASHIER_SECRET_KEY: Optional[str] = None
    # This API's public https origin (e.g. https://api.masarai.net): Kashier posts
    # the webhook to <origin>/api/v1/payments/kashier/webhook and returns the
    # shopper to <origin>/api/v1/payments/kashier/return.
    KASHIER_PUBLIC_API_URL: Optional[str] = None
    KASHIER_ALLOWED_METHODS: str = "card,wallet"
    KASHIER_SESSION_MINUTES: int = 60
    KASHIER_TIMEOUT_SECONDS: float = 20.0

    # ─── Payments (Paymob, historical only) ────────────────────────────────
    # No new Paymob payment is ever started. These remain so the Paymob
    # webhook can still verify and reconcile the payments and refunds of the
    # orders Paymob took before the switch to Kashier.
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

    def llm_config_problems(self) -> list[str]:
        """What stops the AI provider from working, named by setting.

        Returns names only, never values: the result ends up in logs and in
        the production boot error. An empty list means a call can be made.

        The blank-model case is not hypothetical. pydantic-settings takes an
        empty environment variable over the default, so `GENERATION_MODEL_ID=`
        — which deploy/production.env.example used to ship — resolves to ""
        and every provider call is then rejected for having no model.
        """
        problems: list[str] = []
        key_setting = _LLM_KEY_SETTING.get(self.GENERATION_BACKEND)
        if key_setting is None:
            problems.append(
                "GENERATION_BACKEND must be one of: " + ", ".join(sorted(_LLM_KEY_SETTING))
            )
        elif not (getattr(self, key_setting) or "").strip():
            problems.append(f"{key_setting} must be set when GENERATION_BACKEND={self.GENERATION_BACKEND}")
        if not self.GENERATION_MODEL_ID.strip():
            problems.append("GENERATION_MODEL_ID must not be blank")
        return problems

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

    @property
    def project_lab_backend(self) -> str:
        """The effective Project Lab execution backend (see the settings above)."""
        chosen = self.PROJECT_LAB_EXECUTION_BACKEND.strip().lower()
        if chosen:
            return chosen
        return "disabled" if self.is_production else "local"

    def project_lab_problems(self) -> list[str]:
        problems: list[str] = []
        backend = self.project_lab_backend
        if backend not in {"runner", "local", "disabled"}:
            problems.append("PROJECT_LAB_EXECUTION_BACKEND must be one of: runner, local, disabled")
        if backend == "runner" and not self.PROJECT_LAB_RUNNER_SOCKET.strip().startswith("/"):
            problems.append("PROJECT_LAB_RUNNER_SOCKET must be an absolute socket path when PROJECT_LAB_EXECUTION_BACKEND=runner")
        token = self.PROJECT_LAB_RUNNER_TOKEN.strip()
        if backend == "runner" and (len(token) < 24 or "change-me" in token):
            problems.append(
                "PROJECT_LAB_RUNNER_TOKEN must be a random value of 24+ characters (not the compose "
                "default) when PROJECT_LAB_EXECUTION_BACKEND=runner"
            )
        return problems

    @property
    def kashier_configured(self) -> bool:
        return all((self.KASHIER_MERCHANT_ID, self.KASHIER_API_KEY, self.KASHIER_SECRET_KEY,
                    self.KASHIER_PUBLIC_API_URL))

    def kashier_problems(self, *, production: bool) -> list[str]:
        """Payments off (nothing set) is allowed; half a configuration is not."""
        problems: list[str] = []
        if self.KASHIER_MODE not in {"test", "live"}:
            problems.append("KASHIER_MODE must be test or live")
        values = (self.KASHIER_MERCHANT_ID, self.KASHIER_API_KEY, self.KASHIER_SECRET_KEY,
                  self.KASHIER_PUBLIC_API_URL)
        if any(values) and not all(values):
            problems.append(
                "Kashier is partly configured: set all of KASHIER_MERCHANT_ID, KASHIER_API_KEY, "
                "KASHIER_SECRET_KEY and KASHIER_PUBLIC_API_URL (or none, to keep payments off)"
            )
        if production and any(values):
            if self.KASHIER_MODE != "live":
                problems.append("KASHIER_MODE must be live in production (test keys take no real payments)")
            if not (self.KASHIER_PUBLIC_API_URL or "").startswith("https://"):
                problems.append("KASHIER_PUBLIC_API_URL must be an https:// origin in production")
        return problems


settings = Settings()

# ─── Fail fast on unsafe production config ─────────────────────────────────
if settings.is_production:
    _problems = []
    if settings.SECRET_KEY == "change-me-in-production" or len(settings.SECRET_KEY) < 32:
        _problems.append("SECRET_KEY must be set to a random value of at least 32 characters")
    if len(set(settings.SECRET_KEY)) < 8:
        _problems.append("SECRET_KEY has too little variation to be a real random value")
    if settings.ALGORITHM not in {"HS256", "HS384", "HS512"}:
        # Tokens are signed and verified with the shared SECRET_KEY only; any
        # other value ("none", an asymmetric alg) is a misconfiguration.
        _problems.append("ALGORITHM must be HS256, HS384 or HS512")
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
    if not settings.RESEND_API_KEY:
        # Newly load-bearing. Billable features now require a verified
        # email address (app.core.authz + wallet_service.deduct_credits),
        # and resend_service fails SOFT when unconfigured — it logs and
        # returns False rather than raising. Those two together mean a
        # production deploy without an email provider would hand every new
        # user an account that can never verify and therefore can never
        # spend a credit, with nothing in the logs but a warning. Fail at
        # boot instead of discovering it from support tickets.
        _problems.append(
            "RESEND_API_KEY must be set in production: credit-spending "
            "features require a verified email address, and without an "
            "email provider no user can ever verify"
        )
    # The AI mentor, exercise grading and hints all run on this. Every other
    # check here stops a bad deploy from booting; without this one a deploy
    # with no key (or a blank model id) boots cleanly, passes /health, and
    # then fails every AI request with the first sign being user reports.
    _problems.extend(settings.llm_config_problems())
    _problems.extend(settings.project_lab_problems())
    _problems.extend(settings.kashier_problems(production=True))
    if settings.project_lab_backend == "local":
        # The local adapter runs learner code as the API's own user, with the
        # API's filesystem and network. It exists for development and tests;
        # in production it would hand every learner the API container.
        _problems.append(
            "PROJECT_LAB_EXECUTION_BACKEND=local is not a sandbox and is refused in "
            "production; use runner (or disabled)"
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
