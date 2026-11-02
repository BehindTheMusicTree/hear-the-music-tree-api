# Hear The Music Tree API

Django/DRF API for users and their uploaded tracks. `README.md` and `CONTRIBUTING.md` are the authoritative setup and contribution references; the developer Compose stack and launch procedure live in `.agents/skills/launch/SKILL.md`. `UploadedTrack` is the app’s concrete track type; recording refers to a MusicBrainz entity. Shared model and HTTP behavior live in genre-kit and api-kit.

## Validation

CI runs `pre-commit run --all-files` and Docker-backed pytest on `hear/test/` (see `.github/workflows/test.yml`). Use the documented setup and avoid launching or changing databases unless requested.

## Task-specific guidance

Before any substantive repository change, read `.agents/rules/changelog-alignment.md` and update `CHANGELOG.md` as required. For PR and release work read `CONTRIBUTING.md` and the relevant sources `.agents/rules/git-flow-workflow.md`, `.agents/rules/commit-message-convention.md`, `.agents/rules/pull-request-convention.md`, `.agents/rules/pr-description-in-separate-file.md`, and `.agents/rules/pre-pr-checklist.md`. For changelog work also read `.agents/rules/changelog-best-practices.md` and `.agents/rules/changelog-entry-placement.md`. For issue work read `.agents/rules/issue-template-usage.md` and `.agents/rules/issue-description-in-separate-file.md`; for dependency changes read `.agents/rules/dependency-pinning.md`.

## Scoped project rules

Before working on `**/*.py`, read `.agents/rules/use-pipe-none.md`.
Before working on `hear/**/*.py`, read `.agents/rules/use-custome-validation-exception.md`.
Before working on `hear/view/**/*.py`, read `.agents/rules/openapi-validation-documentation.md`.
Before working on `hear/**/*.py`, read `.agents/rules/strenum-string-enums.md`.
Before working on `hear/test/**/*.py`, read `.agents/rules/test-structure.md`.
Before working on `hear/**/*.py`, read `.agents/rules/no-useless-comments.md`.
Before working on `hear/**/*.py`, read `.agents/rules/private-resource-filtering.md`.
Before working on `hear/test/**/*.py`, read `.agents/rules/divide-test-cases.md`.
Before working on `hear/test/**/*.py`, read `.agents/rules/test-naming-convention.md`.
Before working on `hear/test/**/*.py`, read `.agents/rules/use-assert-not-assertequal.md`.
Before working on `hear/**/*.py`, read `.agents/rules/field-name-constants.md`.
Before working on `hear/**/*.py`, read `.agents/rules/one-class-per-file.md`.

Claude `paths:` metadata is not a Codex loader. Graphify can be used when installed and useful.
