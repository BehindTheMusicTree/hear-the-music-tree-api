# syntax=docker/dockerfile:1
# Base Image: Debian Bookworm, slim variant (no compiler toolchain baked in).
# None of our direct dependencies need to compile from source (psycopg2-binary ships wheels),
# so the full python:3.14-bookworm image's ~1GB of pre-installed build tooling is dead weight.
FROM python:3.14-slim-bookworm AS base

ARG APP_TITLE
ARG API_DIR_NAME
ARG STATIC_FILES_URL=/static/
ARG APP_NAME=htmt-api
ARG SOURCE_COMMIT

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
    DB_IS_NEEDED=true \
    GIT_COMMIT=$SOURCE_COMMIT

RUN apt-get update && \
    apt-get install -y gosu git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR $PROJECT_DIR

COPY scripts/install-dependencies.sh scripts/
RUN apt update && \
    bash scripts/install-dependencies.sh && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

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

RUN apt update && \
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

# Disable for images whose CMD/entrypoint is overridden to run something that isn't the HTTP
# server (e.g. the worker placeholder, which runs `sleep infinity` via a Coolify entrypoint
# override) — HEALTHCHECK itself can't be made conditional at build time, so the check always
# runs but no-ops to success when unset.
ARG HEALTHCHECK_ENABLED=true
HEALTHCHECK --interval=5s --timeout=3s --start-period=30s --retries=10 \
    CMD [ "$HEALTHCHECK_ENABLED" != "true" ] || curl -f "http://127.0.0.1:${APP_PORT:-8000}/health/"

ENTRYPOINT ["bash", "scripts/entrypoint.sh"]
CMD ["bash", "scripts/start-server.sh"]

# Runtime image (default final stage): no test fixtures, no dev tooling.
# This is what a plain `docker build .` (e.g. production deploys) produces.
FROM base AS runtime

COPY --from=trimmed-src /src $PROJECT_DIR

RUN pip install --upgrade pip && pip install .

RUN chmod +x scripts/entrypoint.sh scripts/start-server.sh

ARG HEALTHCHECK_ENABLED=true
HEALTHCHECK --interval=5s --timeout=3s --start-period=30s --retries=10 \
    CMD [ "$HEALTHCHECK_ENABLED" != "true" ] || curl -f "http://127.0.0.1:${APP_PORT:-8000}/health/"

ENTRYPOINT ["bash", "scripts/entrypoint.sh"]
CMD ["bash", "scripts/start-server.sh"]
