# Implementation Tasks: feat/002-yaml-content-layer/002-legacy-cleanup-ci-verification

## Phase 1: Legacy Artifact Removal & Pipeline Verification
**Goal**: Remove superseded legacy markdown files, port any remaining STAR story data to YAML, and verify CI/CD pipeline and build toolchain are fully compatible with the YAML-driven architecture.

### Tasks

- [x] T001: Legacy File Removal and Post-Cleanup Build Integrity
  - **Type**: Migration
  - **Mode**: IMMEDIATE
  - **Verification**: `test ! -f content/master-list.md && test ! -f content/star-stories.md && mise run check && typst fmt --check content/data.typ lib/template.typ`
  - **Estimated Time**: 60 minutes
  - **Files**:
    - `content/master-list.md`
    - `content/star-stories.md`
    - `content/star-stories.yaml`
  - **Rationale**: `content/master-list.md` and `content/star-stories.md` are the two legacy files targeted for removal by US-001 (Scenarios 1 & 2). `content/star-stories.yaml` is the canonical YAML target that receives any STAR story data not yet migrated from `star-stories.md`. No `.typ` files reference either legacy file (confirmed via grep), so no source modifications are needed for dangling reference resolution (US-001 Scenario 3).
  - **Details**:
    - **Implementation**: Delete `content/master-list.md` via `git rm` — fully superseded by `content/experience.yaml` + `content/star-stories.yaml`
    - **Implementation**: Compare `content/star-stories.md` against `content/star-stories.yaml` to identify STAR stories present in the `.md` but absent from the `.yaml`; append missing data to `content/star-stories.yaml` preserving its existing schema per `data-model.md`
    - **Implementation**: Delete `content/star-stories.md` via `git rm` after confirming all data is ported
    - **Implementation**: Run `git grep -c "master-list\|star-stories.md" -- "*.typ"` to confirm zero dangling references (expected: zero, already verified in exploration)
    - **Implementation**: Run `mise run check` to confirm all 5 entry points compile successfully after file removal
    - **Implementation**: Run `typst fmt --check content/data.typ lib/template.typ` to confirm formatting compliance
    - **Edge Cases**: If `star-stories.md` contains stories with no `id` field, generate a slug from the story title using the convention `^[a-z0-9-]+$` from the data model; if a story already exists in YAML by content match, skip the duplicate
    - **Acceptance**: Both legacy `.md` files are removed from git tracking, `star-stories.yaml` contains 100% of the STAR story data, `mise run check` passes, `typst fmt --check` passes, and `git grep` returns zero matches for either deleted filename in `.typ` sources

- [ ] T002: CI Pipeline and Build Determinism Verification
  - **Type**: Config
  - **Mode**: IMMEDIATE
  - **Verification**: `grep -rn "http://\|https://" content/*.yaml lib/*.typ || echo "no network refs" && grep -A5 "matrix:" .github/workflows/release.yml | grep -q "cv.typ" && mise run check`
  - **Estimated Time**: 30 minutes
  - **Dependency**: T001
  - **Files**:
    - `.github/workflows/release.yml`
    - `.mise.toml`
  - **Rationale**: `.github/workflows/release.yml` is the CI workflow that must be verified to compile all variants using the YAML adapter layer per US-002 (Scenarios 1 & 2). `.mise.toml` defines the local build tasks (`check`, `build`, etc.) that must pass after legacy file removal per US-002 (Scenario 3) and US-003 (Scenario 1). Neither file requires modification — this task is purely verification.
  - **Details**:
    - **Implementation**: Inspect `.github/workflows/release.yml` — confirm `typst compile` commands reference `.typ` entry points (not deleted markdown files) and include `--font-path fonts` per US-002 Scenario 1
    - **Implementation**: Verify CI matrix strategy covers all CV variants (`cv.typ`, `cv_systems.typ`, `cv_infrastructure.typ`, `cover_letter.typ`) per US-002 Scenario 2
    - **Implementation**: Run `grep -rn "http://\|https://" content/*.yaml lib/*.typ` to confirm zero external network references per US-002 Scenario 3 (deterministic build mandate)
    - **Implementation**: Run `mise run check` to confirm all variant entry points compile via the local toolchain per US-003 Scenario 1
    - **Implementation**: Run `typst fmt --check content/data.typ lib/template.typ` to confirm formatting compliance per US-003 Scenario 2
    - **Edge Cases**: If CI workflow references a file that was deleted in T001, flag the reference for update (the CI workflow already references `.typ` entry points only, but double-check)
    - **Acceptance**: CI workflow references only `.typ` entry points with `--font-path fonts`, zero `http://`/`https://` references in YAML or Typst sources, `mise run check` exits 0, `typst fmt --check` exits 0

---

## Implementation Strategy
**Execution Order**:
1. Phase 1 (T001 then T002 — T001 must complete first as T002 verifies the state after deletion)

**Critical Dependency Chains**:
- T001 (Legacy File Removal) must precede T002 (CI Pipeline Verification)

**Risk Hotspots**:
- `content/star-stories.yaml` schema divergence: the `data-model.md` requires `id` slugs matching `^[a-z0-9-]+$`; star-stories.md stories may lack structured IDs and require slug generation during migration
- `star-stories.md` is 538 lines vs `star-stories.yaml` at 142 lines — expect significant data to port; manual comparison is error-prone

**Merge Conflict Boundaries**:
- `content/star-stories.yaml` is also touched by ISS-001 workflow branches; coordinate merge order
- No other files are touched by multiple phases within this issue
