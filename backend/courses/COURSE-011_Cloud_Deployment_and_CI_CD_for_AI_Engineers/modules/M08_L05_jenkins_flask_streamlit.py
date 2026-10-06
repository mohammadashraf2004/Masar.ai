"""M08.L05 — Deploying More Robust Applications: Jenkins, Flask, and Streamlit.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
BOOK-XXX, Chapter 5, page numbers not provided in the supplied chapter export.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel

LESSON_CODE = "M08.L05"
MODULE_ORDER = 8
MODULE_TITLE = "Secure Cloud Deployment Foundations"
MODULE_DESCRIPTION = (
    "Extend the AWS deployment into a multi-application environment containing Streamlit, "
    "Jenkins, and an authenticated Flask prediction API backed by a trained machine-learning model."
)
SOURCE_CHAPTER = 5
SOURCE_PAGES = "Page numbers not provided in supplied chapter export"

TOPIC = {
    "title": "Deploying More Robust Applications: Jenkins, Flask, and Streamlit",
    "slug": "jenkins-flask-streamlit-deployment-m08-l05",
    "description": (
        "Build a richer multi-service deployment by persisting Jenkins state, managing Linux permissions, "
        "training and serializing a Random Forest model, serving predictions through Flask, and exposing "
        "Jenkins, Flask, and Streamlit through Docker Compose and Nginx."
    ),
    "order": 5,
    "difficulty": DifficultyLevel.beginner,
    "estimated_hours": 4.0,
    "skill_tags": [
        "jenkins", "flask", "streamlit", "docker-compose", "nginx", "linux-permissions",
        "jupyter", "scikit-learn", "random-forest", "pickle", "api-authentication", "module-08"
    ],
    "prerequisite_ids": ["M08.L04"],

    "lesson": {
        "title": "Deploying More Robust Applications: Jenkins, Flask, and Streamlit",
        "content": r"""
# Deploying More Robust Applications: Jenkins, Flask, and Streamlit

> **Course:** Secure Cloud Deployment Foundations  
> **Lesson:** M08.L05  
> **Source alignment:** BOOK-XXX, Chapter 5. The lesson preserves the source's Jenkins, Flask, Streamlit, Docker Compose, Nginx, model-training, and authentication workflow. Source formatting glitches are called out rather than silently treated as exact commands.

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Explain why Jenkins state must be persisted outside the container.
- Explain the purpose of the `jenkins_shared` Linux group in the source.
- Understand why the Jenkins UID/GID values are exported through `.env`.
- Trace HTTPS traffic on port 8504 through Nginx to Jenkins on internal port 8080.
- Complete the source's initial Jenkins setup flow.
- Explain why enabling Docker at boot matters for an EC2-hosted deployment.
- Configure VS Code/Jupyter to use the project virtual environment.
- Reproduce the source's synthetic binary-classification training workflow.
- Explain train/test split, Random Forest fitting, and evaluation with accuracy, precision, recall, and classification report.
- Save and reload the trained model with `pickle`.
- Convert an API payload into model input and return a prediction score.
- Explain GET versus POST requests in the source's Flask workflow.
- Interpret common HTTP status codes.
- Explain the source's Flask authentication-file structure.
- Deploy Streamlit, Flask, Jenkins, and Nginx together with Docker Compose.
- Send authenticated GET and POST requests to the deployed Flask API.

---

## 1. From one application to a multi-service server

The previous AWS lessons established:

```text
EC2
+
Docker
+
Nginx
+
TLS certificate
+
Streamlit
```

Chapter 5 adds two major services:

```text
Jenkins
Flask prediction API
```

The final learning architecture becomes:

```text
               Nginx
            /    |    \
           /     |     \
   Streamlit   Flask   Jenkins
     :8501     :8502    :8080 internal
```

Externally, the source still exposes application-specific secure ports through Nginx:

```text
Streamlit → 8501
Flask     → 8502
Jenkins   → 8504
```

Jenkins itself runs internally on:

```text
8080
```

and Nginx proxies:

```text
8504 → jenkins:8080
```

[[IMAGE_NEEDED: Chapter 5 multi-service architecture | A diagram showing Nginx with TLS in front of three Docker services: Streamlit on internal 8501, Flask on 8502, and Jenkins on 8080, with external secure ports 8501, 8502, and 8504 | Learner should notice that the external Jenkins port differs from the internal Jenkins port]]

---

## 2. Jenkins needs persistent state

Jenkins is not a disposable stateless service.

During initial setup it creates:

- configuration,
- plugins,
- users,
- job state,
- secrets.

If all of that lives only inside a container filesystem, removing the container can remove the Jenkins state.

The source therefore maps a host directory into the Jenkins container.

Conceptually:

```text
EC2 host
jenkins/var/jenkins_home
        ⇅
Jenkins container
/var/jenkins_home
```

This is a persistent Docker volume/bind-mount pattern.

### Why this matters

Container:

```text
can be rebuilt/recreated
```

Jenkins data:

```text
must survive
```

That separation is a core container operations concept.

### Linux ownership problem

The host directory must be writable by the user running Jenkins inside the container.

The source solves this by creating a shared group:

```text
jenkins_shared
```

and adding several users:

```text
ec2-user
docker
jenkins
nginx
```

to that group.

It then changes ownership and permissions on:

```text
jenkins/var/jenkins_home
```

### `.env` UID/GID handoff

The source writes:

```text
JENKINS_UID=<jenkins user id>
JENKINS_GID=<jenkins group id>
```

into `.env`.

Docker Compose then uses:

```yaml
user: "${JENKINS_UID}:${JENKINS_GID}"
```

The important idea is:

> The container process uses a user/group identity that matches the host-side permissions expected by the persistent Jenkins directory.

[[IMAGE_NEEDED: Jenkins persistent volume and UID/GID mapping | A diagram showing the EC2 host Jenkins directory owned for the shared group, mounted into `/var/jenkins_home`, with Docker Compose passing Jenkins UID and GID from `.env` | Learner should notice how host permissions and container identity must align]]

{{exercise:M08.L05.EX01}}

---

## 3. Add Jenkins to Docker Compose and Nginx

The source's Docker Compose configuration includes:

```text
streamlit_calc
jenkins
nginx
```

while Flask is temporarily commented out during the first Jenkins setup.

### Jenkins Compose details

The source uses:

```yaml
ports:
  - "8080"
```

inside the Jenkins service.

It also mounts:

```text
jenkins/.aws
jenkins/var/jenkins_home
streamlit_calc/data
```

according to its project structure.

### Nginx exposes Jenkins on 8504

The source's Nginx server block listens with TLS on:

```text
8504
```

and forwards traffic to:

```nginx
proxy_pass http://jenkins:8080;
```

This demonstrates reverse-proxy port translation:

```text
Browser
https://domain:8504
      ↓
Nginx :8504
      ↓
Jenkins container :8080
```

### Why Nginx uses the service name

Inside a Compose network, services can address each other by their Compose service names.

So:

```text
jenkins
```

acts as the internal host name in:

```text
http://jenkins:8080
```

---

## 4. Perform the initial Jenkins setup

After starting the Compose stack:

```bash
docker-compose up -d --build
```

the source opens Jenkins at:

```text
https://<your-domain>:8504/
```

### Initial admin password

The source retrieves it from the persisted Jenkins home:

```text
jenkins/var/jenkins_home/secrets/initialAdminPassword
```

This is another demonstration of why persistent Jenkins storage matters.

### Setup sequence

The source then performs:

1. unlock Jenkins with the initial password,
2. install suggested plugins,
3. create the first admin user,
4. configure the Jenkins URL,
5. start using Jenkins.

The source later changes this URL again in Chapter 6 when moving from:

```text
https://domain:8504/
```

to a dedicated Jenkins subdomain.

---

## 5. Make Docker start automatically after EC2 reboots

The source repeats an operational requirement:

```bash
sudo systemctl enable docker
sudo systemctl status docker
```

Why?

Because a cloud VM may be:

```text
stopped
→ restarted later
```

If Docker does not start at boot, the application stack will not be available until an engineer connects and manually starts Docker.

This is infrastructure lifecycle thinking:

```text
application availability
depends on
service startup behavior
```

---

## 6. Prepare VS Code and Jupyter for model training

Before building the Flask prediction API, the source trains a model in:

```text
model_training.ipynb
```

using VS Code.

### Source setup flow

The source instructs the learner to:

- open the notebook,
- install/enable suggested notebook extensions,
- install Microsoft's Jupyter extension in the remote SSH environment,
- install Microsoft's Python extension,
- choose the project's virtual environment as the notebook kernel,
- install `ipykernel` if requested,
- install `scikit-learn`.

The important mental model is:

```text
Notebook kernel
        =
Python environment that executes notebook cells
```

If the notebook uses the wrong environment, imports installed in:

```text
venv-webs
```

may not be available.

### Activate the project environment

The source uses:

```bash
cd ~/Documents/GitHub/deploy-secure-ds-apps-book
source venv-webs/bin/activate
pip install scikit-learn
```

---

## 7. Train a Random Forest classification model

The source's ML example is intentionally simple.

It creates a synthetic binary-classification dataset using:

```python
make_classification
```

with:

```text
1,000 samples
4 input features
4 informative features
0 redundant features
2 classes
balanced class weights
random_state=42
```

### Dataset shape

The resulting DataFrame contains:

```text
4 predictors
+
1 target
=
5 columns
```

### Split the data

The source uses:

```python
train_test_split(..., test_size=0.2, random_state=42)
```

which produces:

```text
80% training
20% validation/test
```

### Train the model

The source fits:

```python
RandomForestClassifier(random_state=42)
```

on the training set.

### Evaluate

It computes:

```text
accuracy
precision
recall
classification report
```

The figure in the source reports example values around:

```text
accuracy  = 0.90
precision = 0.92
recall    = 0.89
```

These are results from the source's example run, not universal expected values.

### Why separate validation data?

The source evaluates on unseen rows rather than measuring only training fit.

The learning goal is:

> Evaluate the model on data that was not used to fit it.

[[IMAGE_NEEDED: Model training flow | A flow diagram showing synthetic data → DataFrame → 80/20 split → RandomForest training on training set → predictions on validation set → accuracy/precision/recall/classification report | Learner should notice the separation between model fitting and evaluation]]

{{exercise:M08.L05.EX02}}

---

## 8. Save the model so the API can reuse it

Retraining on every API request would be wasteful.

The source serializes the fitted model with:

```python
pickle.dump(...)
```

to a file under:

```text
flask/models/random_forest_model.pkl
```

Then it demonstrates reloading with:

```python
pickle.load(...)
```

The purpose is:

```text
train once
   ↓
save model object
   ↓
Flask loads model
   ↓
API serves predictions
```

### Convert a payload to model input

The source creates a payload such as:

```python
{
    "Feature_1": 1.0,
    "Feature_2": 1.0,
    "Feature_3": 1.0,
    "Feature_4": 1.0
}
```

Then converts values into:

```text
shape (1, 4)
```

for model prediction.

### Prediction score

The source calls:

```python
predict_proba
```

and selects the class with the highest probability using:

```python
argmax
```

Then it returns the confidence for that predicted class as:

```text
predicted_score
```

The source notes a default binary threshold idea around `0.5` and mentions that thresholds can be optimized for a specific use case.

---

## 9. Test the Flask API locally before container deployment

The source runs:

```bash
cd ~/Documents/GitHub/deploy-secure-ds-apps-book/flask
source venv-webs/bin/activate
python app.py
```

and serves locally on:

```text
localhost:8502
```

### GET request

The source first sends:

```text
GET /
```

and expects a successful HTTP response.

### POST request

Then it sends JSON to:

```text
POST /predict
```

A source example response is:

```json
{
  "model_name": "random_forest_model",
  "score": 0.77
}
```

### Request versus payload

The chapter explicitly distinguishes:

```text
HTTP request
= method + headers + metadata + body

payload
= actual body data sent to the API
```

That is an important API concept.

### Common HTTP codes from the source

| Code | Meaning in source |
|---:|---|
| 200 | OK |
| 201 | Created |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 500 | Internal Server Error |

---

## 10. Add authentication configuration and deployment folders

Before Docker deployment, the source creates:

```text
flask/logs/
flask/config/auth_flask.json
```

The source's authentication-file example is:

```json
{
  "prod": {
    "user": "admin",
    "password": "password"
  }
}
```

This is a source example used to demonstrate authentication mechanics.

The important architectural idea is:

```text
Flask app
loads credentials/config
        ↓
HTTP Basic Authentication
        ↓
authorized requests reach API behavior
```

The source also adjusts permissions so Docker can access the new directories.

### Source formatting warning

One pasted ownership command is visibly malformed:

```text
sudo chown -R:jenkins_shared
```

Treat the repository/code bundle as the authoritative source for exact runnable syntax rather than copying malformed pasted text.

---

## 11. Deploy all applications together

After preparing Flask, the source re-enables it in:

```text
docker-compose.yaml
```

and Nginx.

The final service stack is:

```text
streamlit_calc
flask
jenkins
nginx
```

External URLs in the source are:

```text
Streamlit → https://<your-domain>:8501/
Flask     → https://<your-domain>:8502/
Jenkins   → https://<your-domain>:8504/
```

### Authenticated Flask calls

The source loads credentials from `auth_flask.json` and uses:

```python
HTTPBasicAuth(user, password)
```

with both GET and POST requests.

Authenticated prediction flow:

```text
Client
  ↓ HTTPS + Basic Auth
Nginx
  ↓
Flask
  ↓ validate credentials
prediction payload
  ↓
loaded Random Forest model
  ↓
prediction score
  ↓
JSON response
```

[[IMAGE_NEEDED: Authenticated ML API deployment | A flow showing client with credentials and JSON payload → HTTPS/Nginx → Flask authentication → deserialized Random Forest model → prediction score → JSON response | Learner should notice where authentication occurs relative to prediction logic]]

{{exercise:M08.L05.EX03}}

---

## Important misconceptions

### Misconception 1
> "Jenkins can be recreated freely without persistent storage."

Its configuration and plugin state live under Jenkins home and must persist if you want continuity.

### Misconception 2
> "Port 8504 is Jenkins' internal application port."

In the source, Nginx listens externally on 8504 and proxies to Jenkins internally on 8080.

### Misconception 3
> "The notebook's Python kernel is unrelated to the virtual environment."

The source deliberately selects `venv-webs` as the kernel environment.

### Misconception 4
> "The API payload is the entire HTTP request."

The source explicitly distinguishes the body/payload from the full request.

### Misconception 5
> "A trained model must be retrained every time the Flask app starts."

The source persists it with pickle and reloads it.

---

## Key terminology

| Term | Meaning |
|---|---|
| Jenkins | Automation server deployed by the source |
| Jenkins home | Persistent state directory for Jenkins |
| UID/GID | Linux user/group numeric identities |
| Bind mount | Host directory mounted into a container |
| Jupyter kernel | Python environment executing notebook cells |
| Random Forest | Classification algorithm used in the source |
| Train/test split | Separation between fitting and evaluation data |
| Precision | Fraction of predicted positives that are correct |
| Recall | Fraction of actual positives correctly identified |
| Pickle | Python serialization used by the source to save the model |
| Payload | Request body data |
| HTTP Basic Auth | Authentication method used by the source's Flask API |
| Reverse proxy | Nginx forwarding external traffic to internal services |

---

## Self-check

1. Why is Jenkins home mounted to host storage?
2. Why does the source create `jenkins_shared`?
3. Why are Jenkins UID/GID values written to `.env`?
4. Trace browser port 8504 to internal Jenkins port 8080.
5. Why enable Docker with `systemctl enable`?
6. Why must the notebook use `venv-webs`?
7. Describe the synthetic dataset.
8. Why split into 80% training and 20% evaluation?
9. Which metrics does the source calculate?
10. Why serialize the model with pickle?
11. What is the difference between a GET request and a POST prediction request?
12. What is the difference between a request and its payload?
13. What does HTTP 401 mean in the source's table?
14. What files/directories are created before Flask container deployment?
15. Trace an authenticated POST request from client to model response.

---

## Retain this idea

**A production-style data application is a system of cooperating services: persist stateful tools such as Jenkins, isolate and serialize ML logic, place APIs behind authentication, and use Docker Compose plus Nginx to make the services operate as one deployable stack.**
""",
        "estimated_minutes": 240,
        "has_code_examples": True,
        "has_manual_image_requests": True,
        "sections": [
            {"id": "multi-service", "title": "From one application to a multi-service server", "order": 1},
            {"id": "jenkins-persistence", "title": "Jenkins needs persistent state", "order": 2},
            {"id": "compose-jenkins", "title": "Add Jenkins to Docker Compose and Nginx", "order": 3},
            {"id": "jenkins-setup", "title": "Perform the initial Jenkins setup", "order": 4},
            {"id": "docker-autostart", "title": "Make Docker start automatically after EC2 reboots", "order": 5},
            {"id": "jupyter-setup", "title": "Prepare VS Code and Jupyter for model training", "order": 6},
            {"id": "train-model", "title": "Train a Random Forest classification model", "order": 7},
            {"id": "serialize-model", "title": "Save the model so the API can reuse it", "order": 8},
            {"id": "flask-local", "title": "Test the Flask API locally before container deployment", "order": 9},
            {"id": "flask-auth", "title": "Add authentication configuration and deployment folders", "order": 10},
            {"id": "full-deployment", "title": "Deploy all applications together", "order": 11},
        ],
    },

    "exercises": [
        {
            "id": "M08.L05.EX01",
            "title": "Reason About Jenkins Persistence and Permissions",
            "lesson_code": "M08.L05",
            "section_id": "jenkins-persistence",
            "placement": "after_section",
            "description": "Explain why persistent state and Linux identities must align.",
            "instructions": (
                "Draw the host-to-container Jenkins volume mapping. Identify the shared Linux group, the users placed "
                "in it, the role of `chown`/`chmod`, and how JENKINS_UID/JENKINS_GID from `.env` affect the container."
            ),
            "expected_output": "A permissions/persistence diagram and explanation.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["jenkins", "linux-permissions", "docker-volumes"],
        },
        {
            "id": "M08.L05.EX02",
            "title": "Reconstruct the Model Training Pipeline",
            "lesson_code": "M08.L05",
            "section_id": "train-model",
            "placement": "after_section",
            "description": "Connect dataset generation, splitting, fitting, evaluation, and persistence.",
            "instructions": (
                "Create a flow diagram using the source values: 1,000 rows, four informative features, binary target, "
                "80/20 split, RandomForestClassifier, accuracy/precision/recall, then pickle persistence. "
                "Explain why the validation set is separate from training."
            ),
            "expected_output": "A complete ML pipeline diagram with source-specific settings.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["machine-learning", "random-forest", "evaluation"],
        },
        {
            "id": "M08.L05.EX03",
            "title": "Trace an Authenticated Prediction Request",
            "lesson_code": "M08.L05",
            "section_id": "full-deployment",
            "placement": "after_section",
            "description": "Follow one HTTPS POST request through the deployed system.",
            "instructions": (
                "Starting from a JSON payload with Feature_1..Feature_4, trace Basic Auth, Nginx, Flask, "
                "model loading/input conversion, `predict_proba`, selected score, and the JSON response. "
                "Include where a 401 would occur if credentials were invalid."
            ),
            "expected_output": "An end-to-end prediction request sequence.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["flask", "http", "authentication", "ml-serving"],
        },
    ],

    "quiz": {
        "id": "M08.L05.QZ01",
        "title": "Jenkins, Flask, and Streamlit Deployment — Knowledge Check",
        "lesson_code": "M08.L05",
        "placement": "lesson_end",
        "questions": [
            {"id": "M08.L05.Q01", "section_id": "jenkins-persistence", "question": "Why is Jenkins home mounted to the host?", "options": ["To change DNS", "To preserve Jenkins state across container recreation", "To create an Elastic IP", "To train the model"], "correct": 1, "explanation": "The source explicitly uses the volume so Jenkins data survives container stop/restart."},
            {"id": "M08.L05.Q02", "section_id": "compose-jenkins", "question": "Which internal Jenkins port does Nginx proxy to?", "options": ["80", "443", "8080", "8504"], "correct": 2, "explanation": "The source proxies `jenkins:8080`."},
            {"id": "M08.L05.Q03", "section_id": "jenkins-setup", "question": "Where does the source retrieve the initial Jenkins password?", "options": ["GitHub", "Jenkins home secrets file", "IAM", "DNS"], "correct": 1, "explanation": "It is read from `secrets/initialAdminPassword` under Jenkins home."},
            {"id": "M08.L05.Q04", "section_id": "docker-autostart", "question": "What does `systemctl enable docker` provide?", "options": ["Model serialization", "Docker startup at boot", "SSL validation", "Git authentication"], "correct": 1, "explanation": "It configures Docker to start after EC2 reboot."},
            {"id": "M08.L05.Q05", "section_id": "train-model", "question": "What train/test split does the source use?", "options": ["50/50", "60/40", "80/20", "90/10"], "correct": 2, "explanation": "The source uses `test_size=0.2`."},
            {"id": "M08.L05.Q06", "section_id": "serialize-model", "question": "Why use pickle in the source?", "options": ["To store DNS", "To save and reload the trained model", "To encrypt Nginx traffic", "To create users"], "correct": 1, "explanation": "Pickle persists the fitted Random Forest object."},
            {"id": "M08.L05.Q07", "section_id": "flask-local", "question": "Which endpoint receives prediction payloads?", "options": ["/", "/predict", "/jenkins", "/metrics"], "correct": 1, "explanation": "The source sends POST requests to `/predict`."},
            {"id": "M08.L05.Q08", "section_id": "flask-local", "question": "Which status means Unauthorized in the source table?", "options": ["200", "400", "401", "500"], "correct": 2, "explanation": "401 means authentication is missing or invalid."},
            {"id": "M08.L05.Q09", "section_id": "full-deployment", "question": "Which external source port corresponds to Flask before the subdomain migration?", "options": ["8501", "8502", "8504", "8080"], "correct": 1, "explanation": "The source exposes Flask through 8502."},
            {"id": "M08.L05.Q10", "section_id": "full-deployment", "type": "open", "question": "Explain the complete Chapter 5 architecture, including Jenkins persistence, model training/persistence, Flask authentication, and Nginx routing."},
        ],
        "passing_score": 70,
    },
}
