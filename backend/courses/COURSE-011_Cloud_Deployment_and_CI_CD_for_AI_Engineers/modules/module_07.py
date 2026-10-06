"""M07.L01 — Monitoring, Logging, and Observability.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
BOOK-XXX, Chapter 10, page numbers not provided in the supplied chapter export.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M07.L01"

MODULE_ORDER = 7

MODULE_TITLE = "Monitoring, Logging, and Observability"

MODULE_DESCRIPTION = (
    "Learn how to understand production systems using logs, metrics, and traces; "
    "centralize logs with the ELK Stack; collect and visualize metrics with "
    "Prometheus and Grafana; create proactive alerts with Alertmanager; and "
    "understand source-described AI-assisted observability patterns."
)

SOURCE_CHAPTER = 10

SOURCE_PAGES = "Page numbers not provided in supplied chapter export"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Monitoring, Logging, and Observability",

    "slug": "monitoring-logging-observability-m07-l01",

    "description": (
        "Move beyond simply deploying software and learn how to understand whether "
        "a production system is healthy, why failures occur, where latency originates, "
        "and how to build proactive operational feedback using open-source observability tools."
    ),

    "order": 1,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 3.5,

    "skill_tags": [
        "observability",
        "monitoring",
        "logging",
        "metrics",
        "tracing",
        "elk",
        "elasticsearch",
        "logstash",
        "kibana",
        "prometheus",
        "grafana",
        "alertmanager",
        "opentelemetry",
        "jaeger",
        "module-07",
    ],

    "prerequisite_ids": ["M06.L01"],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Monitoring, Logging, and Observability",

        "content": r"""
# Monitoring, Logging, and Observability

> **Course:** Cloud & DevOps Foundations  
> **Lesson:** M07.L01  
> **Module:** Monitoring, Logging, and Observability  
> **Source alignment:** BOOK-XXX, Chapter 10. Page numbers were not provided in the supplied chapter export. This lesson is an instructor-authored curriculum adaptation rather than a reproduction of the source text.

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Explain the difference between monitoring and observability using the chapter's known-unknown versus unknown-unknown framing.
- Distinguish logs, metrics, and traces and identify when each is most useful.
- Explain why structured logs are easier to search and analyze than unstructured text.
- Explain why metrics are efficient for dashboards, trends, and alerts.
- Describe how distributed traces connect spans across services to reveal request bottlenecks.
- Explain the OpenTelemetry + Jaeger tracing workflow introduced by the source.
- Explain why centralized logging becomes necessary when applications run across many containers.
- Describe the roles of Elasticsearch, Logstash, and Kibana in the ELK Stack.
- Read the source's Logstash input/output pipeline concept.
- Explain how Prometheus scrapes metrics and how Grafana visualizes them.
- Read a basic Prometheus scrape configuration.
- Explain why dashboards alone are reactive and why Alertmanager enables proactive operations.
- Describe the path from a Prometheus alert rule to Alertmanager and then to a notification receiver.
- Identify the inconsistency in the source's example alert name versus its latency expression.
- Explain source-described AIOps use cases such as code review assistance, anomaly detection, correlation, and automated rollback.
- Combine logs, metrics, traces, and alerts into one practical incident-investigation workflow.

---

## 1. Monitoring tells you what you expected to watch; observability helps you investigate why

After software reaches production, deployment is no longer the main question.

Now you need to ask:

- Is the service healthy?
- Are users receiving errors?
- Why did latency increase?
- Which dependency is failing?
- Did the latest deployment cause the problem?
- What changed before the incident?

The source uses a useful distinction.

### Monitoring: known-unknowns

Monitoring focuses on signals you already know are important.

Examples:

```text
CPU usage
memory usage
request rate
error rate
disk capacity
```

You decide in advance:

> "I know this value matters, so I want to watch it."

Then you collect it and display it on a dashboard or evaluate it against a threshold.

### Observability: unknown-unknowns

Observability is broader.

It means having enough internal evidence from the system to ask questions you did **not** know in advance.

For example:

> "Why are checkout requests slow only for one region and only after the latest deployment?"

You may not have created a dashboard specifically for that exact question.

But if your system emits rich logs, metrics, and traces, you can investigate.

### The doctor analogy

The source compares operations to medicine.

Monitoring is similar to checking routine vital signs:

```text
temperature
heart rate
blood pressure
```

Observability is the broader diagnostic capability used to discover **why** a symptom exists.

This distinction matters because production incidents are often surprising.

A dashboard can tell you:

```text
latency is high
```

but investigation must answer:

```text
why is latency high?
```

[[IMAGE_NEEDED: Monitoring versus observability | A side-by-side diagram. Monitoring side shows predefined dashboards watching CPU, memory, latency, and errors. Observability side shows an engineer starting with an unexpected symptom and exploring correlated logs, metrics, and traces to discover a root cause | Learner should notice that monitoring answers predefined questions while observability supports exploratory investigation]]

### Three sources of evidence

The source organizes observability around three foundational data types:

```text
Logs    → what happened?
Metrics → how much / how often / how fast?
Traces  → where did one request spend its time?
```

They are most powerful when used together.

---

## 2. Logs: the detailed chronological record

A **log** is a discrete, timestamped event.

Examples:

```text
user logged in
database query failed
payment request timed out
service started
authorization denied
```

Logs are especially useful when investigating one specific incident.

Suppose a user says:

> "My payment failed at 3:15 P.M."

Logs can help you filter by:

- timestamp,
- user identifier,
- transaction identifier,
- service,
- severity,
- error text.

### Unstructured logging

An unstructured message might look like:

```text
User login failed
```

A human can read it.

But a machine has little context.

### Structured logging

The source gives a JSON-style example:

```json
{
  "timestamp": "...",
  "level": "error",
  "userID": "123",
  "message": "Invalid password"
}
```

Now the fields can be indexed separately.

You can ask:

```text
level = error
AND userID = 123
AND timestamp between 15:10 and 15:20
```

That is much easier to search at scale.

### What logs are good at

Logs are strong for:

- detailed incident reconstruction,
- stack traces,
- debugging one failed request,
- auditing discrete events,
- understanding exact error messages.

### What logs are not ideal for

Imagine one million request log entries.

If you want to know:

```text
"What was the average request latency over the last hour?"
```

that is usually better represented as a metric.

So do not treat every observability question as a logging question.

---

## 3. Metrics: compact numerical health signals over time

**Metrics** are numerical measurements tracked over time.

The source divides examples into two broad groups.

### System metrics

Examples:

```text
CPU utilization
memory usage
disk space
```

### Application metrics

Examples:

```text
request latency
error rate
request throughput
```

Metrics are efficient to store and query because they summarize numerical behavior rather than recording every detailed event.

### Metrics answer trend questions

Logs might tell you:

```text
Request 8,382 failed at 14:03:09.
```

A metric might tell you:

```text
Error rate increased from 0.4% to 8.2%
between 14:00 and 14:05.
```

That makes metrics ideal for:

- dashboards,
- capacity planning,
- performance trends,
- service-level monitoring,
- alerts.

### Alerting example from the source

The source gives the idea:

> Do not alert on every individual failed request.

Instead, alert when an aggregated condition becomes meaningful, such as:

```text
error rate > threshold
for sustained period
```

This prevents every isolated event from becoming a page.

### Metrics detect; logs explain

A useful beginner model is:

```text
Metric:
"Something is wrong."

Log:
"Here is the detailed event that happened."
```

This is not an absolute rule, but it is a useful way to understand why both data types exist.

---

## 4. Traces: follow one request across a distributed system

A **trace** represents the journey of a single request through multiple services.

This is especially useful in microservice architectures.

Imagine:

```text
Browser
  ↓
Frontend
  ↓
Authentication service
  ↓
User service
  ↓
Database
```

If the request takes 2 seconds, which component is responsible?

Without distributed tracing, every service may look independently healthy.

### Trace ID

The request receives a unique trace ID.

That identity follows the request across services.

### Spans

Each service contributes a **span**.

A span records one portion of the request journey.

For example:

```text
Frontend span        50 ms
Auth span            80 ms
User service span   120 ms
Database span      1750 ms
```

Now the bottleneck is obvious.

### Waterfall view

Tracing backends can display spans as a waterfall.

This lets you see:

- sequence,
- duration,
- parent/child relationships,
- bottlenecks.

[[IMAGE_NEEDED: Distributed trace waterfall | A trace waterfall for one request showing Frontend, Auth Service, User Service, and Database spans with horizontal duration bars, where the Database span is dramatically longer than the others | Learner should notice that traces reveal where one request spends its time across services]]

### OpenTelemetry + Jaeger

The source introduces:

- **OpenTelemetry** for instrumentation and span emission,
- **Jaeger** as a tracing backend and visualization system.

The source gives a local Jaeger example:

```bash
docker run -d \
  -p 16686:16686 \
  -p 4318:4318 \
  jaegertracing/all-in-one
```

Then Jaeger's UI is available at:

```text
http://localhost:16686
```

The chapter does not provide a full application instrumentation walkthrough, but it explains the architecture:

```text
Application
   ↓
OpenTelemetry SDK
   ↓
spans
   ↓
Jaeger
   ↓
trace waterfall
```

### Three pillars together

The source summarizes them well:

```text
Metrics detect a problem.
Logs explain events.
Traces show where a distributed request spent time.
```

{{exercise:M07.L01.EX01}}

---

## 5. Centralized logging with the ELK Stack

With one container, you can run:

```bash
docker logs <container_id>
```

But what if you have:

```text
30 containers
across 8 machines
```

Now logs are scattered.

Worse, when a short-lived container disappears, its local logs may disappear with it.

Centralized logging solves this by shipping logs into one searchable platform.

### The ELK Stack

The source introduces three components.

### Elasticsearch

**Elasticsearch** stores and indexes log data.

Its purpose here is:

```text
search
index
analytics
```

### Logstash

**Logstash** is the ingestion and transformation pipeline.

It can:

```text
receive logs
parse them
transform them
send them onward
```

### Kibana

**Kibana** is the web interface for:

```text
searching logs
exploring data
building visualizations
creating dashboards
```

### Data flow

```text
Applications / services
        ↓
      Logstash
        ↓
  Elasticsearch
        ↓
      Kibana
```

[[IMAGE_NEEDED: ELK centralized logging pipeline | A diagram showing multiple application containers sending logs into Logstash, Logstash transforming and forwarding them to Elasticsearch, and Kibana querying Elasticsearch for search and dashboards | Learner should notice that logs from many services converge into one searchable system]]

### Source Docker Compose setup

The source uses Docker Compose with:

- Elasticsearch 7.17.0,
- Logstash 7.17.0,
- Kibana 7.17.0.

The source excerpt configures ports such as:

```text
Elasticsearch: 9200, 9300
Logstash:      5044
Kibana:        5601
```

It also sets Elasticsearch as a single node.

### Resource requirement

The source warns that Elasticsearch is memory-intensive.

It recommends at least:

```text
2 GB RAM allocated to Docker
```

with:

```text
4 GB recommended
```

for the chapter environment.

### Logstash pipeline

The source creates:

```text
logstash/pipeline/logstash.conf
```

and introduces the classic flow:

```text
input
→ filter/transform
→ output
```

Its supplied example listens for JSON lines over TCP:

```text
port 5044
```

and writes to Elasticsearch using an index pattern:

```text
app-logs-YYYY.MM.dd
```

### Kibana exploration

After starting the stack:

```bash
docker compose up
```

the source uses:

```text
http://localhost:5601
```

for Kibana.

It suggests an index pattern such as:

```text
app-logs-*
```

for exploring application logs.

### Source-format caution

The supplied Docker Compose excerpt has a visible indentation irregularity around:

```text
ES_JAVA_OPTS
```

This lesson does not silently treat that excerpt as guaranteed copy-paste-ready configuration. Use the source's downloadable code bundle if you need the exact runnable chapter configuration.

### Production debugging story

The source provides a useful incident scenario.

Users report payment failures.

With scattered logs, an engineer might need to manually visit multiple machines and containers.

With centralized logs:

```text
Kibana
  ↓
filter incident time
  ↓
search payment + error
  ↓
filter by transaction ID
  ↓
discover database connection timeout
```

This illustrates the practical value:

> Centralized logs let you correlate events across services instead of treating each container as an isolated island.

{{exercise:M07.L01.EX02}}

---

## 6. Prometheus and Grafana: collect and visualize system health

Logs explain discrete events.

Metrics give you continuous numerical health.

The source introduces:

- **Prometheus** for metrics collection and storage,
- **Grafana** for visualization.

### Prometheus pull model

Prometheus expects applications or exporters to expose metrics over HTTP.

A common endpoint is:

```text
/metrics
```

Prometheus periodically **scrapes** those endpoints.

Conceptually:

```text
Application /metrics
        ↑
     scrape
        |
    Prometheus
```

This is called a pull model because Prometheus requests the metrics from targets.

### Prometheus configuration

The source provides:

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: "prometheus"
    static_configs:
      - targets: ["localhost:9090"]

  - job_name: "my-app"
    static_configs:
      - targets: ["host.docker.internal:8080"]
```

### `scrape_interval`

```yaml
scrape_interval: 15s
```

means Prometheus collects configured metrics every 15 seconds.

### Targets

Each job defines one or more metric endpoints.

The source uses:

```text
localhost:9090
```

for Prometheus itself and:

```text
host.docker.internal:8080
```

for the sample application.

### Linux note from the source

The chapter warns that:

```text
host.docker.internal
```

may not resolve automatically on Linux.

It suggests either:

- adding an `extra_hosts` mapping using `host-gateway`,
- or using the default Docker bridge address shown in the source.

This is a platform-specific troubleshooting point rather than a universal architecture requirement.

### Grafana

Grafana connects to Prometheus as a data source.

Then you can visualize:

- latency,
- error rate,
- CPU,
- memory,
- request throughput.

The source mentions **PromQL**, Prometheus' query language, as the basis for querying metric data.

### Dashboard example

The source mentions Grafana community dashboard ID:

```text
1860
```

for **Node Exporter Full**.

This is presented as a quick-start example for host metrics when `node_exporter` is available.

### Local interfaces

The source uses:

```text
Prometheus → http://localhost:9090
Grafana    → http://localhost:3000
```

It also states that the chapter's Grafana setup defaults to:

```text
username: admin
password: admin
```

and prompts for a password change at first login.

### Dashboards are not enough

A dashboard is valuable only if someone looks at it.

At 3 A.M., the dashboard does not wake the on-call engineer by itself.

That is why alerting is the next layer.

[[IMAGE_NEEDED: Prometheus and Grafana metric flow | A diagram showing application /metrics endpoints being scraped by Prometheus, Prometheus storing time-series data, and Grafana querying Prometheus to build latency, error-rate, CPU, and memory dashboards | Learner should notice that Prometheus collects/stores metrics while Grafana visualizes them]]

---

## 7. Alertmanager: turn metrics into proactive operational signals

A mature monitoring system must notify the team when something important happens.

The source introduces **Alertmanager** for this role.

### Alert flow

The workflow is:

```text
Prometheus metrics
       ↓
PromQL alert rule
       ↓
condition true long enough
       ↓
Prometheus fires alert
       ↓
Alertmanager
       ↓
group / deduplicate / route
       ↓
email / Slack / PagerDuty / other receiver
```

### What Alertmanager adds

The source highlights:

- deduplication,
- grouping,
- routing.

Without those capabilities, one underlying problem might generate many duplicate notifications.

### Alert rule structure

The source gives:

```yaml
groups:
- name: example
  rules:
  - alert: HighErrorRate
    expr: job:request_latency_seconds:mean5m{job="my-app"} > 0.5
    for: 1m
    labels:
      severity: page
    annotations:
      summary: High request latency
```

Let's read its structure.

### `alert`

```yaml
alert: HighErrorRate
```

is the alert name.

### `expr`

```yaml
job:request_latency_seconds:mean5m{job="my-app"} > 0.5
```

is the PromQL condition.

### `for`

```yaml
for: 1m
```

means the condition must remain true continuously for one minute before firing.

This helps avoid alerting on momentary spikes.

### Labels

```yaml
severity: page
```

adds routing/classification metadata.

### Annotations

```yaml
summary: High request latency
```

provide human-readable context.

### Important source inconsistency

The source names this rule:

```text
HighErrorRate
```

but the expression and summary are about:

```text
request latency
```

The source itself then explains it as a high-latency alert.

Do not copy this mismatch into a production alerting system.

A professional alert should keep these aligned:

```text
alert name
expression
summary
runbook meaning
```

For example, conceptually:

```text
HighRequestLatency
```

would better match the source expression, but that is an instructional observation rather than a claim that the source contained that corrected name.

### Memory leak example

The source also gives a scenario:

```text
container memory > 80% of limit
for > 10 minutes
```

Then:

```text
Alertmanager
   ↓
Slack / on-call notification
```

The engineer can inspect Grafana, intervene before a crash, and create follow-up work.

This illustrates the shift from:

```text
react after outage
```

to:

```text
detect dangerous trend before outage
```

{{exercise:M07.L01.EX03}}

---

## 8. AI-assisted observability and anomaly detection

The source finishes by introducing AI-assisted operations, often called **AIOps**.

This section is best understood as a set of source-described examples rather than a replacement for the fundamentals learned earlier.

### Static thresholds have limits

A threshold rule says:

```text
if value > X
then alert
```

That is useful when you know the dangerous boundary.

But sometimes the problem is:

```text
"This behavior is abnormal for this service."
```

even if no static threshold has been crossed yet.

AI-based anomaly detection attempts to learn patterns and surface deviations.

### Amazon CodeGuru in the source

The source describes two components.

#### CodeGuru Reviewer

The source presents it as an AI/ML-assisted code review service for identifying issues such as:

- code-quality problems,
- security concerns,
- implementation defects.

#### CodeGuru Profiler

The source presents this as production profiling to identify costly or CPU-intensive code paths.

The learning point is:

```text
code-level insight
+
production performance insight
```

### Amazon DevOps Guru in the source

The chapter describes DevOps Guru as analyzing:

- metrics,
- logs,
- events,

to identify abnormal operational behavior and correlate related symptoms.

The source examples include:

- gradual memory growth,
- related failures across services,
- slow latency degradation across deployments.

### Correlation matters

Imagine:

```text
API latency increases
Lambda timeouts rise
database errors appear
connection pool becomes exhausted
```

An engineer might otherwise receive four different alerts.

The source's AIOps idea is to correlate related signals into one incident context.

### Self-healing pipeline scenario

The final source scenario combines:

```text
new deployment
      ↓
small traffic shift
      ↓
health monitoring
      ↓
anomaly / alarm
      ↓
automatic rollback
```

Specifically, the chapter describes a blue/green deployment in which monitoring can trigger rollback to the stable environment.

The educational point is:

> Observability data can become an automated feedback signal for deployment safety.

### Treat AI as another diagnostic layer

A useful model is:

```text
Logs + Metrics + Traces
          ↓
Rules + Dashboards
          ↓
Alerts
          ↓
Optional AI correlation/anomaly assistance
```

AI does not remove the need for good telemetry.

Without useful underlying signals, intelligent analysis has little trustworthy evidence to work with.

---

## 9. End-to-end incident investigation: combine all three pillars

Consider this incident:

> Users report that checkout has become slow and some payments fail.

### Step 1 — Metrics detect the symptom

Grafana shows:

```text
request latency ↑
error rate ↑
```

Now you know:

```text
something changed
```

### Step 2 — Alerting notifies the team

Prometheus detects a sustained condition.

Alertmanager routes the notification to the responsible team.

Now the issue does not depend on someone watching a dashboard.

### Step 3 — Traces locate the slow segment

A trace shows:

```text
Frontend      40 ms
Auth          70 ms
Cart         110 ms
Payment      900 ms
Database    1800 ms
```

The request spends most of its time near the database dependency.

### Step 4 — Logs explain the exact event

Centralized logs show:

```text
Database connection timeout
```

for failed payment transactions.

Now you have:

```text
Metrics → when and how badly?
Traces  → where?
Logs    → what exactly happened?
```

### Step 5 — Investigate the change context

Operational context may show:

- a recent deployment,
- infrastructure saturation,
- a dependency issue.

### Step 6 — Restore service

The team can:

- rollback,
- restart,
- scale,
- fix configuration,
- or repair the failing dependency,

depending on evidence.

### Step 7 — Improve the system

After the incident:

- add a better alert,
- improve structured logging,
- instrument missing traces,
- add a dashboard,
- fix the root cause.

This closes the DevOps feedback loop.

[[IMAGE_NEEDED: End-to-end observability incident workflow | A flow showing Alert → Grafana metric spike → distributed trace bottleneck → Kibana log error → identified root cause → remediation → follow-up improvement | Learner should notice how different telemetry sources answer different parts of the same incident]]

{{exercise:M07.L01.EX04}}

---

## Important misconceptions

### Misconception 1

> "Monitoring and observability are the same thing."

### Why this is incomplete

The source distinguishes monitoring as watching predefined signals and observability as the broader ability to investigate unexpected system behavior.

---

### Misconception 2

> "Logs are the best tool for every operational question."

### Why this is wrong

Logs are excellent for detailed events.

Metrics are more efficient for numerical trends and alerts.

Traces are better for following one request across distributed services.

---

### Misconception 3

> "A trace is just a long log file."

### Why this is wrong

A trace models the end-to-end path of one request and is composed of spans across services.

---

### Misconception 4

> "Kibana stores the logs."

### Why this is wrong

In the ELK model taught by the source:

```text
Elasticsearch stores/indexes
Logstash ingests/transforms
Kibana explores/visualizes
```

---

### Misconception 5

> "Grafana collects metrics from applications."

### Why this is incomplete

In the chapter's architecture, Prometheus scrapes and stores metrics.

Grafana queries Prometheus and visualizes them.

---

### Misconception 6

> "A dashboard automatically alerts the team."

### Why this is wrong

Dashboards are primarily visual.

Alerting rules plus Alertmanager create the proactive notification path.

---

### Misconception 7

> "Every one-off error should page the on-call engineer."

### Why this is wrong

The source emphasizes aggregated metric conditions for alerting rather than paging on every isolated log event.

---

### Misconception 8

> "The source's `HighErrorRate` example is internally consistent."

### Why this is wrong

The supplied example's name says error rate, but its PromQL expression and summary describe request latency.

This should be treated as a source inconsistency and not copied blindly.

---

### Misconception 9

> "AI anomaly detection means logs, metrics, traces, and alerts are no longer necessary."

### Why this is wrong

AI-based analysis still depends on useful operational data.

The telemetry remains the evidence.

---

## Key terminology

| Term | Meaning |
|---|---|
| Monitoring | Watching predefined signals and thresholds |
| Observability | Ability to explore a system's internal behavior to investigate expected and unexpected questions |
| Log | Discrete timestamped event |
| Structured log | Machine-readable log with explicit fields, often JSON |
| Metric | Numerical time-series measurement |
| Trace | End-to-end record of one request across distributed components |
| Span | One timed segment within a trace |
| Trace ID | Identifier connecting spans belonging to the same request |
| OpenTelemetry | Instrumentation framework introduced by the source for producing telemetry such as traces |
| Jaeger | Tracing backend/UI introduced by the source |
| Centralized logging | Aggregating logs from many services into one searchable platform |
| Elasticsearch | ELK component used to index/store searchable log data |
| Logstash | ELK ingestion/transformation pipeline |
| Kibana | ELK visualization and search interface |
| Prometheus | Metrics collection and time-series monitoring system |
| Scrape | Prometheus operation that pulls metric values from a target |
| PromQL | Prometheus query language |
| Grafana | Dashboard and visualization platform used with Prometheus in the source |
| Alert rule | Condition evaluated against metrics that can generate an alert |
| Alertmanager | Component that groups, deduplicates, and routes alerts |
| Receiver | Destination for alert notifications |
| AIOps | Use of AI/ML techniques to assist IT operations and observability |
| Anomaly detection | Identification of behavior that deviates from a learned or expected pattern |
| Self-healing pipeline | Source-described automation pattern where operational signals can trigger corrective action such as rollback |

---

## Self-check

Before continuing, make sure you can answer:

1. How does the source distinguish monitoring from observability?
2. What is a known-unknown?
3. What is an unknown-unknown?
4. What are the three pillars introduced by the chapter?
5. Why are structured logs easier to analyze?
6. What are system metrics versus application metrics?
7. Why are metrics useful for alerting?
8. What is a trace?
9. What is a span?
10. How can traces reveal a database bottleneck?
11. What roles do OpenTelemetry and Jaeger play in the source's tracing workflow?
12. Why does centralized logging become necessary with many containers?
13. What does Elasticsearch do?
14. What does Logstash do?
15. What does Kibana do?
16. What resource warning does the source give for Elasticsearch?
17. What does Prometheus mean by "scraping" a target?
18. What is Grafana's role?
19. Why is a dashboard alone insufficient at 3 A.M.?
20. What does Alertmanager add after Prometheus fires an alert?
21. What does `for: 1m` mean in an alert rule?
22. What inconsistency exists in the source's `HighErrorRate` example?
23. How does the source describe AI-assisted anomaly detection?
24. Why does AI still depend on underlying telemetry?
25. In an incident, which pillar helps answer "when/how bad," "where," and "what exactly happened"?
26. Explain a complete investigation path from alert to root cause and follow-up improvement.

---

## Retain this idea

**Observability turns production behavior into evidence: metrics reveal patterns, traces locate distributed bottlenecks, logs explain concrete events, and alerting ensures the right people learn about important changes before users have to report them.**
""",

        "estimated_minutes": 210,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {
                "id": "monitoring-vs-observability",
                "title": "Monitoring tells you what you expected to watch; observability helps you investigate why",
                "order": 1,
            },
            {
                "id": "logs",
                "title": "Logs: the detailed chronological record",
                "order": 2,
            },
            {
                "id": "metrics",
                "title": "Metrics: compact numerical health signals over time",
                "order": 3,
            },
            {
                "id": "traces",
                "title": "Traces: follow one request across a distributed system",
                "order": 4,
            },
            {
                "id": "centralized-logging",
                "title": "Centralized logging with the ELK Stack",
                "order": 5,
            },
            {
                "id": "prometheus-grafana",
                "title": "Prometheus and Grafana: collect and visualize system health",
                "order": 6,
            },
            {
                "id": "alerting",
                "title": "Alertmanager: turn metrics into proactive operational signals",
                "order": 7,
            },
            {
                "id": "ai-observability",
                "title": "AI-assisted observability and anomaly detection",
                "order": 8,
            },
            {
                "id": "incident-workflow",
                "title": "End-to-end incident investigation: combine all three pillars",
                "order": 9,
            },
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M07.L01.EX01",

            "title": "Choose the Right Observability Signal",

            "lesson_code": "M07.L01",

            "section_id": "traces",

            "placement": "after_section",

            "description": (
                "Practice choosing logs, metrics, traces, or a combination based on "
                "the operational question being asked."
            ),

            "instructions": (
                "For each scenario, choose the best primary signal and explain why:\n"
                "1. Determine whether error rate increased during the last 30 minutes.\n"
                "2. Find the exact stack trace for one failed user request at 15:12.\n"
                "3. Discover which microservice consumed most of a slow request's 2.4-second latency.\n"
                "4. Determine whether memory usage has been trending upward for six hours.\n"
                "5. Investigate a checkout incident using all three pillars: state what each would contribute."
            ),

            "expected_output": (
                "A five-row table mapping each operational question to logs, metrics, traces, "
                "or a combination, with a concise justification."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "logs",
                "metrics",
                "traces",
                "observability",
            ],
        },

        {
            "id": "M07.L01.EX02",

            "title": "Trace a Log Through the ELK Pipeline",

            "lesson_code": "M07.L01",

            "section_id": "centralized-logging",

            "placement": "after_section",

            "description": (
                "Practice understanding the full centralized logging path rather than "
                "memorizing ELK component names."
            ),

            "instructions": (
                "Scenario: a payment service emits a JSON error log containing timestamp, "
                "transaction_id, level, and message.\n"
                "1. Explain how that event enters Logstash in the chapter's architecture.\n"
                "2. Explain what Logstash can do before forwarding it.\n"
                "3. Explain where Elasticsearch stores/indexes it.\n"
                "4. Explain how Kibana lets an engineer find all failures for the same transaction_id.\n"
                "5. Draw the flow: Payment Service → Logstash → Elasticsearch → Kibana.\n"
                "6. Explain why this is better than manually running docker logs on many containers."
            ),

            "expected_output": (
                "A logging flow diagram plus an explanation of ingestion, indexing, search, "
                "and the operational benefit of centralization."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "elk",
                "logstash",
                "elasticsearch",
                "kibana",
                "structured-logging",
            ],
        },

        {
            "id": "M07.L01.EX03",

            "title": "Design a Useful Alert Rule",

            "lesson_code": "M07.L01",

            "section_id": "alerting",

            "placement": "after_section",

            "description": (
                "Practice designing alerts whose names, expressions, durations, and messages "
                "all describe the same operational condition."
            ),

            "instructions": (
                "1. Review the source's alert named HighErrorRate and identify why its name does not match its latency expression and summary.\n"
                "2. Design a conceptually consistent high-latency alert with a matching name, condition, duration, severity, and summary.\n"
                "3. Separately design a true high-error-rate alert concept.\n"
                "4. For each alert, explain why a sustained duration is preferable to paging on one brief spike.\n"
                "5. Explain what Prometheus does and what Alertmanager does after the rule fires."
            ),

            "expected_output": (
                "Two internally consistent alert designs plus an explanation of rule evaluation, "
                "sustained duration, and Alertmanager routing."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "prometheus-alerting",
                "promql-concepts",
                "alertmanager",
                "alert-design",
            ],
        },

        {
            "id": "M07.L01.EX04",

            "title": "Investigate a Production Checkout Incident",

            "lesson_code": "M07.L01",

            "section_id": "incident-workflow",

            "placement": "after_section",

            "description": (
                "Integrate metrics, alerts, traces, and centralized logs into one incident-response workflow."
            ),

            "instructions": (
                "Scenario: checkout latency doubles and payment failures increase after a deployment.\n"
                "1. Identify which metrics you would inspect first.\n"
                "2. Describe one alert condition that could notify the team.\n"
                "3. Explain how a distributed trace could identify the slowest service or dependency.\n"
                "4. List structured log fields that would help correlate failed payment requests.\n"
                "5. Explain how you would use Kibana after identifying a suspicious transaction or trace.\n"
                "6. Describe one remediation and one follow-up observability improvement.\n"
                "7. Explain where an AI-assisted anomaly/correlation system could help without replacing human verification."
            ),

            "expected_output": (
                "A chronological incident investigation showing detection, notification, localization, "
                "root-cause evidence, remediation, and follow-up improvement."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "incident-response",
                "observability",
                "metrics",
                "traces",
                "logs",
                "alerting",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M07.L01.QZ01",

        "title": "Monitoring, Logging, and Observability — Knowledge Check",

        "lesson_code": "M07.L01",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M07.L01.Q01",

                "section_id": "monitoring-vs-observability",

                "question": (
                    "How does the source primarily distinguish observability from monitoring?"
                ),

                "options": [
                    "Monitoring uses logs while observability uses only metrics",
                    "Monitoring watches predefined signals, while observability supports exploring unexpected system questions",
                    "Observability is only for Kubernetes",
                    "Monitoring is automated while observability must be manual",
                ],

                "correct": 1,

                "explanation": (
                    "The chapter frames monitoring around known-unknowns and observability around the ability "
                    "to investigate unknown-unknowns."
                ),
            },

            {
                "id": "M07.L01.Q02",

                "section_id": "logs",

                "question": (
                    "Why are structured logs generally easier to search at scale?"
                ),

                "options": [
                    "They contain no timestamps",
                    "They expose machine-readable fields such as level, user ID, and message",
                    "They cannot include errors",
                    "They are automatically metrics",
                ],

                "correct": 1,

                "explanation": (
                    "Explicit fields can be indexed, filtered, grouped, and queried more reliably than free-form text."
                ),
            },

            {
                "id": "M07.L01.Q03",

                "section_id": "metrics",

                "question": (
                    "Which observability signal is best suited to tracking overall error rate over time?"
                ),

                "options": [
                    "Metrics",
                    "One unstructured log line",
                    "A Helm Chart",
                    "A Docker image tag",
                ],

                "correct": 0,

                "explanation": (
                    "Error rate is a numerical time-series measurement, which fits the metrics model taught by the chapter."
                ),
            },

            {
                "id": "M07.L01.Q04",

                "section_id": "traces",

                "question": (
                    "What is a span in distributed tracing?"
                ),

                "options": [
                    "A full Docker container",
                    "One timed segment of a request's journey through the system",
                    "A Prometheus dashboard",
                    "A Kibana index pattern",
                ],

                "correct": 1,

                "explanation": (
                    "A trace is built from spans, each describing one segment of the end-to-end request path."
                ),
            },

            {
                "id": "M07.L01.Q05",

                "section_id": "traces",

                "question": (
                    "What roles do OpenTelemetry and Jaeger play in the source's tracing model?"
                ),

                "options": [
                    "OpenTelemetry instruments/emits telemetry, while Jaeger receives and visualizes traces",
                    "Jaeger builds Docker images while OpenTelemetry stores Git commits",
                    "Both are ELK components",
                    "Both are only used for CPU metrics",
                ],

                "correct": 0,

                "explanation": (
                    "The source introduces OpenTelemetry for instrumentation and Jaeger as the tracing backend/UI."
                ),
            },

            {
                "id": "M07.L01.Q06",

                "section_id": "centralized-logging",

                "question": (
                    "Which ELK component stores and indexes the log data?"
                ),

                "options": [
                    "Kibana",
                    "Logstash",
                    "Elasticsearch",
                    "Grafana",
                ],

                "correct": 2,

                "explanation": (
                    "Elasticsearch is the storage/search engine in the ELK architecture taught by the source."
                ),
            },

            {
                "id": "M07.L01.Q07",

                "section_id": "centralized-logging",

                "question": (
                    "What is Logstash's main role in the chapter?"
                ),

                "options": [
                    "Ingest and transform data before sending it to Elasticsearch",
                    "Display Grafana dashboards",
                    "Run distributed traces",
                    "Replace Docker Compose",
                ],

                "correct": 0,

                "explanation": (
                    "Logstash is the ingestion and processing pipeline in the ELK flow."
                ),
            },

            {
                "id": "M07.L01.Q08",

                "section_id": "prometheus-grafana",

                "question": (
                    "What does Prometheus mean by scraping a target?"
                ),

                "options": [
                    "Deleting old logs",
                    "Periodically requesting exposed metric values from a configured endpoint",
                    "Restarting a container",
                    "Rendering a Grafana dashboard image",
                ],

                "correct": 1,

                "explanation": (
                    "Prometheus uses a pull model and periodically retrieves metrics from configured targets."
                ),
            },

            {
                "id": "M07.L01.Q09",

                "section_id": "prometheus-grafana",

                "question": (
                    "What is Grafana's primary role in the source architecture?"
                ),

                "options": [
                    "Collect metrics directly from every application",
                    "Visualize/query metrics from a data source such as Prometheus",
                    "Replace Alertmanager",
                    "Store Docker images",
                ],

                "correct": 1,

                "explanation": (
                    "Prometheus collects/stores the metrics; Grafana is used to query and visualize them."
                ),
            },

            {
                "id": "M07.L01.Q10",

                "section_id": "alerting",

                "question": (
                    "What does `for: 1m` mean in the source's Prometheus alert rule?"
                ),

                "options": [
                    "The alert is deleted after one minute",
                    "The condition must remain true for one minute before the alert fires",
                    "Prometheus scrapes only once per minute",
                    "Alertmanager waits one minute before starting",
                ],

                "correct": 1,

                "explanation": (
                    "The rule requires the condition to persist continuously for the specified duration."
                ),
            },

            {
                "id": "M07.L01.Q11",

                "section_id": "alerting",

                "question": (
                    "What inconsistency exists in the source's example alert rule?"
                ),

                "options": [
                    "It uses Grafana syntax inside a Dockerfile",
                    "It is named HighErrorRate but its expression and summary describe request latency",
                    "It has no expression at all",
                    "It sends logs directly to Jaeger",
                ],

                "correct": 1,

                "explanation": (
                    "The rule name refers to error rate, while the metric expression and summary are latency-related."
                ),
            },

            {
                "id": "M07.L01.Q12",

                "section_id": "alerting",

                "question": (
                    "What does Alertmanager add after Prometheus generates an alert?"
                ),

                "options": [
                    "Container image builds",
                    "Grouping, deduplication, and routing to notification receivers",
                    "Kubernetes scheduling",
                    "Git commit history",
                ],

                "correct": 1,

                "explanation": (
                    "The source describes Alertmanager as handling grouping, deduplication, and notification routing."
                ),
            },

            {
                "id": "M07.L01.Q13",

                "section_id": "incident-workflow",

                "type": "open",

                "question": (
                    "A checkout API suddenly becomes slow and starts returning errors. Describe an investigation "
                    "using metrics, Alertmanager, distributed traces, and centralized logs. Explain what each signal "
                    "contributes and how the evidence can lead to remediation and a future observability improvement."
                ),
            },
        ],

        "passing_score": 70,
    },
}
