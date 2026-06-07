# Design: YAML Content Layer Migration

## [RECOMMENDED_ARCHITECTURE]

**Nested Monolithic YAML with Typst Adapter Layer**

- **Data Layer**: Consolidate `content/data.typ` (298 lines) and `content/master-list.md` into a single canonical file: `content/data.yaml`. This file will contain a top-level `base` dictionary for shared content and a `variants` dictionary keyed by variant name (`general`, `embedded`, `enterprise`), satisfying the constitution's mandate that "YAML (`content/*.yaml`) is the single source of truth".
- **Integration Seam (Typst)**: Modify `lib/template.typ` to load the data via Typst's built-in `let data = yaml("content/data.yaml")`. Update the existing `_resolve()` and `_resolve_entries()` functions to operate on this nested YAML structure (e.g., merging `data.base` with `data.variants[variant]`). This preserves the existing `cv.typ` entry point signature (`render_cv(cv_data, variant: "general")`) with zero changes to the presentation layer.
- **Integration Seam (Astro)**: The Astro website consumes the exact same `content/data.yaml` file natively via Node.js `fs` or a YAML parser, requiring no build-step preprocessing and guaranteeing "Deterministic Builds: Zero external network calls during compilation."

## [OPTIONS_MATRIX]

| Option | Complexity | Testability | Constitutional Alignment | Reversibility | Blast Radius | Verdict |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Option 1: Nested Monolithic YAML | Low | High | Aligned | Easy | Medium | Recommended |
| Option 2: Modular Split YAML | Medium | Medium | Aligned | Easy | Low | Rejected |
| Option 3: Build-Script Preprocessed YAML | High | Medium | Tension | Low | Medium | Rejected |

## [REJECTED_OPTIONS]

- **Option 3: Build-Script Preprocessed YAML**: Violates Constitution v0.2.0 constraint: "Content must be strictly separated from layout logic — stored in `content/*.yaml`, consumed via Typst's built-in `yaml()`." Introducing a preprocessing script shifts the variant-resolution logic out of Typst and into an external toolchain, increasing blast radius and adding a non-deterministic build dependency.
- **Option 4: Pure Typst Data Module (Status Quo)**: Fails the core problem statement: "Replace the current hardcoded `content/data.typ` + `content/master-list.md` duality with a single YAML-based canonical content layer that both Typst... and Astro... consume." Astro cannot natively consume `.typ` files without complex, brittle AST parsing.

## [DESIGN_TRADEOFFS]

| Decision | Trade-off | Why This Side |
| :--- | :--- | :--- |
| File Size vs. Merge Complexity | Monolithic YAML is larger, but eliminates complex merge logic. Split YAML improves readability but requires manual Typst dictionary merging. | Favor Monolithic. Current `content/data.typ` is only 298 lines. A YAML equivalent will remain well under 500 lines, avoiding the fragility of manual Typst dictionary merging. |
| Typst Native vs. Astro Native Resolution | Typst's `yaml()` returns a Typst dictionary, while Astro expects a JavaScript object. | The nested monolithic structure (`{ base: {...}, variants: { general: {...} } }`) is natively understood by both ecosystems without transformation, guaranteeing symmetric consumption. |
| Variant Scalability | Monolithic YAML may become cumbersome if variants grow beyond 3-4. | The architecture is reversible. If variant count exceeds 5, the system can be incrementally refactored to Modular Split YAML without changing the `cv.typ` entry point. |

## [CONTRARIAN_VIEWPOINTS]

- **The Type-Safety Regression**: Migrating from `.typ` dictionaries to `.yaml` sacrifices compile-time structural validation. Typst natively understands `.typ` syntax and can catch malformed dictionaries during parsing. YAML is treated as an opaque blob until `yaml()` evaluates it at runtime, deferring structural errors from parse-time to render-time.
- **The Silent Failure Trap**: The proposed defensive `.at(key, default: ...)` pattern prioritizes build stability over data integrity. If an author misspells a key in YAML, the Typst compiler will not fail; it will silently resolve to `none` or the default value. This results in blank or incomplete sections in the final PDF without any warning.
- **YAML Feature Limitations**: Typst's built-in `yaml()` may not support advanced YAML features (e.g., anchors `&`, aliases `*`). If the CV content grows in complexity, authors may hit expressive limits in pure YAML that were previously solvable with Typst's native scripting capabilities.

## [RISK_REGISTER]

| Risk ID | Risk | Likelihood | Impact | Mitigation | Owner | Source Anchor |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| RSK-001 | Silent Data Loss: Misspelled YAML keys resolve to `none` via `.at()`, producing incomplete PDFs that pass CI. | High | Medium | Implement a pre-commit hook or `validate.typ` script that asserts critical top-level keys are not `none`. | Dev Agent | `explore.md`: "No schema validation: Missing keys cause runtime errors" |
| RSK-002 | Environmental Divergence: CI/CD or contributor machines run Typst `< 0.14.2`, causing `unknown function: yaml` errors. | Medium | High | Explicitly pin Typst version (e.g., `0.14.2`) in `.mise.toml` and CI workflow. | Dev Agent | `explore.md`: "Typst 0.14.2 has built-in `yaml()`" |
| RSK-003 | Null Handling Ambiguity: YAML `null` implicitly converts to Typst `none`, creating ambiguity between "missing" and "explicitly empty". | Low | Low | Establish strict convention: use empty strings `""` for explicit emptiness, reserve `null` for fallback defaults. | Dev Agent | `explore.md`: "YAML `null` → Typst `none`" |
| RSK-004 | Schema Drift: Without formal YAML schema, `content/*.yaml` structure can drift over time. | Medium | Medium | Maintain a reference `content/example.yaml` and enforce via lightweight CI validation (e.g., `yamllint`). | Dev Agent | `explore.md`: "No schema validation" |

## [CONSTITUTIONAL_ALIGNMENT_AUDIT]

| Constitutional Clause | Architectural Decision | Alignment | Notes |
| :--- | :--- | :--- | :--- |
| "Content must be strictly separated from layout logic — stored in `content/*.yaml`, consumed via Typst's built-in `yaml()`." | Migrate `data.typ` and `master-list.md` to `content/*.yaml` and consume via `yaml()`. | Aligned | Directly satisfies the mandate to decouple data from Typst layout logic. |
| "YAML (`content/*.yaml`) is the single source of truth — imported via Typst's built-in `yaml()`. No external packages required." | Use Typst's native `yaml()` without third-party package managers. | Aligned | Adheres strictly to the single source of truth principle and prohibition on external packages. |
| "Zero external network calls during compilation." | Local YAML file resolution via `yaml()`. | Aligned | File system reads are inherently deterministic and require no network egress. |
| "`typst compile` succeeds, `typst check` passes, `typst fmt --check` passes." | Rely on default Typst tooling combined with defensive `.at(key, default:)` to prevent runtime crashes. | Tension | Ensures `typst compile` succeeds, but creates false positives. Builds will pass even when critical content is missing, violating the spirit of a reliable, verified canonical source. |

## [SOURCE_REGISTRY]

| ID | Type | Source / Path (Strictly Relative to Repo Root) | Relevance Note |
| :--- | :--- | :--- | :--- |
| SRC-001 | Constitution | `specs/constitution.md` | Defines architectural principles, tech stack, and testing protocols for the migration. |
| SRC-002 | Explore_MD | `specs/002-yaml-content-layer/explore.md` | Provides empirical findings on Typst 0.14.2 built-in `yaml()`, current `data.typ` structure, and ecosystem research. |
| SRC-003 | Codebase_File | `content/data.typ` | Current 298-line hardcoded data dictionary, target of migration. |
| SRC-004 | Codebase_File | `lib/template.typ` | Layout engine containing `_resolve()` and `_resolve_entries()` functions to be adapted. |

## [STATUS_SUMMARY]

| Metric | Value |
| :--- | :--- |
| STATUS | AWAITING_HITL_GATE_1 |
| FEATURE_SLUG | 002-yaml-content-layer |
| EPIC_ID | 002 |
| GIT_BRANCH | main |
| SPEC_TARGET_DESIGN | `specs/002-yaml-content-layer/design.md` |
| SPEC_TARGET_DATAMODEL | `specs/002-yaml-content-layer/data-model.md` |
| NEXT_ACTION | Human reviews design.md + data-model.md, then invokes the `prd` skill |
