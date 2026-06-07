# FEATURE_SPECIFICATION: specs/002-yaml-content-layer/001-yaml-driven-cv-compilation/spec.md
## SYSTEM_TOPOLOGY_MAPPING
- **Epic Domain**: `002-yaml-content-layer`
- **Issue ID**: `ISS-001`
- **Workstation Paths** (relative to repo root):
  - **Create**:
    - `content/config.yaml` — personal info, contact, summary
    - `content/experience.yaml` — roles with tagged bullets
    - `content/star-stories.yaml` — STAR stories with unique `id` slugs
    - `content/skills.yaml` — categorized skill lists
    - `content/projects.yaml` — projects with curation tags
    - `content/education.yaml` — education entries with `cv_priority`
  - **Rewrite**:
    - `content/data.typ` — thin YAML import adapter replacing hardcoded dictionary
  - **Modify**:
    - `lib/template.typ` — consume YAML-derived data structure
  - **Verify Only**:
    - `cv.typ` — general entry point
    - `cv_systems.typ` — systems variant entry point
    - `cv_infrastructure.typ` — infrastructure variant entry point
    - `cv_embedded.typ` — embedded variant entry point
    - `cv_enterprise.typ` — enterprise variant entry point
    - `cover_letter.typ` — cover letter entry point

## THE_PROBLEM_CONTRACT
The current CV system uses a 298-line hardcoded Typst dictionary (`content/data.typ`) and a supplementary markdown file (`content/master-list.md`) as dual data sources. This architecture prevents:

1. **Unified consumption** — A future Astro website cannot import Typst dictionary literals.
2. **Explicit curation** — No metadata exists to control which bullets appear on which CV variant vs. the website.
3. **STAR story linking** — No structured mechanism to link experience bullets to detailed STAR stories.

This issue delivers the complete vertical pipeline: canonical YAML files are created, a thin Typst adapter imports them via the built-in `yaml()` function, and the template engine consumes the adapted data to produce valid PDFs. After this issue, `typst compile cv.typ W_Bisschoff_CV.pdf` produces a PDF sourced entirely from YAML.

## SCOPE_BOUNDARIES
### Hard Inclusions
1. **Create 6 canonical YAML files** in `content/` conforming to schemas in `specs/002-yaml-content-layer/data-model.md`:
   - `config.yaml` — personal info, contact, summary
   - `experience.yaml` — all roles with bullets tagged `cv_priority` ∈ {1,2,3}, `website_show` ∈ {true,false}, `star_ref` ∈ string|null
   - `star-stories.yaml` — all STAR stories with unique `id` slugs
   - `skills.yaml` — categorized skill lists
   - `projects.yaml` — projects with `cv_priority` and `website_show` tags
   - `education.yaml` — education entries with `cv_priority`
2. **Rewrite `content/data.typ`** as a thin YAML import adapter:
   - Use Typst's built-in `yaml()` function (NOT any external package)
   - Export a `cv_data` dictionary compatible with `lib/template.typ`'s existing `render_cv(cv_data, variant: "...")` signature
   - Use `.at(key, default: ...)` for ALL nested YAML access to prevent runtime crashes from missing keys
   - Implement variant filtering: bullets where `cv_priority <= max_priority_for_variant`
   - Implement `star_ref` resolution: lookup in `star-stories.yaml`, degrade silently if `null` or broken reference
3. **Update `lib/template.typ`** to consume YAML-derived data:
   - Preserve existing `render_cv()` entry point signature
   - Ensure all data access uses defensive `.at(key, default:)` patterns
   - Remove any remaining hardcoded data references
   - Ensure `star_ref` resolution renders STAR story details or degrades gracefully

### Defensive Exclusions
- Do NOT delete `content/master-list.md` (deferred to ISS-002 / FR-004)
- Do NOT modify `.github/workflows/release.yml` (deferred to ISS-002)
- Do NOT implement Astro website integration (out of scope for this epic)
- Do NOT introduce external YAML preprocessing scripts (violates deterministic build mandate)
- Do NOT use `@preview/yaml` or any external package (constitution forbids it)
- Do NOT add automated YAML schema validation tooling (mitigated via manual assertions)

## PERFORMANCE_CONSTRAINTS
- **Compilation time**: Typst compilation must not increase by more than 15% compared to the baseline `content/data.typ` hardcoded implementation
- **YAML file size**: Total combined YAML content must remain under 500 lines to prevent merge conflict fatigue
- **Constitutional compliance**: Zero external network calls during compilation; all YAML files resolved via local file system paths relative to the calling Typst file

## MULTI_TIERED_VERIFICATION_TARGETS
### Unit-Level (Per-File)
- Each YAML file passes `yamllint` without errors
- `content/data.typ` exports `cv_data` without runtime errors
- `lib/template.typ` passes `typst fmt --check`
- `content/data.typ` passes `typst fmt --check`

### Integration-Level (Cross-File)
- `typst compile --font-path fonts cv.typ W_Bisschoff_CV.pdf` succeeds
- `typst compile --font-path fonts cv_systems.typ W_Bisschoff_CV_systems.pdf` succeeds with correct variant filtering (`cv_priority <= 2`)
- `typst compile --font-path fonts cv_infrastructure.typ W_Bisschoff_CV_infrastructure.pdf` succeeds
- `typst compile --font-path fonts cv_embedded.typ W_Bisschoff_CV_embedded.pdf` succeeds
- `typst compile --font-path fonts cv_enterprise.typ W_Bisschoff_CV_enterprise.pdf` succeeds
- `typst compile --font-path fonts cover_letter.typ W_Bisschoff_Cover_Letter.pdf` succeeds
- `star_ref` links resolve correctly in PDF output (visual verification)
- `mise run check` passes on all entry points

## ATDD_ACCEPTANCE_CRITERIA_LEDGER
### US-001-YAML-DATA-LAYER: Canonical YAML Data Creation
- **Upstream Requirement Traceability**: `FR-001`
- **Goal**: Migrate all hardcoded data from `content/data.typ` and `content/master-list.md` into 6 canonical YAML files with explicit curation metadata (`cv_priority`, `website_show`, `star_ref`), each conforming to the schemas defined in `specs/002-yaml-content-layer/data-model.md`.

**Scenario 1 — All 6 YAML files created with complete legacy data**
- **Given**: The legacy `content/data.typ` and `content/master-list.md` files exist containing the current source of truth
- **When**: The migration is performed (manual or script-assisted)
- **Then**: All 6 YAML files (`config.yaml`, `experience.yaml`, `skills.yaml`, `star-stories.yaml`, `projects.yaml`, `education.yaml`) exist in `content/` and contain 100% of the legacy data, with every experience bullet tagged with `cv_priority` and `website_show`

**Scenario 2 — experience.yaml passes YAML lint validation**
- **Given**: The new `content/experience.yaml` file has been created
- **When**: `yamllint` is executed against `content/experience.yaml`
- **Then**: The file passes all YAML syntax and structural validation rules without errors

**Scenario 3 — Missing cv_priority defaults to 3 (web-only)**
- **Given**: An experience bullet in `experience.yaml` has no `cv_priority` field
- **When**: The Typst adapter loads the YAML data
- **Then**: The bullet is treated as `cv_priority = 3` and excluded from all CV variants (appears only in website rendering)

**Scenario 4 — Empty YAML list silently skips section**
- **Given**: A YAML file (e.g., `projects.yaml`) contains an empty list `[]` with no entries
- **When**: The Typst template renders the corresponding section
- **Then**: The section heading is omitted entirely from the PDF output — no empty heading or whitespace is rendered

### US-002-TYPST-ADAPTER: Typst YAML Import Adapter Layer
- **Upstream Requirement Traceability**: `FR-002`
- **Goal**: Replace the 298-line hardcoded `content/data.typ` with a thin adapter that imports the canonical YAML files via Typst's built-in `yaml()` function and re-exports them in a shape compatible with `lib/template.typ`'s existing `render_cv(cv_data, variant: "...")` signature.

**Scenario 1 — typst compile cv.typ succeeds and PDF matches baseline**
- **Given**: The new `content/data.typ` YAML import adapter is implemented and the 6 canonical YAML files exist
- **When**: `typst compile cv.typ W_Bisschoff_CV.pdf` is executed
- **Then**: The compilation succeeds without runtime errors, and the output PDF visually matches the baseline generated from the legacy hardcoded `data.typ`

**Scenario 2 — Variant filtering correctly excludes low-priority bullets**
- **Given**: A variant entry point (e.g., `cv_systems.typ`) invokes `render_cv(cv_data, variant: "systems")`
- **When**: `typst compile cv_systems.typ W_Bisschoff_CV_systems.pdf` is executed
- **Then**: The compilation succeeds, and the output correctly filters experience bullets based on `cv_priority <= max_priority_for_variant` (bullets with `cv_priority > 2` are excluded for `systems` variant)

**Scenario 3 — Defensive .at(key, default:) prevents runtime crashes from missing keys**
- **Given**: A YAML file is missing an optional key (e.g., `contact.github` or `star_ref` on a bullet)
- **When**: The Typst adapter accesses the nested value using `.at(key, default: ...)`
- **Then**: The adapter returns the specified default value without causing a runtime panic or compilation failure

**Scenario 4 — All variant entry points compile successfully**
- **Given**: The YAML adapter is implemented and all 6 YAML files exist
- **When**: Each variant entry point (`cv.typ`, `cv_systems.typ`, `cv_infrastructure.typ`, `cv_embedded.typ`, `cv_enterprise.typ`, `cover_letter.typ`) is compiled in sequence
- **Then**: Every compilation succeeds without errors, producing valid PDF output

### US-003-TEMPLATE-ALIGNMENT: Template Engine Compatibility
- **Upstream Requirement Traceability**: `FR-003`
- **Goal**: Ensure `lib/template.typ` correctly consumes the YAML-derived data structure without requiring a complete rewrite of the rendering logic, including `star_ref` resolution for enriching experience bullets with STAR story details.

**Scenario 1 — typst fmt --check passes on template files**
- **Given**: The `lib/template.typ` and `content/data.typ` files have been updated
- **When**: `typst fmt --check` is executed
- **Then**: Both files pass formatting checks, and no legacy hardcoded data references remain in either file

**Scenario 2 — Valid star_ref resolves and renders STAR story details**
- **Given**: An experience bullet has a `star_ref` field pointing to a valid `StarStory.id` in `star-stories.yaml`
- **When**: The template renders the experience section
- **Then**: The corresponding STAR story details (Situation, Task, Action, Result) are resolved and appended/expanded alongside the bullet in the PDF output

**Scenario 3 — Broken star_ref degrades silently**
- **Given**: An experience bullet has a `star_ref` field pointing to a non-existent `id` in `star-stories.yaml`
- **When**: The template attempts to resolve the `star_ref`
- **Then**: The resolution fails silently — no STAR story is appended and no compilation warning or error is emitted

**Scenario 4 — Null star_ref is handled gracefully**
- **Given**: An experience bullet has `star_ref: null`
- **When**: The template renders the experience section
- **Then**: No STAR story lookup is attempted and the bullet renders as plain text without error

**Scenario 5 — render_cv() entry point signature preserved**
- **Given**: The updated `lib/template.typ` consumes YAML-derived `cv_data`
- **When**: Any variant entry point invokes `render_cv(cv_data, variant: "...")`
- **Then**: The function accepts the same parameter signature as the legacy implementation and produces valid output

## SYSTEM_STATUS_SUMMARY
| Parameter | Value |
| :--- | :--- |
| **STATUS** | SPEC_AUTHORED |
| **EPIC_SLUG** | 002-yaml-content-layer |
| **BRANCH_NAME** | feat/002-yaml-content-layer/001-yaml-driven-cv-compilation |
| **SPEC_PATH** | specs/002-yaml-content-layer/001-yaml-driven-cv-compilation/spec.md |
| **ISSUE_ID** | ISS-001 |
| **NEXT_ACTION** | Run `<SKILL_DIR>/deviate-specify.sh post` to validate, commit, and transition to Tasks phase |
