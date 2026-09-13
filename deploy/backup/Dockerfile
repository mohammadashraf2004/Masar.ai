# deploy/backup/Dockerfile
#
# postgres:16 (Debian, not -alpine — see pg-backup.sh's own comment on why:
# alpine ships libssl but not the openssl CLI) plus the AWS CLI v2, needed
# only by this one service for the off-host backup copy. Kept out of the
# api/frontend images entirely: neither of those touches backup storage or
# its credentials, and this is the one place in the repo that legitimately
# needs an AWS SDK/CLI dependency.
FROM postgres:16

# Official static installer (not pip/apt) — self-contained, no Python
# dependency pulled into an image that otherwise has none, and it is the
# method AWS documents for exactly this (a container base with no package
# for it). curl + unzip are build-time only and removed again below; the
# installed CLI itself has no further runtime dependency on either.
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl unzip ca-certificates \
    && curl -fsS "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o /tmp/awscliv2.zip \
    && unzip -q /tmp/awscliv2.zip -d /tmp \
    && /tmp/aws/install \
    && rm -rf /tmp/awscliv2.zip /tmp/aws \
    && apt-get purge -y curl unzip \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

# Baked in rather than bind-mounted: this service now has its own image to
# build (it didn't before — it used the bare postgres:16 image), so the
# script lives with it the same way backend/app and frontend/src do in
# their own Dockerfiles. Deploying a script change means `--build`, exactly
# like every other code change in this repo's documented deploy command.
COPY pg-backup.sh /usr/local/bin/pg-backup.sh
RUN chmod +x /usr/local/bin/pg-backup.sh

# Non-root — matches backend/Dockerfile (appuser) and frontend/Dockerfile
# (nextjs). The official postgres:16 entrypoint drops root via gosu
# internally *after* running as root for data-directory initialization;
# replacing that entrypoint with pg-backup.sh (below) skips that drop
# entirely; unnoticed until checked directly (`docker run --entrypoint id`
# showed uid=0) — this container talks to Postgres over the network only,
# never touches a local data directory, and needs no root privilege at
# any point, so there is no equivalent step to preserve here.
#
# Reuses the `postgres` user this base image already ships (uid 999) —
# no new user needed, and it sidesteps a real collision: Debian's own
# base image already reserves the name `backup` (uid 34, for
# /var/backups), so `useradd backup` fails outright.
#
# The backup volume's ownership has to be set BEFORE `USER` switches away
# from root: `/backups` doesn't exist in the base image, so Docker
# initializes docker-compose.prod.yml's named `backup_data` volume by
# copying this directory (permissions included) into it on first mount —
# get the ownership right here once, or every write after the USER switch
# fails against a volume Docker created as root:root.
RUN mkdir -p /backups && chown -R postgres:postgres /backups
USER postgres

ENTRYPOINT ["/bin/sh", "/usr/local/bin/pg-backup.sh"]
