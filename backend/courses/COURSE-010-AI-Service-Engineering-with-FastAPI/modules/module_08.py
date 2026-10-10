"""M01.L08 — Authentication and Authorization for GenAI Services.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
Source: Chapter 8, pages not provided in the supplied chapter extract.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M01.L08"

MODULE_ORDER = 1

MODULE_TITLE = "Generative AI Service Foundations"

MODULE_DESCRIPTION = (
    "Secure GenAI services by verifying identities, protecting credentials and tokens, "
    "integrating OAuth identity providers, understanding common authentication attacks, "
    "and enforcing role-, relationship-, and attribute-based authorization at the "
    "application layer."
)

SOURCE_CHAPTER = 8

SOURCE_PAGES = "Not provided in supplied source"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Authentication and Authorization for GenAI Services",

    "slug": "generative-ai-services-m01-l08",

    "description": (
        "Learn how authentication verifies identity and authorization controls actions. "
        "Implement the mental models behind Basic authentication, JWTs, password hashing, "
        "token lifecycle, OAuth2 with an identity provider, CSRF protection, RBAC, ReBAC, "
        "ABAC, hybrid authorization, and authorization services for GenAI APIs."
    ),

    "order": 8,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 4.5,

    "skill_tags": [
        "authentication",
        "authorization",
        "fastapi-security",
        "jwt",
        "password-hashing",
        "bcrypt",
        "oauth2",
        "sso",
        "csrf",
        "rbac",
        "rebac",
        "abac",
        "authorization-guards",
        "genai-security",
    ],

    "prerequisite_ids": [
        "M01.L07",
    ],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Authentication and Authorization for GenAI Services",

        "content": """
# Authentication and Authorization for GenAI Services

> **Course:** Building Generative AI Services  
> **Lesson:** M01.L08  
> **Module:** Generative AI Service Foundations  
> **Source alignment:** Chapter 8 from the supplied source. This lesson is an instructor-authored curriculum adaptation rather than a reproduction of the source text.

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Clearly distinguish authentication from authorization.
- Compare Basic, token/JWT, OAuth, and key-based authentication at a high level.
- Explain why Basic authentication is mainly suitable for simple prototypes or controlled environments.
- Describe the three main parts of a JWT: header, payload, and signature.
- Model users and access tokens in a relational database.
- Explain why raw passwords should never be stored.
- Explain password hashing and salting conceptually.
- Use a password service to hash and verify passwords.
- Describe how short-lived access tokens are issued, decoded, validated, revoked, and expired.
- Explain registration, login, logout, verification, password reset, refresh token, and MFA flows.
- Recognize attacks such as credential stuffing, password spraying, CSRF, open redirect, and phishing.
- Explain OAuth2 authorization-code flow with an identity provider.
- Explain the purpose of scopes, redirect URIs, authorization codes, access tokens, refresh tokens, and state parameters.
- Compare major OAuth2 flows introduced in the chapter.
- Explain authorization as a decision over actor, action, and resource.
- Compare RBAC, ReBAC, and ABAC.
- Implement authorization guards through FastAPI dependencies conceptually.
- Restrict GenAI models and resources based on user privileges.
- Explain why authorization must be enforced by trusted application logic rather than delegated to an LLM.
- Explain why complex permission systems may benefit from a separate authorization service.

---

## 1. Authentication is not authorization

The chapter begins by separating two terms that are often confused.

### Authentication

Authentication asks:

> **Who are you?**

It verifies that an actor really is the identity it claims to be.

Possible authenticators include:

- passwords,
- access tokens,
- security keys,
- identity-provider assertions.

### Authorization

Authorization asks:

> **What are you allowed to do?**

After a user is authenticated, the application still needs to determine whether that user can perform a requested action on a specific resource.

### Airport analogy

The source gives a useful analogy:

```text
Authentication
→ presenting your passport and proving who you are

Authorization
→ having the visa/permission needed for the activity or destination
```

### GenAI example

Suppose Mohammad logs into an AI application successfully.

Authentication may establish:

```text
current user = Mohammad
```

Authorization still needs to answer questions such as:

```text
Can Mohammad use the premium model?
Can Mohammad read conversation 42?
Can Mohammad delete another user's conversation?
Can Mohammad access image generation?
Can Mohammad manage user accounts?
```

### 401 versus 403

A useful practical distinction:

```text
401 Unauthorized
→ identity could not be authenticated

403 Forbidden
→ identity is known, but the action is not permitted
```

The central mental model is:

```text
request
  ↓
authenticate identity
  ↓
authorize requested action
  ↓
execute or deny
```

[[IMAGE_NEEDED: Authentication versus authorization | Two-stage access diagram showing a user first proving identity, then passing a second permission check for a resource/action | Learner should notice that knowing who the user is does not automatically grant access]]

{{exercise:M01.L08.EX01}}

---

## 2. Authentication methods

The chapter introduces four broad approaches.

### Basic authentication

Uses a username and password on the request.

Strength:

- simple to understand and implement.

Main concern:

- reusable credentials are sent with requests, so the mechanism must be handled very carefully and is mainly presented by the source for prototype/internal scenarios rather than public production use.

### Token authentication

The user first authenticates and receives an access token.

Later requests send the token instead of resending the password.

Advantages from the chapter include:

- scalability,
- suitability for APIs,
- decoupling between services,
- customizable claims,
- reduced repeated database checks in some designs.

Challenges include:

- token storage,
- expiry,
- refresh,
- revocation,
- theft risk,
- token size.

### OAuth

Authentication/authorization is delegated to an external identity provider.

Examples mentioned by the source include providers such as:

- GitHub,
- Google,
- Microsoft,
- Apple,
- Meta,
- LinkedIn.

This can reduce how much credential-handling infrastructure your application owns.

### Key-based authentication

Uses cryptographic key pairs.

The chapter introduces the category but does not explore its cryptographic implementation in depth.

[[IMAGE_NEEDED: Authentication methods overview | Four-column diagram for Basic credentials, token/JWT, OAuth identity provider, and public/private-key authentication, each showing the client and server interaction at a high level | Learner should recognize that authentication mechanisms prove identity in different ways]]

### Choosing a mechanism

The source recommends considering:

- security requirements,
- project environment,
- implementation time,
- budget,
- need for external identity/resource access,
- client type.

The right mechanism depends on the system.

---

## 3. Basic authentication in FastAPI

Basic authentication sends an HTTP header shaped like:

```text
Authorization: Basic <encoded credentials>
```

The credentials conceptually contain:

```text
username:password
```

encoded for transport.

### Important point

Encoding is not the same thing as encryption.

The source therefore treats Basic authentication as appropriate mainly for:

- prototypes,
- sandbox systems,
- controlled development environments.

### FastAPI security dependency

A teaching version:

```python
import secrets

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

security = HTTPBasic()


def authenticate_user(
    credentials: HTTPBasicCredentials = Depends(security),
) -> str:
    username_ok = secrets.compare_digest(
        credentials.username.encode("utf-8"),
        b"ali",
    )

    password_ok = secrets.compare_digest(
        credentials.password.encode("utf-8"),
        b"secretpassword",
    )

    if not (username_ok and password_ok):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect credentials",
            headers={"WWW-Authenticate": "Basic"},
        )

    return credentials.username
```

### Constant-time comparison

The source uses `secrets.compare_digest()`.

The idea is to reduce information leakage through timing differences during secret comparison.

### Generic error messages

Authentication failures should avoid revealing unnecessary information.

Prefer:

```text
Incorrect credentials
```

rather than:

```text
Username exists, but password is wrong
```

The second message gives attackers useful account-enumeration information.

### Dependency-based protection

FastAPI dependencies make security reusable.

```python
@app.get("/users/me")
def current_user(
    username: str = Depends(authenticate_user),
):
    ...
```

This same pattern becomes more powerful with JWT and authorization guards later.

---

## 4. JSON Web Tokens (JWT)

A JWT is a compact token format used to carry claims between systems.

The chapter breaks a JWT into three parts:

```text
header.payload.signature
```

### Header

Describes information such as:

- token type,
- signing algorithm.

### Payload

Contains claims.

Possible claims include:

- user identifier,
- role,
- issuer,
- expiration,
- token identifier.

### Signature

Protects the integrity of the token.

The signature allows the server to detect whether the signed token data has been modified.

[[IMAGE_NEEDED: JWT anatomy | Diagram showing a JWT split into header, payload, and signature, with example claims such as user ID, role, issuer, and expiration | Learner should notice that Base64-style encoding makes token parts compact/readable but the signature is what protects integrity]]

### JWT is not the same as encryption

A crucial beginner distinction:

```text
encoding
≠ encryption
```

Do not put sensitive secrets into a token merely because it is encoded.

### Why tokens are useful

After login:

```text
username/password
      ↓
server verifies credentials
      ↓
server issues access token
      ↓
client sends token on later requests
```

The password does not need to be resent on every protected API call.

---

## 5. Model users and tokens in the database

The chapter extends the relational database from the previous lesson.

### User data

The user entity includes concepts such as:

- unique identifier,
- email/username,
- hashed password,
- account active state,
- role,
- created timestamp,
- updated timestamp.

### Token data

The token entity contains:

- token identifier,
- linked user ID,
- expiration,
- active/revoked state,
- IP metadata,
- timestamps.

### One-to-many relationship

One user may have several token records.

```text
User
 ├── token A
 ├── token B
 └── token C
```

This can support:

- multiple logged-in devices,
- login tracking,
- token revocation.

[[IMAGE_NEEDED: User-token entity relationship | ER diagram showing users → tokens as a one-to-many relationship, with user role/hashed password and token expiry/active state highlighted | Learner should notice that token records make revocation and session tracking possible]]

### Why use unpredictable IDs?

The source uses UUID-style identifiers for sensitive entities.

The intention is to make identifiers harder to guess than simple sequential public IDs.

### Indexes and uniqueness

Email/username should normally be uniquely constrained.

Indexes can improve common queries such as:

```text
find user by email
find tokens for user
find tokens by IP
```

---

## 6. Never store raw passwords

A raw password should not be stored directly in the database.

Why?

If the database is compromised:

```text
plaintext passwords
→ immediately usable by attacker
```

Instead, the chapter uses password hashing.

### Hashing

A cryptographic hash transforms the password into a nonreversible representation.

Conceptually:

```text
password
   ↓
hash function
   ↓
hashed password
```

The application verifies a login by hashing/checking the supplied password using the password-hash algorithm and comparing the result appropriately.

### Hashing versus encoding

```text
Base64
→ encoding
→ reversible

password hashing
→ one-way cryptographic transformation
```

These should never be confused.

---

## 7. Salt password hashes

Hashing alone is not the whole story.

If two users choose the same password, a naïve deterministic hash would produce the same result.

Attackers can also use precomputed hash databases.

A **salt** adds randomness.

Conceptually:

```text
password
   +
random salt
   ↓
password-hash algorithm
   ↓
unique stored hash representation
```

Even identical passwords can produce different stored hashes.

[[IMAGE_NEEDED: Password hashing and salting | Registration path showing password + random salt → password-hash algorithm → stored salted hash, and login path showing candidate password verified against the stored hash | Learner should notice that the plain password is never stored and that the salt makes identical passwords produce different hash records]]

### What salting does not solve

The source also warns that password hashing/salting does not eliminate every attack.

Examples include:

- password spraying,
- credential stuffing.

That is why authentication security also needs:

- rate limiting,
- MFA,
- account lockouts,
- monitoring,
- compromised-password awareness.

---

## 8. Encapsulate password operations in a service

The chapter creates a password service around a password-hashing library.

Conceptually:

```python
class PasswordService:
    async def hash_password(
        self,
        password: str,
    ) -> str:
        ...

    async def verify_password(
        self,
        password: str,
        hashed_password: str,
    ) -> bool:
        ...
```

### Why a service?

The rest of the application should not need to know:

- hashing-library details,
- algorithm configuration,
- salt handling.

Instead:

```text
AuthService
   ↓
PasswordService
```

This keeps the security-sensitive operation centralized.

### Security principle

> **Do not implement your own password cryptography from mathematical primitives. Use mature security libraries and keep the cryptographic responsibility isolated.**

---

## 9. Token lifecycle: issue, validate, revoke, expire

The token service in the chapter has several responsibilities.

### 1. Issue a token

After successful login:

```text
verified user
   ↓
create token metadata
   ↓
set expiration
   ↓
sign JWT
   ↓
return access token
```

### 2. Decode and verify

When a later request sends the token:

```text
Bearer token
   ↓
verify signature
   ↓
read claims
```

Invalid tokens are rejected.

### 3. Check active state

The source stores token state in the database so tokens can be revoked.

```text
JWT is cryptographically valid
        +
database token is_active == True
        ↓
accept
```

### 4. Expire

Access tokens should be short-lived.

The chapter's example uses a finite expiration window.

The principle is:

> The shorter a stolen token remains useful, the smaller the attack window.

### 5. Revoke

On logout or a security event:

```text
token.is_active = False
```

Future use should be denied.

### Token claims

The source includes claim concepts such as:

- `exp` — expiry,
- `iss` — issuer,
- `sub` — subject/token identifier.

[[IMAGE_NEEDED: JWT lifecycle | Flow showing login → issue signed short-lived JWT → client sends Bearer token → server verifies signature/claims and active token record → allow request; separate branches for expiry and logout/revocation | Learner should notice that token issuance is only the start of the lifecycle]]

{{exercise:M01.L08.EX02}}

---

## 10. Build a higher-level authentication service

The chapter combines:

- user service,
- password service,
- token service

inside a higher-level `AuthService`.

### Registration

```text
registration request
    ↓
validate fields
    ↓
check user does not already exist
    ↓
hash password
    ↓
store user
```

### Login

```text
username/password
    ↓
load user
    ↓
verify password
    ↓
issue token
```

### Current user

Protected requests:

```text
Authorization: Bearer <token>
        ↓
decode token
        ↓
validate token
        ↓
load user
        ↓
inject authenticated user
```

### Logout

```text
current token
    ↓
decode token
    ↓
mark token inactive
```

### Dependency injection

The chapter turns these operations into FastAPI dependencies.

That allows routes or entire routers to declare:

```text
authentication required
```

without repeating authentication logic in every controller.

---

## 11. Protect FastAPI routers

The source separates authentication routes from protected resource routes.

### Authentication router

Example conceptual routes:

```text
POST /auth/register
POST /auth/token
POST /auth/logout
POST /auth/reset-password
```

### Protected resource router

Example:

```text
/generate/text
/generate/image
/generate/audio
```

A router-level authentication dependency can protect every endpoint inside the router.

```text
resource router
   ↓
get_current_user dependency
   ↓
all routes require valid identity
```

This is cleaner than remembering to add authentication independently to every route.

{{image:jwt-auth-architecture}}

### Why routers matter

Security policy becomes visible in architecture:

```text
/auth
→ public authentication flows

/generate
→ authenticated resources
```

---

## 12. Production authentication needs more than login

A usable authentication system needs more than:

```text
register
login
```

The source identifies several additional flows.

### Email or identity verification

Helps reduce:

- spam accounts,
- automated abuse,
- fake identities.

### Password reset

The reset process should not reveal whether an account exists.

Good generic response pattern:

```text
If an account exists, reset instructions will be sent.
```

After a password reset, previously active tokens may need to be revoked.

### Forced logout

A security operation can revoke all active tokens.

Useful when:

- a token is believed stolen,
- a password was compromised,
- the user requests logout everywhere.

### Disable account

An inactive account should no longer authenticate successfully.

### Delete account

Applications may need to remove personally identifying information depending on their retention requirements.

### Rate-limit failed login attempts

Repeated failed login attempts can trigger:

- throttling,
- temporary lockout,
- monitoring.

### Refresh tokens

Pattern:

```text
short-lived access token
        +
longer-lived refresh token
```

When the access token expires:

```text
refresh token
→ request new access token
```

This reduces frequent password entry while keeping access tokens short-lived.

### MFA / 2FA

Adds another verification factor.

Examples from the source include:

- OTP,
- authentication apps,
- email/SMS verification mechanisms.

{{exercise:M01.L08.EX03}}

---

## 13. Authentication attack vectors

A security system should be designed around expected attacks.

### Credential stuffing

Attackers use username/password combinations leaked from other services.

Defense categories include:

- MFA,
- rate limits,
- monitoring,
- compromised-password controls.

### Password spraying

Attackers try a small number of common passwords against many accounts.

This can evade simple per-user brute-force limits.

### Timing attacks

Attackers analyze how long comparisons take.

The chapter introduces constant-time comparison as a mitigation in credential checks.

### Token theft

If a token is stolen, an attacker may use it until:

- it expires,
- it is revoked.

This motivates:

- short lifetimes,
- secure storage,
- revocation,
- careful browser handling.

### Security is layered

No one measure solves everything.

A realistic design combines:

```text
strong password handling
+ token controls
+ MFA
+ rate limiting
+ monitoring
+ secure transport
+ authorization
```

---

## 14. OAuth2 and identity providers

The chapter next introduces OAuth2.

OAuth2 lets an application obtain limited delegated access to resources on another service.

It is commonly used with an **identity provider (IDP)**.

### Why use an identity provider?

Instead of owning every credential flow yourself:

```text
Your app
→ relies on external provider authentication
```

The provider authenticates the user and issues tokens/claims according to the OAuth flow.

### Examples

The source mentions identity platforms such as:

- GitHub,
- Google,
- Microsoft,
- Apple,
- Meta,
- LinkedIn.

### OAuth is about delegated access

The application may request scopes such as:

```text
read user profile
read email
access calendar
```

The user consents to specific permissions.

### Scope

A **scope** describes what access the application is requesting.

Principle:

> Request only the access needed for the feature.

---

## 15. Authorization code flow

The chapter implements an authorization-code flow.

### Step 1 — user starts login

```text
User clicks "Login with GitHub"
```

### Step 2 — redirect to provider

Your application sends the browser to the provider with data such as:

- client ID,
- requested scope,
- redirect URI,
- state.

### Step 3 — provider authenticates user

The user logs in on the provider's site.

Your application does not need to receive the provider password.

### Step 4 — consent

The provider displays requested scopes.

The user decides whether to grant access.

### Step 5 — authorization code

The provider redirects back to your registered callback URI with a temporary code.

### Step 6 — code exchange

Your server sends the code to the provider's token endpoint.

The provider returns an access token.

### Step 7 — use provider resource API

Your server can use the token to fetch permitted information.

{{image:oauth-flow}}

{{exercise:M01.L08.EX04}}

---

## 16. Protect OAuth with state and redirect validation

OAuth contains redirects.

Redirect flows can be attacked if the application does not verify that callback traffic belongs to the flow it initiated.

### CSRF

Cross-site request forgery tricks an authenticated user into executing an action they did not intend.

In an OAuth flow, a forged or substituted authorization sequence can be especially dangerous.

### State parameter

The chapter uses a unique state value.

Conceptually:

```text
app starts OAuth
→ generate random state
→ save server-associated session state
→ send state to provider

provider redirects back
→ state returned

application compares:
returned state == expected state?
```

If not:

```text
reject callback
```

### Redirect URI validation

The provider should only redirect to registered/approved callback URLs.

This helps reduce open-redirect style abuse.

### Session middleware

The source demonstrates server-associated session state through middleware.

Important principle:

> Do not trust arbitrary client-provided state simply because it came back in a cookie or query parameter.

### Protect provider access tokens

The source warns against unnecessarily exposing a provider access token to browser code.

A useful architecture is:

```text
provider access token
→ kept server-side

browser
→ receives your application's own short-lived session/access credential
```

This reduces the damage if your application token is compromised.

[[IMAGE_NEEDED: OAuth state/CSRF protection | Two OAuth callback paths: legitimate flow where stored state matches returned state and proceeds, and attacker/forged flow where state mismatches and is rejected | Learner should notice that state binds the callback to the original login attempt]]

{{exercise:M01.L08.EX05}}

---

## 17. OAuth2 flow types introduced in the chapter

The source describes several OAuth2 flows.

### Authorization code flow

Designed for applications with a backend capable of handling:

- client secrets,
- code exchange,
- provider tokens.

### Authorization code + PKCE

Adds:

```text
code_verifier
+
code_challenge
```

to protect against authorization-code interception.

The source highlights it for clients where protecting a traditional client secret is difficult, such as mobile applications.

### Implicit flow

The source presents this as a flow where an access token is returned without an intermediate authorization-code exchange.

For this course, remember it mainly as one of the historical/available flow patterns discussed in the source; actual provider guidance should be checked when implementing authentication.

### Client credentials flow

Used for machine-to-machine communication.

There is no end-user login.

```text
service A credentials
→ token
→ service B resource
```

### Resource owner password credentials flow

Directly exchanges a user's credentials for a token.

The source strongly discourages it except in legacy/trusted situations.

### Device authorization flow

Useful for devices with poor input capability.

Example mental model:

```text
TV displays code
   ↓
user opens website on phone
   ↓
authenticates
   ↓
TV receives authorization
```

### Flow selection table

| Scenario | Flow introduced in source |
|---|---|
| Backend web application | Authorization code |
| Mobile/public client needing interception protection | Authorization code + PKCE |
| Service-to-service | Client credentials |
| Limited-input device | Device authorization |
| Legacy direct credential exchange | Resource owner password |
| Source-discussed browser-only simplified flow | Implicit |

---

## 18. Common OAuth integration problems

The chapter lists several recurring failures.

### Invalid redirect URI

Cause:

```text
callback URL does not match provider configuration
```

Solution:

```text
register/allowlist correct redirect URI
```

### Invalid client credentials

Cause:

- wrong client ID,
- wrong client secret.

### Expired access token

Possible solution:

- obtain a new token,
- use a refresh-token flow when supported.

### Missing scope

The application did not request the permission needed for the resource.

### Incorrect token endpoint

The code/token exchange is sent to the wrong provider URL.

### CORS issues

Depending on architecture, browser requests may be blocked by provider/browser policy.

A server-side exchange can avoid exposing sensitive OAuth operations in browser code.

### Wrong grant type

The provider expects a specific flow/grant configuration.

### Practical lesson

OAuth failures are frequently **configuration failures** rather than Python syntax bugs.

Always verify:

- provider documentation,
- callback URL,
- scopes,
- credentials,
- token endpoint,
- selected flow.

---

## 19. Authorization as actor + action + resource

Once the user is authenticated, authorization begins.

A useful abstraction from the chapter is:

```text
authorize(
    actor,
    action,
    resource
) → allow / deny
```

### Actor

Who is making the request?

Examples:

- user,
- administrator,
- service acting for user.

### Action

What is requested?

Examples:

- READ,
- CREATE,
- UPDATE,
- DELETE,
- GENERATE_IMAGE,
- USE_PREMIUM_MODEL.

### Resource

What object is being accessed?

Examples:

- conversation,
- team,
- model,
- document,
- user account.

### Authorization data

The decision may depend on:

- roles,
- permissions,
- ownership,
- team membership,
- resource visibility,
- subscription attributes,
- environment attributes.

{{image:external-authorization-service}}

### Enforcement

Allowed:

```text
continue request
```

Denied:

```text
403 Forbidden
```

The challenge is keeping this logic consistent as the system grows.

---

## 20. Role-Based Access Control (RBAC)

RBAC groups permissions under roles.

Example:

```text
USER
→ text generation
→ own conversations

ADMIN
→ all user capabilities
→ manage accounts
→ image generation
→ privileged resources
```

### Why RBAC is attractive

It is easy to understand.

Instead of assigning 30 individual permissions to every user:

```text
assign role = ADMIN
```

The role carries predefined permissions.

### FastAPI authorization guard

The source demonstrates a dependency such as:

```python
async def is_admin(
    user = Depends(get_current_user),
):
    if user.role != "ADMIN":
        raise HTTPException(
            status_code=403,
            detail="Not allowed",
        )

    return user
```

Then:

```python
@router.post(
    "/image",
    dependencies=[Depends(is_admin)],
)
async def generate_image():
    ...
```

### Restrict GenAI capabilities

This lets the application express rules such as:

```text
ADMIN
→ image model

USER
→ text model only
```

### Critical security rule

The source warns against using an LLM prompt as the authorization mechanism.

Do not rely on:

```text
system prompt:
"Do not give non-admin users premium output."
```

Why?

A model can be vulnerable to adversarial prompting.

Authorization belongs in trusted application code **before** the model or tool is allowed to perform the privileged operation.

[[IMAGE_NEEDED: RBAC for GenAI models | Diagram showing authenticated USER and ADMIN roles flowing through an authorization guard; USER can access text generation while ADMIN can access text and image/premium models | Learner should notice that model access is enforced in application logic]]

{{exercise:M01.L08.EX06}}

---

## 21. More complex RBAC and role explosion

Applications may grow beyond:

```text
USER
ADMIN
```

You may introduce:

- moderator,
- editor,
- analyst,
- organization owner.

A reusable role-check guard can accept several roles.

Conceptually:

```python
def has_role(
    user,
    allowed_roles: list[str],
):
    if user.role not in allowed_roles:
        raise HTTPException(403)

    return user
```

### Role explosion

RBAC becomes difficult when many tiny roles are created to represent combinations of:

- resource,
- team,
- subscription,
- privacy,
- location,
- ownership.

For example:

```text
TEAM_A_EDITOR
TEAM_A_VIEWER
TEAM_B_EDITOR
TEAM_B_VIEWER
PREMIUM_TEAM_A_EDITOR
...
```

This is one reason the chapter introduces ReBAC and ABAC.

---

## 22. Relationship-Based Access Control (ReBAC)

ReBAC makes relationships first-class authorization data.

Examples:

```text
user is member of team
user owns conversation
conversation belongs to folder
folder belongs to organization
```

Permission can be inherited through relationships.

### Example

```text
Team Alpha
  ├── Member: User A
  └── Private Conversations
          ├── Conversation 1
          └── Conversation 2
```

A rule may say:

```text
team member
→ can read team conversations
```

Now you do not need to share every conversation individually.

### Why model relationships as graphs?

ReBAC often looks like:

```text
user ─member-of→ team
team ─owns→ folder
folder ─contains→ conversation
```

Authorization can follow these relationships.

[[IMAGE_NEEDED: ReBAC hierarchy | Graph showing a user connected as member of a team, team linked to a private folder, and folder containing conversations/threads; permission inheritance flows through relationships | Learner should notice that access can come from relationships rather than one global role]]

### Benefits

- natural for teams/groups,
- hierarchical permissions,
- reduces some RBAC role explosion,
- supports resource-level relationships.

### Costs

- more complex,
- more authorization data,
- harder auditing,
- potentially expensive permission evaluation.

{{exercise:M01.L08.EX07}}

---

## 23. Attribute-Based Access Control (ABAC)

ABAC bases decisions on attributes.

Possible attributes include:

### User attributes

```text
plan = PRO
country = ...
department = ...
```

### Resource attributes

```text
is_public = True
contains_pii = True
sensitivity = HIGH
```

### Environment attributes

```text
time
network
request context
```

### GenAI examples from the chapter

```text
user.plan == PAID
→ allow premium model
```

or:

```text
upload.has_pii == True
→ deny upload to certain RAG workflow
```

[[IMAGE_NEEDED: ABAC GenAI policy | Policy diagram showing attributes such as `user.plan=paid`, `resource.is_public`, and `upload.has_pii` being evaluated to allow or deny premium-model/document actions | Learner should notice that policies can be dynamic and context-sensitive]]

### Strength

ABAC can create highly granular rules.

### Cost

When many attributes participate, determining access can become difficult to reason about and audit.

---

## 24. Hybrid authorization

Real systems often combine authorization models.

Example:

```text
RBAC:
ADMIN can access everything

ReBAC:
team member can access team resources

ABAC:
public resource can be read by anyone
```

The chapter demonstrates a combined decision:

```python
if user.role == "ADMIN":
    allow

if user.id in team.members:
    allow

if resource.is_public:
    allow

deny
```

### Why combine them?

Each model solves a different shape of policy.

```text
RBAC
→ simple organization-wide roles

ReBAC
→ ownership and hierarchy

ABAC
→ dynamic contextual attributes
```

### Complexity warning

As rules grow:

```text
exceptions
+ overrides
+ inheritance
+ attributes
+ teams
+ subscriptions
```

authorization code can become difficult to maintain.

{{image:authorization-models}}

---

## 25. Separate authorization into its own service

For volatile or complex policies, the chapter introduces a dedicated authorization service.

Architecture:

```text
GenAI API
   ↓
authorization request:
user + resource + action
   ↓
Authorization Service
   ↓
policy evaluation
   ↓
allowed = true/false
   ↓
GenAI API enforces decision
```

### Why separate it?

Benefits can include:

- central policies,
- less duplicated logic,
- easier updates,
- consistent decisions across services,
- clearer audit boundaries.

### Example authorization response

```json
{
  "allowed": true
}
```

The GenAI service does not need to know every policy rule.

It asks:

```text
May this actor perform this action on this resource?
```

### Enforcement remains local

Even if policy evaluation is external, the GenAI API must still enforce the decision.

```text
allowed
→ continue

denied
→ return 403
```

### Providers

The source mentions that teams may use dedicated authorization products instead of building a full policy engine from scratch.

The larger lesson is architectural:

> **Centralize authorization decisions when policy complexity becomes a separate system problem.**

{{exercise:M01.L08.EX08}}

---

## 26. Secure the GenAI layer itself

Authentication and authorization are not separate from AI product design.

They control:

- which model can be called,
- which documents can be retrieved,
- which conversation can be read,
- which tools can be executed,
- which output capabilities are available.

### Model entitlement

Example:

```text
FREE user
→ small text model

PAID user
→ premium text model

ADMIN
→ experimental image model
```

### Data authorization

RAG retrieval should not retrieve every document merely because semantic similarity is high.

The request should also satisfy permissions:

```text
semantic match
        +
user authorized for document
        ↓
eligible context
```

### Tool authorization

If the model proposes:

```text
delete conversation
send email
modify billing
```

the application must authorize the operation before execution.

### Prompt injection boundary

The source's strongest GenAI-specific warning is:

> **Never treat model instructions as a trusted authorization boundary.**

An attacker may manipulate prompts.

So authorization should be enforced:

```text
outside the model
inside trusted application/service logic
```

### Complete secure flow

```text
Request
   ↓
Authentication
   ↓
Current user
   ↓
Authorization decision
   ↓
Validate resource/model/tool access
   ↓
GenAI model or tool
   ↓
Response
```

---

## Important misconceptions

### Misconception 1

> Authentication and authorization are interchangeable terms.

### Why this is wrong

Authentication establishes identity. Authorization determines what that identity may do.

### Misconception 2

> Base64-encoding a password makes it encrypted.

### Why this is wrong

Encoding is reversible and does not provide encryption.

### Misconception 3

> A valid JWT means a user should always be granted access.

### Why this is wrong

Authentication can establish identity, but authorization still has to approve the requested action/resource.

### Misconception 4

> JWT payload data should be treated as secret because the token is encoded.

### Why this is wrong

Encoding is not confidentiality. Sensitive data should not be placed in token claims simply because the token is compact.

### Misconception 5

> Password hashing and salting prevent every password attack.

### Why this is wrong

They help protect stored credentials, but password spraying, credential stuffing, phishing, and other attacks still require additional defenses.

### Misconception 6

> A long-lived token is more convenient, so it is automatically better.

### Why this is wrong

Longer lifetime increases the window in which a stolen token can be abused.

### Misconception 7

> Logout is just a frontend action.

### Why this is wrong

If the server tracks revocable tokens, logout should invalidate the current credential so future requests are rejected.

### Misconception 8

> OAuth means your application gets the user's provider password.

### Why this is wrong

The provider authenticates the user. Your application receives authorization artifacts such as codes/tokens according to the flow.

### Misconception 9

> OAuth state is decorative metadata.

### Why this is wrong

It helps bind the callback to the login flow initiated by the application and protects against forged authorization sequences.

### Misconception 10

> Authorization can safely be delegated to the LLM through a system prompt.

### Why this is wrong

Model instructions can be attacked or bypassed. Permissions must be enforced by trusted application logic.

### Misconception 11

> RBAC can express every permission system cleanly.

### Why this is wrong

Resource relationships and dynamic attributes can cause role explosion or require finer-grained ReBAC/ABAC rules.

### Misconception 12

> ReBAC and ABAC are always better than RBAC.

### Why this is wrong

They provide more flexibility but increase policy complexity, data requirements, and auditing cost.

### Misconception 13

> If authorization logic is moved to another service, the GenAI API no longer needs to enforce access.

### Why this is wrong

The policy service produces a decision; the resource service must still enforce it.

---

## Key terminology

| Term | Meaning |
|---|---|
| Authentication | Verifying an actor's identity |
| Authorization | Verifying that an actor may perform an action on a resource |
| Authenticator | Credential/evidence used to prove identity |
| Basic authentication | HTTP authentication using reusable username/password credentials |
| Bearer token | Credential where possession of the token is sufficient to present it for authentication |
| JWT | JSON Web Token; compact signed claims format |
| Claim | Piece of data represented inside a token payload |
| JWT header | Metadata describing token type/signing configuration |
| JWT payload | Token claims |
| JWT signature | Integrity-protection result over token data |
| Hashing | One-way cryptographic transformation |
| Salt | Random value incorporated into password hashing |
| Credential stuffing | Trying credentials leaked from other systems |
| Password spraying | Trying common passwords across many accounts |
| Timing attack | Inferring secret information from operation timing differences |
| Access token | Credential used to access protected resources |
| Refresh token | Longer-lived credential used to obtain new access tokens |
| Revocation | Making a credential invalid before natural expiry |
| MFA | Authentication requiring more than one factor |
| OAuth2 | Framework for delegated authorization/access |
| Identity provider | External system that authenticates users and issues identity/access artifacts |
| Scope | Permission requested from an OAuth provider |
| Authorization code | Temporary code exchanged for an access token |
| Redirect URI | Registered callback URL used by an OAuth provider |
| State | OAuth value used to correlate/protect the authorization flow |
| CSRF | Attack that tricks an authenticated user into an unintended request/action |
| Open redirect | Unsafe redirect behavior that can send users or authorization artifacts to attacker-controlled destinations |
| PKCE | Proof Key for Code Exchange; extra verification for authorization-code flows |
| RBAC | Role-Based Access Control |
| ReBAC | Relationship-Based Access Control |
| ABAC | Attribute-Based Access Control |
| Role | Named grouping of permissions |
| Permission | Allowed action on a resource |
| Guard | Dependency/policy check that prevents unauthorized access |
| Actor | Identity requesting an operation |
| Action | Operation the actor wants to perform |
| Resource | Object/capability affected by the action |
| Authorization service | Separate system responsible for evaluating access policies |

---

## Self-check

Before continuing, make sure you can answer:

1. What is authentication?
2. What is authorization?
3. How does the airport passport/visa analogy distinguish them?
4. What is the practical difference between 401 and 403?
5. What four authentication mechanisms are introduced in the chapter?
6. Why does the source mainly position Basic authentication for prototypes/internal use?
7. Why is Base64 not encryption?
8. Why use constant-time secret comparison?
9. Why should authentication errors avoid leaking whether a username exists?
10. What are the three main JWT components?
11. What kind of data belongs in a JWT payload?
12. Why does a JWT signature matter?
13. Why should token encoding not be treated as confidentiality?
14. Why store token records in a database in the chapter's design?
15. What is the relationship between users and token records?
16. Why should raw passwords never be stored?
17. What is the difference between hashing and encoding?
18. What does a salt add to password hashing?
19. Which password attacks are not solved by hashing/salting alone?
20. What responsibilities belong to a password service?
21. What are the stages of an access-token lifecycle?
22. Why should access tokens expire?
23. What does token revocation achieve?
24. What does a high-level authentication service coordinate?
25. Why protect routers through reusable dependencies?
26. Which flows beyond login/register are needed for a production authentication system?
27. Why might password reset revoke active tokens?
28. What is the purpose of refresh tokens?
29. Why can MFA reduce the impact of a stolen password?
30. What is credential stuffing?
31. What is password spraying?
32. Why can rate limiting and account lockout help?
33. What is an identity provider?
34. What is a scope?
35. What are the major steps of the OAuth authorization-code flow?
36. Why is the redirect URI important?
37. What does the authorization code represent?
38. Why is the state parameter important?
39. What is CSRF?
40. Why should provider access tokens be carefully protected from browser exposure?
41. What problem does PKCE address?
42. Which OAuth flow is used for service-to-service authentication in the source?
43. What is device authorization useful for?
44. What kinds of configuration mistakes commonly break OAuth integrations?
45. What are the three inputs in the actor-action-resource authorization model?
46. What is RBAC?
47. How can RBAC restrict access to a premium GenAI model?
48. Why should application code enforce that restriction instead of the model prompt?
49. What is role explosion?
50. What is ReBAC?
51. How can team membership grant access to team conversations?
52. What is ABAC?
53. Give one GenAI-specific ABAC policy.
54. Why can ABAC become difficult to audit?
55. Why do large systems combine RBAC, ReBAC, and ABAC?
56. When does a separate authorization service become useful?
57. What does an authorization service return?
58. Who must enforce the allow/deny decision?
59. How should permissions interact with RAG retrieval?
60. How should permissions interact with model tool calls?

---

## Retain this idea

**Secure GenAI services in layers: authenticate the actor, protect credentials and tokens throughout their lifecycle, use trusted OAuth flows when delegating identity, and then authorize every sensitive action against roles, relationships, attributes, and resource ownership. Never let the model itself be the security boundary—trusted application logic must decide which data, models, tools, and actions each user is allowed to access.**
""",

        "estimated_minutes": 270,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {"id": "authentication-vs-authorization", "title": "Authentication is not authorization", "order": 1},
            {"id": "authentication-methods", "title": "Authentication methods", "order": 2},
            {"id": "basic-auth", "title": "Basic authentication in FastAPI", "order": 3},
            {"id": "jwt-basics", "title": "JSON Web Tokens (JWT)", "order": 4},
            {"id": "auth-database-models", "title": "Model users and tokens in the database", "order": 5},
            {"id": "password-hashing", "title": "Never store raw passwords", "order": 6},
            {"id": "salting", "title": "Salt password hashes", "order": 7},
            {"id": "password-service", "title": "Encapsulate password operations in a service", "order": 8},
            {"id": "token-lifecycle", "title": "Token lifecycle: issue, validate, revoke, expire", "order": 9},
            {"id": "auth-service", "title": "Build a higher-level authentication service", "order": 10},
            {"id": "auth-router", "title": "Protect FastAPI routers", "order": 11},
            {"id": "production-auth-flows", "title": "Production authentication needs more than login", "order": 12},
            {"id": "auth-attacks", "title": "Authentication attack vectors", "order": 13},
            {"id": "oauth-introduction", "title": "OAuth2 and identity providers", "order": 14},
            {"id": "oauth-auth-code", "title": "Authorization code flow", "order": 15},
            {"id": "oauth-state-csrf", "title": "Protect OAuth with state and redirect validation", "order": 16},
            {"id": "oauth-flow-types", "title": "OAuth2 flow types introduced in the chapter", "order": 17},
            {"id": "oauth-troubleshooting", "title": "Common OAuth integration problems", "order": 18},
            {"id": "authorization-model", "title": "Authorization as actor + action + resource", "order": 19},
            {"id": "rbac", "title": "Role-Based Access Control (RBAC)", "order": 20},
            {"id": "rbac-complexity", "title": "More complex RBAC and role explosion", "order": 21},
            {"id": "rebac", "title": "Relationship-Based Access Control (ReBAC)", "order": 22},
            {"id": "abac", "title": "Attribute-Based Access Control (ABAC)", "order": 23},
            {"id": "hybrid-authorization", "title": "Hybrid authorization", "order": 24},
            {"id": "external-authorization-service", "title": "Separate authorization into its own service", "order": 25},
            {"id": "secure-genai", "title": "Secure the GenAI layer itself", "order": 26},
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M01.L08.EX01",
            "title": "Authentication or Authorization?",
            "lesson_code": "M01.L08",
            "section_id": "authentication-vs-authorization",
            "placement": "after_section",
            "description": "Classify identity checks separately from permission decisions.",
            "instructions": (
                "Classify each operation as `authentication`, `authorization`, or `both`:\n\n"
                "1. Verify a password during login.\n"
                "2. Check whether a user may delete conversation 42.\n"
                "3. Validate a bearer token and then check whether the authenticated user owns a document.\n"
                "4. Decide whether an ADMIN may access an experimental image model.\n"
                "5. Verify the identity supplied by an OAuth provider.\n\n"
                "For each answer, explain what identity or permission question is being answered."
            ),
            "expected_output": "Five classifications with short explanations.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["authentication", "authorization", "security-reasoning"],
        },
        {
            "id": "M01.L08.EX02",
            "title": "Trace the JWT Lifecycle",
            "lesson_code": "M01.L08",
            "section_id": "token-lifecycle",
            "placement": "after_section",
            "description": "Practice the complete lifecycle of a revocable short-lived access token.",
            "instructions": (
                "Draw a flow covering:\n"
                "1. login credentials,\n"
                "2. password verification,\n"
                "3. token-record creation,\n"
                "4. JWT signing,\n"
                "5. Bearer token on a protected request,\n"
                "6. JWT decoding/signature verification,\n"
                "7. active-token check,\n"
                "8. expiration,\n"
                "9. logout/revocation.\n\n"
                "Then explain why a token can be structurally valid yet still be rejected."
            ),
            "expected_output": "A token-lifecycle diagram plus an explanation of revocation/expiry.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["jwt", "token-lifecycle", "revocation"],
        },
        {
            "id": "M01.L08.EX03",
            "title": "Design Production Authentication Flows",
            "lesson_code": "M01.L08",
            "section_id": "production-auth-flows",
            "placement": "after_section",
            "description": "Extend a minimal login system into a safer user-account lifecycle.",
            "instructions": (
                "For a public GenAI SaaS, design flows for:\n"
                "1. registration,\n"
                "2. email verification,\n"
                "3. login,\n"
                "4. logout,\n"
                "5. password reset,\n"
                "6. refresh token,\n"
                "7. logout all devices,\n"
                "8. repeated failed-login protection,\n"
                "9. optional MFA.\n\n"
                "For each flow, identify what database/token state changes."
            ),
            "expected_output": "A nine-flow security lifecycle table.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["auth-flows", "token-management", "account-security"],
        },
        {
            "id": "M01.L08.EX04",
            "title": "Trace an OAuth Authorization-Code Login",
            "lesson_code": "M01.L08",
            "section_id": "oauth-auth-code",
            "placement": "after_section",
            "description": "Follow the browser, backend, identity-provider, and token-exchange responsibilities.",
            "instructions": (
                "Draw a sequence diagram with these actors:\n"
                "- user/browser,\n"
                "- FastAPI backend,\n"
                "- identity-provider authorization server,\n"
                "- provider resource API.\n\n"
                "Include:\n"
                "1. login click,\n"
                "2. redirect with client ID/scope/state/redirect URI,\n"
                "3. provider login + consent,\n"
                "4. callback with authorization code,\n"
                "5. code exchange,\n"
                "6. access token,\n"
                "7. user-info API request.\n\n"
                "Mark where the user's provider password is handled."
            ),
            "expected_output": "An OAuth sequence diagram and password-boundary explanation.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["oauth2", "authorization-code-flow", "identity-provider"],
        },
        {
            "id": "M01.L08.EX05",
            "title": "Stop a Forged OAuth Callback",
            "lesson_code": "M01.L08",
            "section_id": "oauth-state-csrf",
            "placement": "after_section",
            "description": "Apply state validation and redirect restrictions to an OAuth login.",
            "instructions": (
                ('1. Assume your app generates state `ABC123` before redirecting to the provider.\n'
                 '2. Evaluate these callbacks:\n'
                 '   - A. `state=ABC123` from the registered callback path.\n'
                 '   - B. `state=WRONG`.\n'
                 '   - C. Correct state, but the authorization flow uses an unregistered attacker-controlled redirect URI.\n'
                 '3. For each, state whether to continue or reject and why.\n'
                 '4. Then explain why provider access tokens should not be exposed unnecessarily to browser code.')
            ),
            "expected_output": "Three callback decisions plus a token-exposure explanation.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["csrf", "oauth-state", "redirect-validation"],
        },
        {
            "id": "M01.L08.EX06",
            "title": "Protect GenAI Models with RBAC",
            "lesson_code": "M01.L08",
            "section_id": "rbac",
            "placement": "after_section",
            "description": "Use application-level authorization guards to restrict model capabilities.",
            "instructions": (
                "Define three roles: `USER`, `MODERATOR`, and `ADMIN`.\n\n"
                "Create a permission table for:\n"
                "- text generation,\n"
                "- premium text model,\n"
                "- image generation,\n"
                "- viewing another user's conversation,\n"
                "- user-account administration.\n\n"
                "Then write pseudocode for a reusable FastAPI dependency that accepts a set "
                "of allowed roles and returns 403 when the current user's role is not included.\n"
                "Explain why the same rule must not be implemented only as an LLM system prompt."
            ),
            "expected_output": "Role/permission matrix, reusable guard pseudocode, and prompt-injection explanation.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["rbac", "authorization-guards", "genai-security"],
        },
        {
            "id": "M01.L08.EX07",
            "title": "Model Team Access with ReBAC and ABAC",
            "lesson_code": "M01.L08",
            "section_id": "rebac",
            "placement": "after_section",
            "description": "Compare relationship-based and attribute-based decisions in one collaboration scenario.",
            "instructions": (
                "Scenario:\n"
                "- A private conversation belongs to Team Alpha.\n"
                "- Sara is a Team Alpha member.\n"
                "- Omar is not a member.\n"
                "- The conversation has `is_public=False`.\n"
                "- Omar has `plan=PRO`.\n\n"
                "1. Write a ReBAC rule for team membership.\n"
                "2. Write an ABAC rule using `is_public`.\n"
                "3. Decide whether Sara can read the conversation.\n"
                "4. Decide whether Omar can read it if PRO subscription alone does not grant private-resource access.\n"
                "5. Explain what would change if `is_public=True`."
            ),
            "expected_output": "ReBAC/ABAC rules and access decisions for Sara and Omar.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["rebac", "abac", "resource-authorization"],
        },
        {
            "id": "M01.L08.EX08",
            "title": "Design an Authorization Service",
            "lesson_code": "M01.L08",
            "section_id": "external-authorization-service",
            "placement": "after_section",
            "description": "Separate volatile policy evaluation from the GenAI application's business logic.",
            "instructions": (
                "Design a minimal authorization-service contract.\n\n"
                "Request fields:\n"
                "- user_id,\n"
                "- action,\n"
                "- resource_id.\n\n"
                "Response:\n"
                "- allowed: bool.\n\n"
                "Then describe how the GenAI service should:\n"
                "1. call the authorization service,\n"
                "2. handle `allowed=True`,\n"
                "3. handle `allowed=False`,\n"
                "4. handle authorization-service failure,\n"
                "5. avoid calling a privileged model/tool before the authorization decision is complete."
            ),
            "expected_output": "An authorization API contract and enforcement flow.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["authorization-service", "policy-enforcement", "service-architecture"],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M01.L08.QZ01",

        "title": "Authentication and Authorization — Knowledge Check",

        "lesson_code": "M01.L08",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M01.L08.Q01",
                "section_id": "authentication-vs-authorization",
                "question": "Which question is primarily answered by authentication?",
                "options": [
                    "Who is making this request?",
                    "May this user delete this conversation?",
                    "Which model may this subscription tier use?",
                    "Is this resource public?",
                ],
                "correct": 0,
                "explanation": "Authentication verifies identity; authorization decides permissions.",
            },
            {
                "id": "M01.L08.Q02",
                "section_id": "basic-auth",
                "question": "Why is Base64-encoding credentials not equivalent to encrypting them?",
                "options": [
                    "Base64 is reversible encoding rather than confidentiality protection",
                    "Base64 is a password-hashing algorithm",
                    "Base64 automatically signs requests",
                    "Base64 prevents interception without TLS",
                ],
                "correct": 0,
                "explanation": "Base64 changes representation; it does not provide secrecy.",
            },
            {
                "id": "M01.L08.Q03",
                "section_id": "jwt-basics",
                "question": "Which three parts make up a JWT?",
                "options": [
                    "Header, payload, signature",
                    "Username, password, cookie",
                    "Scope, redirect, database",
                    "Actor, action, resource",
                ],
                "correct": 0,
                "explanation": "JWTs are represented as header, payload, and signature sections.",
            },
            {
                "id": "M01.L08.Q04",
                "section_id": "salting",
                "question": "What is the main purpose of adding a random salt to password hashing?",
                "options": [
                    "To make identical passwords produce different stored hash representations",
                    "To make passwords readable by administrators",
                    "To eliminate the need for MFA",
                    "To turn hashing into encryption",
                ],
                "correct": 0,
                "explanation": "Salting adds randomness and reduces the usefulness of precomputed hash tables.",
            },
            {
                "id": "M01.L08.Q05",
                "section_id": "token-lifecycle",
                "question": "Why should access tokens generally have an expiration time?",
                "options": [
                    "To limit how long a stolen token remains usable",
                    "To make the JWT payload secret",
                    "To remove the need for authentication",
                    "To guarantee the user is authorized for every resource",
                ],
                "correct": 0,
                "explanation": "Short-lived access tokens reduce the exposure window after theft.",
            },
            {
                "id": "M01.L08.Q06",
                "section_id": "production-auth-flows",
                "question": "What is the purpose of a refresh token?",
                "options": [
                    "Obtain a new short-lived access token without requiring the full login flow each time",
                    "Replace password hashing",
                    "Store authorization roles in plaintext",
                    "Disable all tokens automatically",
                ],
                "correct": 0,
                "explanation": "Refresh tokens support renewed access tokens while keeping access tokens short-lived.",
            },
            {
                "id": "M01.L08.Q07",
                "section_id": "auth-attacks",
                "question": "What is credential stuffing?",
                "options": [
                    "Trying credentials stolen from other services against this service",
                    "Adding too many JWT claims",
                    "Using several authorization roles",
                    "Generating multiple salts",
                ],
                "correct": 0,
                "explanation": "Credential stuffing reuses compromised username/password pairs across services.",
            },
            {
                "id": "M01.L08.Q08",
                "section_id": "oauth-auth-code",
                "question": "What does the authorization code do in the OAuth flow?",
                "options": [
                    "It is a temporary artifact the backend exchanges for an access token",
                    "It is the user's provider password",
                    "It is the final API response body",
                    "It replaces the redirect URI",
                ],
                "correct": 0,
                "explanation": "The backend exchanges the temporary authorization code at the provider's token endpoint.",
            },
            {
                "id": "M01.L08.Q09",
                "section_id": "oauth-state-csrf",
                "question": "What is the main purpose of the OAuth state value?",
                "options": [
                    "Bind the callback to the authorization flow initiated by the application and help prevent CSRF-style forgery",
                    "Store the user's password",
                    "Increase model context length",
                    "Choose the database engine",
                ],
                "correct": 0,
                "explanation": "State is checked on callback to ensure the returned flow corresponds to the one the application initiated.",
            },
            {
                "id": "M01.L08.Q10",
                "section_id": "authorization-model",
                "question": "Which three inputs form the chapter's basic authorization decision model?",
                "options": [
                    "Actor, action, resource",
                    "Header, payload, signature",
                    "User, password, salt",
                    "Prompt, model, embedding",
                ],
                "correct": 0,
                "explanation": "Authorization evaluates who is acting, what they want to do, and which resource is affected.",
            },
            {
                "id": "M01.L08.Q11",
                "section_id": "rbac",
                "question": "What does RBAC primarily base access decisions on?",
                "options": [
                    "Roles assigned to users",
                    "Only geographic location",
                    "Only resource ownership graphs",
                    "Randomly generated model output",
                ],
                "correct": 0,
                "explanation": "RBAC groups permissions under roles and assigns roles to users.",
            },
            {
                "id": "M01.L08.Q12",
                "section_id": "rebac",
                "question": "What does ReBAC make central to authorization decisions?",
                "options": [
                    "Relationships between identities and resources",
                    "Only JWT expiration time",
                    "Only password strength",
                    "Only HTTP methods",
                ],
                "correct": 0,
                "explanation": "ReBAC uses relationships such as membership, ownership, grouping, and hierarchy.",
            },
            {
                "id": "M01.L08.Q13",
                "section_id": "abac",
                "question": "Which is an ABAC-style rule?",
                "options": [
                    "Allow premium model if user.plan == 'PAID'",
                    "Allow access because the user has role ADMIN only",
                    "Allow access because the user belongs to Team Alpha only",
                    "Allow access because the JWT contains three sections",
                ],
                "correct": 0,
                "explanation": "ABAC evaluates attributes of users, resources, or environment.",
            },
            {
                "id": "M01.L08.Q14",
                "section_id": "secure-genai",
                "question": "Where should privileged GenAI actions be authorized?",
                "options": [
                    "In trusted application/policy logic before the model or tool executes the action",
                    "Only inside a system prompt",
                    "Only in the browser UI",
                    "After the privileged operation is completed",
                ],
                "correct": 0,
                "explanation": "Authorization must be enforced outside the probabilistic model in trusted code.",
            },
            {
                "id": "M01.L08.Q15",
                "section_id": "secure-genai",
                "type": "open",
                "question": (
                    "Design the security flow for a GenAI SaaS where all authenticated users "
                    "can use a basic text model, paid users can use a premium model, team members "
                    "can access team conversations, and only administrators can manage accounts. "
                    "Explain the authentication mechanism, token lifecycle, and which decisions "
                    "belong to RBAC, ReBAC, and ABAC."
                ),
            },
        ],

        "passing_score": 70,
    },
}
