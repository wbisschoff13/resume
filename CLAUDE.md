# CLAUDE.md — latex-cv / Typst Migration

## Project Identity

This repository migrates a LaTeX CV to Typst. The project produces 4 PDF documents from Typst source:

- `cv.typ` — general CV
- `cv_embedded.typ` — embedded systems variant
- `cv_enterprise.typ` — enterprise variant
- `cover_letter.typ` — cover letter

Content lives in `content/data.typ`; layout logic lives in `lib/template.typ`.

## Execution Contract

Primary Tool Execution API: `mise run <task>`

| Task | Description |
|------|-------------|
| `mise run build` | Compile all 4 documents to PDF |
| `mise run check` | Run all verification checks (compile + format-check) |
| `mise run check-compile` | Verify all documents compile without errors |
| `mise run format` | Format all Typst sources (needs typst >= 0.13) |
| `mise run format-check` | Check formatting without modifying (read-only) |
| `mise run lint` | Validate syntax via compilation (no dedicated linter) |
| `mise run fix` | Apply formatting fixes |
| `mise run dev` | Watch general CV and recompile on changes |
| `mise run dev-embedded` | Watch embedded CV variant |
| `mise run dev-enterprise` | Watch enterprise CV variant |
| `mise run clean` | Remove generated PDF artifacts |
| `mise run setup` | Verify mise toolchain and typst version |
| `mise run help` | List all available tasks |

## Verification Loop

- Run `mise run check` before any commit
- Compilation success is the primary test (no unit test framework)
- Review generated PDFs visually for layout regressions

## Constraints

- **ATS Compatibility**: single-column layout, `ligatures: false` on `set text()`
- **Data/Presentation Separation**: content in `content/data.typ`, layout in `lib/template.typ`
- **Bi-Variant Output**: embedded + enterprise variants with filtered experience/skills
- **LaTeX Removal**: all `.tex`, `.cls`, LaTeX Dockerfiles must be removed
- **No secrets** in code, config, or commit history
- **Never use `--no-verify`** with git commit/push without explicit user approval
