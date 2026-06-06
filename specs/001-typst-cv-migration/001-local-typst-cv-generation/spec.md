# FEATURE_SPECIFICATION: specs/001-typst-cv-migration/001-local-typst-cv-generation/spec.md

## SYSTEM_TOPOLOGY_MAPPING

- **Epic Domain**: `001-typst-cv-migration`
- **Local File Paths**:
  - `content/data.typ` — Centralized data dictionary (FR-001-DATA)
  - `lib/template.typ` — Pure layout engine (FR-002-LAYOUT)
  - `cv.typ` — General variant entry point (FR-003-ENTRY)
  - `cv_embedded.typ` — Embedded variant entry point (FR-003-ENTRY)
  - `cv_enterprise.typ` — Enterprise variant entry point (FR-003-ENTRY)
  - `cover_letter.typ` — Cover letter entry point (FR-003-ENTRY)
- **Workstation Paths**: Local Typst CLI environment (`typst` binary, latest stable).
- **Downstream Dependencies**: `FR-004-CI` (GitHub Actions pipeline) and `FR-005-CLEANUP` (LaTeX artifact removal) are deferred to `ISS-002`.
- **Upstream Source**: `specs/001-typst-cv-migration/prd.md`

## THE_PROBLEM_CONTRACT

As a user, I need a local, functional Typst-based CV generation system that separates data from layout and produces ATS-compatible PDFs for multiple variants (general, embedded, enterprise) and cover letters, without relying on any CI/CD pipeline or legacy LaTeX files.

The current repository is LaTeX-based. The migration to Typst requires bootstrapping three foundational modules — data dictionary, layout engine, and variant entry points — that together enable local `typst compile` for CV generation. CI pipeline migration and LaTeX artifact removal are intentionally deferred to preserve a working fallback until the local Typst system is verified.

## SCOPE_BOUNDARIES

### Hard Inclusions

- Implement `content/data.typ` with a centralized `cv_data` dictionary containing all professional experience, education, skills, and personal information as native Typst dictionary entries.
- Implement `lib/template.typ` as a pure layout function module that accepts a data dictionary, enforces `#set text(ligatures: false)` and single-column page margins, and returns a formatted document tree. The template must contain no inline content data.
- Create four variant entry points (`cv.typ`, `cv_embedded.typ`, `cv_enterprise.typ`, `cover_letter.typ`) that import both `content/data.typ` and `lib/template.typ`, apply variant-specific overrides via dictionary merge at the entry point, and submit the merged data to the template function for rendering.
- Each entry point must be independently compilable via `typst compile <entry>.typ <entry>.pdf` on a local workstation.
- All `.typ` files must pass `typst check` (syntax validation) and `typst fmt --check` (code style) without errors.

### Defensive Exclusions

- Do NOT modify `.github/workflows/release.yml` — CI migration is `FR-004-CI`, deferred to `ISS-002`.
- Do NOT delete any `.tex` or `.cls` files — LaTeX artifact removal is `FR-005-CLEANUP`, deferred to `ISS-002`.
- Do NOT migrate `written_interview.tex` — excluded per PRD stakeholder decision.
- Do NOT migrate `analysis/` or `amazon-lp-cheatsheet-draft.md` — unrelated to CV output.
- Do NOT implement external JSON/YAML serialization — native Typst dictionaries are the chosen format.

## PERFORMANCE_CONSTRAINTS

- Compilation time must remain under 2 seconds per variant on a modern local workstation.
- PDF output must be clean, single-column, and free of complex tables or color fills to ensure ATS parsing compatibility.
- No external network calls during compilation.
- All fonts must be explicitly declared; vendored custom fonts are preferred, with Typst-native equivalents as hardcoded fallback in `lib/template.typ` when vendored fonts are unavailable on the compilation host.
- Missing optional dictionary keys must not cause compilation failure; affected sections are silently omitted.

## MULTI_TIERED_VERIFICATION_TARGETS

| Tier | Command | Target | Expected Outcome |
| :--- | :--- | :--- | :--- |
| **Unit/Static** | `typst check content/data.typ` | Data dictionary | Exit code 0, no syntax errors |
| **Unit/Static** | `typst fmt --check lib/template.typ` | Layout engine | Exit code 0, consistent code style |
| **Unit/Static** | `typst fmt --check content/data.typ` | Data dictionary | Exit code 0, consistent code style |
| **Integration** | `typst compile cv.typ cv.pdf` | General variant | Valid, non-empty PDF generated |
| **Integration** | `typst compile cv_embedded.typ cv_embedded.pdf` | Embedded variant | Valid, non-empty PDF with position "Embedded Systems & Real-Time Software Engineer" |
| **Integration** | `typst compile cv_enterprise.typ cv_enterprise.pdf` | Enterprise variant | Valid, non-empty PDF generated |
| **Integration** | `typst compile cover_letter.typ cover_letter.pdf` | Cover letter | Valid, non-empty PDF generated |
| **Integration** | `typst check` on all `.typ` files | All modules | All exit code 0, no missing keys or syntax errors |

## ATDD_ACCEPTANCE_CRITERIA_LEDGER

### US-001-DATA: Centralized Data Dictionary Implementation

* **Upstream Requirement Traceability**: `FR-001-DATA`
* **Covered ACs**: `AC-001-DATA-01`, `AC-001-DATA-02`

**Scenario 1: Syntactic validation of the data dictionary**

- **Given** `content/data.typ` has been created with the `cv_data` dictionary containing entries for `name`, `email`, `phone`, `location`, `position`, `summary`, `experience`, `education`, `projects`, `skills`, `ai_policy`, and `job_target`
- **When** `typst check content/data.typ` is executed
- **Then** the command exits with code 0, confirming syntactic validity of the dictionary structure

**Scenario 2: Experience array contains required keys**

- **Given** the `experience` array is defined in `content/data.typ`
- **When** the data dictionary is evaluated (implicitly via `typst check`)
- **Then** the `experience` array contains at least one entry, and each entry defines the keys `role`, `company`, `location`, `start_date`, and `description`

---

### US-002-LAYOUT: Pure Layout Engine Implementation

* **Upstream Requirement Traceability**: `FR-002-LAYOUT`
* **Covered ACs**: `AC-002-LAYOUT-01`, `AC-002-LAYOUT-02`

**Scenario 1: Code style consistency**

- **Given** `lib/template.typ` is implemented as a pure function module accepting a data dictionary and returning a formatted document tree
- **When** `typst fmt --check lib/template.typ` is executed
- **Then** the command exits with code 0, confirming consistent code style without reformatting changes

**Scenario 2: ATS compatibility constraints enforced globally**

- **Given** the layout engine function in `lib/template.typ` is invoked with any data dictionary
- **When** the function renders the document tree
- **Then** it enforces `#set text(ligatures: false)` and single-column page margins (e.g., via `#set page(columns: 1)` or equivalent default), and does not produce tables or color fills that could interfere with ATS parsing

**Scenario 3: Missing optional keys silently skip their sections**

- **Given** a data dictionary is passed to the template that omits an optional key (e.g., `ai_policy` or `job_target`)
- **When** the template renders the document tree
- **Then** compilation succeeds without error, and the section corresponding to the missing key is silently omitted from output

**Scenario 4: Typst-native font fallback when vendored fonts absent**

- **Given** the compilation host does not have vendored custom fonts available in the expected location
- **When** the template sets text fonts
- **Then** it falls back to Typst-native equivalents (e.g., `"DejaVu Sans"`, `"Libertinus Serif"`) producing a valid PDF without compilation errors, though cosmetic appearance may differ from the vendored-font output

---

### US-003-ENTRY: Variant Entry Point Orchestration

* **Upstream Requirement Traceability**: `FR-003-ENTRY`
* **Covered ACs**: `AC-003-ENTRY-01`, `AC-003-ENTRY-02`

**Scenario 1: Embedded variant compiles with correct position override**

- **Given** `cv_embedded.typ` exists, imports `content/data.typ` and `lib/template.typ`, overrides the `position` field to `"Embedded Systems & Real-Time Software Engineer"` via dictionary merge, and calls the template function
- **When** `typst compile cv_embedded.typ cv_embedded.pdf` is executed
- **Then** a valid, non-empty PDF is generated and the rendered position matches the overridden value

**Scenario 2: All four entry points pass static validation**

- **Given** `cv.typ`, `cv_embedded.typ`, `cv_enterprise.typ`, and `cover_letter.typ` all exist, each importing the data dictionary and layout engine with variant-specific overrides applied via dictionary merge at the entry point
- **When** `typst check` is run on each entry point individually
- **Then** all four exit with code 0, confirming no missing dictionary keys, no import resolution errors, and no syntax violations

**Scenario 3: Variant overrides do not mutate the base data dictionary**

- **Given** `cv_embedded.typ` imports `cv_data` from `content/data.typ` and applies a variant-specific override of `position` by creating a merged dictionary (e.g., `cv_data + (position: "Embedded ...")`)
- **When** another entry point (`cv_enterprise.typ`) imports the same `cv_data` without the override
- **Then** the base `cv_data.position` retains its original value from the data dictionary, confirming overrides are local to each entry point and do not leak across variants

---

### US-004-REGRESSION: No LaTeX Artifact Regression

* **Upstream Requirement Traceability**: `FR-005-CLEANUP` (pre-verification gate)
* **Covered ACs**: N/A (defensive gate, not an FR from ISS-001 scope)

**Scenario 1: No LaTeX files are modified or deleted**

- **Given** the repository contains existing `.tex` files, `.cls` files, and LaTeX Dockerfiles in their current state
- **When** all ISS-001 implementation changes are committed
- **Then** no `.tex` or `.cls` file has been modified or deleted (`git diff --name-only` against the parent commit shows no changes to `*.tex` or `*.cls`), confirming the defensive exclusion boundary is intact

## SYSTEM_STATUS_SUMMARY

| Parameter | Value |
| :--- | :--- |
| STATUS | `SPECIFIED` |
| EPIC_SLUG | `001-typst-cv-migration` |
| BRANCH_NAME | `feat/001-typst-cv-migration/001-local-typst-cv-generation` |
| SPEC_PATH | `specs/001-typst-cv-migration/001-local-typst-cv-generation/spec.md` |
| ISSUE_ID | `ISS-001` |
| NEXT_ACTION | `Run deviate-specify.sh post to validate, commit, and transition to TASKS phase` |
