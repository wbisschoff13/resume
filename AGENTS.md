# AGENTS.md

### [PRESENTATION]

- Content in `content/data.typ`, layout in `lib/template.typ`
- Never mix data and layout logic
- No `.tex` or `.cls` files may be introduced

### [VERIFICATION]

- Always run `mise run check` before committing
- Verify new Typst source files compile: `typst compile <file>.typ`
- Check PDF output visually for layout shifts

### [COMMIT]

- Scope: use `001` for Typst migration work (branch `feat/001-typst-cv-migration/*`)
- Convention: `type(scope): description`
