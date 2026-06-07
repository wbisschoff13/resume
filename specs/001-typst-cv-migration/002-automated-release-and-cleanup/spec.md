# FEATURE_SPECIFICATION: specs/001-typst-cv-migration/002-automated-release-and-cleanup/spec.md

## SYSTEM_TOPOLOGY_MAPPING

| Component | Path | Action |
|-----------|------|--------|
| CI Release Workflow | `.github/workflows/release.yml` | Migrate to `typst-community/setup-typst@v5` with matrix strategy |
| Git Ignore Rules | `.gitignore` | Add Typst cache/build exclusion patterns |
| Legacy LaTeX Sources | `*.tex`, `*.cls` (all subdirectories including `example/`) | Delete |
| Legacy Docker Assets | `docker/Dockerfile`, `docker/build.sh` | Delete |
| Legacy Dev Configs | `.devcontainer/*`, `.vscode/*` | Delete |
| Content & Template | `content/data.typ`, `lib/template.typ` | **Untouched** (owned by ISS-001) |
| Advisory Files | `analysis/`, `amazon-lp-cheatsheet-draft.md` | **Untouched** (explicit exclusion) |

**Execution Hosts**: GitHub Actions (Ubuntu runner), Local Git CLI.

## THE_PROBLEM_CONTRACT

As a maintainer, I need the Typst CV generation to be fully automated via GitHub Actions on semantic-version tag pushes (`v*.*.*`), and I need all legacy LaTeX artifacts and configurations removed from the repository — including the `example/` directory — to prevent build confusion and scope creep, ensuring a clean, Typst-only codebase. Advisory files (`analysis/`, `amazon-lp-cheatsheet-draft.md`) are explicitly retained as-is.

## SCOPE_BOUNDARIES

### Hard Inclusions

1. Migrate `.github/workflows/release.yml` to use `typst-community/setup-typst@v5` with a matrix strategy for multi-platform builds.
2. Configure the release workflow to trigger on git tags matching the pattern `v*.*.*` (semantic versioning).
3. Produce a release artifact named `cv.pdf` attached to the GitHub Release.
4. Update `.gitignore` to exclude Typst cache (`.typst/`) and build artifacts.
5. Remove **all** `.tex` and `.cls` files from the repository, including those in the `example/` directory.
6. Remove `docker/Dockerfile`, `docker/build.sh`, `.devcontainer/*`, and `.vscode/*`.
7. Clean up any empty `docker/`, `.devcontainer/`, and `.vscode/` directories after file removal.

### Defensive Exclusions

1. Do **NOT** modify `content/data.typ` or `lib/template.typ` (under active development by ISS-001).
2. Do **NOT** delete `analysis/` directory or `amazon-lp-cheatsheet-draft.md` (advisory files, retained as-is).
3. Do **NOT** modify any Typst files outside the scope of `.gitignore` updates.
4. Do **NOT** introduce new `.tex` or `.cls` files under any circumstances.
5. Do **NOT** alter the repository's branch protection rules or tag conventions.

## PERFORMANCE_CONSTRAINTS

| Constraint | Target | Rationale |
|------------|--------|-----------|
| CI Matrix Job Duration | < 5 minutes per job | Typst compilation should be fast; setup and artifact upload are the only overhead |
| Release Artifact Size | < 10 MB | Single-page CV PDF, no embedded fonts beyond defaults |
| Git Clone (CI) | < 30 seconds | Shallow clone sufficient for Typst compilation |
| Tag-to-Release Latency | < 10 minutes total | End-to-end from tag push to release published |

## MULTI_TIERED_VERIFICATION_TARGETS

### Static Verification

- `find . -name "*.tex" -o -name "*.cls" | wc -l` — must return `0` (no `.tex` or `.cls` files anywhere, including `example/`)
- `test ! -f docker/Dockerfile && test ! -f docker/build.sh` — must return zero (neither file exists)
- `test ! -d .devcontainer && test ! -d .vscode` — must return zero (neither directory exists)
- `grep "\.typst/" .gitignore` — must return a match (Typst cache pattern present)
- `grep "typst-community/setup-typst@v5" .github/workflows/release.yml` — must return a match

### Integration Verification

1. Push a test tag `v0.0.1-test` to trigger the release workflow.
2. Verify the GitHub Actions matrix build completes successfully (all platform jobs green).
3. Verify a GitHub Release is created with `cv.pdf` attached as an asset.
4. Verify `cv.pdf` is a valid PDF with expected content (manual or automated visual check).

### Regression Gates

- `mise run check` passes with no regressions (Typst compilation succeeds on the cleaned repository).
- No LaTeX-related references remain in CI configuration or repository files (excluding advisory documents).

## ATDD_ACCEPTANCE_CRITERIA_LEDGER

### US-001-CI: Migrate CI Release Pipeline to Typst

* **Upstream Requirement Traceability**: FR-004-CI (GitHub Actions Pipeline Migration)
* **Acceptance Criteria**: AC-004-CI-01, AC-004-CI-02

**Scenario 1: Workflow trigger on semantic version tag**

- **Given** the repository has an updated `.github/workflows/release.yml` using `typst-community/setup-typst@v5`
- **And** the workflow `on.push.tags` filter matches the pattern `v*.*.*`
- **When** a maintainer pushes a git tag `v1.0.0`
- **Then** the GitHub Actions release workflow is triggered automatically
- **And** the workflow completes all matrix jobs successfully

**Scenario 2: Matrix build produces valid PDF artifact**

- **Given** the release workflow is triggered by a matching tag
- **When** the matrix build job executes Typst compilation
- **Then** a `cv.pdf` file is generated successfully
- **And** the PDF is attached as a release asset to the corresponding GitHub Release

**Scenario 3: Non-version tags do not trigger release**

- **Given** the release workflow is configured to trigger only on `v*.*.*` tags
- **When** a maintainer pushes a tag that does not match the pattern (e.g., `test`, `draft-1`)
- **Then** the release workflow is **not** triggered

**Scenario 4: Typst compilation failure blocks release**

- **Given** the release workflow is triggered by a matching tag
- **When** Typst compilation fails (e.g., due to a syntax error in `content/data.typ`)
- **Then** the workflow job fails with a non-zero exit code
- **And** no GitHub Release is created
- **And** no `cv.pdf` artifact is uploaded

### US-002-CLEANUP: Remove All Legacy LaTeX Artifacts

* **Upstream Requirement Traceability**: FR-005-CLEANUP (LaTeX Artifact Removal)
* **Acceptance Criteria**: AC-005-CLEANUP-01, AC-005-CLEANUP-02

**Scenario 1: Complete removal of all .tex and .cls files**

- **Given** the repository currently contains `.tex` and `.cls` files across multiple directories including `example/`
- **When** the cleanup is executed
- **Then** `find . -name "*.tex" -o -name "*.cls"` returns zero results
- **And** no `.tex` or `.cls` file exists anywhere in the repository

**Scenario 2: Removal of Docker build infrastructure**

- **Given** the repository contains `docker/Dockerfile` and `docker/build.sh`
- **When** the cleanup is executed
- **Then** neither `docker/Dockerfile` nor `docker/build.sh` exists
- **And** the `docker/` directory is removed if empty

**Scenario 3: Removal of dev tooling configurations**

- **Given** the repository contains `.devcontainer/` and `.vscode/` directories
- **When** the cleanup is executed
- **Then** neither `.devcontainer/` nor `.vscode/` exists in the repository

**Scenario 4: Content and template files are preserved**

- **Given** the repository contains `content/data.typ` and `lib/template.typ`
- **When** the cleanup is executed
- **Then** both `content/data.typ` and `lib/template.typ` remain unchanged
- **And** `mise run check` passes without errors

**Scenario 5: Advisory files are preserved**

- **Given** the repository contains `analysis/` and `amazon-lp-cheatsheet-draft.md`
- **When** the cleanup is executed
- **Then** both `analysis/` and `amazon-lp-cheatsheet-draft.md` remain untouched

### US-003-GITIGNORE: Update .gitignore for Typst Artifacts

* **Upstream Requirement Traceability**: FR-004-CI (GitHub Actions Pipeline Migration)
* **Acceptance Criteria**: AC-004-CI-01

**Scenario 1: Typst cache directory is excluded**

- **Given** the `.gitignore` file exists in the repository root
- **When** the `.gitignore` is updated with Typst-specific exclusion patterns
- **Then** `.typst/` is listed in `.gitignore`
- **And** running `git status` after a local Typst compilation shows no untracked files from `.typst/`

**Scenario 2: Build artifacts are excluded**

- **Given** the `.gitignore` is updated for Typst
- **When** a Typst build produces output artifacts
- **Then** no build output files appear in `git status` as untracked

## SYSTEM_STATUS_SUMMARY

| Key | Value |
|-----|-------|
| STATUS | DRAFT |
| EPIC_SLUG | 001-typst-cv-migration |
| BRANCH_NAME | feat/001-typst-cv-migration/002-automated-release-and-cleanup |
| SPEC_PATH | specs/001-typst-cv-migration/002-automated-release-and-cleanup/spec.md |
| ISSUE_ID | ISS-002 |
| NEXT_ACTION | Run post-script to validate, commit, and advance ledger state |
