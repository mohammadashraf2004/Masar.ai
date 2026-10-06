"""M08.L06 — Create and Secure Your Subdomains.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
BOOK-XXX, Chapter 6, page numbers not provided in the supplied chapter export.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel

LESSON_CODE = "M08.L06"
MODULE_ORDER = 8
MODULE_TITLE = "Secure Cloud Deployment Foundations"
MODULE_DESCRIPTION = (
    "Replace application-specific public ports with HTTPS subdomains, update AWS networking, "
    "and issue a multi-domain certificate covering the root domain and application subdomains."
)
SOURCE_CHAPTER = 6
SOURCE_PAGES = "Page numbers not provided in supplied chapter export"

TOPIC = {
    "title": "Create and Secure Your Subdomains",
    "slug": "secure-subdomains-m08-l06",
    "description": (
        "Move Streamlit, Flask, and Jenkins from port-based URLs to dedicated HTTPS subdomains by "
        "updating Nginx, Docker Compose, AWS security groups and target groups, DNS, and a multi-domain SSL certificate."
    ),
    "order": 6,
    "difficulty": DifficultyLevel.beginner,
    "estimated_hours": 3.5,
    "skill_tags": [
        "subdomains", "nginx", "docker-compose", "aws", "load-balancer", "ssl", "tls",
        "san", "csr", "dns", "https", "module-08"
    ],
    "prerequisite_ids": ["M08.L05"],

    "lesson": {
        "title": "Create and Secure Your Subdomains",
        "content": r"""
# Create and Secure Your Subdomains

> **Course:** Secure Cloud Deployment Foundations  
> **Lesson:** M08.L06  
> **Source alignment:** BOOK-XXX, Chapter 6. Source prices and provider UI references are treated as book-specific examples, not current market facts.

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Explain why subdomains improve organization compared with port-suffixed URLs.
- Move Nginx public listeners from 8501/8502/8504 to standard HTTPS port 443.
- Explain the source's use of distinct `server_name` values for each application.
- Update Docker Compose so Nginx exposes only ports 80 and 443.
- Explain why source security groups and target groups remove application-specific ports.
- Explain why the original certificate becomes invalid/inappropriate for the new subdomains.
- Compare the source's wildcard and multi-domain certificate concepts.
- Explain SANs (Subject Alternative Names) in the source.
- Build a `csr.conf` containing the root domain plus three subdomains.
- Verify SANs before submitting the CSR.
- Complete the source's CNAME-based domain-control validation.
- Add A records for `streamlit`, `flask`, and `jenkins`.
- Combine certificate and CA bundle files.
- Redeploy the stack and explain why Jenkins' configured URL must be updated.

---

## 1. Replace port-oriented URLs with service-oriented names

Before Chapter 6, the source uses URLs such as:

```text
https://domain:8501
https://domain:8502
https://domain:8504
```

Chapter 6 moves to:

```text
https://streamlit.domain
https://flask.domain
https://jenkins.domain
```

### Why this is cleaner

A URL like:

```text
flask.example.com
```

communicates service identity directly.

A URL like:

```text
example.com:8502
```

requires the user to know what port 8502 means.

Subdomains separate services by DNS name instead of public port number.

### New public web ports

The source standardizes on:

```text
80  → HTTP
443 → HTTPS
```

This lets browsers connect without explicit `:port` suffixes.

[[IMAGE_NEEDED: Port-based URLs versus subdomain URLs | A before/after diagram. Before: one domain with :8501, :8502, :8504. After: streamlit.domain, flask.domain, jenkins.domain all entering through ports 80/443 | Learner should notice that service identity moves from the port number into the hostname]]

---

## 2. Update Nginx to route by hostname

Before the change, the source conceptually has:

```nginx
listen 8501 ssl;
server_name primary-domain;
```

for Streamlit, with similar application-specific listener ports for Flask and Jenkins.

After the change:

```nginx
listen 443 ssl;
server_name streamlit.primary-domain;
```

and separate server blocks for:

```text
flask.primary-domain
jenkins.primary-domain
```

### Host-based routing

Now Nginx can route based on the request's host name.

Conceptually:

```text
streamlit.domain
      ↓
proxy_pass → streamlit_calc:8501

flask.domain
      ↓
proxy_pass → flask:8502

jenkins.domain
      ↓
proxy_pass → jenkins:8080
```

The applications keep their internal ports.

Only the public interface changes.

### HTTP redirect

The source still uses port 80 to redirect browsers toward HTTPS.

### Docker Compose update

Nginx's public port section changes from:

```text
8501
8502
8504
```

to:

```yaml
ports:
  - "80:80"
  - "443:443"
```

Internal application service ports remain available inside the Compose network.

[[IMAGE_NEEDED: Host-based Nginx routing | A diagram showing all external HTTPS traffic arriving on port 443, then Nginx selecting one of three upstreams based on hostname: streamlit → 8501, flask → 8502, jenkins → 8080 | Learner should notice that public port 443 is shared while internal service ports remain distinct]]

{{exercise:M08.L06.EX01}}

---

## 3. Simplify AWS security groups and load-balancer listeners

Once public traffic uses only:

```text
80
443
```

the old application-facing ports are no longer needed at the AWS edge.

The source explicitly removes:

```text
8501
8502
8504
```

from the relevant security-group/load-balancer configuration.

### Load-balancer security group

Final source pattern:

```text
22  → SSH
80  → HTTP
443 → HTTPS
```

from the trusted `/32` source.

### EC2 security group

The source similarly changes EC2 inbound access to:

```text
22
80
443
```

from the load-balancer side shown in its architecture.

### Target groups/listeners

The source moves to target groups/listeners for:

```text
22
80
443
```

instead of three separate application service ports.

This is an example of reducing unnecessary exposed interfaces.

---

## 4. Why the old certificate does not secure the new subdomains

After switching to subdomains, the source observes that the browser reports the HTTPS connection as insecure.

It gives two reasons:

1. the existing certificate is not appropriate for the subdomains,
2. the original CSR did not explicitly include those subdomains.

A certificate must cover the names clients use.

If users visit:

```text
streamlit.domain
flask.domain
jenkins.domain
```

those names need to be represented in the certificate's allowed identities.

That leads to **SANs**.

---

## 5. Wildcard versus multi-domain certificates in the source

The source discusses two certificate approaches.

### Wildcard certificate

Conceptually:

```text
*.example.com
```

can cover many subdomains.

The source describes this as flexible because new subdomains can be added without reissuing for each specific name.

### Multi-domain/SAN certificate

A **SAN certificate** lists specific names.

The source's required names are:

```text
primary domain
streamlit subdomain
flask subdomain
jenkins subdomain
```

for a total of four SAN entries in its example.

### Source-reported pricing

The source includes Namecheap pricing comparisons for wildcard and multi-domain certificates.

Those values are provider/time-specific and should be treated only as source-reported examples.

The durable learning distinction is:

```text
wildcard
→ broad subdomain pattern

multi-domain SAN
→ explicit fixed list of names
```

The source chooses the multi-domain option for its fixed set of applications.

---

## 6. Build a CSR that explicitly contains all hostnames

Instead of relying only on an interactive OpenSSL prompt, the source creates:

```text
csr.conf
```

The important part is:

```ini
[req_ext]
subjectAltName = @alt_names

[alt_names]
DNS.1 = example.com
DNS.2 = streamlit.example.com
DNS.3 = flask.example.com
DNS.4 = jenkins.example.com
```

### Why this matters

The CSR now explicitly requests a certificate covering all service hostnames.

### Generate

The source uses:

```bash
openssl req \
  -new \
  -newkey rsa:2048 \
  -nodes \
  -keyout private.key \
  -out example_com.csr \
  -config csr.conf
```

### Verify before submitting

The source then runs:

```bash
openssl req -text -noout -verify -in example_com.csr
```

to confirm that the expected names are actually present.

This is an excellent deployment habit:

> Verify generated security material before submitting or installing it.

[[IMAGE_NEEDED: SAN CSR structure | A diagram showing csr.conf with primary domain and three SAN subdomains feeding OpenSSL, producing private.key and a CSR whose SAN list is then verified | Learner should notice that the certificate request explicitly names every hostname to be secured]]

{{exercise:M08.L06.EX02}}

---

## 7. Validate domain control and add subdomain DNS records

The source again uses CNAME-based domain-control validation.

### CNAME validation

Provider supplies:

```text
host key
target key
```

The learner updates the DNS CNAME record and waits for validation.

### Application DNS

The source keeps the apex/root A record and adds:

```text
streamlit → load-balancer public IP
flask     → load-balancer public IP
jenkins   → load-balancer public IP
```

So all hostnames resolve to the same load-balancer entry point.

Nginx later differentiates the services by hostname.

### DNS flow

```text
streamlit.domain ─┐
flask.domain     ─┼→ same load-balancer IP
jenkins.domain   ─┘
                         ↓
                      Nginx
                         ↓
              route by server_name
```

---

## 8. Prepare the new certificate and redeploy

The source downloads:

```text
certificate .crt
CA bundle
.p7b file
```

and combines:

```text
certificate
+
CA bundle
```

into:

```text
combined.crt
```

The private key remains separate.

The source organizes the new certificate material under a dedicated backup/new-certificate folder.

### Redeploy

It then performs:

```bash
docker-compose down
docker-compose up -d --build
```

The pasted source sometimes contains a typographic dash before `build`; the repository file should be used for exact runnable syntax.

### Verify

The source expects:

```text
flask.domain
streamlit.domain
jenkins.domain
```

to be reachable securely.

{{exercise:M08.L06.EX03}}

---

## 9. Update Jenkins' own configured URL

After the infrastructure changes, the external Jenkins URL becomes:

```text
https://jenkins.domain
```

But Jenkins may still believe its old URL is:

```text
https://domain:8504/
```

The source reports noticeably slower behavior until that internal configuration is updated.

### Fix

The source goes to:

```text
Manage Jenkins
→ System
→ Jenkins Location
→ Jenkins URL
```

and replaces the old address with the new subdomain.

This illustrates an important application/infrastructure boundary:

> Changing the reverse proxy and DNS does not automatically update every application's own idea of its canonical URL.

[[IMAGE_NEEDED: Jenkins URL mismatch | A before/after diagram showing Nginx/DNS routing to `jenkins.domain` while Jenkins still believes its URL is `domain:8504`, then showing both aligned after updating Jenkins Location | Learner should notice that application-level URL configuration must match infrastructure routing]]

---

## Important misconceptions

### Misconception 1
> "Moving to subdomains changes each container's internal port."

No. Nginx still proxies to the same internal service ports.

### Misconception 2
> "A certificate for the root domain automatically covers every subdomain."

The source explicitly encounters failure because the original certificate/CSR did not cover the new names.

### Misconception 3
> "DNS decides whether traffic reaches Streamlit or Flask."

DNS sends all service hostnames to the same load-balancer address. Nginx routes based on hostname.

### Misconception 4
> "Jenkins automatically discovers its new canonical URL."

The source updates Jenkins Location manually.

---

## Key terminology

| Term | Meaning |
|---|---|
| Subdomain | Hostname below a parent domain, such as `flask.example.com` |
| Port 80 | Standard HTTP port |
| Port 443 | Standard HTTPS port |
| Host-based routing | Selecting an upstream based on requested hostname |
| SAN | Subject Alternative Name listed in a certificate |
| Wildcard certificate | Certificate covering a subdomain pattern |
| Multi-domain certificate | Certificate listing multiple explicit names |
| CNAME validation | DNS-based proof of domain control |
| A record | DNS mapping from name to IPv4 address |

---

## Self-check

1. Why are subdomains easier to use than port-based URLs?
2. Which external port handles HTTPS after the migration?
3. Which internal ports do Streamlit, Flask, and Jenkins still use?
4. Why can the old certificate fail after introducing subdomains?
5. What is a SAN?
6. How does a wildcard differ from a multi-domain certificate?
7. Why verify the CSR before submission?
8. Which DNS A records are added for the three applications?
9. Why do all service hostnames point to the same load-balancer IP?
10. Why must Jenkins Location be updated?

---

## Retain this idea

**Subdomains move service identity from public port numbers into hostnames; Nginx performs host-based routing on standard HTTPS port 443, while a SAN-aware certificate and matching DNS records make those hostnames securely usable.**
""",
        "estimated_minutes": 210,
        "has_code_examples": True,
        "has_manual_image_requests": True,
        "sections": [
            {"id": "why-subdomains", "title": "Replace port-oriented URLs with service-oriented names", "order": 1},
            {"id": "nginx-subdomains", "title": "Update Nginx to route by hostname", "order": 2},
            {"id": "aws-network-update", "title": "Simplify AWS security groups and load-balancer listeners", "order": 3},
            {"id": "cert-problem", "title": "Why the old certificate does not secure the new subdomains", "order": 4},
            {"id": "wildcard-vs-san", "title": "Wildcard versus multi-domain certificates in the source", "order": 5},
            {"id": "san-csr", "title": "Build a CSR that explicitly contains all hostnames", "order": 6},
            {"id": "dns-validation", "title": "Validate domain control and add subdomain DNS records", "order": 7},
            {"id": "prepare-redeploy", "title": "Prepare the new certificate and redeploy", "order": 8},
            {"id": "fix-jenkins", "title": "Update Jenkins' own configured URL", "order": 9},
        ],
    },

    "exercises": [
        {
            "id": "M08.L06.EX01",
            "title": "Translate Port Routing into Host Routing",
            "lesson_code": "M08.L06",
            "section_id": "nginx-subdomains",
            "placement": "after_section",
            "description": "Map the source's old and new public-routing designs.",
            "instructions": (
                "Create a before/after table for Streamlit, Flask, and Jenkins. Include old URL, new subdomain, "
                "old external port, new external port, and unchanged internal upstream port."
            ),
            "expected_output": "A three-service port-to-host routing table.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["nginx", "subdomains", "reverse-proxy"],
        },
        {
            "id": "M08.L06.EX02",
            "title": "Build and Verify the SAN List",
            "lesson_code": "M08.L06",
            "section_id": "san-csr",
            "placement": "after_section",
            "description": "Practice defining exactly which names the certificate must secure.",
            "instructions": (
                "Write the `[alt_names]` section for a primary domain and three application subdomains. "
                "Then explain what the OpenSSL verification command should confirm before the CSR is submitted."
            ),
            "expected_output": "A four-name SAN configuration plus a verification checklist.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["openssl", "csr", "san", "tls"],
        },
        {
            "id": "M08.L06.EX03",
            "title": "Trace One Subdomain Request",
            "lesson_code": "M08.L06",
            "section_id": "prepare-redeploy",
            "placement": "after_section",
            "description": "Connect DNS, AWS networking, TLS, Nginx, and the application.",
            "instructions": (
                "Trace `https://flask.example.com` from DNS A record → load balancer → port 443 → EC2/Nginx → "
                "matching `server_name` → Flask service port 8502. Identify where the certificate is presented."
            ),
            "expected_output": "An end-to-end secure subdomain request flow.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["dns", "aws", "tls", "nginx"],
        },
    ],

    "quiz": {
        "id": "M08.L06.QZ01",
        "title": "Create and Secure Your Subdomains — Knowledge Check",
        "lesson_code": "M08.L06",
        "placement": "lesson_end",
        "questions": [
            {"id": "M08.L06.Q01", "section_id": "why-subdomains", "question": "Which public HTTPS port does the new source architecture standardize on?", "options": ["22", "443", "8502", "8504"], "correct": 1, "explanation": "The source moves application HTTPS traffic to port 443."},
            {"id": "M08.L06.Q02", "section_id": "nginx-subdomains", "question": "What chooses the internal upstream after traffic reaches Nginx?", "options": ["IAM role", "Requested hostname/server_name", "Elastic IP only", "Git branch"], "correct": 1, "explanation": "Nginx uses separate host-specific server blocks."},
            {"id": "M08.L06.Q03", "section_id": "aws-network-update", "question": "Which application-specific public ports are removed?", "options": ["22,80,443", "8501,8502,8504", "8080,9090,9200", "3000,5601,16686"], "correct": 1, "explanation": "Those old application ports are no longer needed publicly."},
            {"id": "M08.L06.Q04", "section_id": "cert-problem", "question": "Why does the old certificate fail for new subdomains?", "options": ["Docker is stopped", "The certificate/CSR does not cover those names", "The EC2 disk is full", "The IAM user is missing"], "correct": 1, "explanation": "The source explicitly identifies missing subdomain coverage."},
            {"id": "M08.L06.Q05", "section_id": "wildcard-vs-san", "question": "What does a SAN certificate do?", "options": ["Lists multiple explicit domain names", "Changes EC2 type", "Creates target groups", "Runs Jenkins"], "correct": 0, "explanation": "SANs identify additional names secured by the certificate."},
            {"id": "M08.L06.Q06", "section_id": "san-csr", "question": "Why run `openssl req -text -noout -verify`?", "options": ["To deploy Docker", "To inspect and verify the CSR contents", "To create a DNS A record", "To restart Jenkins"], "correct": 1, "explanation": "The source checks that all expected subdomains appear."},
            {"id": "M08.L06.Q07", "section_id": "dns-validation", "question": "Where do the three subdomain A records point?", "options": ["Different application IPs", "The same load-balancer public IP", "GitHub", "The Jenkins container"], "correct": 1, "explanation": "The source points all application hostnames to the same load-balancer address."},
            {"id": "M08.L06.Q08", "section_id": "prepare-redeploy", "question": "Which files are combined for the server certificate chain?", "options": ["Private key + CSR", "Issued certificate + CA bundle", "Nginx config + Dockerfile", "Git config + IAM policy"], "correct": 1, "explanation": "The source concatenates the certificate and CA bundle."},
            {"id": "M08.L06.Q09", "section_id": "fix-jenkins", "question": "Why update Jenkins Location?", "options": ["To match the new external Jenkins subdomain", "To install Python", "To change model features", "To create a CNAME"], "correct": 0, "explanation": "Jenkins still held the old port-based URL."},
            {"id": "M08.L06.Q10", "section_id": "fix-jenkins", "type": "open", "question": "Explain the complete migration from port-based application URLs to secure HTTPS subdomains."},
        ],
        "passing_score": 70,
    },
}
