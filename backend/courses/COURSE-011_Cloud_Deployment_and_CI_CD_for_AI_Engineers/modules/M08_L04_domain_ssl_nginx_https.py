"""M08.L04 — Domain, SSL Certificates, Nginx, and HTTPS Deployment.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
BOOK-XXX, Chapter 4, page numbers not provided in the supplied chapter export.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel

LESSON_CODE = "M08.L04"
MODULE_ORDER = 8
MODULE_TITLE = "Secure AWS Deployment Foundations"
MODULE_DESCRIPTION = "Add a custom domain and TLS certificate, then terminate HTTPS with Nginx in front of Streamlit."
SOURCE_CHAPTER = 4
SOURCE_PAGES = "Page numbers not provided in supplied chapter export"

TOPIC = {
    "title": "Domain, SSL Certificates, Nginx, and HTTPS Deployment",
    "slug": "domain-ssl-nginx-https-m08-l04",
    "description": (
        "Follow the source's Namecheap-based domain and certificate workflow, generate a CSR, validate domain control, "
        "prepare certificate files, map DNS to the load-balancer layer, and use Nginx plus Docker Compose to proxy "
        "HTTPS traffic to the Streamlit application."
    ),
    "order": 4,
    "difficulty": DifficultyLevel.beginner,
    "estimated_hours": 3.25,
    "skill_tags": ["dns", "ssl", "tls", "csr", "openssl", "nginx", "docker-compose", "https", "namecheap", "module-08"],
    "prerequisite_ids": ["M08.L03"],

    "lesson": {
        "title": "Domain, SSL Certificates, Nginx, and HTTPS Deployment",
        "content": r"""
# Domain, SSL Certificates, Nginx, and HTTPS Deployment

> **Course:** Secure AWS Deployment Foundations  
> **Lesson:** M08.L04  
> **Source alignment:** BOOK-XXX, Chapter 4. The supplied chapter uses Namecheap, a purchased PositiveSSL certificate, manual CSR/DNS validation, an A record, Docker Compose, and Nginx. These are source-specific workflow choices, not claims about the only way to deploy HTTPS.

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Explain why a domain name improves usability over raw IP addressing.
- Explain the purpose of TLS/SSL in the source architecture.
- Generate a certificate signing request (CSR) and private key using OpenSSL.
- Explain which CSR fields identify the certificate subject.
- Explain why the private key must remain protected.
- Describe the source's certificate activation and CNAME-based domain-control validation.
- Explain the purpose of DNS A and CNAME records in the source workflow.
- Explain how the source combines the server certificate and CA bundle.
- Read the source's Docker Compose relationship between Streamlit and Nginx.
- Explain Nginx's HTTP-to-HTTPS redirect.
- Explain TLS certificate/key directives.
- Explain Nginx reverse proxying from HTTPS traffic to `streamlit_calc:8501`.
- Trace the final request path from domain name to Streamlit.

---

## 1. Move from infrastructure addresses to a professional domain and HTTPS

So far, users reached the application through technical endpoints such as:

```text
Elastic IP:8501
```

or:

```text
load-balancer DNS:8501
```

Chapter 4 adds two user-facing improvements:

```text
custom domain
+
TLS/SSL encryption
```

The result becomes conceptually:

```text
https://your-domain:8501
```

### Domain name

A domain gives users a stable human-readable name.

Instead of remembering an AWS-generated hostname or IP address, they can use a branded/application-specific address.

### TLS/SSL

The chapter uses an SSL certificate to enable encrypted HTTPS communication.

The key idea is:

```text
HTTP
→ plaintext application protocol

HTTPS
→ HTTP protected by TLS encryption/authentication
```

The source implements TLS through Nginx.

[[IMAGE_NEEDED: Final domain and HTTPS architecture | A high-level flow showing Browser → custom domain DNS → AWS load-balancer layer → EC2 → Nginx TLS termination → Streamlit container | Learner should notice that the custom domain identifies the service while Nginx presents the certificate and proxies to the application]]

---

## 2. The source's domain and certificate provider workflow

The supplied chapter uses:

```text
Namecheap
```

for:

- domain registration,
- SSL certificate purchase,
- DNS management.

It chooses a basic certificate product named:

```text
PositiveSSL
```

This is the source's vendor-specific workflow.

Prices and vendor UI shown in the chapter are not treated as timeless technical facts in this lesson.

The lasting technical concepts are:

```text
own/control a domain
        +
obtain a certificate for that domain
        +
prove domain control
        +
configure DNS
        +
install certificate/private key on the TLS endpoint
```

---

## 3. Generate a CSR and private key with OpenSSL

The source generates a certificate signing request on the EC2 host.

Its command is:

```bash
openssl req \
  -new \
  -newkey rsa:2048 \
  -nodes \
  -keyout private.key \
  -out your_domain_csr.crt
```

### Two outputs

This creates:

```text
private.key
```

and:

```text
your_domain_csr.crt
```

These have different purposes.

### Private key

```text
private.key
```

must remain private.

It is later configured in Nginx as the TLS private key.

### CSR

The CSR contains the certificate request information that is sent to the certificate provider.

### Fields requested by the source

The OpenSSL prompts include:

- country,
- state/province,
- locality/city,
- organization,
- common name,
- email,
- optional challenge/company fields.

The most important domain-oriented field in the source is the **common name**, which uses the purchased domain.

### Why private-key handling matters

The certificate can be distributed publicly.

The private key cannot.

Conceptually:

```text
certificate
→ public identity material

private key
→ proves control of that certificate identity
```

Do not commit the private key to source control.

[[IMAGE_NEEDED: CSR and private-key relationship | A diagram showing OpenSSL generating `private.key` (keep secret) and `your_domain_csr.crt` (send to certificate provider), then the provider issuing a certificate that will later be paired with the private key in Nginx | Learner should notice that the private key never needs to be sent to the certificate provider]]

{{exercise:M08.L04.EX01}}

---

## 4. Activate the certificate and prove domain control

The source activates the purchased certificate by pasting the CSR into the provider's certificate workflow.

Then it selects:

```text
CNAME record
```

for domain-control validation.

### Why validation exists

A certificate authority needs evidence that the requester controls the domain.

The source's provider generates:

```text
Host
Target
```

values for a CNAME record.

Then the learner adds that record to the domain's DNS settings.

Conceptually:

```text
certificate provider
        ↓ gives validation token
DNS CNAME record
        ↓ publicly proves control
certificate provider checks DNS
        ↓
certificate becomes active
```

### TTL

The source lowers the DNS TTL during setup to speed up the feedback loop.

That is a practical deployment convenience in the chapter.

### Host and target

The source distinguishes:

```text
Host
→ validation record name

Target
→ provider-specified destination/value
```

Both must be copied correctly.

---

## 5. Route the domain toward the AWS entry point

After certificate validation, the source configures an A record.

Its conceptual configuration is:

```text
Type: A
Host: @
Value: <load-balancer public IP>
```

This is the exact routing model described by the supplied chapter.

### What `@` means in this context

In the source's DNS UI, `@` represents the root/apex domain.

So:

```text
@
```

means the domain itself rather than a subdomain such as:

```text
www
```

### DNS resolution concept

```text
user enters domain
        ↓
DNS lookup
        ↓
A record
        ↓
AWS load-balancer address
```

This replaces the need for users to type a raw address manually.

### Source-specific note

The chapter explicitly instructs mapping the domain to a load-balancer public IP as shown in its AWS/Namecheap setup.

This lesson preserves that workflow instead of substituting a different DNS architecture.

---

## 6. Prepare the certificate files for Nginx

After certificate activation, the source obtains certificate files from the provider.

It then creates a combined certificate file.

Conceptually:

```text
your_domain.crt
      +
your_domain.ca-bundle
      ↓
your_domain_combined.crt
```

The source stores the private key separately under a private folder.

Its intended structure is conceptually:

```text
config/
├── your_domain_combined.crt
└── private/
    └── private.key
```

### Why combine certificate and CA bundle?

The server needs to present enough certificate-chain information for clients to validate the certificate path.

The source accomplishes this by concatenating the issued certificate and CA bundle into one file for Nginx.

---

## 7. Put Nginx in front of Streamlit with Docker Compose

The source's Compose file contains two main services:

```text
streamlit_calc
nginx
```

### Streamlit service

The application container exposes port:

```text
8501
```

inside the Compose network.

### Nginx service

Nginx mounts:

- `nginx.conf`,
- combined certificate,
- private key,
- proxy parameters.

It depends on the Streamlit service.

The host publishes:

```text
8501:8501
```

for the Nginx service in the source's test deployment.

### Conceptual architecture

```text
Browser HTTPS
    ↓
Nginx container
    ↓ reverse proxy
Streamlit container
```

Nginx becomes the TLS-facing proxy.

[[IMAGE_NEEDED: Nginx reverse proxy in Docker Compose | A diagram showing browser HTTPS traffic reaching an Nginx container with mounted certificate/private key, then Nginx forwarding internally to `streamlit_calc:8501` over the Compose network | Learner should notice that Streamlit handles the application while Nginx handles TLS and proxying]]

---

## 8. Read the source's Nginx HTTPS configuration

The source config contains two important server behaviors.

### HTTP redirect

A server block listens on port 80 and returns a redirect:

```nginx
return 301 https://$server_name$request_uri;
```

Conceptually:

```text
HTTP request
   ↓
301 redirect
   ↓
HTTPS URL
```

### TLS listener

The source then configures:

```nginx
listen 8501 ssl;
```

and sets:

```nginx
ssl_certificate
ssl_certificate_key
```

to the mounted certificate and private-key files.

### Reverse proxy

Inside:

```nginx
location /
```

the source uses:

```nginx
proxy_pass http://streamlit_calc:8501;
```

That means:

```text
incoming HTTPS handled by Nginx
        ↓
Nginx decrypts/proxies request
        ↓
Streamlit service on internal Compose network
```

### Forwarded headers

The source includes proxy headers such as:

```text
Host
X-Real-IP
X-Forwarded-For
X-Forwarded-Proto
```

These preserve useful information about the original request as traffic crosses the proxy.

### WebSocket-related headers

The source also sets:

```nginx
Upgrade
Connection
```

which are useful for applications that rely on upgraded HTTP connections such as WebSockets.

Streamlit can make use of persistent interactive connections.

{{exercise:M08.L04.EX02}}

---

## 9. Deploy and validate the HTTPS application

The source then runs the Compose deployment from the repository root.

Its pasted command appears as:

```text
docker-compose up -d –build
```

The dash before `build` in the pasted text is visibly a typographic/Unicode dash.

The chapter's intent is clearly:

> run Docker Compose in detached mode and rebuild the services.

Treat the repository's source file as the authoritative copy-paste syntax.

### Final browser test

The chapter validates with a URL conceptually like:

```text
https://your-domain:8501
```

### What a successful page proves

If the page loads securely, then all of these are working:

```text
DNS
+
load-balancer path
+
security rules
+
EC2
+
Docker Compose
+
Nginx
+
certificate/private key
+
reverse proxy
+
Streamlit
```

### Final request path

```text
Browser
  ↓ https://your-domain:8501
DNS resolution
  ↓
AWS load-balancer layer
  ↓
EC2
  ↓
Nginx :8501 TLS
  ↓
proxy_pass
  ↓
streamlit_calc:8501
  ↓
application response
```

{{exercise:M08.L04.EX03}}

---

## Important misconceptions

### Misconception 1
> "The CSR contains the private key."

The source creates the CSR and private key as separate files.

### Misconception 2
> "The private key should be pasted into the certificate provider's CSR form."

No. The CSR is shared; the private key remains private.

### Misconception 3
> "A DNS validation CNAME and the application A record serve the same purpose."

They do different jobs in the source: one proves domain control for certificate issuance; the other routes user traffic.

### Misconception 4
> "Streamlit terminates TLS in this architecture."

Nginx terminates TLS and reverse-proxies to Streamlit.

### Misconception 5
> "The certificate alone is enough for Nginx."

The source configures both certificate chain material and the corresponding private key.

---

## Key terminology

| Term | Meaning |
|---|---|
| Domain name | Human-readable DNS name for the application |
| TLS/SSL | Encryption/authentication layer used by HTTPS |
| CSR | Certificate Signing Request |
| Private key | Secret cryptographic key paired with the issued certificate |
| CNAME record | DNS alias record used by the source for domain-control validation |
| A record | DNS record mapping a name to an IPv4 address in the source workflow |
| TTL | DNS caching lifetime |
| CA bundle | Certificate-chain material from the certificate provider |
| Nginx | Web server/reverse proxy used by the source for TLS termination |
| Reverse proxy | Server that receives client requests and forwards them to an internal application |
| `proxy_pass` | Nginx directive that forwards traffic to an upstream service |

---

## Self-check

1. Why does the source add a domain name?
2. What problem does TLS solve?
3. What two files are generated by the OpenSSL CSR command?
4. Which file must remain secret?
5. What does the common name represent in the source?
6. Why does the provider require DNS validation?
7. What is the role of the CNAME validation record?
8. What is the role of the A record in the source?
9. Why combine the issued certificate and CA bundle?
10. What does Nginx do in front of Streamlit?
11. What does the port-80 server block do?
12. What does `proxy_pass http://streamlit_calc:8501` mean?
13. Trace the complete HTTPS request path from browser to Streamlit.

---

## Retain this idea

**HTTPS deployment is a chain of trust and routing: prove control of the domain, obtain and protect certificate material, route the domain to your infrastructure, terminate TLS at Nginx, and proxy the decrypted request to the application service.**
""",
        "estimated_minutes": 195,
        "has_code_examples": True,
        "has_manual_image_requests": True,
        "sections": [
            {"id": "domain-tls", "title": "Move from infrastructure addresses to a professional domain and HTTPS", "order": 1},
            {"id": "purchase-source", "title": "The source's domain and certificate provider workflow", "order": 2},
            {"id": "csr", "title": "Generate a CSR and private key with OpenSSL", "order": 3},
            {"id": "domain-validation", "title": "Activate the certificate and prove domain control", "order": 4},
            {"id": "route-domain", "title": "Route the domain toward the AWS entry point", "order": 5},
            {"id": "cert-files", "title": "Prepare the certificate files for Nginx", "order": 6},
            {"id": "compose-nginx", "title": "Put Nginx in front of Streamlit with Docker Compose", "order": 7},
            {"id": "nginx-config", "title": "Read the source's Nginx HTTPS configuration", "order": 8},
            {"id": "deploy-https", "title": "Deploy and validate the HTTPS application", "order": 9},
        ],
    },

    "exercises": [
        {
            "id": "M08.L04.EX01",
            "title": "Separate CSR, Certificate, and Private Key",
            "lesson_code": "M08.L04",
            "section_id": "csr",
            "placement": "after_section",
            "description": "Build a correct mental model of certificate material.",
            "instructions": (
                "Create a three-column table for private key, CSR, and issued certificate. "
                "For each, state who creates it, whether it can be shared, and where the source uses it later."
            ),
            "expected_output": "A certificate-material ownership and usage table.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["tls", "csr", "private-key"],
        },
        {
            "id": "M08.L04.EX02",
            "title": "Trace the Nginx Reverse Proxy",
            "lesson_code": "M08.L04",
            "section_id": "nginx-config",
            "placement": "after_section",
            "description": "Explain how Nginx turns an external HTTPS request into an internal Streamlit request.",
            "instructions": (
                "Trace a request through: domain, Nginx TLS listener, certificate/key, `location /`, "
                "`proxy_pass`, and `streamlit_calc:8501`. Explain the purpose of Host, X-Real-IP, "
                "X-Forwarded-For, and X-Forwarded-Proto."
            ),
            "expected_output": "A reverse-proxy flow diagram plus header explanations.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["nginx", "reverse-proxy", "https"],
        },
        {
            "id": "M08.L04.EX03",
            "title": "Debug an HTTPS Deployment Failure",
            "lesson_code": "M08.L04",
            "section_id": "deploy-https",
            "placement": "after_section",
            "description": "Use the full source architecture to troubleshoot a failed secure request.",
            "instructions": (
                "Suppose https://your-domain:8501 fails. Check, in order, DNS resolution, certificate files, "
                "Nginx startup, Docker Compose service health, load-balancer path, EC2 reachability, and Streamlit. "
                "For each layer, write one piece of evidence that would confirm or eliminate it."
            ),
            "expected_output": "A layered HTTPS troubleshooting checklist.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["dns", "tls", "nginx", "docker-compose", "troubleshooting"],
        },
    ],

    "quiz": {
        "id": "M08.L04.QZ01",
        "title": "Domain, SSL Certificates, Nginx, and HTTPS — Knowledge Check",
        "lesson_code": "M08.L04",
        "placement": "lesson_end",
        "questions": [
            {"id": "M08.L04.Q01", "section_id": "domain-tls", "question": "What two major capabilities does Chapter 4 add?", "options": ["Git and Docker", "Domain name and TLS/SSL", "IAM and S3", "Kubernetes and Helm"], "correct": 1, "explanation": "The source adds a professional domain and encrypted HTTPS."},
            {"id": "M08.L04.Q02", "section_id": "csr", "question": "Which file must remain private?", "options": ["CSR", "Private key", "Public certificate", "DNS CNAME"], "correct": 1, "explanation": "The TLS private key must be protected."},
            {"id": "M08.L04.Q03", "section_id": "csr", "question": "What does the CSR get sent to?", "options": ["Certificate provider/authority workflow", "Docker daemon only", "Git branch", "IAM group"], "correct": 0, "explanation": "The CSR is used to request the certificate."},
            {"id": "M08.L04.Q04", "section_id": "domain-validation", "question": "What DNS record type does the source use for certificate validation?", "options": ["MX", "TXT", "CNAME", "AAAA"], "correct": 2, "explanation": "The source uses a CNAME record for domain-control validation."},
            {"id": "M08.L04.Q05", "section_id": "route-domain", "question": "What does `@` represent in the source DNS UI?", "options": ["The root/apex domain", "An email server", "A Docker container", "A target group"], "correct": 0, "explanation": "The source uses @ for the domain apex."},
            {"id": "M08.L04.Q06", "section_id": "cert-files", "question": "What is combined with the issued certificate in the source?", "options": ["IAM policy", "CA bundle", "Docker image", "Git commit"], "correct": 1, "explanation": "The source concatenates the certificate and CA bundle."},
            {"id": "M08.L04.Q07", "section_id": "compose-nginx", "question": "Which service terminates TLS in the source architecture?", "options": ["Streamlit", "Nginx", "GitHub", "IAM"], "correct": 1, "explanation": "Nginx mounts the certificate and private key and accepts TLS traffic."},
            {"id": "M08.L04.Q08", "section_id": "nginx-config", "question": "What does the port-80 server block do?", "options": ["Runs Python", "Redirects HTTP to HTTPS", "Creates a certificate", "Registers a target group"], "correct": 1, "explanation": "It returns a 301 redirect to the HTTPS URL."},
            {"id": "M08.L04.Q09", "section_id": "nginx-config", "question": "Where does Nginx proxy application traffic?", "options": ["streamlit_calc:8501", "GitHub:22", "IAM:443", "Elasticsearch:9200"], "correct": 0, "explanation": "The source proxies to the internal Streamlit service."},
            {"id": "M08.L04.Q10", "section_id": "deploy-https", "type": "open", "question": "Trace the full request path from entering the HTTPS domain URL to receiving the Streamlit response."},
        ],
        "passing_score": 70,
    },
}
