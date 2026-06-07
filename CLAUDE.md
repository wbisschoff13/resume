# CLAUDE.md — latex-cv / Typst Migration

## Project Identity

This repository produces 4 PDF documents from Typst source:

| File | Variant | Output |
|------|---------|--------|
| `cv.typ` | General | `W_Bisschoff_CV.pdf` |
| `cv_systems.typ` | Systems (edge/embedded) | `W_Bisschoff_CV_systems.pdf` |
| `cv_infrastructure.typ` | Infrastructure (cloud/platform) | `W_Bisschoff_CV_infrastructure.pdf` |
| `cover_letter.typ` | Cover letter | `W_Bisschoff_Cover_Letter.pdf` |

Content lives in `content/data.typ`; layout logic lives in `lib/template.typ`.

> **Old files `cv_embedded.typ` / `cv_enterprise.typ` are deprecated.** The internal variant keys were renamed `embedded → systems` and `enterprise → infrastructure`. Only `cv_systems.typ` and `cv_infrastructure.typ` are active.

> **Structural note:** The internal variant keys were renamed `embedded → systems` and `enterprise → infrastructure`
> in a single session (June 2026). This touched `data.typ`, both variant files, `.mise.toml`, `.github/workflows/`,
> and `analysis/experience_master.md`. The old `cv_embedded.typ` / `cv_enterprise.typ` files are **deprecated and broken**
> (they filter for old variant keys). Use only `cv_systems.typ` / `cv_infrastructure.typ`.

## Execution Contract

Primary Tool Execution API: `mise run <task>`

| Task | Description |
|------|-------------|
| `mise run build` | Compile all 4 documents to PDF |
| `mise run check` | Run all verification checks (compile) |
| `mise run check-compile` | Verify all documents compile without errors |
| `mise run lint` | Validate syntax via compilation |
| `mise run dev` | Watch general CV and recompile on changes |
| `mise run dev-systems` | Watch systems CV variant |
| `mise run dev-infrastructure` | Watch infrastructure CV variant |
| `mise run clean` | Remove generated PDF artifacts |
| `mise run setup` | Verify mise toolchain and typst version |
| `mise run help` | List all available tasks |

## Verification Loop

- Run `mise run check` before any commit
- Compilation success is the primary test (no unit test framework)
- Review generated PDFs visually for layout regressions
- **Check page count**: after any content change, verify PDF page count via `pdfinfo <file>.pdf`. Both systems and infrastructure variants must fit on **1 page each**. The general CV may be 2 pages. If overflowing, trim experience bullets (Junior Lecturer can be dropped from variants, or shorten verbose bullets).
- **Check skills section rendering**: run `pdftotext -layout <file>.pdf` and inspect the Skills section to ensure category labels render inline with values (not wrapped/column-reordered). Non-layout `pdftotext` reads grid content column-by-column, giving false-positives.

## Content Master

- `content/master-list.md` is the canonical source of truth for all CV content. It uses the variant labels `general / systems / infrastructure`.
- Each experience entry is cross-referenced to its STAR story in `content/star-stories.md` via `[STAR N]` tags.
- Any addition/change to CV content must also be made in `content/master-list.md` — and vice versa. After content rework sessions, check the master list for drift and sync it.
- The CV may never contain content not present in the master list.
- Before editing `content/data.typ`, verify the master list is up to date first.
- When trimming for space, remove entries from `variant_tags` rather than deleting content — the master list preserves the full text for future use.

## Profile Discernment

The two CV variants target distinct roles. Every piece of content must pass the smell test for its target:

### Systems Engineer — about the device
> The thing that runs code in the physical world. Close to the hardware: microcontrollers, sensors, real-time operating systems, communication protocols. You're building the edge node that collects data and makes decisions at millisecond speed.

- **Focus:** The device / firmware / edge
- **Languages:** C, C++, Assembly, FreeRTOS
- **Concerns:** Real-time, memory, protocols (UART/SPI/I2C)
- **The product:** A thing that senses and acts
- **Target roles:** IoT, HIL, embedded roles
- **Avoid:** Docker Compose, cloud platform details, front-end frameworks

### Infrastructure Engineer — about the environment
> The servers, networks, and pipelines that data flows through. Docker, cloud services, databases, CI/CD. Building the platform that runs reliably at scale.

- **Focus:** The servers / cloud / platform
- **Languages:** Python, Bash, Pulumi (IaC)
- **Concerns:** Uptime, scaling, networking, data persistence
- **The product:** A system that runs reliably
- **Target roles:** Cloud, Platform, SRE roles
- **Avoid:** Microcontroller parameters, NFC APDU, low-level hardware terms, front-end frameworks (Expo/React Native → front-end ATS classification)

> **ATS classification guard:** Never mention Expo, React Native, or any front-end/mobile framework on the infrastructure CV. It will cause ATS to classify as a front-end or generic app developer, not a platform/infrastructure engineer.

### Overlap warning
Content that spans both domains (e.g., the Divergent Tabletop Wiki project which has both CRDT systems-level mechanics AND PostgreSQL RLS platform work) must be framed differently per variant. Systems variant leads with data structures and synchronization; infrastructure variant leads with database isolation and async execution.

## Conventions (from rework sessions)

- **Skills format**: Use inline `Category : Value1, Value2` format (no grid columns). ATS parsers read grids column-by-column, not row-by-row, causing categories to appear after their values in extraction.
- **Skills categories**: Use descriptive tier labels. Keep category names short enough to fit on one line at 11pt bold.
- **Certification marker**: Appended as a separate line in the header subtitle band, not inlined with the position title.
- **Spec-Driven Development (SDD)**: Present in both systems and infrastructure skills matrices (`Cross-Domain Integration` for systems, `Systems & Automation` for infrastructure). Keep only if page count allows.
- **No inline math/tilde symbols**: `~60%` → `approximately 60%`. Audit for these on initial read.
- **Tool name casing**: Verify against official ecosystem casing (e.g., `pytest` not `Pytest`, `pandas` not `Pandas`, `Agile` not `AGILE`).
- **Experience reframes**: Use STAR (Situation, Task, Action, Result) structure for project bullets when reframing. Lead with the architecture/mechanism, then quantify the outcome.
- **Variant exclusion**: To remove an entry from a variant, remove its tag from `variant_tags` — don't delete the entry itself. If removing the last non-general variant, keep the entry under `("general",)`.

## Layout

- **Skills position**: The skills matrix sits directly beneath the Professional Summary (top-third of page), not below Experience. This matches the recruiter/ATS scan path.
- **Position override**: Variant files (`cv_systems.typ`, `cv_infrastructure.typ`) override the `position` field from `data.typ` via dictionary merge. Keep both in sync.
- **Certification**: Rendered as a separate line in the header after the position subtitle, via `author.certification`.

## Constraints

- **ATS Compatibility**: single-column layout, inline skills (no grid columns), `ligatures: false` on `set text()`
- **Data/Presentation Separation**: content in `content/data.typ`, layout in `lib/template.typ`
- **Bi-Variant Output**: systems + infrastructure variants with filtered experience/skills via `variant_tags`
- **LaTeX Removal**: all `.tex`, `.cls`, LaTeX Dockerfiles must be removed
- **No secrets** in code, config, or commit history
- **Never use `--no-verify`** with git commit/push without explicit user approval
