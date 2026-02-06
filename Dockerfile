# syntax=docker/dockerfile:1
# Base Image: Debian Bookworm (a full Debian distribution).
# Size: Larger, as it includes more tools and libraries by default.
# Use Case: Suitable when you need a full Debian environment with more pre-installed tools and libraries.
FROM python:3.14-bookworm

ARG PROJECT_DIR

RUN if [ -z "$PROJECT_DIR" ]; then \
	echo "ERROR: The PROJECT_DIR argument is not provided" >&2; \
	exit 1; \
fi

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PROJECT_DIR=$PROJECT_DIR

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

RUN chmod +x ${PROJECT_DIR}scripts/entrypoint.sh && \
    FIXTURES_DIR=${PROJECT_DIR}api/fixtures/ && \
    for subdir in app genres users/test users/umg; do \
        if [ -d "$${FIXTURES_DIR}$${subdir}" ] && [ -n "$$(ls -A "$${FIXTURES_DIR}$${subdir}" 2>/dev/null)" ]; then \
            cp "$${FIXTURES_DIR}$${subdir}"/* "$${FIXTURES_DIR}"; \
        fi; \
    done

# Set the entrypoint using shell form to allow environment variable expansion
ENTRYPOINT ["bash", "-c", "${PROJECT_DIR}scripts/entrypoint.sh"]