"""M08.L02 — SSH, Server Tooling, GitHub, Python, and First Streamlit Deployment.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
BOOK-XXX, Chapter 2, page numbers not provided in the supplied chapter export.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel

LESSON_CODE = "M08.L02"
MODULE_ORDER = 8
MODULE_TITLE = "Secure AWS Deployment Foundations"
MODULE_DESCRIPTION = "Prepare the EC2 host as a practical development and deployment server."
SOURCE_CHAPTER = 2
SOURCE_PAGES = "Page numbers not provided in supplied chapter export"

TOPIC = {
    "title": "SSH, Server Tooling, GitHub, Python, and First Streamlit Deployment",
    "slug": "ssh-server-tooling-streamlit-m08-l02",
    "description": (
        "Connect securely to the EC2 instance with SSH and VS Code, install Docker and Docker Compose, "
        "configure GitHub SSH access, install Python with a virtual environment, and validate the server "
        "by running a simple Streamlit application."
    ),
    "order": 2,
    "difficulty": DifficultyLevel.beginner,
    "estimated_hours": 3.0,
    "skill_tags": ["ssh", "vscode", "docker", "docker-compose", "github", "python", "venv", "streamlit", "ec2"],
    "prerequisite_ids": ["M08.L01"],

    "lesson": {
        "title": "SSH, Server Tooling, GitHub, Python, and First Streamlit Deployment",
        "content": r"""
# SSH, Server Tooling, GitHub, Python, and First Streamlit Deployment

> **Course:** Secure AWS Deployment Foundations  
> **Lesson:** M08.L02  
> **Source alignment:** BOOK-XXX, Chapter 2. This lesson preserves the source's Amazon Linux, VS Code, Docker, GitHub, Python 3.9.9, and Streamlit workflow. Obvious pasted-text formatting defects are explicitly noted instead of silently treated as exact shell syntax.

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Explain the anatomy of an SSH command using an EC2 private key.
- Configure VS Code Remote - SSH around an SSH config entry.
- Explain why port 22 must be permitted from the trusted source.
- Install and verify Docker on the Amazon Linux EC2 host using the source's workflow.
- Explain `systemctl start`, `enable`, and `status`.
- Install and verify the Docker Compose plugin using the source's directory layout.
- Generate and register an ED25519 SSH key for GitHub.
- Explain the distinction between the EC2 SSH key and the GitHub SSH key.
- Explain Linux permission numbers such as `700`.
- Clone the book repository and create a development branch.
- Explain why Python virtual environments prevent dependency conflicts.
- Install/activate the source's Python environment.
- Run a Streamlit test application and access it on port 8501.

---

## 1. SSH into the EC2 instance

The source's direct SSH form is:

```bash
ssh -i /path_to_private_key/private_key.pem ec2-user@PUBLIC_IP
```

This command contains three important pieces.

### `-i`

```bash
-i /path/to/private_key.pem
```

tells SSH which private key to use.

### `ec2-user`

For the Amazon Linux AMI in the source, the Linux username is:

```text
ec2-user
```

This is **not** the AWS IAM user.

It is a user account inside the EC2 Linux operating system.

### Public IP

The destination is the instance's public/Elastic IP.

So the connection model is:

```text
local computer
   ↓ private key proves identity
SSH over TCP 22
   ↓
security group allows trusted source
   ↓
Amazon Linux EC2
   ↓
ec2-user shell
```

[[IMAGE_NEEDED: EC2 SSH connection anatomy | A diagram showing local computer + private PEM key → TCP 22 security-group rule → EC2 Elastic IP → Amazon Linux ec2-user shell | Learner should notice the separate roles of private key, network rule, public address, and Linux username]]

---

## 2. Use VS Code Remote - SSH for a richer remote workflow

The source prefers VS Code Remote - SSH over repeatedly typing long SSH commands.

It creates an SSH configuration entry conceptually like:

```text
Host lb-ec2-mywebserver
HostName <EC2_PUBLIC_IP>
IdentityFile ~/Documents/config/my-web-server-key-pair.pem
User ec2-user
```

Then VS Code's Remote - SSH extension can connect using the alias:

```text
lb-ec2-mywebserver
```

### Why this is useful

A remote VS Code session gives you:

- terminal access,
- remote file explorer,
- editor support,
- syntax highlighting.

This changes the server from "a shell you occasionally SSH into" into a manageable remote development environment.

### Network prerequisite

The chapter reminds you that the security group must allow:

```text
TCP 22
```

from your trusted IP or VPN.

Without network permission, correct SSH keys are not enough.

---

## 3. Install Docker and make it survive instance restarts

The source installs Docker with Amazon Linux package tooling.

It begins with:

```bash
sudo yum install docker -y
docker --version
```

Then it also shows adding Docker's official repository and installing `docker-ce`.

The key learning goal is less about memorizing one package-manager sequence and more about understanding the service lifecycle.

### Start Docker

```bash
sudo systemctl start docker
```

Starts Docker now.

### Enable Docker

```bash
sudo systemctl enable docker
```

Configures Docker to start automatically when the EC2 instance boots.

This matters because the source expects the server to continue supporting applications after shutdown/restart cycles.

### Check status

```bash
sudo systemctl status docker
```

Answers:

> Is the service currently running?

### Inspect Docker

```bash
sudo docker info
```

provides system-wide Docker information.

### Important distinction

```text
start
→ current runtime state

enable
→ boot-time behavior
```

A service can be:

```text
running now
but not enabled for next boot
```

That distinction is important for server operations.

{{exercise:M08.L02.EX01}}

---

## 4. Install Docker Compose using the source's plugin path

The source manually downloads a Docker Compose binary into:

```text
$HOME/.docker/cli-plugins/
```

Its sequence is conceptually:

```bash
DOCKER_CONFIG=${DOCKER_CONFIG:-$HOME/.docker}
mkdir -p $DOCKER_CONFIG/cli-plugins

curl -SL <compose-binary-url> \
  -o $DOCKER_CONFIG/cli-plugins/docker-compose

chmod +x $DOCKER_CONFIG/cli-plugins/docker-compose
```

Then it modifies shell path/alias configuration and creates a symlink so the command is available through `sudo`.

Finally:

```bash
docker-compose --version
```

verifies installation.

### Source-era command style

This chapter uses the hyphenated form:

```text
docker-compose
```

because that is how the supplied source is written.

Earlier course material introduced the modern plugin spelling:

```text
docker compose
```

Do not mix these mentally:

- the source chapter demonstrates `docker-compose`,
- modern installations may expose Compose through `docker compose`.

This lesson stays faithful to the supplied source.

---

## 5. Configure GitHub access from the EC2 server

The EC2 server needs to clone and update source code.

The source configures GitHub using a new ED25519 SSH key.

### Generate the key

```bash
ssh-keygen -t ed25519 -C "your_email@gmail.com"
```

This creates:

```text
~/.ssh/id_ed25519
~/.ssh/id_ed25519.pub
```

### Private versus public

```text
id_ed25519
→ private key
→ keep on the EC2 server

id_ed25519.pub
→ public key
→ copy to GitHub
```

### SSH agent

The source uses:

```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

so the private key is available to the SSH client.

### SSH config

The source adds an entry conceptually like:

```text
Host *.github.com
AddKeysToAgent yes
IdentityFile ~/.ssh/id_ed25519
```

### Add the public key to GitHub

Display it:

```bash
cat ~/.ssh/id_ed25519.pub
```

Then add that public value under GitHub's SSH key settings.

For a corporate GitHub account, the source notes that SSO authorization may also be required.

### Test

```bash
ssh -T git@github.com
```

checks whether GitHub recognizes the key.

### EC2 SSH key versus GitHub SSH key

These are two different trust relationships.

```text
Local computer → EC2
uses the EC2 .pem private key

EC2 → GitHub
uses the ED25519 key generated on EC2
```

[[IMAGE_NEEDED: Two SSH trust relationships | A split diagram showing Local Laptop → EC2 using the downloaded EC2 PEM key, and EC2 → GitHub using the EC2-generated ED25519 key whose public half is registered in GitHub | Learner should notice these are separate key pairs for separate connections]]

### Permission notation

The pasted source shows commands such as:

```text
chmod 700.ssh/
chmod 400.ssh/config
```

which appear to be missing spaces in the pasted text.

The intended Linux command structure is:

```text
chmod MODE PATH
```

The source then explains the permission arithmetic:

```text
read    = 4
write   = 2
execute = 1
```

and:

```text
7 = 4 + 2 + 1
```

So:

```text
700
```

means:

```text
user   = read + write + execute
group  = no permissions
others = no permissions
```

---

## 6. Clone the project and work on a secondary branch

The source verifies Git:

```bash
git version
```

and installs it if needed with:

```bash
sudo yum install git -y
```

Then it creates a project directory and clones the companion repository through SSH:

```bash
mkdir -p ~/Documents/GitHub
cd ~/Documents/GitHub

git clone git@github.com:lucasbraga461/deploy-secure-ds-apps-book.git
```

### `.gitignore`

The source instructs the learner to create/use a `.gitignore` so local files that should not be committed stay out of the main branch.

### Development branch

Instead of working directly on `main`, the source creates:

```bash
git checkout -b first_commits
```

This reinforces the Git workflow learned earlier:

```text
main
  \
   first_commits
        ↓
   development
        ↓
   pull request
        ↓
      main
```

---

## 7. Install Python and isolate dependencies with a virtual environment

The source installs Python 3.9.9 from source on the EC2 machine.

Its sequence includes:

```bash
wget
tar
./configure
make
make altinstall
```

and verifies with:

```bash
python3.9 --version
```

### Source formatting warning

The pasted chapter contains visible typography/spacing problems in some shell snippets, including the Python alias line.

For example, it shows variants resembling:

```text
alias python=’usr/bin/python3.9’
```

The educational intent is:

> make the Python 3.9 executable conveniently accessible from the shell.

Treat the book repository/code bundle as the source of exact runnable syntax.

### Why virtual environments?

A virtual environment isolates project dependencies.

Without one:

```text
Project A wants package X v1
Project B wants package X v2
```

Global installation can create conflict.

With virtual environments:

```text
Project A venv
└── X v1

Project B venv
└── X v2
```

### Source environment

The chapter creates:

```bash
python -m venv venv-webs
source venv-webs/bin/activate
```

Once activated, `pip install` targets that project environment.

{{exercise:M08.L02.EX02}}

---

## 8. Validate the server by running Streamlit

The chapter uses Streamlit as a simple validation application.

Install it inside the virtual environment:

```bash
pip install streamlit
```

The source's sample application conceptually contains:

```python
import streamlit as st

def main():
    st.title("Streamlit App running ec2 via port 8501")
    st.write("Test successful!")

if __name__ == "__main__":
    main()
```

Then run:

```bash
streamlit run st_example.py
```

### What this test proves

If you can visit:

```text
ELASTIC_IP:8501
```

and see the application, several layers are working:

```text
EC2 is running
        +
SSH/server setup succeeded
        +
Python environment works
        +
Streamlit is installed
        +
application process is listening
        +
security group permits 8501
        +
public addressing is reachable
```

This is why small validation apps are useful during infrastructure setup.

[[IMAGE_NEEDED: First direct EC2 application access | A flow showing browser → EC2 Elastic IP:8501 → security group → Streamlit process running inside the Python virtual environment | Learner should notice this is direct instance exposure before the later load-balancer layer]]

{{exercise:M08.L02.EX03}}

---

## Important misconceptions

### Misconception 1
> "The IAM developer username and `ec2-user` are the same identity."

They live at different layers: AWS identity versus Linux operating-system identity.

### Misconception 2
> "If Docker is running now, it will automatically run after every reboot."

Not unless its service is enabled for startup.

### Misconception 3
> "The EC2 `.pem` key should be uploaded to GitHub."

No. The source creates a separate GitHub SSH key pair on the EC2 host.

### Misconception 4
> "Virtual environments are only for multiple Python versions."

Their main purpose here is dependency isolation.

### Misconception 5
> "Seeing the Streamlit page tests only Streamlit."

It validates several infrastructure layers simultaneously.

---

## Key terminology

| Term | Meaning |
|---|---|
| SSH | Secure remote shell protocol |
| `ec2-user` | Default Linux account used by the source's Amazon Linux instance |
| VS Code Remote - SSH | Extension/workflow for editing and operating a remote machine |
| `systemctl start` | Start a service now |
| `systemctl enable` | Configure service to start at boot |
| Docker Compose | Multi-container tooling installed by the source |
| ED25519 | Key type used for the source's GitHub SSH key |
| SSH agent | Process that holds private keys for SSH authentication |
| `chmod` | Linux command for changing permissions |
| Virtual environment | Isolated Python package environment |
| Streamlit | Python framework used for the source's validation app |

---

## Self-check

1. What does `-i` mean in the SSH command?
2. What is `ec2-user`?
3. Why must port 22 be open from the trusted source?
4. Why does the source use VS Code Remote - SSH?
5. What is the difference between starting and enabling Docker?
6. Why verify `docker --version` and `docker-compose --version`?
7. Why does the source generate a second SSH key pair for GitHub?
8. What does `700` mean in Linux permission arithmetic?
9. Why create `first_commits` instead of editing main directly?
10. Why create `venv-webs`?
11. What does the Streamlit test prove about the environment?

---

## Retain this idea

**A deployment server is more than an EC2 instance: it needs secure remote access, reproducible tooling, source-control access, isolated application dependencies, and a small end-to-end validation that proves the whole path works.**
""",
        "estimated_minutes": 180,
        "has_code_examples": True,
        "has_manual_image_requests": True,
        "sections": [
            {"id": "ssh-basics", "title": "SSH into the EC2 instance", "order": 1},
            {"id": "vscode-remote", "title": "Use VS Code Remote - SSH for a richer remote workflow", "order": 2},
            {"id": "docker-install", "title": "Install Docker and make it survive instance restarts", "order": 3},
            {"id": "compose-install", "title": "Install Docker Compose using the source's plugin path", "order": 4},
            {"id": "github-ssh", "title": "Configure GitHub access from the EC2 server", "order": 5},
            {"id": "git-clone", "title": "Clone the project and work on a secondary branch", "order": 6},
            {"id": "python-venv", "title": "Install Python and isolate dependencies with a virtual environment", "order": 7},
            {"id": "streamlit-validation", "title": "Validate the server by running Streamlit", "order": 8},
        ],
    },

    "exercises": [
        {
            "id": "M08.L02.EX01",
            "title": "Explain the Docker Service Lifecycle",
            "lesson_code": "M08.L02",
            "section_id": "docker-install",
            "placement": "after_section",
            "description": "Distinguish install, start, enable, status, and inspect operations.",
            "instructions": (
                ('1. For each command in the source—docker --version, systemctl start docker, systemctl enable docker, systemctl status docker, and docker info—write what question it answers.\n'
                 "2. Then explain the difference between 'running now' and 'starts automatically after reboot'.")
            ),
            "expected_output": "A five-row command-purpose table and a boot-lifecycle explanation.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["docker", "systemd", "server-operations"],
        },
        {
            "id": "M08.L02.EX02",
            "title": "Map the Two SSH Key Pairs",
            "lesson_code": "M08.L02",
            "section_id": "github-ssh",
            "placement": "after_section",
            "description": "Separate EC2 access credentials from GitHub credentials.",
            "instructions": (
                ('1. Draw two connections: Local computer → EC2 and EC2 → GitHub.\n'
                 '2. For each, identify the private key, public-key destination, username/host, and what would fail if the wrong key were used.')
            ),
            "expected_output": "A two-connection SSH trust diagram.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["ssh", "github", "ec2", "key-management"],
        },
        {
            "id": "M08.L02.EX03",
            "title": "Validate the Direct Streamlit Deployment",
            "lesson_code": "M08.L02",
            "section_id": "streamlit-validation",
            "placement": "after_section",
            "description": "Use the source's test app to reason about every layer that must work.",
            "instructions": (
                ('1. Run through the deployment mentally or in your lab.\n'
                 '2. List every dependency between typing `streamlit run st_example.py` and seeing the page at the Elastic IP on port 8501.\n'
                 '3. Include process, port, security group, addressing, and Python environment.')
            ),
            "expected_output": "An end-to-end dependency chain from process startup to browser response.",
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["streamlit", "ec2", "security-groups", "debugging"],
        },
    ],

    "quiz": {
        "id": "M08.L02.QZ01",
        "title": "SSH, Server Tooling, GitHub, Python, and Streamlit — Knowledge Check",
        "lesson_code": "M08.L02",
        "placement": "lesson_end",
        "questions": [
            {"id": "M08.L02.Q01", "section_id": "ssh-basics", "question": "What does `-i` select in the source SSH command?", "options": ["IAM policy", "Private identity key", "EC2 instance type", "Streamlit port"], "correct": 1, "explanation": "The `-i` option points SSH to the EC2 private key file."},
            {"id": "M08.L02.Q02", "section_id": "vscode-remote", "question": "What does the SSH Host alias simplify?", "options": ["AWS billing", "Repeated connection parameters", "Docker builds", "IAM group creation"], "correct": 1, "explanation": "The alias stores host, key, and user details for easier connection."},
            {"id": "M08.L02.Q03", "section_id": "docker-install", "question": "Which command configures Docker to start on boot?", "options": ["systemctl start docker", "systemctl enable docker", "docker info", "docker --version"], "correct": 1, "explanation": "`enable` configures boot-time startup."},
            {"id": "M08.L02.Q04", "section_id": "github-ssh", "question": "Which key is copied into GitHub settings?", "options": ["The private ED25519 key", "The public ED25519 key", "The EC2 private PEM key", "The IAM access key"], "correct": 1, "explanation": "The public key is registered with GitHub; the private key remains on the EC2 host."},
            {"id": "M08.L02.Q05", "section_id": "github-ssh", "question": "What does permission value 7 mean?", "options": ["Read only", "Read+write", "Read+write+execute", "No permissions"], "correct": 2, "explanation": "7 is 4+2+1."},
            {"id": "M08.L02.Q06", "section_id": "git-clone", "question": "Why does the source create `first_commits`?", "options": ["To avoid changing main directly", "To store Docker images", "To replace IAM", "To host Streamlit"], "correct": 0, "explanation": "The branch supports a pull-request development workflow."},
            {"id": "M08.L02.Q07", "section_id": "python-venv", "question": "What is the primary purpose of the virtual environment?", "options": ["Public IP stability", "Dependency isolation", "SSL validation", "Load balancing"], "correct": 1, "explanation": "The source creates it to keep Python project dependencies isolated."},
            {"id": "M08.L02.Q08", "section_id": "streamlit-validation", "question": "Which port does the source's Streamlit app use?", "options": ["22", "80", "8501", "8504"], "correct": 2, "explanation": "The test Streamlit application runs on 8501."},
            {"id": "M08.L02.Q09", "section_id": "streamlit-validation", "question": "What network component must permit port 8501 for direct access?", "options": ["Git branch", "Security group", "Python venv", "SSH agent"], "correct": 1, "explanation": "The EC2 security group controls inbound reachability."},
            {"id": "M08.L02.Q10", "section_id": "streamlit-validation", "type": "open", "question": "Explain the complete path from your browser to the running Streamlit process on the EC2 instance."},
        ],
        "passing_score": 70,
    },
}
