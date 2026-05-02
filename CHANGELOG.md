# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Changelog Best Practices

### General Principles

- Changelogs are for humans, not machines.
- Include an entry for every version, with the latest first.
- Group similar changes under: Added, Changed, Improved, Deprecated, Removed, Fixed, Documentation, Performance, CI.
- **"Test" is NOT a valid changelog category** - tests should be mentioned within the related feature or fix entry, not as standalone entries.
- Use an "Unreleased" section for upcoming changes.
- Follow Semantic Versioning where possible.
- Use ISO 8601 date format: 2026-03-14.
- Avoid dumping raw git logs; summarize notable changes clearly.

### Guidelines for Contributors

All contributors (including maintainers) should update `CHANGELOG.md` when creating PRs:

1. **Add entries to the `[Unreleased]` section** - Add your changes under the appropriate category (Added, Changed, Improved, Deprecated, Removed, Fixed, Documentation, Performance, CI)
2. **Follow the changelog format** - See examples below and `.cursor/rules/changelog-best-practices.mdc` for detailed guidelines
3. **Group related changes** - Similar changes should be grouped together
4. **Be descriptive** - Write clear, user-focused descriptions of what changed
5. **Mention tests when relevant** - Tests should be mentioned within the related feature or fix entry, not as standalone entries

**Example:**

```markdown
## [Unreleased]

### CI

- **python-project-standards v4.1.0 layout**: Vendored [**`baselines/`**](baselines/) (`ruff.toml`, **`DIGESTS`**, **`expected-mypy.json`**), thin **`[tool.ruff] extend`** in [`pyproject.toml`](pyproject.toml), [**`STANDARDS_VERSION`**](STANDARDS_VERSION) **`4.1.0`**, and [**`scripts/check_lint_baseline.py`**](scripts/check_lint_baseline.py) (with [**`verify-standards.sh`**](scripts/verify-standards.sh) invoking it). [**`pre-commit-hooks`**](.pre-commit-config.yaml) **`rev`** bumped to **`v6.0.0`**. Pre-commit still runs **inline** in [`.github/workflows/test.yml`](.github/workflows/test.yml) (no org **`reusable-pre-commit`** job).

### Added

- **Track API**: Added batch upload endpoint for multiple tracks

  - Includes comprehensive unit tests covering various file formats and error scenarios
  - Supports parallel upload processing for improved performance

- **Genre Hierarchy**: Added support for custom genre tree import via JSON
  - Includes validation tests for tree structure and circular reference detection

### Fixed

- **Track Upload**: Fixed issue with handling large audio files exceeding size limits
  - Includes regression tests to prevent future occurrences
  - Improved error messages for better user feedback
- **Spotify library sync**: Fixed Spotify library sync

### CI

- **Branch Protection**: Added automated enforcement of Git Flow branching rules
  - Blocks invalid PRs to main and develop branches
```

**Note:** During releases, maintainers will move entries from `[Unreleased]` to a versioned section (e.g., `## [0.2.8] - 2025-01-XX`).

## [Unreleased]

### CI

- **Publish**: **`call-redeployment-webhook`** pinned to **`@v0.2.0`**; pass required **`hook_id_base`** from **`vars.REDEPLOYMENT_HOOK_ID_BASE`** ([**BehindTheMusicTree/github-workflows**](https://github.com/BehindTheMusicTree/github-workflows/releases/tag/v0.2.0)). [**.github/actionlint.yaml**](.github/actionlint.yaml): allow **`REDEPLOYMENT_HOOK_ID_BASE`** for actionlint.

## [v2.2.4] - 2026-04-30

### CI

- **python-project-standards v4.3.0** ([org **`v4.3.0`**](https://github.com/BehindTheMusicTree/python-project-standards/releases/tag/v4.3.0)): Root [**`STANDARDS_VERSION`**](STANDARDS_VERSION) **`4.3.0`**. [**`scripts/verify-standards.sh`**](scripts/verify-standards.sh) matches org **`templates/scripts/`** on that tag (verification rejects an **isort** pre-commit hook; import order uses Ruff **`I`** from [**`baselines/ruff.toml`**](baselines/ruff.toml) with **`ruff format`**). Removed the **isort** hook from [**.pre-commit-config.yaml**](.pre-commit-config.yaml); **isort** remains in **[`pyproject.toml`](pyproject.toml)** dev extras for optional local or IDE use. [**.cursor/rules/changelog-alignment.mdc**](.cursor/rules/changelog-alignment.mdc) unchanged from **v4.2.0** alignment. [docs/ci/python-project-standards.md](docs/ci/python-project-standards.md) and [DEVELOPMENT.md](DEVELOPMENT.md) updated for **v4.3.0**.

- **python-project-standards v4.3.1** ([org **`v4.3.1`**](https://github.com/BehindTheMusicTree/python-project-standards/releases/tag/v4.3.1)): Root [**`STANDARDS_VERSION`**](STANDARDS_VERSION) **`4.3.1`**. [**`scripts/check_lint_baseline.py`**](scripts/check_lint_baseline.py) matches org **`templates/scripts/`** on that tag. Org **[`docs/versioning.md`](https://github.com/BehindTheMusicTree/python-project-standards/blob/main/docs/versioning.md)** adds macOS **`bump-my-version`** troubleshooting and optional **`BUMP_MY_VERSION_PYTHON`** for **`scripts/standards_release_bump.sh`**. [docs/ci/python-project-standards.md](docs/ci/python-project-standards.md) and [DEVELOPMENT.md](DEVELOPMENT.md) updated for **v4.3.1**.

### Added

- **Dev setup**: Split setup into explicit host and Docker scripts: [`scripts/setup-host-dev-tools.sh`](scripts/setup-host-dev-tools.sh) installs the tracked Docker-backed git hook ([`.githooks/pre-commit`](.githooks/pre-commit)) into `.git/hooks/pre-commit`, and [`scripts/setup-docker-dev-tools.sh`](scripts/setup-docker-dev-tools.sh) builds/starts `api` then verifies container tooling (`pre-commit`, `shellcheck`, `ruff`). [`scripts/setup-worktree.sh`](scripts/setup-worktree.sh) now runs both.

- **Linting (audiometa-python baseline)**: [`.pre-commit-config.yaml`](.pre-commit-config.yaml) matches the audiometa-python hook stack (tool version check, YAML/JSON/TOML, shellcheck, `no-assert`, ruff-format, ruff, mypy + django-stubs, pydocstringformatter, long-comment fixer, Prettier, optional PSScriptAnalyzer) plus **`prefer-strenum`** (pre-commit no longer runs **isort**; org **v4.3+** verifier forbids it alongside **ruff format**). Configuration lives in [`pyproject.toml`](pyproject.toml); linter and test dependencies are pinned under `[project.optional-dependencies] dev`. Ruff **select** matches audiometa; extra **ignores** document Django/DRF cleanup debt. Mypy is plugin-aligned but **gradual** (`ignore_missing_imports`, non-strict) until typing can match audiometa strictness.

- **Packaging (PEP 621, audiometa-style)**: Runtime and dev dependencies are declared in `pyproject.toml` (`[project]` / `[project.optional-dependencies] dev`) with setuptools as the build backend. Local and CI use `pip install -e ".[dev]"`; production Docker builds use `pip install .`. There is no `requirements.txt`; `pyproject.toml` is the only dependency manifest. Release bumps update `pyproject.toml` `[project] version` via **bump-my-version** (`[tool.bumpversion]`). `fake-samples-loader` is pinned to `1.0.13`; `django-dynamic-fixture` is a dev extra (tests only).

- **[`.pre-commit-hooks/`](.pre-commit-hooks/)**: Shell wrappers copied from audiometa-python (`tool-wrapper`, `check-tool-versions`, shellcheck, `no-assert`, etc.).

### Changed

- **Git pre-commit workflow**: [`.githooks/pre-commit`](.githooks/pre-commit) runs **`pre-commit` only inside the `api` container**; commits fail if Docker or **`api`** is unavailable (no host fallback). [`scripts/setup-host-dev-tools.sh`](scripts/setup-host-dev-tools.sh) installs the hook and requires Docker on PATH.

- **Workflow DB app naming variables**: Updated `.github/workflows/publish.yml`, `.github/workflows/test.yml`, and `.github/actionlint.yaml` to use `DB_APP_NAME_SUFFIX` instead of `DB_APP_NAME`. DB app/container names are derived by appending `DB_APP_NAME_SUFFIX` to `HTMT_API_APP_NAME`.

- **Sync env contract (runtime paths)**: `.github/workflows/sync-env-to-server.yml` writes explicit runtime path keys in the server fragment; `scripts/setup-filesystem.sh` no longer calls `load_project_calculated_paths_env_vars`.

- **Static files contract simplified**: Startup scripts use `STATIC_FILES` as the single runtime static path for collect and serving flows; split default/static path drift from `STATIC_FILES_DEFAULT` is removed where paths are generated.

- **Workflows and Docker build**: CI and Docker workflows use `STATIC_FILES` (instead of `STATIC_FILES_INTERNAL`) as the canonical static path input where relevant.

- **Removed calculated paths loader layer**: Deleted `scripts/generate-calculated-paths-env-file.sh` and removed `load_calculated_env_paths()` from Django settings; scripts and tests consume final runtime env vars directly (no `env/calculated_paths/.env` sourcing).

- **Local Python tooling**: Pre-commit hooks resolve pinned tools from `PATH` ([`.pre-commit-hooks/tool-wrapper.sh`](.pre-commit-hooks/tool-wrapper.sh), [`check-tool-versions.sh`](.pre-commit-hooks/check-tool-versions.sh)); no `.venv`/`venv` activation or path injection. [`.vscode/settings.json`](.vscode/settings.json) no longer pins `./.venv`; [`pyrightconfig.json`](pyrightconfig.json) no longer references `.venv` extraPaths.

- **Ruff**: Aligned `pyproject.toml` ignores with **0.15.x** (removed no-op `PT004` / `UP038`; `TRY302` → `TRY203`). Version remains **0.15.9**.

- **String enums**: Existing `(str, Enum)` types under `api/` now subclass `StrEnum` for consistency with Python 3.11+ stdlib guidance.

- **pytest**: `pytest.ini` live logging default is **INFO** instead of **DEBUG** so suites do not look hung; use `-o log_cli_level=DEBUG` when diagnosing failures.

- **Docker Compose local workflow (no legacy path layer)**: Added repository-level `docker-compose.yml` and `docker-compose.override.yml` for app-local development (`api`/`db`/`afp`) with direct runtime path variables (`MEDIA_DIR`, `TMP_UPLOADED_FILES`, `METADATA_SESSION_DIR`, `DJANGO_LOG_DIR`, `GUNICORN_LOG_DIR`) and shared conventions for image/env/healthcheck alignment with infra deployment.

- **Docker Compose AFP pool volume**: The `afp` service mounts the same named volume as `api` at `TMP_UPLOADED_FILES`, and `POOL_DIR_EXTERNAL` follows that path, so uploaded files are visible to the fingerprinter (fixes integration tests that fingerprint pool files).

- **Docker Compose + pytest optional flags**: [`docker-compose.yml`](docker-compose.yml) defaults `SPOTIFY_ENABLED`, `GOOGLE_OAUTH_ENABLED`, and `MUSICBRAINZ_LOOKUP_ENABLED` to **true** (with existing placeholder client secrets) so `docker compose exec api pytest` matches the suite’s “optional services enabled” guard; [`env/dev/.env.compose.dev.example`](env/dev/.env.compose.dev.example) documents the same.

- **Dockerfile dev install toggle**: Added **`INSTALL_DEV`** build-arg (`false` by default for CI/production `pip install .`; Compose defaults **`INSTALL_DEV=true`** so the API image includes **`pip install -e ".[dev]"`** and `pytest` is available for `docker compose exec api pytest`).

- **Host tooling env source**: Host-side scripts now load environment from repository root `.env` only (no fallback to `env/.env`), aligning local tooling with the Docker-first contract and reducing env-source ambiguity.

- **Pre-commit cache persistence (Docker Compose)**: `api` now sets `PRE_COMMIT_HOME` and mounts a named volume (`api-pre-commit-cache`) at that path so pre-commit hook environments are reused across container recreations instead of re-initializing on each commit.

- **Library path env contract**: Removed runtime usage of `LIBRARIES_DIR_NAME`; settings and user library path generation now rely on `LIBRARIES_DIR` only. Updated Compose defaults, test workflow env, and dev env example accordingly.

- **Release tooling**: Replaced deprecated **bump2version** with **[bump-my-version](https://github.com/callowayproject/bump-my-version)** (`bump-my-version==1.3.0`); bump rules live under `[tool.bumpversion]` in [`pyproject.toml`](pyproject.toml) (`.bumpversion.cfg` removed). [`scripts/prepare_release_bump.py`](scripts/prepare_release_bump.py) runs `bump-my-version bump patch|minor|major`; maintainers only need the CLI on `PATH` (pipx, pyenv-backed install, or Compose `api` with dev extras). [CONTRIBUTING.md](CONTRIBUTING.md) §7 updated accordingly. Runtime **Click** is bumped from `7.0` to `8.3.3` (`click<8.4` required by bump-my-version) so dev installs can run the bump CLI in the same environment.

### CI

- **Test workflow**: Workflow-level `STATIC_FILES` and `STATIC_FILES_URL` are omitted so Django uses `STATIC_FILES_STATE` `NOT_NEEDED` in CI (migrate/pytest/pre-commit); API tests do not rely on static file serving (`urls.py` only adds static routes when collecting/serving).

- **Pre-commit**: PR workflow runs `pre-commit run --all-files` (StrEnum checker, Ruff fatal rules, YAML / merge-conflict checks) in an **inline** job (checkout, Python 3.14, `pip install -e ".[dev]"`), not via org `reusable-pre-commit`. Integration **pytest** stays in-repo. Added **`verify-python-project-standards`** ([`scripts/verify-standards.sh`](scripts/verify-standards.sh)); removed the `STANDARDS_VERSION` file and workflow pin checks. See [docs/ci/python-project-standards.md](docs/ci/python-project-standards.md).

### Fixed

- **Docker dev tooling parity**: Added `shellcheck` to [`scripts/install-dependencies.sh`](scripts/install-dependencies.sh) so `docker compose exec api pre-commit run --all-files` can run the local `shellcheck` hook without manual installation inside the API container.

- **FLAC upload (`fix_md5_checking`)**: Replaced `os.rename` with `shutil.move` when moving the audiometa-corrected FLAC into `TemporaryUploadedFile`’s path so MD5 repair works across mount points (e.g. default temp dir vs `FILE_UPLOAD_TEMP_DIR` in Docker), avoiding `OSError: [Errno 18] Invalid cross-device link` and 500s on affected FLAC uploads.

- **Metadata session imports**: Restored `api.utils.metadata_session` utility exports (`create_session`, `get_session`) so metadata-session view imports resolve correctly in API runtime.

- **Audio metadata serializers**: Restored missing [`api/serializer/audio_metadata/Fields.py`](api/serializer/audio_metadata/Fields.py) and [`api/serializer/audio_metadata/AudioMetadataSessionDownload.py`](api/serializer/audio_metadata/AudioMetadataSessionDownload.py) so `api.urls` and metadata-session views import cleanly (fixes `ModuleNotFoundError` on Docker startup).

- **`verify-standards.sh`**: Synced from **python-project-standards v3.0.1**: stricter local **ruff check** detection (not **`ruff-format`** alone); optional **`STANDARDS_VERSION`** vs **`@v…`** pin scan uses a workflow file loop instead of fragile **`grep -r --include`** ordering (still accepts **astral-sh/ruff-pre-commit** remote repo).

- **Django startup in deploy images**: `coverage` is only appended to `INSTALLED_APPS` during pytest when the module is installed, avoiding `ModuleNotFoundError: No module named 'coverage'` in staging/production.

- **API startup (Gunicorn)**: Runtime `setuptools` is pinned so `pkg_resources` remains available in slim deploy images.

### Documentation

- **Development**: [DEVELOPMENT.md](DEVELOPMENT.md) links org-wide policy to [python-project-standards `docs/development.md`](https://github.com/BehindTheMusicTree/python-project-standards/blob/main/docs/development.md) (with [`string-enums.md`](https://github.com/BehindTheMusicTree/python-project-standards/blob/main/docs/string-enums.md) for `StrEnum`); notes **Ruff UP042** as primary enforcement and **`prefer-strenum`** as an extra guardrail. [docs/ci/python-project-standards.md](docs/ci/python-project-standards.md) references the same hub and notes org **v3+** dropped **reusable-test-matrix** (only **reusable-pre-commit** remains for shared lint).

- **Contributing**: [CONTRIBUTING.md](CONTRIBUTING.md) documents explicit host (`scripts/setup-host-dev-tools.sh`) and Docker (`scripts/setup-docker-dev-tools.sh`) setup flows for pre-commit and Docker-based workflows; the Testing section explains when pytest feels stuck (verbose logging, DB).

- **Cursor**: `.cursor/rules/strenum-string-enums.mdc` matches [python-project-standards `templates/cursor-rules/strenum-string-enums.mdc`](https://github.com/BehindTheMusicTree/python-project-standards/blob/main/templates/cursor-rules/strenum-string-enums.mdc) and encodes the `StrEnum` convention for contributors using Cursor.

- **README**: Added ecosystem context with portfolio links (`themusictree.org`, HearTheMusicTree project page) and clarified that portfolio/marketing source-of-truth lives in `the-music-tree-frontend`.

- **README**: Corrected the GrowTheMusicTree ecosystem link to the `grow-the-music-tree-frontend` repository.

- **Git Flow / branch protection**: CONTRIBUTING and `.cursor/rules/git-flow-workflow.mdc` state how PRs to `develop` relate to classic Git Flow (`feature/*` plus `chore/*`, `dependabot/*`, `release/*`), list disallowed prefixes (e.g. `docs/*`), and describe the usual fix when the branch-name check fails. The branch protection workflow failure message and `docs/workflows.md` point to the same guidance. **Pre-PR checklist** and **pull-request-convention** Cursor rules are aligned (`dependabot/*`, target branches, invalid prefixes).

- **Docker local dev**: Added Compose quick start and responsibility split guidance in [README.md](README.md), plus [env/dev/.env.compose.dev.example](env/dev/.env.compose.dev.example) as the dedicated app-repo Compose environment template.

- **Docker-only local workflow**: Documented Docker Compose as the default developer path and aligned [CONTRIBUTING.md](CONTRIBUTING.md) and [`.cursor/rules/pre-pr-checklist.mdc`](.cursor/rules/pre-pr-checklist.mdc) setup/testing notes with `docker compose exec api …` (optional local `pip install -e ".[dev]"` for `pytest`; no dedicated `.venv` workflow).

- **Env file contract (host scripts)**: One-time and helper scripts now use `.env` as the single default host env file (or explicit `ENV_FILE`) to avoid legacy `env/.env` drift from Docker Compose defaults.

## [v2.2.3] - 2026-04-01

### Changed

- **Release tooling**: `scripts/prepare_release_bump.py` exits unless run inside a Python virtual environment (with dependencies from `pip install -r requirements.txt`), so maintainers do not hit a missing `bump2version` when using the system interpreter.

### Fixed

- **Metadata session download headers**: File download responses now set standards-compliant `Content-Disposition` with both `filename` (ASCII fallback) and `filename*` (RFC5987 UTF-8), expose `Content-Disposition` to browser JS via `Access-Control-Expose-Headers`, and return a real MIME type (with fallback to `application/octet-stream`) instead of a generic `file` content type.

- **Release tooling**: `prepare_release_bump.py` no longer treats `##` headings inside fenced Markdown code blocks as real changelog sections when deciding whether to insert a new empty `## [Unreleased]` after a bump, so the in-file template example cannot mask the actual latest `[Unreleased]` heading.

### CI

- **Actionlint config variables**: Updated `.github/actionlint.yaml` to align workflow variable names with staging/prod conventions by using `SPOTIFY_CLIENT_ID_STAGING` and `GOOGLE_CLIENT_ID_STAGING` (and removing legacy `*_TEST` names).

## [v2.2.2] - 2026-03-25

### Security

- **Startup and request logging**: OAuth client ids are no longer printed in full by default (masked prefix/suffix); redirect URIs and scopes are summarized unless **`DJANGO_VERBOSE_STARTUP=true`**. **`load_required_bool_env_var`** no longer echoes the raw string before parsing. If **`APP_IS_EXPOSED`** and **`DEBUG`** are both true, a **security warning** is printed. Removed debug **`print`** from **`SpotifyLibTrackViewSet`**; **`TreeField`** criteria validation uses **`logging.debug`**; Spotify artist batch errors use **`logger.exception`**.

### Fixed

- **Sync env to server**: Single step validates and builds `fragment.env`; **`FILE_UPLOAD_ENABLED`** and the other compose-required API `*_ENABLED` keys are hardcoded **`true`** in the workflow YAML.

- **Calculated `LIBRARIES_DIR`**: `generate-calculated-paths-env-file.sh` concatenated `${MEDIA_DIR}${LIBRARIES_DIR_NAME}`, which produced `/app/medialibraries` when `MEDIA_DIR` was `/app/media` and `LIBRARIES_DIR_NAME` was `libraries`—while Django uses `MEDIA_DIR` / `LIBRARIES_DIR_NAME` (`/app/media/libraries`). Filesystem setup created the wrong path and `manage.py check` failed in deploy.

- **Container setup-filesystem: Django log paths**: `DJANGO_LOG_DIR` is `/var/log/django` (no trailing slash) in deploy; the script concatenated `${DJANGO_LOG_DIR}${filename}`, producing `/var/log/djangorequests_debug.log` instead of `/var/log/django/requests_debug.log`. Django log and Gunicorn log file paths now join with `${VAR%/}/filename`.

### Changed

- **`FILE_UPLOAD_ENABLED` required at runtime**: No inference from `TMP_UPLOADED_FILES`. Django and `scripts/setup-filesystem.sh` fail fast if it is unset or not `true`/`false`. Set it in local `.env` (see `env/dev/.env.dev.example`). **Sync env to server** hardcodes **`FILE_UPLOAD_ENABLED=true`** (and the other compose-required API booleans) in the server fragment.

- **Sync env: compose API booleans hardcoded**: **Sync env to server** always writes **`FILE_UPLOAD_ENABLED=true`**, **`SPOTIFY_ENABLED=true`**, **`GOOGLE_OAUTH_ENABLED=true`**, **`MUSICBRAINZ_LOOKUP_ENABLED=true`**, **`HTMT_API_AFP_ENABLED=true`** (no GitHub Variables for those keys).

- **Entrypoint: collectstatic at runtime**: When `STATIC_FILES` is set, the container runs `manage.py collectstatic --noinput` on startup (after Django check, before migrate). The static root (e.g. `/app/static`) is then populated so nginx or the app can serve files without a separate build-step; same image works across envs.
- **Sync env to server**: Fragment includes **`SPOTIFY_SCOPES`** from GitHub Variable `SPOTIFY_SCOPES` (required). Use the same scopes as in `env/dev/.env.dev.example` unless you need fewer. Redeploy compose fails if Spotify is enabled and scopes are absent.

### Documentation

- **Release tooling**: `scripts/prepare_release_bump.py` automates the maintainer Note → `bump2version` → `fix_changelog_after_bump.py` → empty `## [Unreleased]` steps. CONTRIBUTING.md §7, docs/versioning.md, and changelog Cursor rule updated accordingly.

## [v2.2.1] - 2026-03-17

### CI

- **Single Publish workflow**: Replaced separate Publish and Publish staging with one `publish.yml`. Triggers: push to `main` (→ TEST env, staging, image tag `staging`); push to version tags `v*` (prerelease/dev tag → TEST/staging, release tag → PROD/production). `workflow_dispatch` and `workflow_call` retained. Build workflow accepts optional `environment` (TEST/PROD). Removed `publish-staging.yml`. See docs/workflows.md.
- **Branch protection status checks**: Use job-level required checks (Test / Pytest, Test / Check vars and secrets, Branch Protection Check / Actionlint, Branch Protection Check / Verify PR source branch) instead of workflow-level names. Removed report-status jobs; configure branch protection to require the exact check names above. See docs/workflows.md.

## [v2.2.0] - 2026-03-14

### Fixed

- **Track file validator**: Corrected FLAC magic bytes from extension string (`.flac`) to the actual stream signature (`fLaC`) so FLAC uploads (e.g. to full metadata endpoint) are accepted. Unit test added for FLAC magic-byte validation.

### Added

- **Sync env to server workflow**: Manually triggerable workflow `sync-env-to-server.yml` that merges app secrets and vars (DB*APP*_, DJANGO*SECRET_KEY, SUPERADMIN*_, DEMO\_\*, TMTA_USERNAME, OAuth secrets, DEMO_EMAIL, SUPERADMIN_EMAIL) into the server `scripts/.env` for test and prod; compose-required API booleans are written in the workflow. Use after changing these in this repo so the server has the latest values without running the full infrastructure transfer. See [docs/workflows.md](docs/workflows.md#sync-env-to-server).
- **Metadata session (no auth)**: Two-step public flow: (1) `POST /v1/audio/metadata/session/` — upload file (or URL), get metadata plus `session_token` and `session_expires_in_seconds` (900); (2) `POST /v1/audio/metadata/session-download/` — send token (header `X-Session-Token` or body) and optional metadata, receive file with tags written. Session valid 15 minutes; multi-use (download multiple times with different metadata). No auth, no DB persistence. Session and upload temp use separate env-defined dirs (`METADATA_SESSION_DIR`, `TMP_UPLOADED_FILES`). Frontend instructions in `docs/frontend/one_time_metadata_update.md`.
- **Audio metadata (full)**: Optional request parameter `include_musicbrainz_analysis` for `POST /v1/audio/metadata/full/`. When `true`, the response includes `musicbrainz_raw_data` with raw AcoustID/MusicBrainz lookup result (or an error payload if fingerprinting or lookup fails). No authentication required; no DB records are created. Ephemeral fingerprinting and non-persisting MusicBrainz lookup added for this flow. Integration, unit, and e2e tests added.
- **FILE_UPLOAD_ENABLED**: Explicit env flag for file upload / media. When `true`, setup-filesystem creates upload temp, metadata session, and media dirs; when `false`, skips them. Env example, CI, and local builds use the flag; deployed stacks get **`true`** from **Sync env to server**.

### Changed

- **Metadata keys**: `AppMetadataKey` is the single source of truth for metadata field names (literal values). Track input Fields and writable metadata (session-download, file update) use it; `APP_METADATA_WRITABLE_KEYS` and `WritableMetadataFieldsMixin` shared. Genre in metadata is `genres_names` (array of strings) everywhere.
- **Storage**: `METADATA_SESSION_DIR` and `TMP_UPLOADED_FILES` are independent env-defined paths (not one under the other). Setup-filesystem creates `METADATA_SESSION_DIR` when file upload is enabled. Deploy and CI set both.
- **Deploy (runtime config)**: Path variables are no longer written into the app .env by the deploy workflow; they are supplied at runtime by the server or Compose environment (12-factor style). Affected: `METADATA_SESSION_DIR_EXTERNAL`, `TMP_UPLOADED_FILES_EXTERNAL`, `MEDIA_DIR_EXTERNAL`, `STATIC_FILES_EXTERNAL`, `DJANGO_LOG_DIR_EXTERNAL`, `GUNICORN_LOG_DIR`. The generated Compose part passes these from the host env into the API container and mounts volumes at those paths; the server must set them (e.g. in a .env next to docker-compose) when starting the stack.

### CI

- **Publish workflows**: Staging and release flows now set image tags on the server (API, DB, AFP) via `set-image-tag-on-server` before calling the redeploy webhook, so the server pulls the correct image versions when redeploying.
- **DB and AFP image tags must be pinned**: `DB_VERSION` and `AFP_VERSION` are required (no `latest`). Set them in Settings → Variables (e.g. `16`, `1.0`). New job **check-pinned-tags** fails the workflow if either is unset. Redeploy on the server also aborts if DB or AFP tag is still `latest`.
- **Test workflow**: `FILE_UPLOAD_ENABLED=true`; `METADATA_SESSION_DIR_EXTERNAL` uses a separate path (`/tmp/ci-metadata-sessions/`). Upload temp dir tearDown expects no leftover files (session dir is separate).
- **Deploy workflow**: `FILE_UPLOAD_ENABLED` in required vars check and app .env output; `METADATA_SESSION_DIR_EXTERNAL` removed from workflow (set at runtime on server).

## [v2.1.1] - 2026-03-08

### Documentation

- **Release tooling**: bump2version added to keep `VERSION`, `package.json`, and `schema.yml` in sync; release steps in CONTRIBUTING.md updated to use `bump2version patch|minor|major` before finalizing CHANGELOG and tagging.
- **Scripts**: One-time DB/maintenance scripts moved to `scripts/one-time/` with README; CONTRIBUTING.md updated with "One-time and maintenance scripts" subsection.

### CI

- **Test strategy**: CI now enables all optional services (Spotify, Google OAuth, MusicBrainz) with fake/placeholder credentials and mocks at the boundary. Only AFP is required to be reachable for e2e; third-party reachability is not checked in CI. See api/test/README.md and CONTRIBUTING.

### Added

- **Audio meta analysis**: AFP and MB lookup toggled by `AFP_ENABLED` and `MUSICBRAINZ_LOOKUP_ENABLED`. New MB missing cause `MUSICBRAINZ_LOOKUP_DISABLED` (code 9) when AFP on and MB off. CI: AFP on, MB off.

### Removed

- **Fixture files**: Removed all JSON fixtures from `api/fixtures/` (users, genres, app). Reference data is provided by data migrations; test data is created in code via `ModelFixtureFactory` and `AppTestCase.setUp()`. Removed fixture loading from `init-django-data.sh`, the "Set up fixtures files" CI step, and Dockerfile fixture copy. `api/fixtures/` kept with `.gitkeep` for optional local use.
- **Reference Spotify library**: Removed reference API `/v1/reference/library/spotify/` and `ReferenceSpotifyLibTrackViewSet`. Exposing one Spotify account’s library to all users would violate Spotify’s User Guidelines and Developer Policy (no account sharing; each user must link their own account). Per-user library under `me/library/spotify/`. See [Spotify compliance](docs/integrations/spotify.md#no-shared-system-spotify-account).

### Changed

- **Missing cause codes**: Renamed `AUDIO_META_AMALYSIS_DISABLED` to `AFP_DISABLED` (code 0) in `FingerprintMissingCauseCode` and `MbRecordingMissingCauseCode`; label updated to "AFP (fingerprinting) is disabled." Migration `0012_rename_audio_meta_analysis_disabled_to_afp_disabled` updates existing rows. API code value remains 0.
- **E2E fail early**: Session checks required services when e2e run; CI requires AFP enabled and reachable; dev requires all enabled services reachable. See `api/test/README.md` and CONTRIBUTING.
- **Settings**: `MUSICBRAINZ_LOOKUP_ENABLED` global; TrackFile calls MB only when both it and `AFP_ENABLED` are true. Startup fails if `MUSICBRAINZ_LOOKUP_ENABLED=true` and `AFP_ENABLED=false` (MB needs fingerprint).
- **Tests**: OAuth/MB/Spotify client mocked per conftest (CI or non-e2e). Audio meta: `override_settings(AFP_ENABLED=...)`, no test-only env override. E2e refactor with `_domain_helper()` and SearchMixin; markers and docs in api/test/README.md.
- **Service flags**: `SPOTIFY_ENABLED`, `GOOGLE_OAUTH_ENABLED`, `AFP_ENABLED`, `MUSICBRAINZ_LOOKUP_ENABLED` required (no defaults). CI sets Spotify/Google/MB false; deploy sets all true.
- **Settings**: Renamed to `AFP_ENABLED`; added to example env. AFP vars (`AFP_CONTAINER_NAME`, `AFP_URL`, `AFP_PORT`, `AFP_POST_ENDPOINT`) are required only when `AFP_ENABLED=true`; when false they must be unset (file upload disabled) or optional.
- **Model table names**: Table-prefix metaclass removed. Every concrete model now sets `db_table` explicitly in `Meta` (e.g. `db_table = 'htmt_api_user'`), matching migration and raw SQL names. Aligns with Django best practice and "explicit is better than implicit"; model renames no longer affect table names unless `db_table` is changed. `TablePrefixModelBase` and `PolymorphicTablePrefixModelBase` deleted; `DB_TABLE_PREFIX` removed from settings.

### Documentation

- **API docs**: Audio metadata endpoint path aligned in `docs/api/index.md` and `docs/api/audio_metadata.md`.
- **CONTRIBUTING**: Note that ffprobe (ffmpeg) must be installed and working for WAV-based tests; troubleshooting for broken install (e.g. `brew reinstall ffmpeg` on macOS).

### Improved

- **Tests**: Pytest fails fast when ffprobe is missing or broken: session-start runs `ffprobe -version` and probes the WAV fixture `duration=472s.wav`; clear exit message if probe fails. `test_duration` (album retrieve) uses WAV again (DURATION_472S_WAV, expected 277 + 472).

## [v2.1.0] - 2026-02-23

### Added

- **Audio Metadata**: Added POST to get full raw metadata from a file

## [v2.0.1] - 2026-02-22

### Fixed

- **Deploy**: Requests to the bare domain (e.g. `themusictree.org`) and `www` no longer trigger `DisallowedHost`. Deploy workflow now adds the domain and `www.${DOMAIN_NAME}` to `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS`.
- **Request logging**: Fixed "Error reading request body: You cannot access body after reading from request's data stream" on multipart requests (e.g. track upload to `uploaded/`). RequestLoggingMiddleware no longer reads `request.body` for `multipart/form-data` and logs a placeholder instead. Includes unit test.

- **Spotify OAuth**: Fixed backend always returning the same Spotify user regardless of which account completed login. Spotipy’s token cache was used by default, so the first user’s token was returned for every subsequent code exchange. The code exchange now uses `check_cache=False` so each login uses the provided authorization code.

### Removed

- **Admin**: SpotifyUser is no longer registered in Django admin (model was removed in v2.0.0 unified account).

### Changed

- **Dev env example**: `APP_NAME` default set to `htmt-api` (was `htmt_api`).
- **Scripts**: `run-db-and-afp-containers.sh` loads `env/.env` when present before running containers; `utils.sh` env loader trims keys and skips lines starting with `#`; `purge-django-data` cleanup (removed unused variable and redundant debug logs).

### Improved

- **Spotify OAuth**: When Spotify returns 403 "user may not be registered" (app in Development mode), the API now returns 401 with error code **1007** (`spotify_user_not_allowlisted`) and a clear user-facing message so the frontend can show a specific message without parsing. Docs and tests updated.

## [v2.0.2] - 2026-02-21

### Fixed

- **Spotify auth**: When Spotify returns `invalid_client` (e.g. wrong/missing app credentials), API now returns 500 with a generic "Sign-in is temporarily misconfigured" message instead of 401, since the failure is server configuration, not the user

### Changed

- **CI / Deploy**: Differentiate DB container port from host port: use `DB_PORT_CONTAINER` (and `DB_PORT_HOST`) instead of a single `DB_PORT` in workflows, Docker Compose generation, and env files
- **CI / Deploy**: Standardize container root path to `/home/app/` (`CONTAINER_ROOT_DIR`) across deploy, test, and static-files workflows
- **Dockerfile**: Remove `PROJECT_DIR` build arg; set `PROJECT_DIR=/home/app/` and `API_DIR_NAME=api` in image; build-and-push no longer passes `PROJECT_DIR`
- **Deploy (env and docker-compose)**: Set `FRONT_HOST` per environment (prod vs test) for Spotify/Google redirect URIs; add Django log directory and log filenames to API env file and workflow inputs; simplify env echo for client IDs (no extra quotes)
- **Deploy (docker-compose)**: DB and AFP compose parts use `DB_PORT_CONTAINER`; AFP healthcheck uses `AFP_PORT` instead of `APP_PORT`
- **Scripts**: `init-django-data.sh` validates `API_DIR_NAME` is a relative path (reject leading `/`)

## [v2.0.1] - 2026-02-20

### Changed

- **Deploy (env and docker-compose)**: API app env and reusable workflow input now set `APP_PORT` from `HTMT_API_PORT_TEST` when deploying to test and `HTMT_API_PORT` when deploying to prod
- **Deploy (env and docker-compose)**: AFP env file now sets `APP_PORT` from `AFP_PORT_TEST` when deploying to test and `AFP_PORT_PROD` when deploying to prod

## [v2.0.0] - 2026-02-20

### Added

- **Google OAuth**: `POST auth/google/` endpoint to exchange Google authorization code for session tokens
  - Request: `{ "code": "<authorization_code_from_google_callback>" }`
  - Response: `{ accessToken, refreshToken, expiresAt }` (same shape as Spotify auth for a single session model on the frontend)
  - Backend exchanges code with `oauth2.googleapis.com/token`, fetches user info, creates or links user, issues JWT session
  - Env: `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `GOOGLE_REDIRECT_URI` (must match frontend redirect URI)
  - `GoogleAuthenticationException` mapped to 401; integration tests for view and OAuth service
- **Unified account (Option A)**: One user can have both Google and Spotify linked; backend links by email when the same person signs in with a second provider
  - Single `User` model with optional `spotify_id` and `google_id` (and provider tokens/profiles); `SpotifyUser` and `GoogleUser` subclasses removed
  - Spotify auth: find by `spotify_id`, else by email (link), else create. Google auth: same for `google_id` and email
  - Frontend guide: `docs/frontend/unified-account-and-linking.md`

### Changed

- **API URL prefix**: Path prefix uses the major version only (e.g. `v1/`), derived from `APP_VERSION`; full semantic version is no longer used in URLs. Changelog and docs (README, `docs/versioning.md`, `docs/api/*`, frontend guides) updated to describe and use `v1` consistently
- **Auth response**: Spotify and Google auth now return `expiresAt` (Unix timestamp in milliseconds) for client-side expiry handling; JWT util returns `expires_at_ms` from access token payload

## [v1.0.5] - 2026-02-15

### Changed

- **API**: Current user's Spotify profile endpoint moved from `users/spotify/` to `me/spotify/` for consistency with other "current user" resources (`me/artists`, `me/playlists`, etc.). Admin user management remains at `users/`.
  - Docs: `docs/api/me_spotify.md`, `docs/api/index.md`, `docs/frontend/authentication-and-spotify.md`, README updated
- **API (me/spotify)**: Removed `GET /me/spotify/{id}/` (retrieve). Only `GET /me/spotify/` is supported; it returns a list of 0 or 1 item (current user's profile). Retrieve by id was redundant since the only valid id is the current user's.

- **Spotify / Auth**: Consistent 401 vs 403 for me/spotify and Spotify-required endpoints
  - **401** when not logged in to the app (API code 1006, `authentication_required`): frontend should redirect to app login
  - **403** when logged in but Spotify not linked (API code 1005, `spotify_authorization_required`): frontend should redirect to Spotify OAuth
  - `IsAuthenticatedReturn401` permission returns 401 instead of DRF default 403 for unauthenticated requests to Spotify user endpoints
  - Exception handler converts PermissionDenied to 401 when request is unauthenticated (fallback)
  - `AUTH_SPOTIFY_NOT_AUTHENTICATED` (1005) mapped to 403; `AUTH_NOT_AUTHENTICATED` (1006) to 401
  - Frontend guide: `docs/frontend/authentication-and-spotify.md`; API doc `docs/api/me_spotify.md` updated with error codes and link

### Fixed

- **API / OpenAPI**: Decimal fields are serialized as JSON numbers via `AppModelSerializer`: model `DecimalField` and `GeneratedField` with decimal `output_field` map to `FloatField` so schema and response use `number` (fixes Zod/client type mismatch)
- **Test**: Unit test enforces that all model serializers (Meta.model) extend `AppModelSerializer` so decimal-as-number stays consistent
- **URL routing**: Spotify profile moved to `me/spotify` (no longer under `users/`), so no route conflict with BaseUserViewSet
- **Spotify**: Added SpotifyAuthenticationException to custom exception handler so Spotify auth failures return 401 JSON instead of 500 in DEBUG

### Improved

- **env**: Add SUPERADMIN and DEMO credentials to .env.dev.example for enhanced configuration

## [v1.0.4] - 2026-02-13

### Added

- **Users**: Added SUPERADMIN and DEMO environment variables to deployment workflow for enhanced configuration

### Fixed

- **Workflow**:Improved branch detection in static-files workflow by excluding symbolic refs

## [v1.0.3] - 2026-02-13

### Changed

- **Dependencies**: Upgrade drf-spectacular to version 0.29.0

- **OpenAPI schema**: Title and version now configurable and aligned with app

  - OpenAPI `info.version` uses `APP_VERSION` (e.g. 1.0.4) instead of hardcoded 0.1.0
  - OpenAPI title set via `APP_TITLE` for human-readable docs title

- **OpenAPI schema**: Path prefix updated for subdomain deployment
  - `SCHEMA_PATH_PREFIX` changed from `/api/v[0-9]` to `/v[\d.]+` so it matches the version segment only (no `/api/` prefix)

### Fixed

- **OpenAPI schema**: Fix TypeError when generating schema for models with DecimalField/GeneratedField
  - Add custom AppAutoSchema that maps GeneratedField via output_field and passes max_digits/decimal_places for DecimalField so /schema/ and docs endpoints work

## [v1.0.2] - 2026-02-13

### Added

- **Reference Contexts**: Implement public read-only reference contexts for all major API endpoints

  - Add reference contexts for genres, albums, artists, plays, tags, and library/uploaded endpoints
  - Create Reference ViewSets with AllowAny permissions and system user fallback for public access
  - Add ReferencePlaylistViewSet and ReferenceManualPlaylistViewSet so reference/playlists and reference/manual-playlists expose system-owned public data
  - Restructure URL paths to hierarchical design (/me/ and /reference/ scopes)
  - Update router registrations in urls.py for new hierarchical paths
  - Regenerate API documentation with contexts tables for all endpoints
  - Update test reverse calls and import paths to reflect new URL structure
  - Modify Bruno test files to use new hierarchical URLs
  - Ensure all endpoint tests pass with the new reference contexts

- **Health Check**: Add health check endpoint to API for improved service monitoring

### Fixed

- **CriteriaType**: Seed genre and tag criteria types in migration so reference genre tree load-example and other flows no longer raise DoesNotExist
  - Add data migration `0003_seed_criteria_types` to ensure `CriteriaType` rows with pk 0 (genre) and 1 (tag) exist

### Improved

- **Deployment**: Apply Django migrations on every container start

  - Entrypoint always runs `migrate` after DB is ready (first init and subsequent deploys)
  - Single code path; migrate is idempotent

- **Entrypoint**: Use init-django-data instead of reinit when Django is not initialized

  - Prevents DROP USER / database purge on deploy when the init check fails or on first run
  - Reinit (purge + init) remains for manual use only; container only runs init (create DB/role if missing, migrate, fixtures)

- **init-django-data.sh**: Follow best practices for migrations

  - Only run `makemigrations` if no migration files exist (e.g., after purge)
  - In production/normal init, migrations should already be in repo; only `migrate` runs
  - Capture and log migrate output for better debugging
  - Exit with error code if makemigrations or migrate fails

- **check_data_initialized**: Handle missing tables gracefully

  - Check if User table exists before querying it (prevents ProgrammingError)
  - Properly detect "not initialized" state when tables don't exist
  - Better error messages for debugging

- **entrypoint.sh**: Improve migration error visibility

  - Capture and log migrate output to diagnose migration failures
  - Show exit code when migrations fail

- **check-django-initialized.sh**: Show check command output
  - Display check_data_initialized output instead of hiding it
  - Better visibility into why initialization check passes/fails

### Documentation

- **CONTRIBUTING.md**: Add Database migrations section (create in dev, never makemigrations in prod, migrations run on deploy, backward-compatibility)
- **workflows.md**: Document that migrations are applied by container entrypoint, not by deploy workflow

## [v0.3.6] - 2026-02-06

### CI

- **Versioning**: Derive app version from git tags instead of GitHub repository variables

  - Extract version from git tags in publish.yml workflow (supports pre-release versions: rc, beta, alpha, dev)
  - Pass app_version as input to reusable workflows (static-files, build, deploy, test)
  - Add version extraction logic with fallback to latest git tag
  - Remove dependency on APP_VERSION GitHub repository variable
  - Enables testing Docker images on test server using pre-release tags (e.g., v0.3.5-rc1)

- **Static Files Workflow**: Improve branch detection and conflict handling

  - Fail workflow if branch has newer commits on remote (prevents conflicts and data loss)
  - Check branch sync status before collecting static files and before committing
  - Improved branch detection for release branches and tag-triggered workflows
  - Better error handling with clear messages when branch is out of sync
  - Reorder workflow steps: checkout and verify branch sync before collecting static files

- **Workflows**: Remove workflow_dispatch manual triggers from all workflows
  - Workflows can only be triggered via workflow_call or automatic triggers (push, pull_request, tags)
  - Removes manual triggering capability from GitHub Actions UI
  - Ensures workflows are only triggered through proper channels

### Documentation

- **Dev tags**: remove overlapping document `dev-tag-practices.md`
- **Versioning Strategy**: Add comprehensive versioning.md documentation

  - Document git tag-based versioning approach
  - Explain pre-release version identifiers (rc, beta, alpha, dev) and their usage
  - Document version extraction logic and workflow inputs
  - Update workflows.md to reference versioning approach

- **Dev Tag Practices**: Add comprehensive dev tag documentation and cursor rule
  - Document dev tag naming convention (use branch name without type prefix)
  - Explain version selection strategy (placeholder based on branch type)
  - Provide guidance for republishing dev tags after changes
  - Add cleanup step to release process for removing dev tags
  - Create cursor rule to ensure consistent dev tag practices

## [v0.3.5] - 2026-02-04

### Fixed

- **Production Import Error**: Fix ModuleNotFoundError when importing User model in production
  - Move test utility import (`UploadedTrackTestFilename`) from module level to inside method
  - Prevents import error when `api.test` module is not available in production environment

## [v0.3.4] - 2026-02-04

### Fixed

- **API Schema Generation**: Fix Swagger UI Internal Server Error when accessing `/api/schema/`

  - Handle `list` action in `AppModelViewSet.get_serializer_class()` for drf-spectacular introspection
  - Add authentication check in `queryset` property to handle `AnonymousUser` during schema generation
  - Explicitly define `GeneratedField` as `DecimalField` in `FileDetailedSerializer` to prevent introspection errors
  - Add `SerializerMethodField` for nested JSON fields in `SpotifyUserDetailedSerializer` (display_name, followers, href, images, type, uri)

- **CI**: Add SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET to deploy workflow

  - Spotify credentials are now written to API .env file on server deployment
  - Fixes Django initialization failure when Spotify integration is enabled

- **CI**: Pass secrets to static-files workflow in publish workflow

  - Added `secrets: inherit` to publish workflow so STATIC_FILES_PAT token is available
  - Enables static files workflow to bypass branch protection when using PAT token

- **Git Worktree Configuration**: Added environment file (`env/.env`) to worktree copy configuration
  - Environment files are now automatically copied when creating new git worktrees
  - Improves developer experience by eliminating manual environment file setup

## [v0.3.3] - 2026-02-04

### Fixed

- **CI**: Handle detached HEAD when pushing static files from tag-triggered workflow
  - Static files workflow now detects detached HEAD state and checks out the appropriate branch (main/develop) before committing and pushing
  - Fixes workflow failure when publish workflow is triggered by version tags

## [v0.3.2] - 2026-02-04

### Fixed

- **Docker**: Correct fixture copy paths in Dockerfile to match repository layout

  - Copy from `app/` and `genres/` instead of non-existent `api/`; fixes build failure during image build

- **Docker**: Use python:3.14-bookworm base image instead of python:3.14-buster
  - python:3.14-buster is not published on Docker Hub; Python 3.14 images use Bookworm or Trixie

### Changed

- **Docker**: Run filesystem setup in entrypoint instead of Dockerfile so volume-mounted paths get correct permissions at container start

- **Docker Compose generation**: AFP container working_dir set to /app/ in generate-docker-compose-parts.sh (was /api/)

- **Docker**: Split image build into separate RUN steps for maintainability

  - System deps, Python deps, filesystem setup, and fixture copy each in their own step; easier to debug and reuse layers

- **Repository References**: Updated deploy workflow and package.json to use BehindTheMusicTree org
  - Deploy workflow redeployment webhook calls BehindTheMusicTree/github-workflows
  - package.json repository, bugs, and homepage URLs point to BehindTheMusicTree/the-music-tree-api

### CI

- **Workflows**: Add check-vars-and-secrets job to deploy, build, test, and static-files

  - Fails fast if required environment vars or secrets are missing; reports all missing ones (scripts/check-workflow-env.sh)

- **Publish Workflow**: Run only on version tags (v\*) and manual/workflow_call dispatch; removed push-to-branch trigger

- **Deploy Workflow**: Use SERVER_DEPLOY_USERNAME secret instead of TEST_SERVER_BODZIFY_USERNAME for SSH destination

- **Deploy Workflow**: Remove SSH whitelist handling and scripts/whitelist-runner-ssh.sh

- **Test Workflow**: Run test workflow on push to main, develop, release/_, hotfix/_, chore/\*

  - Ensures tests run on protected and chore branches without requiring a PR

- **Deploy Workflow**: Redeployment webhook calls BehindTheMusicTree/github-workflows; optional push trigger for chore/improve-cicd

  - Aligns CI/CD with BehindTheMusicTree organization

- **Workflow job names**: Shortened job names and publish job ids (static, build, deploy; Set env vars, Set compose files, Redeploy webhook; Static files, Push to Docker Hub) to reduce truncation in GitHub Actions UI
  - Aligned step name "Set up Python" in test workflow with static-files
  - docs/workflows.md documents job id and display name for each workflow

### Documentation

- **GitHub Actions Workflows**: Added docs/workflows.md documenting all workflows with table of contents
  - Describes triggers, steps, and environments for test, publish, build, deploy, static-files, branch-protection, labeler
  - CONTRIBUTING.md links to workflows doc in TOC and in Pull Request Process section

## [v0.3.1] - 2025-12-10

### Changed

- **Project Branding**: Updated references from Bodzify API to HearTheMusicTree API across documentation and configuration files
  - Updated README, VISION document, and various documentation files
  - Clarified project goals and mission statement

### Documentation

- **VISION Document**: Added comprehensive VISION.md document outlining project mission, goals, and principles

  - Describes integration with BehindTheMusicTree ecosystem
  - Outlines key principles: Personal-First, Metadata-First, Genre Intelligence, Privacy & Security, Interoperability, Accessibility
  - Documents ecosystem integration with AudioMeta Python, GrowTheMusicTree, and TheMusicTreeAPI

- **Project Presentation**: Improved project presentation across documentation
  - Updated README to better reflect HearTheMusicTree branding
  - Enhanced clarity of project goals and vision

### CI

- **Branch Protection**: Updated branch protection rules to allow `release/*` branches to target `develop`

  - Aligns with standard Git Flow workflow where release branches merge into both `main` and `develop`
  - Fixes issue where release branches couldn't merge back into `develop` due to branch protection rules

- **VS Code Settings**: Fixed JSON syntax errors in `.vscode/settings.json` and removed deprecated `python.pythonPath` setting
  - Removed trailing commas causing JSON parsing issues
  - Removed deprecated `python.pythonPath` in favor of `python.defaultInterpreterPath`
  - Improves VS Code configuration maintainability

### Changed

- **Test Files Cleanup**: Removed outdated test files from `bodzify_api/test/utils/uploaded_track/files/` directory
  - Deleted 7 duplicate test files from old directory structure
  - All test files now properly located in `api/test/utils/uploaded_track/files/` after test reorganization
  - Reduces repository size and eliminates confusion from duplicate files

## [v0.3.0] - 2025-12-10

### Changed

- **Test Organization**: Reorganized test structure to align with DRF conventions

  - Moved all tests to `api/test/tests/` directory for cleaner organization
  - Unit tests organized by component type (filtering, middleware, serializer, utils, validator)
  - Integration tests organized by endpoint/resource (album, artist, auth, criteria, playlist, uploaded_track, etc.)
  - E2E tests organized by workflow (track_upload, genre_hierarchy, spotify, etc.)
  - Moved middleware and FilterSet tests from integration to unit tests
  - Removed redundant `view/` and `common/` directories from integration tests
  - Updated test documentation to reflect new structure

- **Audio Metadata**: Replaced audio metadata management module with `audiometa-python` (bumped to `0.8.1` in `requirements.txt`)
- **Dependencies**:
  - Updated `Django` from 5.0.3 to 5.2.8
  - Updated `asgiref` from 3.7.2 to 3.8.1 for Django 5.2.8 compatibility
  - Updated `psycopg2-binary` from 2.9.5 to 2.9.11 for Python 3.14 compatibility
  - Updated `django-stubs` from 5.1.1 to 5.2.1 for Django 5.2.8 compatibility
  - Updated `django-filter` from 22.1 to 25.2 for Python 3.14 compatibility (fixes `pkgutil.find_loader` removal)
  - Updated `django-polymorphic` from 3.1.0 to 4.1.0 to resolve pkg_resources deprecation warning and ensure Django 5.2 compatibility
  - Removed `mutagen` from direct dependencies. No longer needed as direct dependency since all audio operations now use `audiometa-python`

### Documentation

- **Test Documentation**: Updated test README and contributing guide

  - Added comprehensive test structure documentation in `api/test/README.md`
  - Added table of contents to test README
  - Updated CONTRIBUTING.md to reference test README
  - Added unit test suggestions document with detailed test scenarios
  - Clarified distinction between unit, integration, and E2E tests

- **Project Management**: Added `TODO.md` for tracking future work and improvements

  - Categorized by priority (high, medium, low)
  - Organized by features, testing, and infrastructure

- **Contributing Documentation**: Comprehensive contributing guide with strict Git Flow workflow

  - Detailed branch naming and merging rules for `main`, `develop`, `feature/*`, `release/*`, `hotfix/*`, and `chore/*` branches
  - Installation and setup instructions
  - Code style guidelines and development best practices
  - Pre-PR checklist and review process
  - Release process documentation

- **Development Guidelines**: Added `DEVELOPMENT.md` with comprehensive coding standards

  - Code quality practices and conventions
  - Django best practices for models, serializers, views, and filtering
  - Type checking and error handling guidelines
  - Documentation standards

- **Cursor Rules**: Added AI assistant rules to enforce project standards

  - Git Flow workflow enforcement
  - Commit message convention (Conventional Commits)
  - Pull request title convention
  - Issue template usage guidelines
  - Pre-PR checklist enforcement
  - Issue descriptions in separate version-controlled files
  - PR descriptions in git-ignored directory for local drafting
  - Test naming convention and structure guidelines
  - Changelog best practices

- **README**: Simplified `README.md` to provide high-level overview with links to detailed documentation

  - Moved detailed setup instructions to `CONTRIBUTING.md`
  - Added badges for license, Python version, and Django version

- **Contributing Guide**: Reorganized installation steps in `CONTRIBUTING.md` for logical flow

  - Environment variables setup before scripts that use them
  - Improved step-by-step instructions clarity

- **License**: Added Apache License 2.0

- **Code of Conduct**: Added Contributor Covenant 2.1

### Added

- **Git Worktree Scripts**: Added npm `git-worktree-scripts` package (v1.4.0) for managing git worktrees
  - Includes `setup-worktree.sh` script for automated worktree setup with virtual environment and dependencies
  - Added `.git-worktree-copy` configuration for copying gitignored files to new worktrees
    - Copies `env/.venv` Python virtual environment
    - Copies fixture files from `api/fixtures/*.json`
  - Integrated filesystem setup into `setup-worktree.sh` for automatic directory and log file creation

### Fixed

- **Error Handling**: Fixed Python 3.14 compatibility issues with exception attribute access

  - Wrapped all `exception.detail` accesses in try-except blocks to handle `AttributeError` and `TypeError`
  - Added safe stringification fallbacks for all `str(exception)` calls
  - Fixed `TypeError: 'super' object has no attribute 'dicts'` error in exception logging middleware
  - Updated `ErrorResponse`, `AppValidationException`, `AppSerializer`, `ExceptionLoggingMiddleware`, and `RequestLoggingMiddleware` to safely handle DRF exceptions in Python 3.14
  - Prevents middleware crashes when exception stringification fails

- **Filesystem Setup**: Fixed `setup-filesystem.sh` to check for `DJANGO_LOG_DIR` instead of `DJANGO_LOGS_DIR` to properly create log directories

  - Updated app name to 'api'

- **Filter Backend**: Added `get_schema_operation_parameters` method to `ConsistentParametersFilterBackend` for drf-spectacular compatibility with django-filter 25.2

- **Django 6.0 Compatibility**: Replaced deprecated `CheckConstraint.check` with `condition` parameter in all model constraints

  - Updated 6 model files: `CriteriaType`, `Criteria`, `Artist`, `Album`, `FingerprintMissingCauseCode`, `ManualPlaylist`
  - Updated migration file `0001_initial.py` to use new syntax
  - Resolves Django 6.0 deprecation warnings for `CheckConstraint.check`

- **Criteria Tree Import**: Removed debug print statements from `import_criteria_tree` method that were causing test hangs
  - Eliminated excessive I/O overhead when processing large tree imports (30,000+ nodes)
  - Fixed test hangs and significantly improved performance for large tree import operations

### CI

- **Test Configuration**: Filtered ResourceWarnings about unclosed files from Django's ORM in pytest configuration

  - Added `ignore:unclosed file:ResourceWarning` filter to `pytest.ini`
  - These warnings are non-actionable as they originate from Django's internal FileField handling
  - Improves test output clarity by reducing noise from Django ORM file handle management
  - Django automatically manages these file handles through garbage collection

- **GitHub Automation**:

  - Auto-labeler workflow (`.github/workflows/labeler.yml`) for automatic PR labeling based on file paths
  - Branch protection workflow (`.github/workflows/branch-protection.yml`) to enforce Git Flow rules
    - Blocks PRs to `main` from non-hotfix/release branches
    - Blocks PRs to `develop` from invalid branch types
  - Issue templates for bug reports and feature requests
  - Pull request template with comprehensive checklist
  - GitHub Discussions setup with category templates

- **Branch Protection**: Added automated enforcement of Git Flow branching rules

  - PRs to `main` must come from `hotfix/*` or `release/*` branches only
  - PRs to `develop` must come from `feature/*`, `chore/*`, or `dependabot/*` branches only
  - Provides clear error messages when branch rules are violated

- **CI Workflow**: Split monolithic CI workflow into focused, reusable workflows

  - Updated `test.yml` workflow to run tests on pushes and pull requests (removed redundant `ci.yml` wrapper)
  - Added fail-fast flag (`-x`) to pytest for faster CI feedback on test failures
  - Created `static-files.yml` workflow for collecting and pushing static files
  - Created `build.yml` workflow for Docker image building and pushing
  - Created `deploy.yml` workflow for server deployment tasks
  - Created `publish.yml` workflow for releases (triggers on version tags `v*`)
  - Publishing workflow handles static files collection, Docker build, and deployment
  - Improved workflow maintainability and reusability
  - Separation of concerns: tests run on every change, publishing only on releases

- **CI/CD**: Updated GitHub Actions workflow to use `develop` branch instead of `dev`
  - Updated Python version to 3.14 in CI workflows
  - Added branch protection checks for Git Flow enforcement

## [v0.2.0] - 2025-04-03

### Added

- Enable Spotify integration with comprehensive API support:
  - Track search and lookup by ID/ISRC
  - Artist information retrieval
  - Audio features analysis (tempo, key, energy, danceability)
  - Spotify OAuth authentication for user accounts
  - Track preview URL support
  - Album information integration
  - Artist popularity and genre data

## [v0.1.3] - 2025-04-02

### Added

- Enable genre tree JSON import
- Enable genre tree JSON export
- Enable delete criteria

### Changed

- Arrays in JSON must be without [] and in multipart with []

## [v0.1.2] - 2025-03-11

### Added

- Enable track archiving
- Complete filtering for all list requests
- Handle more tags formats: ID3v1 (.mp3, .wav, .flac), RIFF (wav)
- Implement a complete and consistent error handling system with precise codes (validation codes for bad requests)

### Changed

- Put all test files in same directory with consistent naming
- Set app not to handle in memory files: small files are handle as regular files

## [v0.1.1] - 2024-09-06

### Added

- Fingerprint check
