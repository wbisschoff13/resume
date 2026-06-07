# FEATURE_SPECIFICATION: specs/002-yaml-content-layer/002-legacy-cleanup-ci-verification/spec.md
## SYSTEM_TOPOLOGY_MAPPING
- **Epic Domain**: `002-yaml-content-layer`
- **Issue ID**: `ISS-002`
- **Workstation Paths** (relative to repo root):
  - **Delete**:
    - `content/master-list.md` — fully superseded by YAML canonical data layer
    - `content/star-stories.md` — superseded by `content/star-stories.yaml`; migrate any missing data first
  - **Update**:
    - `.typ` source files — remove or update any dangling references to deleted files
  - **Verify Only**:
    - `.github/workflows/release.yml` — CI pipeline compiles all variants with YAML adapter
    - `.mise.toml` — task definitions cover all entry points

## THE_PROBLEM_CONTRACT
After ISS-001 establishes the YAML-driven compilation pipeline, legacy artifacts remain in the repository:

1. `content/master-list.md` — superseded by `content/experience.yaml` + `content/star-stories.yaml`
2. `content/star-stories.md` — superseded by `content/star-stories.yaml`; may contain data not yet migrated
3. CI pipeline may reference legacy file paths or lack YAML-aware validation
4. `.typ` source files may contain `#include` or `yaml()` references to files being deleted

This issue delivers the final cleanup: legacy files are removed (with any remaining data ported to YAML first), all dangling references are resolved, the CI pipeline is verified to compile all variants using the new YAML adapter layer, and deterministic build invariants are confirmed. After this issue, the repository contains zero legacy data sources and the CI pipeline validates the complete YAML architecture.

## SCOPE_BOUNDARIES
### Hard Inclusions
1. **Delete `content/master-list.md`** — fully superseded by YAML canonical data layer; confirm no `.typ` file references it before removal
2. **Migrate then delete `content/star-stories.md`**: first identify and port any data in `star-stories.md` not yet present in `content/star-stories.yaml`, then delete the file
3. **Resolve dangling references**: grep all `.typ` files for references to `master-list.md` and `star-stories.md`; update or remove each reference before deleting the target files
4. **Verify CI pipeline** (`.github/workflows/release.yml`):
   - Confirms all variant entry points compile via `typst compile --font-path fonts`
   - No external network calls during compilation (deterministic build mandate) — verified via `grep` for `http://` references in source files
   - Matrix strategy covers all CV variants
5. **Verify `mise run check`** passes for all entry points after legacy file removal
6. **Confirm no dangling references** — grep codebase for imports/references to deleted files post-removal

### Defensive Exclusions
- Do NOT modify YAML files created in ISS-001
- Do NOT modify `content/data.typ` adapter logic (completed in ISS-001)
- Do NOT modify `lib/template.typ` rendering logic (completed in ISS-001)
- Do NOT implement automated YAML schema validation tooling (out of scope)
- Do NOT introduce new CI steps beyond verifying existing compilation pipeline
- Do NOT delete `content/yaml-content-migration-spec.md` or `content/website-rework-handover.md` (not legacy data sources)
- Do NOT add `strace`/`dtruss` or other runtime network-call detection to CI (scope limited to static grep verification)

## PERFORMANCE_CONSTRAINTS
- **Compilation time**: No measurable regression from ISS-001 baseline (no new data sources are added)
- **Constitutional compliance**: Zero external network calls during compilation — verified via `grep` for `http://` and `https://` in `content/*.yaml` and `lib/*.typ` source files
- **Repository hygiene**: After removal, `git grep master-list` and `git grep star-stories.md` must return zero results across all tracked files

## MULTI_TIERED_VERIFICATION_TARGETS
### Unit-Level (Per-File)
- `content/master-list.md` does not exist after deletion (`test ! -f content/master-list.md`)
- `content/star-stories.md` does not exist after migration and deletion (`test ! -f content/star-stories.md`)
- No `.typ` file imports or references either deleted file

### Integration-Level (Cross-File)
- `mise run check` passes — all entry points compile successfully after legacy file removal
- `typst fmt --check` passes on all `.typ` files
- CI workflow references correct compilation paths (no legacy file paths remain)
- `grep` for `http://` or `https://` in `content/*.yaml` and `lib/*.typ` returns zero results (deterministic build verification)

## ATDD_ACCEPTANCE_CRITERIA_LEDGER
### US-001-LEGACY-FILE-REMOVAL: Legacy markdown removal with migration
- **Upstream Requirement Traceability**: `FR-004-LEGACY-CLEANUP`
- **Goal**: Remove `content/master-list.md` (fully superseded) and `content/star-stories.md` (after porting any remaining data to YAML), leaving the repository with zero legacy data-source files.

**Scenario 1 — master-list.md is deleted without breaking compilation**
- **Given**: The new YAML architecture is fully functional and `content/experience.yaml` + `content/star-stories.yaml` contain 100% of the legacy data
- **When**: `git rm content/master-list.md` is executed and committed
- **Then**: The file is removed from the repository, and `mise run check` still passes for all entry points

**Scenario 2 — star-stories.md data is ported then deleted**
- **Given**: `content/star-stories.md` exists and `content/star-stories.yaml` exists
- **When**: The content of `star-stories.md` is compared against `star-stories.yaml`
- **Then**: Any data present in the `.md` file but absent from the `.yaml` file is ported into `star-stories.yaml`, and `git rm content/star-stories.md` is executed; after removal, `mise run check` passes for all entry points

**Scenario 3 — Dangling references are resolved before deletion**
- **Given**: One or more `.typ` files contain `#include` or `yaml()` references to `content/master-list.md` or `content/star-stories.md`
- **When**: The references are detected via `grep`
- **Then**: Each reference is updated (removed or redirected) before the legacy file is deleted; after deletion, `git grep master-list` and `git grep star-stories.md` return zero results across all tracked files

### US-002-CI-VERIFICATION: CI pipeline YAML-aware compilation verification
- **Upstream Requirement Traceability**: `FR-004-LEGACY-CLEANUP`
- **Goal**: Verify the CI/CD pipeline compiles all CV variants using the YAML adapter layer without relying on legacy file paths or making external network calls.

**Scenario 1 — CI workflow references correct paths**
- **Given**: The `.github/workflows/release.yml` file exists
- **When**: The workflow is inspected for `typst compile` commands
- **Then**: All compilation commands reference correct entry-point paths (`.typ` files, not deleted markdown files) and include `--font-path fonts`

**Scenario 2 — All variant entry points compile via CI matrix**
- **Given**: The CI workflow defines a matrix strategy
- **When**: A new tag is pushed triggering the workflow
- **Then**: Each matrix job compiles its variant successfully using the YAML adapter layer, producing a valid PDF artifact without build errors

**Scenario 3 — No external network calls during compilation**
- **Given**: The deterministic build mandate from the constitution
- **When**: `grep -rn "http://\|https://" content/*.yaml lib/*.typ` is executed
- **Then**: Zero results are returned, confirming no external network references exist in source files or data files

### US-003-MISE-VERIFICATION: Post-cleanup build integrity
- **Upstream Requirement Traceability**: `FR-004-LEGACY-CLEANUP`
- **Goal**: Confirm all variant entry points compile successfully after legacy file removal, with formatting checks passing.

**Scenario 1 — mise run check passes all entry points**
- **Given**: All legacy files have been removed and dangling references resolved
- **When**: `mise run check` is executed
- **Then**: The command exits successfully — all variant entry points compile without errors

**Scenario 2 — Typst formatting passes on all source files**
- **Given**: The codebase is in its final cleaned state
- **When**: `typst fmt --check content/data.typ lib/template.typ` is executed
- **Then**: Both files pass formatting checks without errors

## SYSTEM_STATUS_SUMMARY
| Parameter | Value |
| :--- | :--- |
| **STATUS** | SPEC_AUTHORED |
| **EPIC_SLUG** | 002-yaml-content-layer |
| **BRANCH_NAME** | feat/002-yaml-content-layer/002-legacy-cleanup-ci-verification |
| **SPEC_PATH** | specs/002-yaml-content-layer/002-legacy-cleanup-ci-verification/spec.md |
| **ISSUE_ID** | ISS-002 |
| **NEXT_ACTION** | Run `<SKILL_DIR>/deviate-specify.sh post` to validate, commit, and transition to Tasks phase |
