# Environment variables and secrets

Create a local `.env` from `.env.example` and add only the credentials required by the services you actually use.

Example:

```text
OPENAI_API_KEY=
```

Rules:

- Never commit `.env`.
- Never put provider keys in browser/client source.
- Prefer short-lived/ephemeral credentials for client-side realtime connections.
- Scope credentials and tool permissions to the current user/agent responsibility.
- Rotate credentials when required and update the local secret source rather than hardcoding a new value.
