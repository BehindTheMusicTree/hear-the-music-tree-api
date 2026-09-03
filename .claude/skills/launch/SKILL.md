---
name: launch
description: Use this skill when asked to run, start, dev-serve, or preview hear-the-music-tree-api, or to confirm a change works against a real running instance. Covers the Docker Compose dev stack (db, afp, api) and the GHCR auth step needed to pull the afp image.
---

# Launch hear-the-music-tree-api

Local-first Docker Compose setup with three services: `db` (Postgres),
`afp` (audio-fingerprinter, pulled from GHCR), and `api` (Django, built
locally). `docker-compose.override.yml` applies dev overrides (bind mount +
`runserver`) automatically on top of `docker-compose.yml`.

## 1. Env file (first run only)

```bash
cp env/dev/.env.compose.dev.example .env
```

## 2. Authenticate to GHCR (needed to pull the `afp` image)

`afp` pulls `ghcr.io/<GHCR_IMAGE_NAMESPACE>/audio-fingerprinter:<AFP_VERSION>`,
usually a private org package. Log in once with a PAT (`read:packages` scope;
your normal GitHub password will NOT work here):

```bash
gh auth token | docker login ghcr.io -u "$(gh api user -q .login)" --password-stdin
```

(Or a manually created classic PAT — see README.md "Developer environment"
section for the full walkthrough and troubleshooting `unauthorized`/`denied`
errors.)

## 3. Build and start the stack

```bash
docker compose build api && docker compose up
```

Or detached, blocking until `api` reports healthy (`GET /health/` returns 200,
which requires `db` to be reachable):

```bash
docker compose up -d --wait api
```

If `api` exits immediately with code 0 on `--wait`, the local `api` image
likely predates the current `Dockerfile` `ENTRYPOINT`
(`bash scripts/entrypoint.sh`) — rebuild with `docker compose build api` or
`docker compose up --build api`.

## 4. Verify

- App: `http://localhost:8000`
- Swagger: `http://localhost:8000/docs/`
- Logs: `docker compose logs api` (container name `htmt-api`)

Optional integration flags (`SPOTIFY_ENABLED`, `GOOGLE_OAUTH_ENABLED`,
`MUSICBRAINZ_LOOKUP_ENABLED`) default to enabled with placeholder credentials
in Compose, so the app and test suite run without extra env wiring unless you
need those integrations for real.
