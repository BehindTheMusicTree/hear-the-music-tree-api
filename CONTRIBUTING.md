# 🧭 Contributing Guidelines

Thank you for your interest in contributing!

This project is currently maintained by a solo developer, but contributions, suggestions, and improvements are welcome.

## Table of Contents

- [🧑‍🤝‍🧑 Contributors vs Maintainers](#-contributors-vs-maintainers)
  - [Roles Overview](#roles-overview)
  - [Infrastructure & Automation Permissions](#infrastructure--automation-permissions)
- [🧱 Development Workflow](#-development-workflow)
  - [0. Fork & Clone](#0-fork--clone)
  - [1. Environment Setup](#1-environment-setup)
  - [2. Branching](#2-branching)
  - [3. Developing](#3-developing)
  - [4. Testing](#4-testing)
    - [4.1. Testing Docker Images During Development](#41-testing-docker-images-during-development)
  - [5. Committing](#5-committing)
  - [6. Pull Request Process](#6-pull-request-process)
    - [6.1. Pre-PR Checklist](#61-pre-pr-checklist)
    - [6.2. Opening a Pull Request](#62-opening-a-pull-request)
  - [7. Releasing _(For Maintainers)_](#7-releasing-for-maintainers)
- [⚙️ GitHub Actions Workflows](docs/workflows.md)
- [CI: python-project-standards alignment](docs/ci/python-project-standards.md)
- [🪪 License & Attribution](#-license--attribution)
- [📜 Code of Conduct](#-code-of-conduct)
- [📋 TODO List](#-todo-list)
- [🌍 Contact & Discussions](#-contact--discussions)

## Contributors vs Maintainers

### Roles Overview

**Contributors**

Anyone can be a contributor by:

- Submitting bug reports or feature requests via GitHub Issues (use the issue templates: [Bug Report](.github/ISSUE_TEMPLATE/bug_report.yml) and [Feature Request](.github/ISSUE_TEMPLATE/feature_request.yml))
- Proposing code changes through Pull Requests (the PR template will guide you through the process)
- Improving documentation
- Participating in discussions
- Testing and providing feedback

**Maintainers**

The maintainer(s) are responsible for:

- Reviewing and merging Pull Requests
- Managing releases and versioning
- Ensuring code quality and project direction
- Responding to critical issues
- Maintaining the project's infrastructure
- Creating and managing hotfix branches for urgent production fixes
- Creating and managing release branches for preparing releases
- Moving "Unreleased" changelog entries to versioned sections during releases
- Managing repository automation (stale issues/PRs, auto-labeling, auto-assignment, etc.)

**Important:** Even maintainers must go through Pull Requests. No direct commits to `main` or `develop` are allowed - all changes, including those from maintainers, must be submitted via Pull Requests and go through the standard review process.

_Note: Contributors can submit fixes for critical issues via feature branches. Maintainers may promote these to hotfix branches when urgent production fixes are needed._

### Infrastructure & Automation Permissions

**Repository automation policies (maintainer-only):**

- Publishing workflows (`.github/workflows/*.yml`) - handles sensitive secrets and can publish Docker images
- Stale issues/PRs workflow - affects repository management policies
- Auto-assignment workflows - affects review process
- Auto-labeler workflow (`.github/workflows/labeler.yml`) - automatically labels PRs based on changed files
- Other automation workflows that affect repository management

**Auto-labeling configuration (contributors can suggest changes via PRs):**

- Auto-labeling configuration (`.github/labeler.yml`) - contributors can suggest updates when adding new features/components
- Example: If adding a new API endpoint, contributor can suggest adding label rules for that component
- Maintainers review and approve label configuration changes

**Why most automation is maintainer-only:**

- These workflows implement repository policies and management decisions
- Changes can affect how issues/PRs are handled, categorized, and maintained
- They require understanding of project management strategy

**What contributors can do:**

- Suggest changes to auto-labeling configuration (`.github/labeler.yml`) via PRs, especially when adding new features/components
- Suggest improvements or report issues with automation via GitHub Issues
- Add/remove labels on their own issues and PRs (type labels like `bug`, `enhancement`, priority labels, etc.)
- Discuss automation behavior in discussions or issues

**What contributors cannot do:**

- Modify automation workflows (stale, auto-assignment, etc.) - these are policy decisions
- Create or delete repository labels (maintainer-only) - repository labels are the label definitions (like `bug`, `enhancement`, `api`, `track`) that exist in the repository's label list
- Modify labels on issues/PRs they didn't create (unless they have write access)

Currently, this project has a solo maintainer, but the role may expand as the project grows.

## 🧱 Development Workflow

We follow a **strict Git Flow** model:

**Workflow steps:** Fork & Clone → Environment Setup → Branching → Developing → Testing → Committing → Pull Request Process (including Pre-PR Checklist) → Releasing _(For Maintainers)_

### 0. Fork & Clone

**For contributors:**

1. Fork the repository on GitHub
2. Clone your fork:

   ```bash
   git clone https://github.com/YOUR-USERNAME/the-music-tree-api.git
   cd the-music-tree-api
   ```

**For maintainers:**

Clone the main repository directly:

```bash
git clone https://github.com/BehindTheMusicTree/the-music-tree-api.git
cd the-music-tree-api
```

### 1. Environment Setup

#### Prerequisites

- **Python 3.14**
- **Docker** and **Docker Compose** - Required for running the PostgreSQL database and Audio Fingerprinter containers

#### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/BehindTheMusicTree/the-music-tree-api.git
   cd the-music-tree-api
   ```

2. Set up environment variables:

   Create a copy of the file `env/dev/.env.dev.template` as `.env` and set the required values. See the [Environment Variables](#environment-variables) section below for details on all required variables.

   **Note:** Environment variables are required for filesystem setup and running containers in the following steps.

3. Install system dependencies:

   ```bash
   # Ubuntu/Linux
   sudo bash scripts/install-dependencies.sh

   # macOS
   # Install dependencies via Homebrew or use the Linux script as reference
   ```

   This installs required system tools: `flac`, `ffmpeg`, `libchromaprint-tools`, `jq`, `postgresql-client`

   **Note:** Tests that use WAV files require `ffprobe` (from ffmpeg) to be installed and working. If pytest exits with "ffprobe failed to run" or you see "File corrupted" when running audio tests, ffmpeg may be broken (e.g. missing libvpx on macOS). Fix by reinstalling: `brew reinstall ffmpeg` (macOS) or re-run `scripts/install-dependencies.sh` (Linux).

4. Start the Docker Compose development stack:

   ```bash
   cp env/dev/.env.compose.dev.example .env
   docker compose up --build
   ```

   This is the default local workflow for this repository. It runs API + DB + AFP with the same runtime env contract used by deployment.

   **Tests:** With this stack, Postgres and AFP are already Compose services. Run the suite with **`docker compose exec api pytest`** (see [Testing](#testing)); GitHub Actions runs the same stack via **`docker compose`** (see [`.github/workflows/test.yml`](.github/workflows/test.yml)). Step 5 is optional on the host when you need the same directories for scripts outside the container; the **`api`** image startup also prepares paths inside the container.

5. Set up filesystem:

   ```bash
   bash scripts/setup-filesystem.sh
   ```

   This creates necessary directories for:

   - Static files
   - Django logs
   - Gunicorn logs (if app is exposed)
   - Media files and libraries
   - Temporary uploaded files

#### Environment Variables

You need to set up several environment variables for development, build, and run.

**Environment Variable Handling:**

The application uses strict environment variable validation:

- **Required variables**: Must be set or the application will fail to start with a clear error message
- **No fallbacks**: Required environment variables do not have default values - they must be explicitly set
- **Path validation**: Path variables (like `MEDIA_DIR`) are validated to ensure the directories exist
- **Type validation**: Boolean and integer variables are validated for correct types
- **Application data**: Application data files (like reference data, fixtures) are stored relative to the codebase (`BASE_DIR`) and do not require environment variables

**Development:**
Create a copy of the file `env/dev/.env.dev.template` as `.env` and set the values.

**Build:**
The docker build requires the following environment variables:

- `APP_NAME`
- `APP_VERSION`
- `FILE_UPLOAD_ENABLED`
- `LIBRARIES_DIR_INTERNAL` (local/internal path mode) or `LIBRARIES_DIR_EXTERNAL` (server/external path mode)
- `STATIC_FILES`
- `DJANGO_LOG_GENERAL_FILENAME`
- `DJANGO_LOG_INFO_FILENAME`
- `DJANGO_LOG_REQUESTS_FILENAME`
- `DJANGO_LOG_REQUESTS_DEBUG_FILENAME`
- `DJANGO_LOG_EXCEPTIONS_FILENAME`
- `DJANGO_LOG_DJANGO_FILENAME`
- `DJANGO_LOG_APP_FILENAME`
- `GUNICORN_LOG_ERROR_FILENAME`
- `GUNICORN_LOG_ACCESS_FILENAME`

For production deploy, path variables (`TMP_UPLOADED_FILES_EXTERNAL`, `MEDIA_DIR_EXTERNAL`, `STATIC_FILES_EXTERNAL`, `DJANGO_LOG_DIR_EXTERNAL`, `GUNICORN_LOG_DIR`) are set at runtime on the server (e.g. in a `.env` next to docker-compose), not by the workflow. The runtime static path consumed by the app is `STATIC_FILES`. Do not add host-specific path values to GitHub repo or environment vars; the server supplies them when starting the stack.
`STATIC_FILES_INTERNAL` / `STATIC_FILES_EXTERNAL` are deprecated for this app runtime; use `STATIC_FILES` directly.

Log and static filenames (e.g. `GUNICORN_LOG_ERROR_FILENAME`, `DJANGO_LOG_GENERAL_FILENAME`) stay in the workflow. Industry practice: paths vary by host/deployment so they are runtime config (12-factor); filenames are usually fixed or set at deploy time because they rarely differ per environment. Strict 12-factor also prefers logging to stdout and letting the execution environment handle files; when using file-based logging, path = runtime, filename = workflow or code default is a common compromise.

**Running the container:**
Running the container requires the following environment variables:

- `DJANGO_SECRET_KEY`
- `ACOUSTID_API_KEY`
- `CSRF_TRUSTED_ORIGINS`
- `ALLOWED_HOSTS`
- `DB_CONTAINER_NAME`
- `DB_PORT=5432`
- `DB_APP_DB_NAME`
- `DB_APP_USERNAME`
- `DB_APP_USER_PASSWORD`
- `AFP_CONTAINER_NAME` (AFP meaning Audio FingerPrinter)
- `AFP_PORT`
- `AFP_POST_ENDPOINT`

**Note:** Application data files (like the reference genre tree) are stored in the `data/` directory relative to the project root and are deployed with the codebase. They do not require environment variable configuration.

#### Database Requirement

The HearTheMusicTree API requires a PostgreSQL database to function. With **Docker Compose** (step 4), the database is the Compose **`db`** service; CI uses the same Compose model (see [`.github/workflows/test.yml`](.github/workflows/test.yml)).

#### Database migrations

- **Create migrations in development**: Run `python manage.py makemigrations` locally and commit the generated files under `api/migrations/`.
- **Never run `makemigrations` in production**: Schema changes are created in dev and shipped with the code; production only applies them.
- **Migrations run automatically on deploy**: The container entrypoint (`scripts/entrypoint.sh`) runs `migrate` after the database is ready, so every deployment applies pending migrations before starting the app.
- **Keep migrations backward-compatible**: Prefer additive changes (e.g. nullable columns or defaults) so the previous app version keeps working until the new one has run.

#### One-time and maintenance scripts

One-off DB or data fix scripts (e.g. table renames, one-time backfills) live in **`scripts/one-time/`**, grouped by domain (e.g. `db/`, `data/`). They are versioned for audit, for re-running on other environments, and for use after restoring from backup. Each script (or the folder README) describes when and how to run it; run them only when the situation applies.

#### Audio Fingerprinting Requirement

For audio fingerprinting, the HearTheMusicTree API requires an app called Audio Fingerprinter. You can find the Audio Fingerprinter app on GitHub at the following link: [Audio Fingerprinter](https://github.com/BehindTheMusicTree/audio-fingerprinter)

The AFP image creates the Flask app log from `FLASK_LOG_APP_FILENAME` (e.g. `app.log`), which must match what `settings.py` expects (`LOG_APP_FILE`). Path variables (`GUNICORN_LOG_DIR`, `FLASK_LOG_DIR_EXTERNAL`, `POOL_DIR_EXTERNAL`) are runtime-only and required when running the container; the AFP entrypoint fails fast if any is missing. When running AFP as a non-root user (e.g. some local `docker run --user` setups), the image must support non-root (writable `/app/log`). See the AFP README.

### 2. Branching

We follow **strict Git Flow** with the following branch structure:

#### Main Branch (`main`)

- The production-ready, stable branch
- All tests must pass before merging
- Releases are tagged from `main`
- **No direct commits allowed** - All changes must go through Pull Requests, including changes from maintainers
- Only receives merges from `release/*` and `hotfix/*` branches
- **Branch protection enforced** - GitHub Actions automatically blocks PRs to `main` that don't come from `hotfix/*` or `release/*` branches (see `.github/workflows/branch-protection.yml`)

#### Develop Branch (`develop`)

- The integration branch for ongoing development
- Feature and chore branches merge into `develop` via pull requests
- `develop` is merged into `main` via release branches
- **No direct commits allowed** — all changes must go through pull requests
- Pull requests to `develop` are only accepted from `feature/*`, `chore/*`, `dependabot/*`, or `release/*` branches (see **Branch Protection** below)
- **Branch protection enforced** — GitHub Actions blocks PRs to `develop` that do not use one of those source branch prefixes (see `.github/workflows/branch-protection.yml`)

#### 🛡️ Branch Protection

- **PRs to `main`** must come from `hotfix/*` or `release/*` branches only. This keeps production changes traceable and tied to releases or hotfixes.
- **PRs to `develop`** must come from `feature/*`, `chore/*`, `dependabot/*`, or `release/*` branches only. Other prefixes (e.g. `docs/*`, `fix/*`, `refactor/*`) fail the **Branch Protection Check / Verify PR source branch** job and cannot be merged while required checks are enabled.

**How this maps to Git Flow:** In the classic model, work is integrated into `develop` through **`feature/*`** branches. This repository also uses **`chore/*`** for maintenance and documentation-only changes, **`dependabot/*`** for dependency automation, and **`release/*`** when merging release-line work back into `develop`.

**If your PR fails the branch name check:**

1. **Rename the branch locally** (on your work branch): `git branch -m feature/<descriptive-name>` or `git branch -m chore/<descriptive-name>`.
2. **Push the new name** and set upstream: `git push -u origin HEAD`.
3. **Remove the old remote branch** if you already pushed it: `git push origin --delete <old-branch-name>`.
4. **Open a new pull request** from the correctly named branch and close the previous one. (GitHub does not reliably let you retarget an existing PR to a differently named head branch.)

If you had not pushed yet, only steps 1–2 and a new PR are needed. Maintainers cannot “approve past” a failing required check without changing branch protection rules or using an admin merge override — the usual fix is a correctly prefixed branch.

- Enforcement lives in the `branch-protection.yml` workflow at `.github/workflows/branch-protection.yml`.

#### Feature Branches (`feature/<name>`)

- Create one for each new feature or bug fix
- Branch from `develop`
- Include issue numbers when applicable: `feature/123-add-ogg-support`
- Examples:

  ```bash
  git checkout develop
  git pull origin develop
  git checkout -b feature/improve-genre-classification

  git checkout -b feature/123-add-ogg-support        # With issue number
  git checkout -b feature/456-fix-id3v1-encoding    # With issue number
  ```

- Merge into `develop` via Pull Request when complete and tested

#### Chore Branches (`chore/<name>`)

- For maintenance, infrastructure, and configuration work
- Branch from `develop`
- Include issue numbers when applicable: `chore/234-update-dependencies`
- Examples: repository setup, CI/CD changes, dependency updates, documentation infrastructure
- Examples:

  ```bash
  git checkout develop
  git pull origin develop
  git checkout -b chore/github-setup
  git checkout -b chore/update-dependencies
  git checkout -b chore/234-update-dependencies        # With issue number
  ```

- Merge into `develop` via Pull Request when complete

#### Release Branches (`release/<version>`) _(For Maintainers)_

- Created from `develop` when preparing a new release
- Used for final testing, bug fixes, and version bumping
- Examples:

  ```bash
  git checkout develop
  git pull origin develop
  git checkout -b release/v0.2.1
  ```

- Only bug fixes and release-related changes go into release branches
- When ready, merge into both `main` (for production) and `develop` (to keep develop up to date)
- Tag the release on `main` after merging

#### Hotfix Branches (`hotfix/<name>`) _(For Maintainers)_

- For urgent bug fixes on production versions
- Branch from `main`
- Include issue numbers when applicable: `hotfix/789-critical-bug`
- Examples:

  ```bash
  git checkout main
  git pull origin main
  git checkout -b hotfix/critical-metadata-bug

  git checkout -b hotfix/789-critical-security-patch   # With issue number
  ```

- Contributors can submit fixes via feature branches that maintainers may promote to hotfixes if needed
- When complete, merge into both `main` (for immediate production fix) and `develop` (to keep develop up to date)

#### Chore Branches (`chore/<name>`)

- For maintenance, infrastructure, and configuration work
- Branch from `develop`
- Include issue numbers when applicable: `chore/234-update-dependencies`
- Examples: repository setup, CI/CD changes, dependency updates, documentation infrastructure
- Examples:

  ```bash
  git checkout develop
  git pull origin develop
  git checkout -b chore/github-setup
  git checkout -b chore/update-dependencies
  git checkout -b chore/234-update-dependencies        # With issue number
  ```

- Merge into `develop` via Pull Request when complete

#### Dependabot Branches (`dependabot/*`)

- For automated dependency updates created by [Dependabot](https://github.com/dependabot)
- Typically generated/managed by GitHub and follow a naming convention like `dependabot/<ecosystem>/<package>-<version>` (e.g., `dependabot/pip/requests-2.28.0`)
- Branch from `develop`
- Dependabot opens Pull Requests that should target `develop` for dependency bumps and security updates
- Merge into `develop` via Pull Request when complete; treat them like `chore/*` changes or dependency maintenance

### 3. Developing

See [DEVELOPMENT.md](DEVELOPMENT.md) for comprehensive coding standards and best practices.

### 4. Testing

We use pytest for all automated testing with Django.

#### Quick Reference

```bash
# Run all tests
pytest

# Run tests for a specific category
pytest api/test/tests/unit/
pytest api/test/tests/integration/
pytest api/test/tests/e2e/

# Run tests for a specific module
pytest api/test/tests/integration/view/uploaded_track/

# Run tests with coverage
pytest --cov=app --cov-report=html --cov-report=term-missing

# Run tests with verbose output
pytest -v

# Run a specific test file
pytest api/test/tests/integration/view/uploaded_track/test_specific.py

# Quieter / faster-feeling run (disables live log streaming entirely)
pytest -o log_cli=false

# Maximum verbosity for debugging a failure
pytest -o log_cli_level=DEBUG
```

**If pytest seems stuck or extremely slow:**

- **Live logging:** `pytest.ini` sets `log_cli = true`. At **DEBUG** every log line is printed and the suite can look frozen. The default level is **INFO**; use `-o log_cli=false` for minimal console noise or `-o log_cli_level=DEBUG` only when chasing a failure.
- **Database:** Integration and most Django tests need **PostgreSQL** (and env) as in [Environment Setup](#1-environment-setup). A missing or unreachable DB often blocks on connect instead of failing immediately—start the Compose stack (**`docker compose up`**) first, then run **`docker compose exec api pytest`**.
- **Container context:** If `pytest` is not found on your host, run tests from the API container (`docker compose exec api pytest ...`) or install dev dependencies with `python -m pip install -e ".[dev]"` in your active Python environment so `pytest` is on your `PATH`.

**Test Structure:**

- Tests are located in `api/test/tests/` directory, organized by category:
  - `tests/unit/` - Unit tests
  - `tests/integration/` - Integration tests
  - `tests/e2e/` - End-to-end tests
- Follow the naming convention: `test_{scenario}_then_{expected_result}`
- Use `assert` instead of `assertEqual`
- Each test should focus on a single scenario

For detailed information about test structure, organization, and conventions, see [Test README](api/test/README.md).

**Mocked vs real (e2e) tests:**

Integration tests that depend on external services (URLs, third-party APIs) use mocks by default so CI runs without network and stays deterministic.

**Mockable services:** Spotify and Google OAuth (view layer); MusicBrainz (AcoustID) lookup and Spotify API client (service layer); AFP / audio fingerprinting (service layer). AFP and MusicBrainz can be toggled independently (`AFP_ENABLED`, `MUSICBRAINZ_LOOKUP_ENABLED`).

- **Unit and integration tests:** All mocked.
- **E2e tests:**
  - Dev: nothing mocked; e2e can use real providers locally when the corresponding services are enabled (env / feature flags). When the run includes e2e tests, every enabled service must be reachable or the session fails early.
  - All runs: `SPOTIFY_ENABLED`, `GOOGLE_OAUTH_ENABLED`, and `MUSICBRAINZ_LOOKUP_ENABLED` must be true or the test run fails at collection. Use fake credentials in CI; conftest only mocks at the boundary.
  - CI (`ENV=ci_test`): only AFP must be reachable for e2e; other services are mocked.
- Details: [api/test/README.md](api/test/README.md) (OAuth, Spotify API client, Audio meta analysis, fail early).

Add at least one **real** e2e test when the service can be exercised without blocking CI (see [api/test/README.md](api/test/README.md) § E2E tests: when to add, when they hit real services, and how to run them).

**CI Testing:**

- CI runs tests with fail-fast flag (`-x`) - stops on first failure for faster feedback
- Test results are published to GitHub Actions UI
- Tests run automatically on pushes to `main`, `develop`, `release/*`, `hotfix/*` branches and pull requests

#### 4.1. Testing Docker Images During Development

You can test your Docker image on the test server while working on a feature branch by creating a development tag. This is useful for validating changes before merging to `develop`.

**Choosing a Version Number:**

Since the actual release version (major/minor/patch) isn't known until the release branch is created, use the following guidelines for dev tags:

- **Feature branches** (`feature/`): Typically indicate minor version updates (new features, backward compatible)
  - Use the next minor version: if latest is `v0.3.5`, use `v0.3.6-dev-<branch-name>` or `v0.4.0-dev-<branch-name>`
  - Use the branch name **without** the `feature/` prefix: `feature/improve-cicd` → `v0.3.6-dev-improve-cicd`
- **Hotfix branches** (`hotfix/`): Typically indicate patch version updates (bug fixes)
  - Use the next patch version: if latest is `v0.3.5`, use `v0.3.6-dev-<branch-name>`
  - Use the branch name **without** the `hotfix/` prefix: `hotfix/critical-bug` → `v0.3.6-dev-critical-bug`
- **Breaking changes**: Use the next major version: if latest is `v0.3.5`, use `v1.0.0-dev-<branch-name>`

**Note:** The version number in dev tags is just a placeholder for testing. The actual release version will be determined when creating the release branch based on the changes included. Dev tags are temporary and can use any version number that makes sense for your testing needs.

**Process:**

```bash
# On your feature branch (e.g., feature/improve-cicd), create a development tag
# Use the branch name without the type prefix (feature/, hotfix/, etc.)
git tag v0.3.6-dev-improve-cicd  # branch: feature/improve-cicd
git push origin v0.3.6-dev-improve-cicd
```

This automatically triggers the `publish.yml` workflow which will:

- Build Docker image: `username/repo:0.3.6-dev-improve-cicd`
- Deploy to the test server
- Allow you to validate your changes before creating a PR

**Republishing After Changes:**

Git tags are immutable once pushed. If you make changes and need to republish:

1. **Delete the old tag** (recommended for dev tags):

   ```bash
   git tag -d v0.3.6-dev-improve-cicd
   git push origin --delete v0.3.6-dev-improve-cicd
   # Then create and push a new tag with the same name
   git tag v0.3.6-dev-improve-cicd
   git push origin v0.3.6-dev-improve-cicd
   ```

2. **Or use an incrementing suffix** (if you want to keep history):
   ```bash
   git tag v0.3.6-dev-improve-cicd-1  # First iteration
   git push origin v0.3.6-dev-improve-cicd-1
   # After changes:
   git tag v0.3.6-dev-improve-cicd-2  # Second iteration
   git push origin v0.3.6-dev-improve-cicd-2
   ```

**Note:** Development tags are for testing purposes only and should not be used for releases. Delete them after testing if desired:

```bash
git tag -d v0.3.6-dev-improve-cicd
git push origin --delete v0.3.6-dev-improve-cicd
```

### 5. Committing

We follow a structured commit format inspired by [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/).

**IMPORTANT:** Run checks from the Docker workflow so local validation matches the repository runtime.

**Quick reference:**

- Format: `<type>(<scope>): <summary>`
- Run checks in container: `docker compose exec api pytest`

**Pre-commit hook behavior:** This repository installs a tracked host git hook at [`.githooks/pre-commit`](.githooks/pre-commit) via [`scripts/setup-host-dev-tools.sh`](scripts/setup-host-dev-tools.sh). Docker-side tooling is set up via [`scripts/setup-docker-dev-tools.sh`](scripts/setup-docker-dev-tools.sh). The hook shells into Docker and runs `pre-commit` inside the `api` container against staged files. **Commits fail if `api` is not running**—start the stack before committing: `docker compose up -d api`.

**Commit Types:**

- `feat` - New feature
- `fix` - Bug fix
- `refactor` - Code restructuring
- `docs` - Documentation update
- `chore` - Maintenance / infrastructure
- `test` - Adding or updating tests
- `style` - Formatting / lint-only changes
- `ci` - CI/CD pipeline changes

**Examples:**

- `feat(track): add audio fingerprint support`
- `fix(genre): handle duplicate genre names`
- `docs: update API documentation`
- `test(track): add test for track upload`
- `chore: update dependencies`

**Commit Message Guidelines:**

- Use imperative mood ("Add…", "Fix…", "Update…")
- Keep summary under ~70 characters
- Include issue/ticket IDs when applicable (e.g., `fix(#482): handle null values`)
- Be descriptive but concise

### 6. Pull Request Process

#### 6.1. Pre-PR Checklist

Before submitting a Pull Request, ensure the following checks are completed:

**1. Code Quality**

- ✅ Follow code style standards in [DEVELOPMENT.md](DEVELOPMENT.md)
- ✅ Code follows Django best practices
- ✅ Type hints are used where appropriate
- ✅ No debug statements or commented-out code
- ✅ With hooks installed: `pre-commit run --all-files` passes (or run `python3 scripts/check_prefer_strenum.py` before pushing)

**2. Tests**

- ✅ All tests pass: `docker compose exec api pytest` (or `pytest` after `python -m pip install -e ".[dev]"` locally)
- ✅ New features have corresponding tests
- ✅ Bug fixes include regression tests
- ✅ Tests follow the naming convention: `test_{scenario}_then_{expected_result}`
- ✅ Each test focuses on a single scenario

**3. Documentation**

- ✅ Update docstrings for new functions/classes (only when needed)
- ✅ Update README or other documentation if adding new features or changing behavior
- ✅ Add/update type hints where appropriate
- ✅ Update `CHANGELOG.md` with your changes in the `[Unreleased]` section
- ⚠️ Update CONTRIBUTING.md only in exceptional cases

**4. Git Hygiene**

- ✅ Commit messages follow the commit message convention
- ✅ Branch is up to date with target branch (`develop` for features, `main` for hotfixes)
- ✅ No accidental commits (large files, secrets, personal configs)
- ✅ Branch follows naming convention (`feature/`, `chore/`, `dependabot/`, `hotfix/`, `release/`) — see **Branching** / **Branch Protection**

**5. Branch Target**

- ✅ Feature branches target `develop` branch (NOT `main` - GitHub will block PRs to `main` from feature branches)
- ✅ Hotfix branches target `main` branch
- ✅ Release branches target both `main` and `develop` (maintainers only)
- ✅ Chore branches target `develop` branch (NOT `main`)

**Important:** GitHub Actions automatically enforces that PRs to `main` can only come from `hotfix/*` or `release/*` branches. If you try to create a PR from a `feature/*` or `chore/*` branch to `main`, the CI will fail.

#### For Maintainers (Before Opening/Merging a PR)

**All Contributor Checks Plus:**

**1. Code Review**

- ✅ Code follows project conventions and style
- ✅ Logic is sound and well-structured
- ✅ Error handling is appropriate
- ✅ Performance considerations addressed (if applicable)
- ✅ Django best practices are followed

**2. Testing Verification**

- ✅ CI tests pass on all platforms and Python versions
- ✅ Test coverage is adequate
- ✅ Edge cases are handled
- ✅ Integration with existing features works correctly

**3. Documentation Review**

- ✅ API changes are documented
- ✅ Breaking changes are clearly marked and documented
- ✅ Examples and usage are updated if needed
- ✅ Update CONTRIBUTING.md if changing development workflow

**4. Compatibility Verification**

- ✅ Breaking changes have proper versioning plan (major version bump)
- ✅ Backward compatibility maintained (unless intentional breaking change)
- ✅ Migration path documented for breaking changes
- ✅ Dependencies are up to date and compatible

**5. Final Checks**

- ✅ PR description is clear and complete
- ✅ All review comments are addressed
- ✅ No unresolved discussions
- ✅ Ready for release (if applicable)
- ✅ Branch targets correct base branch (`develop` for features, `main` for hotfixes)

#### 6.2. Opening a Pull Request

**Before opening a Pull Request, ensure you have completed the [Pre-PR Checklist](#61-pre-pr-checklist) above.**

##### PR Title Naming Convention

Pull Request titles must follow the same format as commit messages for consistency:

**Format:**

```
<type>(<optional-scope>): <short imperative description>
```

**Allowed Types:**

- `feat` — new feature
- `fix` — bug fix
- `refactor` — code restructuring
- `docs` — documentation update
- `chore` — maintenance / infrastructure (dependency updates, tooling setup, repository configuration)
- `perf` — performance improvement
- `style` — formatting / lint-only changes
- `ci` — CI/CD pipeline changes (GitHub Actions workflows, CI configuration)
- `test` — adding or updating tests

**Rules:**

- Use imperative mood ("Add…", "Fix…", "Update…")
- Keep it under ~70 characters
- Include issue/ticket IDs when applicable (e.g., `fix(#482): handle null values`)
- Avoid "WIP" in titles — use draft PRs instead
- Use lowercase for type and scope (e.g., `feat(track):`, not `Feat(Track):`)

**Note on Branch Prefixes vs PR Title Types:**

Branch prefixes (`feature/`, `chore/`, `hotfix/`, `release/`) are for branch organization and differ from PR title types:

- Branch `feature/add-flac-support` → PR title: `feat: add flac support` (use `feat`, not `feature`)
- Branch `chore/update-dependencies` → PR title: `chore: update dependencies` (use `chore`)
- Branch `hotfix/critical-bug` → PR title: `fix: critical bug` (use `fix`, not `hotfix`)
- Branch `release/v0.2.1` → PR title: `chore: prepare release v0.2.1` (use `chore`)

**Note on GitHub's Auto-Suggested Titles:**

GitHub automatically generates PR titles based on branch names. **GitHub's auto-suggested titles do not follow our convention**, so you must rewrite them to match the standard format:

- ❌ **GitHub suggestion**: `Feature/add album artist tag support` (from branch `feature/add-album-artist-tag-support`)
- ✅ **Correct format**: `feat(track): add album artist tag support`

- ❌ **GitHub suggestion**: `Chore/format code with ruff` (from branch `chore/format-code-with-ruff`)
- ✅ **Correct format**: `style: format code with ruff`

**Examples:**

- `feat(track): add audio fingerprint support`
- `fix(genre): correctly parse genre hierarchy`
- `docs: update contributing guide`
- `chore: update dependencies`
- `test(track): add test for track upload`
- `fix(#482): handle null search values`
- `style: format code with black`
- `ci: update GitHub Actions workflow`

##### PR Description

When opening a Pull Request, a template will be automatically provided. Ensure your PR description includes:

- ✅ Clear description of changes
- ✅ Reference related issues (e.g., "Fixes #123")
- ✅ Note any breaking changes
- ✅ Include testing instructions if applicable
- ✅ Specify the target branch (`develop` for features, `main` for hotfixes)

**Note:** The PR template (`.github/pull_request_template.md`) will guide you through the process and ensure all necessary information is included.

##### Breaking Changes

If your PR includes breaking changes:

- ✅ Breaking changes are clearly documented in the PR description
- ✅ Migration path is provided (if applicable)
- ✅ Breaking changes include proper versioning notes (for maintainers to handle)

##### PR Automations

When you open a Pull Request, several automations will run automatically:

- **Auto-labeling**: Labels are automatically added based on files changed in your PR:
  - **Component labels**: Automatically applied based on which parts of the codebase you've modified (e.g., `track`, `artist`, `album`, `genre`, `tag`, `playlist`, `play`, `user`, `spotify`, `musicbrainz`, `audio-fingerprinting`, `filtering`, `middleware`, `serializer`, `model`, `view`, `exception`, `utils`)
  - **Type labels**: Automatically applied based on file types (e.g., `test`, `documentation`, `ci`, `dependencies`, `docker`, `scripts`, `migration`, `settings`, `admin`, `fixtures`, `logging`, `management`, `validator`)
  - The labeler configuration is defined in `.github/labeler.yml` and runs via the `.github/workflows/labeler.yml` workflow
  - Multiple labels can be applied to a single PR if it touches multiple areas
- **Manual labels**: You should still add type labels (`bug`, `enhancement`, `feature`) and priority labels manually, as these can't be determined from file paths
- **Auto-assignment**: For contributor PRs (not maintainer PRs), reviewers are automatically assigned
- **CI/CD checks**: Automated tests run on your PR
- **Welcome message**: First-time contributors receive a welcome message with helpful links

These automations help streamline the review process and ensure consistency across the project.

**Note:** If you add a new feature or component, you can suggest updates to `.github/labeler.yml` via a PR to ensure future changes to that component are automatically labeled correctly.

##### GitHub Actions Workflows

The project uses focused, reusable GitHub Actions workflows for CI/CD. For a full description of each workflow (triggers, steps, environments), see [GitHub Actions Workflows](docs/workflows.md).

**Test Workflow** (`.github/workflows/test.yml`):

- Runs automatically on pushes to `main` and `develop` branches
- Runs automatically on pull requests targeting `main` or `develop`
- Executes the full test suite with pytest
- Publishes test results to GitHub Actions UI

**Publish Workflow** (`.github/workflows/publish.yml`):

- Runs on **push to `main`** (staging, TEST env) or **push of version tags** (e.g. `v0.2.1`; prerelease tags → staging/TEST, release tags → production/PROD)
- Orchestrates the release process: collects/commits static files, builds and pushes Docker image, deploys to staging or production

**Other Workflows**:

- `build-and-push.yml` - Builds and pushes Docker images (reusable)
- `deploy.yml` - Handles server deployment (reusable)
- `static-files.yml` - Collects and commits static files (reusable)
- `branch-protection.yml` - Enforces Git Flow branching rules
- `labeler.yml` - Automatically labels PRs based on changed files

**Workflow Philosophy**:

- **Separation of concerns**: Tests run on every change, publishing only on releases
- **Reusability**: Individual workflows can be called independently or as part of a pipeline
- **Maintainability**: Each workflow has a single, focused responsibility
- **Flexibility**: All workflows support manual triggering for debugging and testing

### 7. Releasing _(For Maintainers)_

Releases are created from the `main` branch using **strict Git Flow**.

Quick release process:

1. **Ensure `develop` is ready for release** - All features for the release should be merged into `develop`

   ```bash
   git checkout develop
   git pull origin develop
   ```

2. **Create a release branch from `develop`**

   ```bash
   git checkout -b release/v0.2.1
   git push origin release/v0.2.1
   ```

3. **On the release branch, prepare the release:**

   - **Automated (recommended):** from the repo root, with `bump-my-version` on `PATH` (same pin as dev deps in [`pyproject.toml`](pyproject.toml), currently `bump-my-version==1.3.0` — e.g. `pipx install bump-my-version==1.3.0`, a pyenv (or other) Python where `pip install -e ".[dev]"` is allowed, or run bump steps inside the Compose `api` dev image where dev extras are installed). No project `.venv` is required.

     ```bash
     python3 scripts/prepare_release_bump.py patch   # or: minor | major
     ```

     This sets the live `## [Unreleased]  <!-- release -->` marker (only the heading **after** the maintainer Note—not the fenced example), runs [bump-my-version](https://github.com/callowayproject/bump-my-version), runs `python scripts/fix_changelog_after_bump.py`, and adds an empty `## [Unreleased]` above the new version section. By default it passes `--allow-dirty` so you can commit once at the end; use `--no-allow-dirty` if you need a clean tree.

   - **Manual sequence** (same end state): set the live heading after the Note to `## [Unreleased]  <!-- release -->`, then `bump-my-version bump patch` (or `bump minor` / `bump major`; add `--allow-dirty` if needed), then `python scripts/fix_changelog_after_bump.py`, then ensure an empty `## [Unreleased]` sits above `## [vX.Y.Z] - …`. Release bump file rules live under `[tool.bumpversion]` in [`pyproject.toml`](pyproject.toml); the changelog rule only replaces that one heading line — everything below it until the next `## [` belongs to that release.

   - Review and finalize `CHANGELOG.md`:

     - Review the new version entry and the content that was under `[Unreleased]`
     - Review and consolidate entries if needed

   - Make any final bug fixes or adjustments on the release branch
   - Ensure all tests pass: `pytest`

4. **Merge release branch into `main`** (via PR from `release/*` to `main`, or locally if your process allows):

   ```bash
   git checkout main
   git pull origin main
   git merge --no-ff release/v0.2.1
   git push origin main
   ```

5. **Tag the release on `main`**

   ```bash
   git tag v0.2.1
   git push origin v0.2.1
   ```

   **Important:** The tag version must match the version in `VERSION` and `CHANGELOG.md` (use the `v` prefix, e.g. `v2.1.1`).

6. **Clean up pre-release tags**

   Remove all pre-release tags for this version (e.g. `-dev`, `-staging`, `-test`, `-rc`, `-beta`, `-alpha`) from local and remote:

   ```bash
   ./scripts/remove_prerelease_tags.sh
   ```

   The script uses the version from the `VERSION` file (same as after a release bump). You can also pass a version explicitly: `./scripts/remove_prerelease_tags.sh 0.2.1`.

   **Note:** Pre-release tags are temporary and should be cleaned up after the release is published to keep the repository clean.

7. **Merge release branch back into `develop`** (to keep develop up to date)

   ```bash
   git checkout develop
   git pull origin develop
   git merge --no-ff release/v0.2.1
   git push origin develop
   ```

8. **Delete the release branch** (locally and remotely)

   ```bash
   git branch -d release/v0.2.1
   git push origin --delete release/v0.2.1
   ```

9. **CI/CD will automatically:**

   When you push the version tag (step 5), the `publish.yml` workflow will automatically:

   - Collect and commit static files
   - Build and push Docker image to GHCR (`ghcr.io`)
   - Deploy to the test server

   See the [GitHub Actions Workflows](#github-actions-workflows) section above for details on the workflow structure.

**Hotfix Release Process:**

For urgent production fixes:

1. Create hotfix branch from `main`:

   ```bash
   git checkout main
   git pull origin main
   git checkout -b hotfix/critical-bug-fix
   ```

2. Make the fix and update `CHANGELOG.md` in the `[Unreleased]` section

3. Merge hotfix into `main`:

   ```bash
   git checkout main
   git merge --no-ff hotfix/critical-bug-fix
   git tag v0.2.2  # Increment patch version
   git push origin main --tags
   ```

4. Merge hotfix into `develop`:

   ```bash
   git checkout develop
   git merge --no-ff hotfix/critical-bug-fix
   git push origin develop
   ```

5. Delete the hotfix branch

## 🪪 License & Attribution

All contributions are made under the project's Apache License 2.0.

You retain authorship of your code; the project retains redistribution rights under the same license. See the [LICENSE](LICENSE) file for details.

## 📜 Code of Conduct

This project adheres to a Code of Conduct to ensure a welcoming and inclusive environment for all contributors. Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md) when participating in this project.

Our Code of Conduct is based on the [Contributor Covenant](https://www.contributor-covenant.org), version 2.1. It outlines our expectations for behavior, unacceptable behavior, and how to report violations.

## 📋 TODO List

This project maintains a [TODO list](TODO.md) that tracks future work, improvements, and testing tasks. The TODO list is organized by priority and category:

- **Features** - New functionality and enhancements
- **Testing & Quality** - Test coverage, quality improvements, and validation
- **Infrastructure** - CI/CD, deployment, monitoring, and technical improvements
- **Documentation** - Documentation improvements and guides

**Important Notes**:

- **Maintainers are responsible** - Project maintainers are responsible for maintaining and updating the TODO list
- **Contributors should NOT modify it** - Contributors should not edit the TODO list directly
- **Suggest tasks via issues** - If you'd like to suggest a new task or work on an existing one, please open a GitHub issue first for discussion
- **Updated during releases** - Maintainers align and update the TODO list when releasing new versions based on project priorities, completed work, and community feedback

## 🌍 Contact & Discussions

You can open:

- **Issues** → bug reports or new ideas
  - Use the [Bug Report template](.github/ISSUE_TEMPLATE/bug_report.yml) for reporting bugs
  - Use the [Feature Request template](.github/ISSUE_TEMPLATE/feature_request.yml) for suggesting new features
- **Discussions** → suggestions, architecture, or music-related topics

Let's make this API grow together 🌱
