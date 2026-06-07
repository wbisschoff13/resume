# Implementation Tasks: feat/002-yaml-content-layer/001-yaml-driven-cv-compilation

## Phase 1: YAML Data Migration (US-001 — FR-001)
**Goal**: Migrate all hardcoded data from `content/data.typ` and `content/master-list.md` into 6 canonical YAML files with explicit curation metadata (`cv_priority`, `website_show`, `star_ref`), each conforming to the schemas in `specs/002-yaml-content-layer/data-model.md`.

### Tasks

- [x] T001: Create 6 canonical YAML content files from legacy data sources
  - **Type**: Migration
  - **Mode**: IMMEDIATE
  - **Verification**: `ls content/config.yaml content/experience.yaml content/star-stories.yaml content/skills.yaml content/projects.yaml content/education.yaml && yamllint content/*.yaml`
  - **Estimated Time**: 60 minutes
  - **Files**:
    - `content/config.yaml`
    - `content/experience.yaml`
    - `content/star-stories.yaml`
    - `content/skills.yaml`
    - `content/projects.yaml`
    - `content/education.yaml`
  - **Rationale**: These 6 YAML files replace the dual-source legacy system (`content/data.typ` hardcoded dictionary + `content/master-list.md`) as the single canonical data source per constitution v0.2.0. Each file maps to an entity defined in `specs/002-yaml-content-layer/data-model.md` and satisfies US-001 Scenario 1 (complete data migration) and Scenario 2 (YAML lint validation).
  - **Details**:
    - **Implementation**: Extract `_experience_entries` from `content/data.typ` into `content/experience.yaml` as an array of role objects, adding `cv_priority`, `website_show`, and `star_ref` fields to every bullet (default `cv_priority: 1` for essential bullets, `star_ref: null` where no story exists)
    - **Implementation**: Extract `_education_entries` into `content/education.yaml` with `cv_priority` per entry
    - **Implementation**: Extract `_skill_categories` into `content/skills.yaml` as categorized arrays
    - **Implementation**: Extract `_project_entries` into `content/projects.yaml` with `cv_priority` and `website_show` tags per project
    - **Implementation**: Extract name, contact info, summary, position variants, ai_policy, job_target, and certification from `cv_data` and `_cover_letter_data` into `content/config.yaml`, including about_me/why_me/how_i_work per variant under `cover_letter` block
    - **Implementation**: Create `content/star-stories.yaml` with 14 STAR story entries from `content/star-stories.md`, each with unique `id` slug matching `^[a-z0-9-]+$` pattern, and all four STAR components (Situation, Task, Action, Result)
    - **Edge Cases**: Bullets missing `cv_priority` default to `3` (web-only, excluded from all CV variants per HITL resolution); bullets with no related STAR story have `star_ref: null`
    - **Acceptance**: All 6 YAML files exist in `content/`, pass `yamllint` without errors, contain 100% of legacy data from both `content/data.typ` and `content/master-list.md`, every experience bullet tagged with `cv_priority` and `website_show`

## Phase 2: Typst Adapter Layer (US-002 — FR-002)
**Goal**: Replace the 298-line hardcoded `content/data.typ` with a thin adapter that imports the 6 canonical YAML files via Typst's built-in `yaml()` function, applies variant filtering by `cv_priority`, resolves `star_ref` lookups, and re-exports a `cv_data` dictionary backward-compatible with `lib/template.typ`'s existing `render_cv(cv_data, variant: "...")` signature and the variant entry points' filtering patterns.

### Tasks

- [x] [T002]: Rewrite content/data.typ as YAML import adapter with variant filtering and star_ref resolution
  - **Type**: Feature_Batch
  - **Mode**: TDD
  - **Test Strategy**: Integration
  - **Verification**: `typst compile --font-path fonts cv.typ /tmp/test_cv.pdf && typst compile --font-path fonts cv_systems.typ /tmp/test_systems.pdf && typst compile --font-path fonts cv_infrastructure.typ /tmp/test_infra.pdf && typst compile --font-path fonts cover_letter.typ /tmp/test_cover.pdf`
  - **Estimated Time**: 90 minutes
  - **Dependency**: T001
  - **Files**:
    - `content/data.typ`
  - **Rationale**: This is the critical integration seam — the adapter replaces 292 lines of hardcoded Typst dictionaries with `yaml()` imports. Must satisfy US-002 Scenario 1 (cv.typ compiles and matches baseline), Scenario 2 (variant filtering excludes low-priority bullets), Scenario 3 (defensive `.at()` prevents crashes), and Scenario 4 (all variant entry points compile). The adapter must maintain backward compatibility with variant entry points that filter by `.variant_tags.contains(...)` and `cat.variant == ...`.
  - **Details**:
    - **Red**: Before implementation, confirm that `typst compile cv.typ W_Bisschoff_CV.pdf` fails or produces different output when `content/data.typ` is replaced with a bare adapter stub that calls `yaml()` but maps keys incorrectly — validate that baseline compilation against the old hardcoded `data.typ` produces expected output as reference
    - **Green**: Implement `content/data.typ` as a thin adapter: use `let config = yaml("content/config.yaml")`, `let experience = yaml("content/experience.yaml")`, etc. for all 6 YAML files; export `cv_data` with all keys matching the legacy dictionary structure (`name`, `email`, `phone`, `location`, `github`, `website`, `linkedin`, `position`, `summary`, `ai_policy`, `job_target`, `certification`, `experience`, `experience_entries`, `education`, `education_entries`, `skills`, `skill_categories`, `projects`, `project_entries`, `cover_letter_data`)
    - **Green**: Apply `.at(key, default: ...)` for every nested YAML access — top-level keys default to `none` or `()`, nested string fields default to `""`, nested arrays default to `()`
    - **Green**: Implement variant filtering on experience bullets: for each role, filter `bullets` where `cv_priority <= variant_max` (general=3, systems=2, infrastructure=2, embedded=2, enterprise=2); map bullet `text` field into the `description` array expected by the template
    - **Green**: Include backward-compatible `variant_tags` field on each experience entry (derived from which roles have bullets for that variant) and `variant` field on each skill category entry
    - **Green**: Implement `star_ref` resolution: for each bullet with non-null `star_ref`, look up the `id` in `star-stories`; if found, append STAR story content to the bullet text; if not found (broken ref), silently skip per HITL resolution
    - **Refactor**: Remove all hardcoded `_experience_entries`, `_education_entries`, `_skill_categories`, `_project_entries`, and `_cover_letter_data` arrays; ensure `cv_data` dictionary is the only export; verify `typst fmt --check content/data.typ` passes
    - **Acceptance**: `typst compile --font-path fonts cv.typ` succeeds with zero runtime errors; all 5 variant entry points (`cv.typ`, `cv_systems.typ`, `cv_infrastructure.typ`, `cv_embedded.typ`, `cv_enterprise.typ`) and `cover_letter.typ` compile successfully; compiled PDF visually matches baseline for cv.typ (general variant)

## Phase 3: Template Engine Alignment (US-003 — FR-003)
**Goal**: Update `lib/template.typ` to correctly consume the YAML-derived data structure, integrate `star_ref` rendering in experience sections, remove remaining hardcoded data access patterns, and ensure `render_cv()` and `render_cover_letter()` entry point signatures remain preserved.

### Tasks

- [x] T003: Update lib/template.typ for star_ref rendering and YAML data compatibility
  - **Type**: Feature_Batch
  - **Mode**: TDD
  - **Test Strategy**: Integration
  - **Verification**: `typst fmt --check lib/template.typ && typst compile --font-path fonts cv.typ /tmp/test_cv.pdf && typst compile --font-path fonts cv_systems.typ /tmp/test_systems.pdf && typst compile --font-path fonts cv_infrastructure.typ /tmp/test_infra.pdf && typst compile --font-path fonts cv_embedded.typ /tmp/test_embedded.pdf && typst compile --font-path fonts cv_enterprise.typ /tmp/test_enterprise.pdf && typst compile --font-path fonts cover_letter.typ /tmp/test_cover.pdf`
  - **Estimated Time**: 60 minutes
  - **Dependency**: T002
  - **Files**:
    - `lib/template.typ`
  - **Rationale**: The template rendering engine must adapt to the YAML-derived `cv_data` shape while preserving all existing layout logic. Satisfies US-003 Scenario 1 (typst fmt passes), Scenario 2 (valid star_ref renders STAR details), Scenario 3 (broken star_ref degrades silently), Scenario 4 (null star_ref handled gracefully), and Scenario 5 (render_cv signature preserved). The star_ref resolution is new rendering behavior; the template must display resolved STAR content without breaking existing section layouts.
  - **Details**:
    - **Red**: After T002 completes, create a test .typ file that imports the adapter's cv_data and invokes `render_cv` with a variant that includes bullets with `star_ref` values — confirm that before template changes, star_ref content is either not rendered or causes type errors
    - **Green**: Update `_resolve_entries()` to handle the new bullet structure from the adapter (bullets are pre-filtered by variant but retain their YAML-derived shape); ensure the function extracts `text` from each bullet for the description array while also passing through any resolved `star_story` content
    - **Green**: Add star_ref rendering logic: for each bullet in the experience description loop, if the bullet has resolved star story details (situation, task, action, result), render them as nested / indented content below the bullet text using a smaller font size or italic style to differentiate from primary bullet content
    - **Green**: Update skills rendering: the adapter produces skill categories with `category` key and `items` array; ensure `resume-skill-item` receives `cat.category` for the name and `cat.items` for skills (the old code used `cat.category_name` and `cat.skills`)
    - **Green**: Update education rendering: ensure `_resolve_education` and the education section loop handle the YAML-derived shape where `field` and `details` (as an array of strings) are available
    - **Refactor**: Run `typst fmt --check lib/template.typ` and fix any formatting violations; remove any remaining fallback patterns referencing old key names (`experience_entries`, `skill_categories`, `project_entries`, `education_entries`) that are no longer needed since the adapter now produces the primary keys directly
    - **Edge Cases**: Bullet with `star_ref: null` renders as plain text with no star story expansion (no blank space); bullet with broken `star_ref` resolves to `none` from adapter — template skips star story rendering silently; experience entry with zero bullets after filtering renders the company header but no bullet list
    - **Acceptance**: `typst fmt --check lib/template.typ` passes with zero violations; all 6 entry points compile and produce valid PDFs; `render_cv(cv_data, variant: "...")` signature unchanged; star_ref resolution renders expanded STAR content for valid references and degrades silently for null/broken references

---

## Implementation Strategy
**Execution Order**:
1. Phase 1 (T001) — Create YAML files first; these are the canonical data source that Phases 2-3 depend on
2. Phase 2 (T002) — Rewrite the adapter to import YAML; must complete before template can consume new data shape
3. Phase 3 (T003) — Update template to render star_ref content and finalize YAML compatibility

**Critical Dependency Chains**:
- T001 (YAML creation) → T002 (adapter rewrite) — adapter must have valid YAML files to import
- T002 (adapter rewrite) → T003 (template update) — template needs adapter's cv_data shape to render correctly

**Risk Hotspots**:
- **RSK-001 (Silent Data Loss)**: `.at(key, default: ...)` patterns in T002 will mask misspelled YAML keys — verify via visual inspection of compiled PDFs against baseline
- **RSK-003 (Null Handling Ambiguity)**: YAML `null` implicitly converts to Typst `none` — adapter must explicitly handle both cases in star_ref resolution and bullet text access
- **Backward Compatibility**: Variant entry points filter by `variant_tags.contains(...)` and `cat.variant == ...` — T002 must include these fields in the adapter output to prevent entry points from breaking, despite the YAML schemas not having `variant_tags` natively

**Merge Conflict Boundaries**:
- Files touched by multiple tasks: None (each task touches a disjoint set of files)

**Post-Integration Verification**:
- Full suite: `mise run check` (compiles cv.typ, cv_systems.typ, cv_infrastructure.typ, cover_letter.typ)
- Visual verification: Compare PDF output against pre-migration baseline for layout shifts
- Constitutional compliance: No external packages, no network calls, single-column output with `ligatures: false`, all YAML resolved via local file paths