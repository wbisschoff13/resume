# Session Memory — June 2026

## CV Rework — Phase 1

### What changed

- **Variant rename**: `embedded` → `systems`, `enterprise` → `infrastructure`. This was a global rename across `data.typ` (variant keys, variant_tags, dictionary keys), variant files, `.mise.toml`, `.github/workflows/release.yml`, and `analysis/experience_master.md`.
- **New files**: `cv_systems.typ` and `cv_infrastructure.typ` are the active entry points. Old `cv_embedded.typ` / `cv_enterprise.typ` are deprecated and broken (filter for old variant keys).
- **Output PDFs**: `W_Bisschoff_CV_systems.pdf` and `W_Bisschoff_CV_infrastructure.pdf`.

### Skills section

| Change | Detail |
|--------|--------|
| **Position** | Moved from bottom to directly beneath Summary (top-third) |
| **Format** | Grid columns replaced with inline `Category : Value1, Value2` (ATS-safe) |
| **Systems categories** | Primary Competencies, Secondary Competencies, Foundational Systems, Cross-Domain Integration |
| **Infrastructure categories** | Primary Competencies, Secondary Platforms, Data Layer Infrastructure, Systems & Automation |
| **SDD added** | Spec-Driven Development added to both variants (fits on 1 page) |

### Content reframes

| Entry | Systems | Infrastructure |
|-------|---------|---------------|
| Divergent Tabletop | Rewritten as STAR bullets (CRDT, GenServer buffers, BEAM supervision) | Kept original PostgreSQL/RLS/Oban focus |
| FARO Africa (bullet 4) | Kept original | Replaced AWS/Pulumi with Vultr Linux infra reframe |
| Junior Lecturer | Removed | Removed (page space) |

### Key decisions

- Expo/React Native intentionally excluded from infrastructure CV (prevents front-end ATS classification)
- Technical Application Scope section removed entirely (was padding)
- Certification marker added as separate header line
- Pulumi moved from Primary to Systems & Automation (infrastructure CV)
- Python and PostgreSQL promoted to Primary (infrastructure CV)

### Things to watch

- If adding content, check `pdfinfo` page count — both variants must stay on 1 page
- Skills section uses inline format — verify with `pdftotext -layout` that categories render on same line as values
- Cover letter uses `variant: "general"` — unaffected by the rename
- The `position` field in variant files overrides `data.typ` — keep them in sync
