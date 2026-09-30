# syntax=docker/dockerfile:1
# Base Image: Debian Bookworm, slim variant (no compiler toolchain baked in).
# None of our direct dependencies need to compile from source (psycopg2-binary ships wheels),
# so the full python:3.14-bookworm image's ~1GB of pre-installed build tooling is dead weight.
FROM python:3.14-slim-bookworm AS base

ARG APP_TITLE
ARG API_DIR_NAME
ARG STATIC_FILES_URL=/static/
ARG APP_NAME=htmt-api

RUN for var in APP_TITLE API_DIR_NAME; do \
    eval "value=\$$var"; \
    if [ -z "$value" ]; then \
        echo "ERROR: The $var argument is not provided" >&2; \
        exit 1; \
    fi; \
done

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PROJECT_DIR=/home/app/ \
    API_DIR_NAME=$API_DIR_NAME \
    APP_TITLE=$APP_TITLE \
    DB_IS_NEEDED=true

# audiometa shells out to flac/ffprobe/ffmpeg; pg_isready and curl serve the startup and health scripts.
RUN apt-get update && \
    apt-get install -y --no-install-recommends flac postgresql-client curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Static ffmpeg/ffprobe: Debian's ffmpeg package drags in ~440MB of codec/device libraries.
COPY --from=mwader/static-ffmpeg:7.1 /ffmpeg /ffprobe /usr/local/bin/

WORKDIR $PROJECT_DIR

# Trims test fixtures out of the source tree before it reaches the runtime stage below.
# A plain COPY + RUN rm wouldn't shrink anything (the deleted files stay in the earlier
# layer's history) — copying from this throwaway stage's final filesystem state does.
FROM alpine:3.20 AS trimmed-src
COPY . /src
RUN rm -rf /src/hear/test

# Dev/test image: full source (including test fixtures) and dev tooling.
# This is the stage docker-compose.yml targets for local development and CI.
FROM base AS dev

COPY . $PROJECT_DIR

# git: pip clones the kits over git+https.
RUN apt update && \
    apt-get install -y --no-install-recommends git && \
    bash scripts/install-dev-dependencies.sh && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ARG INSTALL_DEV=true
RUN pip install --upgrade pip && \
    if [ "${INSTALL_DEV:-false}" = "true" ]; then \
      pip install -e ".[dev]"; \
    else \
      pip install .; \
    fi

RUN chmod +x scripts/entrypoint.sh scripts/start-server.sh

# No Docker health check here on purpose: this image also runs non-HTTP roles (the Coolify `worker`),
# so health checks are defined per service instead (Coolify app config, docker-compose.yml).
# Never spell the Docker instruction in uppercase in this file, even in a comment: Coolify greps for it
# and then waits on a container health status that never exists, failing the worker's rolling update.
ENTRYPOINT ["bash", "scripts/entrypoint.sh"]
CMD ["bash", "scripts/start-server.sh"]

# Builds the runtime venv, so git and pip's cache never reach the runtime image.
FROM base AS builder

RUN apt-get update && \
    apt-get install -y --no-install-recommends git && \
    rm -rf /var/lib/apt/lists/*

COPY --from=trimmed-src /src $PROJECT_DIR

RUN python -m venv /opt/venv && /opt/venv/bin/pip install --no-cache-dir .

# Runtime image (default final stage): no test fixtures, no dev tooling.
# This is what a plain `docker build .` (e.g. production deploys) produces.
FROM base AS runtime

ENV PATH="/opt/venv/bin:$PATH"

COPY --from=builder /opt/venv /opt/venv
COPY --from=trimmed-src /src $PROJECT_DIR

RUN chmod +x scripts/entrypoint.sh scripts/start-server.sh

# Last so a new commit doesn't invalidate the cached layers above. Not SOURCE_COMMIT: Coolify
# overrides that one at runtime (with "HEAD" for image-based apps).
ARG GIT_COMMIT
ENV GIT_COMMIT=$GIT_COMMIT

ENTRYPOINT ["bash", "scripts/entrypoint.sh"]
CMD ["bash", "scripts/start-server.sh"]
