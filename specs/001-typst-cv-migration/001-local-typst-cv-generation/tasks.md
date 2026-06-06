# Implementation Tasks: feat/001-typst-cv-migration/001-local-typst-cv-generation

## Phase 1: Data Foundation
**Goal**: Centralized data dictionary (`content/data.typ`) containing all CV content ported from legacy LaTeX files, with variant tags for bi-variant filtering.

### Tasks

- [ ] T001: Create content/data.typ — Centralized Data Dictionary
  - **Type**: Migration
  - **Mode**: IMMEDIATE
  - **Verification**: `typst check content/data.typ`
  - **Estimated Time**: 90 minutes
  - **Files**:
    - `content/data.typ`
  - **Rationale**: Implements `FR-001-DATA` and all `US-001-DATA` acceptance criteria. This is the single source of truth for all CV data, required by all downstream modules. The file organizes all experience, education, skills, projects, and personal data into native Typst dictionaries with `variant_tags` for entry-point filtering.
  - **Details**:
    - **Implementation**: Create `content/data.typ` with the root `cv_data` dictionary containing `name`, `email`, `phone`, `location`, `position` (default: "Systems Engineer"), `summary`, `ai_policy`, and `job_target` as content blocks.
    - **Implementation**: Port all employment experience from `analysis/experience_master.md` into `experience_entries` array of dictionaries. Each entry must include `role`, `company`, `location`, `start_date`, `end_date`, `description` (array of content blocks), and `variant_tags` (subset of `("general", "embedded", "enterprise")`).
    - **Implementation**: Port education entries from `cv/education.tex` (and variant copies in `cv/embedded/`, `cv/enterprise/`) into `education_entries`. Each entry: `degree`, `institution`, `location`, `graduation_year`, `details` (array of content).
    - **Implementation**: Port skill categories from `cv/skills.tex` (and variant copies) into `skill_categories`. Each entry: `category_name`, `skills` (array of strings), `variant` (one of `"general"`, `"embedded"`, `"enterprise"`).
    - **Implementation**: Port project entries from `cv/projects.tex` and `cv/opensource.tex` into `project_entries` with `name`, `description`, `link` (optional), `variant_tags`.
    - **Implementation**: Include `cover_letter_data` dictionary with `recipient_name`, `recipient_title`, `company`, `date`, `about_me`, `why_me`, `variant`. Source content from `W_Bisschoff_Cover_Letter.tex` and its variants.
    - **Edge Cases**: Ensure all required keys (`name`, `email`, `experience`, `education`, `skills`) are present to pass `typst check`. Date fields must be strings; `end_date` may be `none` for current positions.
    - **Acceptance**: `typst check content/data.typ` exits 0. `experience_entries` has ≥1 entry with all five required keys (`role`, `company`, `location`, `start_date`, `description`). `education_entries` has ≥1 entry.

---

## Phase 2: Layout Engine
**Goal**: Pure layout module (`lib/template.typ`) that accepts a data dictionary, enforces ATS-compatible formatting, and renders all CV and cover letter sections without containing any inline content data.

### Tasks

- [ ] T002: Create lib/template.typ — Pure Layout Engine
  - **Type**: Feature_Batch
  - **Mode**: IMMEDIATE
  - **Verification**: `typst fmt --check lib/template.typ && typst check lib/template.typ`
  - **Estimated Time**: 90 minutes
  - **Dependency**: T001
  - **Files**:
    - `lib/template.typ`
  - **Rationale**: Implements `FR-002-LAYOUT` and all `US-002-LAYOUT` acceptance criteria. The template must be a pure function module — no data, only rendering logic. It enforces ATS constraints as global defaults and provides section-rendering functions consumed by entry points.
  - **Details**:
    - **Implementation**: Define a main `render_cv(data)` function that accepts a data dictionary and returns a formatted document tree. This function sets global ATS constraints: `#set text(ligatures: false)`, single-column page layout, clean margins.
    - **Implementation**: Implement font configuration with explicit Typst-native fallbacks. Attempt to load vendored fonts (e.g., "Roboto") first; if unavailable, fall back to `"DejaVu Sans"` / `"Libertinus Serif"`. Document the fallback mechanism.
    - **Implementation**: Build section-rendering functions: `render_header(name, email, phone, location)`, `render_summary(summary)`, `render_experience(entries)`, `render_education(entries)`, `render_skills(categories)`, `render_projects(entries)`, `render_ai_policy(content)`, `render_job_target(content)`. Each function checks for key existence before rendering — missing optional keys silently skip.
    - **Implementation**: Build cover letter rendering: `render_cover_letter(data)` with sections for recipient info, salutation, `about_me`, `why_me`, and closing. Uses same ATS constraints as CV template.
    - **Implementation**: Ensure no inline content data exists in the template — all text must come from the passed dictionary. Use `#if "key" in data { ... }` guards for all optional sections.
    - **Edge Cases**: Missing `ai_policy` or `job_target` keys must not crash — sections silently omitted. Missing required keys (`name`, `email`, `experience`) should produce a readable error or empty section rather than panic. Empty arrays (e.g., 0 projects) produce no output for that section.
    - **Acceptance**: `typst fmt --check lib/template.typ` exits 0 (code style). `typst check lib/template.typ` exits 0 (no syntax errors). The file contains no hardcoded personal data strings. `#set text(ligatures: false)` is present at the global scope.

---

## Phase 3: Variant Entry Points
**Goal**: Four self-contained entry point files that import data and template modules, apply variant-specific overrides via dictionary merge, and can each be independently compiled to PDF.

### Tasks

- [ ] T003: Create Entry Points — cv.typ, cv_embedded.typ, cv_enterprise.typ, cover_letter.typ
  - **Type**: Feature_Batch
  - **Mode**: IMMEDIATE
  - **Verification**: `typst check cv.typ && typst check cv_embedded.typ && typst check cv_enterprise.typ && typst check cover_letter.typ`
  - **Estimated Time**: 60 minutes
  - **Dependency**: T002
  - **Files**:
    - `cv.typ`
    - `cv_embedded.typ`
    - `cv_enterprise.typ`
    - `cover_letter.typ`
  - **Rationale**: Implements `FR-003-ENTRY` and all `US-003-ENTRY` acceptance criteria. Each entry point is a thin orchestration layer: import data + template, apply variant overrides via dictionary merge, call the appropriate render function. Variant-specific logic (filtering by `variant_tags`, position overrides) lives here per the design's "no over-abstraction" constraint.
  - **Details**:
    - **Implementation**: `cv.typ` — imports `content/data.typ` and `lib/template.typ`, passes `cv_data` directly to `render_cv()` with no filtering (all entries with `"general"` tag or no tag restriction). Default position is "Systems Engineer".
    - **Implementation**: `cv_embedded.typ` — imports base data, overrides `position` to `"Embedded Systems & Real-Time Software Engineer"` via dictionary merge (`cv_data + (position: "...")`). Filters `experience_entries` to only those whose `variant_tags` include `"embedded"`. Applies same filtering to `education_entries` and `skill_categories`. Calls `render_cv()` with merged+filtered data.
    - **Implementation**: `cv_enterprise.typ` — same pattern as embedded, overriding `position` to `"Enterprise Systems & Automation Architect"` and filtering for `variant_tags` containing `"enterprise"`.
    - **Implementation**: `cover_letter.typ` — imports `cover_letter_data` from `content/data.typ` and `render_cover_letter()` from `lib/template.typ`. Passes data directly. Cover letter data may include variant overrides (embedded/enterprise recipient details).
    - **Implementation**: Ensure variant overrides are local — each entry point creates a merged dictionary without mutating the imported `cv_data`. Typst's `+` operator on dictionaries produces a new dictionary.
    - **Edge Cases**: If no experience entries match a variant's tag filter, the experience section renders empty rather than crashing. Entry points must use `#import` (not `#include`) to avoid token-injection side effects. Each entry point must compile independently with `typst compile`.
    - **Acceptance**: All four entry points pass `typst check` (exit 0). `cv_embedded.typ` overrides `position` to "Embedded Systems & Real-Time Software Engineer" and the rendered output reflects this. Base `cv_data.position` in `content/data.typ` remains "Systems Engineer" after importing from any entry point.

---

## Phase 4: Integration Verification
**Goal**: Compile all variant entry points to PDF, validate outputs are non-empty, and confirm the defensive exclusion boundary (no LaTeX files modified).

### Tasks

- [ ] T004: Compile All Variants and Verify PDF Outputs
  - **Type**: Feature_Batch
  - **Mode**: IMMEDIATE
  - **Verification**: `typst compile cv.typ cv.pdf && typst compile cv_embedded.typ cv_embedded.pdf && typst compile cv_enterprise.typ cv_enterprise.pdf && typst compile cover_letter.typ cover_letter.pdf && ls -lh cv.pdf cv_embedded.pdf cv_enterprise.pdf cover_letter.pdf`
  - **Estimated Time**: 30 minutes
  - **Dependency**: T003
  - **Files**:
    - `.gitignore`
  - **Rationale**: Validates all `US-003-ENTRY` integration acceptance criteria (compilation produces valid PDFs) and `US-004-REGRESSION` (no LaTeX files touched). Updates `.gitignore` to exclude Typst build artifacts so generated PDFs and cache files are not accidentally committed.
  - **Details**:
    - **Implementation**: Run `typst compile` for all four entry points. Verify each generates a non-empty PDF. Check compilation time is under 2 seconds per variant.
    - **Implementation**: Update `.gitignore` to exclude Typst cache directories (`.typst/`) and generated PDF artifacts (`*.pdf` in root or via explicit entries for CV outputs) to prevent accidental commits.
    - **Implementation**: Run `typst fmt --check` on all `.typ` files (`content/data.typ`, `lib/template.typ`, `cv.typ`, `cv_embedded.typ`, `cv_enterprise.typ`, `cover_letter.typ`) to confirm consistent code style across the entire module surface.
    - **Implementation**: Verify defensive exclusion boundary: `git diff --name-only` against the parent commit must not show any changes to `*.tex` or `*.cls` files. Only new `.typ` files and `.gitignore` should appear.
    - **Edge Cases**: If `typst compile` fails on any variant, investigate and fix the specific entry point or template before proceeding. A failure on one variant must not mask failures on others — compile all four independently.
    - **Acceptance**: All four PDF files exist and are non-empty (>0 bytes). All `.typ` files pass `typst fmt --check`. No `.tex` or `.cls` files appear in `git diff --name-only`. `.gitignore` includes `.typst/` and root-level `*.pdf` entries.

---

## Implementation Strategy
**Execution Order**:
1. Phase 1 (T001) — Data dictionary must exist first; all other phases depend on it.
2. Phase 2 (T002) — Layout engine depends on knowing data dictionary shape from T001.
3. Phase 3 (T003) — Entry points require both data (T001) and template (T002).
4. Phase 4 (T004) — Integration verification depends on all files being implemented.

**Critical Dependency Chains**:
- T001 → T002 → T003 → T004 (linear chain, no parallelism possible)

**Risk Hotspots**:
- Data porting from LaTeX to Typst dictionaries in T001 — manual transcription risk; validate with `typst check` after every logical section is added.
- Font fallback logic in T002 — test on a fresh environment to confirm Typst-native fonts are resolved correctly.
- Variant tag filtering in T003 — ensure filtering logic produces correct experience/education/skills subsets per variant.

**Merge Conflict Boundaries**:
- Files unique to ISS-001: `content/data.typ`, `lib/template.typ`, `cv.typ`, `cv_embedded.typ`, `cv_enterprise.typ`, `cover_letter.typ`, `.gitignore`. No overlap with existing tracked files except `.gitignore`.
