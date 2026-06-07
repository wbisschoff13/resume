# Implementation Tasks: feat/001-typst-cv-migration/002-automated-release-and-cleanup

## Phase 1: Repository Cleanup
**Goal**: Remove all legacy LaTeX artifacts, dev tooling configurations, and Docker infrastructure; update `.gitignore` for Typst-specific exclusions. Delivers US-002-CLEANUP and US-003-GITIGNORE.

### Tasks

- [x] T001: Remove all legacy LaTeX artifacts and dev configurations
  - **Type**: Migration
  - **Mode**: IMMEDIATE
  - **Verification**: `[ $(find . -name "*.tex" -o -name "*.cls" | wc -l) -eq 0 ] && test ! -f docker/Dockerfile && test ! -f docker/build.sh && test ! -d .devcontainer && test ! -d .vscode && mise run check`
  - **Estimated Time**: 45 minutes
  - **Files**:
    - `W_Bisschoff_CV.tex`
    - `W_Bisschoff_CV_embedded.tex`
    - `W_Bisschoff_CV_enterprise.tex`
    - `W_Bisschoff_Cover_Letter.tex`
    - `W_Bisschoff_Cover_Letter_embedded.tex`
    - `W_Bisschoff_Cover_Letter_enterprise.tex`
    - `written_interview.tex`
    - `cv/ai_policy.tex`
    - `cv/education.tex`
    - `cv/experience.tex`
    - `cv/job_target.tex`
    - `cv/opensource.tex`
    - `cv/projects.tex`
    - `cv/skills.tex`
    - `cv/summary.tex`
    - `cv/embedded/education.tex`
    - `cv/embedded/experience.tex`
    - `cv/embedded/projects.tex`
    - `cv/embedded/skills.tex`
    - `cv/embedded/summary.tex`
    - `cv/enterprise/education.tex`
    - `cv/enterprise/experience.tex`
    - `cv/enterprise/projects.tex`
    - `cv/enterprise/skills.tex`
    - `cv/enterprise/summary.tex`
    - `example/committees.tex`
    - `example/education.tex`
    - `example/experience.tex`
    - `example/extracurricular.tex`
    - `example/honors.tex`
    - `example/presentation.tex`
    - `example/summary.tex`
    - `example/writing.tex`
    - `awesome-cv.cls`
    - `docker/Dockerfile`
    - `docker/build.sh`
    - `.devcontainer/devcontainer.json`
    - `.devcontainer/Dockerfile`
    - `.devcontainer/postCreateCommand.sh`
    - `.vscode/extensions.json`
    - `.vscode/settings.json`
    - `.vscode/tasks.json`
  - **Rationale**: Each file maps to US-002-CLEANUP (FR-005-CLEANUP) Scenarios 1-5. All `.tex` files must be removed (Scenario 1 — including `example/` per HITL decision). `docker/` (Scenario 2), `.devcontainer/` and `.vscode/` (Scenario 3) must be deleted. `content/data.typ` and `lib/template.typ` are excluded per Scenario 4; `analysis/` and `amazon-lp-cheatsheet-draft.md` are excluded per Scenario 5.
  - **Details**:
    - **Implementation**: Run `git rm` on all 35 `.tex` files across `cv/`, `example/`, and root directories
    - **Implementation**: Run `git rm` on `awesome-cv.cls` class file
    - **Implementation**: Run `git rm -r` on `docker/`, `.devcontainer/`, and `.vscode/` directories
    - **Implementation**: Remove empty parent directories (`cv/embedded/`, `cv/enterprise/`, `cv/`, `example/`) if they become empty after deletion
    - **Edge Cases**: Verify `content/data.typ` and `lib/template.typ` are not modified or deleted (diff before/after)
    - **Edge Cases**: Verify `analysis/` directory and `amazon-lp-cheatsheet-draft.md` are untouched
    - **Refactor**: Remove any LaTeX-related patterns from `.gitignore` that are no longer relevant (e.g., `*.aux`, `*.out`)
    - **Acceptance**: `find . -name "*.tex" -o -name "*.cls"` returns zero results; `mise run check` passes; no Typst source files affected

- [x] T002: Update .gitignore for Typst build artifact exclusion
  - **Type**: Config
  - **Mode**: IMMEDIATE
  - **Verification**: `grep "\.typst/" .gitignore && grep "cv.*\.pdf" .gitignore`
  - **Estimated Time**: 20 minutes
  - **Dependency**: T001
  - **Files**:
    - `.gitignore`
  - **Rationale**: Maps to US-003-GITIGNORE (FR-004-CI), Scenarios 1-2. The `.typst/` cache directory and generated PDF artifacts must be excluded from version control to prevent accidental commits of build output. Run after T001 so LaTeX-specific patterns can be cleaned up.
  - **Details**:
    - **Implementation**: Verify `.typst/` pattern is present and uncommented in `.gitignore`
    - **Implementation**: Verify PDF artifact patterns (`cv.pdf`, `cv_embedded.pdf`, `cv_enterprise.pdf`, `cover_letter.pdf`) are present
    - **Implementation**: Remove stale LaTeX auxiliary patterns (`*.aux`, `*.out`, `*.synctex.gz`) that are no longer relevant post-cleanup
    - **Edge Cases**: Ensure no Typst source files (`*.typ`) are matched by any exclusion pattern
    - **Acceptance**: `grep` confirms `.typst/` in `.gitignore`; `git status` after a local Typst compilation shows no untracked cache or build artifacts

---

## Phase 2: CI Pipeline Migration
**Goal**: Replace the LaTeX-based release pipeline with a Typst-based matrix build. Delivers US-001-CI.

### Tasks

- [x] T003: Migrate release workflow to Typst with matrix build strategy
  - **Type**: Migration
  - **Mode**: IMMEDIATE
  - **Verification**: `grep "typst-community/setup-typst@v5" .github/workflows/release.yml && grep "cv\.typ" .github/workflows/release.yml && grep "v\*\.\*\.\*" .github/workflows/release.yml`
  - **Estimated Time**: 60 minutes
  - **Dependency**: T001
  - **Files**:
    - `.github/workflows/release.yml`
  - **Rationale**: Maps to US-001-CI (FR-004-CI), Scenarios 1-4. The existing workflow uses `xu-cheng/latex-action@v3` and must be replaced with `typst-community/setup-typst@v5`. Tag triggers must narrow to `v*.*.*` only (per HITL decision). Matrix strategy covers all entry points (`cv.typ`, `cv_embedded.typ`, `cv_enterprise.typ`, `cover_letter.typ`). Depends on T001 because the workflow references entry point filenames that exist only after cleanup.
  - **Details**:
    - **Implementation**: Replace all `xu-cheng/latex-action@v3` steps with a single `typst-community/setup-typst@v5` setup step followed by matrix build steps
    - **Implementation**: Define a matrix strategy with entry points `cv.typ`, `cv_embedded.typ`, `cv_enterprise.typ`, `cover_letter.typ`
    - **Implementation**: Update `on.push.tags` to match only `v*.*.*` (remove calver pattern `[0-9][0-9][0-9][0-9].[0-9][0-9]*`)
    - **Implementation**: Update artifact paths in `softprops/action-gh-release@v2` to match Typst output filenames (`cv.pdf`, `cv_embedded.pdf`, `cv_enterprise.pdf`, `cover_letter.pdf`)
    - **Implementation**: Add a font installation step to mitigate RSK-002 (CI build failure due to missing custom fonts on Ubuntu runner)
    - **Edge Cases**: Workflow must fail with non-zero exit if any matrix job fails — verify `fail-fast: false` or equivalent per Scenario 4
    - **Refactor**: Simplify version extraction step to remove calver logic; keep only semver tag parsing
    - **Acceptance**: `grep` confirms `setup-typst@v5` usage; tag filter matches `v*.*.*` only; matrix covers all 4 entry points; manual CI run on test tag produces valid PDFs

---

## Implementation Strategy
**Execution Order**:
1. Phase 1 (T001 → T002) — Clean the repository of all legacy artifacts before modifying CI
2. Phase 2 (T003) — Migrate the CI pipeline on the cleaned codebase

**Critical Dependency Chains**:
- T001 must complete before T002 (gitignore cleanup of stale patterns depends on removed files)
- T001 must complete before T003 (workflow references entry point filenames that exist after cleanup)

**Risk Hotspots**:
- RSK-002 (CI): Missing custom fonts on Ubuntu runner may cause Typst compilation failures — mitigated in T003 by adding font installation step
- Legit CV directory structure: `cv/embedded/`, `cv/enterprise/` directories may become empty after `.tex` file removal; verify no `.typ` files exist in those paths before deleting directories

**Merge Conflict Boundaries**:
- `.gitignore` touched by Phase 1 (T002) — no other phases touch this file
- `.github/workflows/release.yml` touched by Phase 2 (T003) — no other phases touch this file
- All `.tex` file deletions in T001 are independent of any other in-flight work (ISS-001 owns `content/data.typ` and `lib/template.typ` only)