# syntax=docker/dockerfile:1
# Base Image: Debian Bookworm (a full Debian distribution).
# Size: Larger, as it includes more tools and libraries by default.
# Use Case: Suitable when you need a full Debian environment with more pre-installed tools and libraries.
FROM python:3.14-bookworm

ARG APP_VERSION
ARG APP_TITLE
ARG API_DIR_NAME
ARG STATIC_FILES_INTERNAL=staticfiles
ARG STATIC_FILES_URL=/static/
ARG APP_NAME=htmt-api

RUN for var in APP_VERSION APP_TITLE API_DIR_NAME; do \
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
    APP_VERSION=$APP_VERSION \
    APP_TITLE=$APP_TITLE \
    DB_IS_NEEDED=true

RUN apt-get update && \
    apt-get install -y gosu && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY . $PROJECT_DIR

WORKDIR $PROJECT_DIR

RUN apt update && \
    bash scripts/install-dependencies.sh && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

RUN mkdir -p "${PROJECT_DIR}${STATIC_FILES_INTERNAL}" && \
    ENV=collect_static \
    STATIC_FILES="${PROJECT_DIR}${STATIC_FILES_INTERNAL}" \
    STATIC_FILES_URL="${STATIC_FILES_URL}" \
    APP_NAME="${APP_NAME}" \
    APP_IS_EXPOSED=false \
    DEBUG=false \
    DB_IS_NEEDED=false \
    AFP_ENABLED=false \
    MUSICBRAINZ_LOOKUP_ENABLED=false \
    SPOTIFY_ENABLED=false \
    GOOGLE_OAUTH_ENABLED=false \
    python manage.py collectstatic --noinput

RUN chmod +x scripts/entrypoint.sh

# Set the entrypoint using shell form to allow environment variable expansion
ENTRYPOINT ["bash", "-c", "${PROJECT_DIR}scripts/entrypoint.sh"]