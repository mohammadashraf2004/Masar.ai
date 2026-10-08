# Project Lab runner: executes learner Python/SQL for the API.
#
# Build context is backend/project_runner/ alone, so the image physically
# cannot contain application code, settings or a .env file. Project
# templates are mounted read-only at /templates at run time rather than baked
# in, so one runner image serves every project.
#
# Runtime contract (docker-compose.yml, `project-runner`): no network at all,
# read-only root filesystem, the custom seccomp profile seccomp.json, every
# capability dropped except SETUID/SETGID, no-new-privileges, and (in
# production, where the host supports it) the gVisor runtime.
FROM python:3.11-slim AS runner

# gid of the API container's `appuser` (backend/Dockerfile: the first user
# created there gets 1000). The socket directory below belongs to this group.
ARG API_GID=1000

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    MPLBACKEND=Agg \
    MASAR_MPL_SEED=/opt/mplcache

COPY requirements.txt /opt/requirements.txt
RUN pip install --no-cache-dir -r /opt/requirements.txt \
    && rm /opt/requirements.txt \
    # Fonts/caches matplotlib would otherwise build on first import, in a
    # read-only filesystem.
    && MPLCONFIGDIR=/opt/mplcache python -c "import matplotlib.pyplot" \
    && chmod -R a+rX /opt/mplcache

# tini as PID 1: processes a job orphans are reparented to PID 1, and a
# Python server there never reaps them. The zombies would count against the
# sandbox user's process limit until no job could start a subprocess.
RUN apt-get update && apt-get install -y --no-install-recommends tini \
    && rm -rf /var/lib/apt/lists/*

# The uid learner code runs as. No home directory, no shell, no sudo.
RUN groupadd --system --gid 10001 sandbox \
    && useradd --system --uid 10001 --gid 10001 --no-create-home --shell /usr/sbin/nologin sandbox

# The API <-> runner control socket lives here, on a named volume shared with
# the API (Docker seeds a new named volume from this directory, ownership and
# mode included). root:API_GID, mode 2750: the API's group can reach the
# socket, the sandbox user cannot even traverse the directory. The setgid bit
# gives the socket the API's group without the service needing CAP_CHOWN.
RUN mkdir -p /run/project-runner \
    && chown root:${API_GID} /run/project-runner \
    && chmod 2750 /run/project-runner

COPY . /opt/runner/project_runner/
WORKDIR /opt/runner

# Starts as root ON PURPOSE: the service hands every job to the `sandbox`
# user, which needs CAP_SETUID/CAP_SETGID (the only capabilities compose
# keeps). Nothing listens on TCP: the API talks to the Unix socket above.
ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["python", "-I", "/opt/runner/project_runner/server.py"]

# ── Not shipped: the image used to derive seccomp.json ──────────────────────
# `docker build --target trace` adds strace; see project_runner/seccomp/README.md.
FROM runner AS trace
RUN apt-get update && apt-get install -y --no-install-recommends strace \
    && rm -rf /var/lib/apt/lists/*

# Default target: the shipped image.
FROM runner
