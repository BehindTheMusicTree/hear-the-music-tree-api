# python-project-standards alignment

Organization-wide Python tooling and style baselines live in [BehindTheMusicTree/python-project-standards](https://github.com/BehindTheMusicTree/python-project-standards). This API does **not** call org reusable workflows for tests or lint: **pre-commit runs inline** in [`.github/workflows/test.yml`](../../.github/workflows/test.yml), and the **pytest** job stays in this repository because it needs PostgreSQL, Audio Fingerprinter containers, GitHub Environment secrets, and project scripts.

For reference, libraries may call org **`reusable-pre-commit`** (python-project-standards **v3+** no longer ships a reusable test matrix—tests stay in each repo). That pattern does not replace this API’s integration CI.

Org-wide Python development policy is in [python-project-standards `docs/development.md`](https://github.com/BehindTheMusicTree/python-project-standards/blob/main/docs/development.md) (including [string enumerations](https://github.com/BehindTheMusicTree/python-project-standards/blob/main/docs/string-enums.md)).

## Local lint stack (audiometa-python–style)

Pre-commit includes **`verify-python-project-standards`** ([`scripts/verify-standards.sh`](../../scripts/verify-standards.sh)), aligned with [python-project-standards](https://github.com/BehindTheMusicTree/python-project-standards) templates.

CI runs `pre-commit run --all-files` from a checkout with `pip install -e ".[dev]"` (same pins as local dev). The repo’s [`.pre-commit-config.yaml`](../../.pre-commit-config.yaml) follows the same **hook layout** as audiometa-python (version check, generic YAML/JSON/TOML checks, shellcheck, `no-assert`, ruff-format, ruff, isort, mypy with django-stubs, pydocstringformatter, long-comment fixer, Prettier on Markdown, optional PowerShell analyzers), plus this project’s **`prefer-strenum`** hook.

Tool versions for ruff / isort / mypy / pydocstringformatter are pinned in [`pyproject.toml`](../../pyproject.toml) (`[project.optional-dependencies] dev`). Ruff rule **selection** matches audiometa; a set of **ignored rules** documents Django/DRF friction and is meant to be reduced over time. Mypy uses the **django-stubs** plugin with **`ignore_missing_imports = true`** and relaxed strictness until the codebase moves toward audiometa-level strict typing.
