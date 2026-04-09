# python-project-standards (Tier B)

This API repository follows **Tier B** in [BehindTheMusicTree/python-project-standards](https://github.com/BehindTheMusicTree/python-project-standards):

- **Shared:** pre-commit checks in CI via [`reusable-pre-commit.yml` @ `v1.0.0`](https://github.com/BehindTheMusicTree/python-project-standards/blob/v1.0.0/.github/workflows/reusable-pre-commit.yml) (see `.github/workflows/test.yml`).
- **Local:** the **pytest** job stays in this repository because it needs PostgreSQL, Audio Fingerprinter containers, GitHub Environment secrets, and project scripts.

The workflow uses **`@v1.0.0`**, matching the repo root [`STANDARDS_VERSION`](../../STANDARDS_VERSION). When upgrading standards, bump both the `uses: …@…` ref and `STANDARDS_VERSION`, then read [Upstream `CHANGELOG.md`](https://github.com/BehindTheMusicTree/python-project-standards/blob/main/CHANGELOG.md) and [versioning](https://github.com/BehindTheMusicTree/python-project-standards/blob/main/docs/versioning.md).

For libraries with a multi-OS test matrix, use Tier A (`reusable-lint` + `reusable-test-matrix`) instead; that pattern does not replace this API’s integration CI.

## Local lint stack (audiometa-python–style)

CI runs `pre-commit run --all-files` from a checkout with `pip install -e ".[dev]"` (same pins as local dev). The repo’s [`.pre-commit-config.yaml`](../../.pre-commit-config.yaml) follows the same **hook layout** as audiometa-python (version check, generic YAML/JSON/TOML checks, shellcheck, `no-assert`, ruff-format, ruff, isort, mypy with django-stubs, pydocstringformatter, long-comment fixer, Prettier on Markdown, optional PowerShell analyzers), plus this project’s **`prefer-strenum`** hook.

Tool versions for ruff / isort / mypy / pydocstringformatter are pinned in [`pyproject.toml`](../../pyproject.toml) (`[project.optional-dependencies] dev`). Ruff rule **selection** matches audiometa; a set of **ignored rules** documents Django/DRF friction and is meant to be reduced over time. Mypy uses the **django-stubs** plugin with **`ignore_missing_imports = true`** and relaxed strictness until the codebase moves toward audiometa-level strict typing.
