# Data Model: YAML Content Layer Migration

## [ENTITY_DEFINITIONS]

### `Config`
- **Source-of-truth**: `content/config.yaml`
- **Lifecycle owner**: User (manual edit)
- **Attributes**:
  | Attribute | Type | Invariant | Source Anchor |
  | :--- | :--- | :--- | :--- |
  | `name` | string | Required | `explore.md`: "Personal information — used by both CV and website" |
  | `title` | string | Required | `explore.md`: "Position title per variant" |
  | `contact` | object | `email` must be valid format | `explore.md`: "email, phone, location, github, website, linkedin" |
  | `summary` | string | Required | `explore.md`: "Summary per variant" |
- **Invariants**: `contact.email` must be a valid email format; `name` is required.

### `Experience`
- **Source-of-truth**: `content/experience.yaml`
- **Lifecycle owner**: User (manual edit)
- **Attributes**:
  | Attribute | Type | Invariant | Source Anchor |
  | :--- | :--- | :--- | :--- |
  | `id` | string | Unique slug | `explore.md`: "All roles, all bullets, all variants" |
  | `company` | string | Required | `explore.md`: "company: 'Divergent Tabletop'" |
  | `role` | string | Required | `explore.md`: "roles: general, systems, infrastructure" |
  | `start_date` | string | ISO-8601 or "MMM YYYY" | `explore.md`: "start_date: 'Jul 2025'" |
  | `end_date` | string \| null | `start_date` <= `end_date` | `explore.md`: "end_date: null # null = present" |
  | `bullets` | array | Contains `ExperienceBullet` | `explore.md`: "Each bullet carries curation tags" |
- **Invariants**: `start_date` <= `end_date` (if present); `id` is unique.

### `ExperienceBullet` (Embedded Entity)
- **Source-of-truth**: `content/experience.yaml` (nested)
- **Lifecycle owner**: User (manual edit)
- **Attributes**:
  | Attribute | Type | Invariant | Source Anchor |
  | :--- | :--- | :--- | :--- |
  | `text` | string | Required | `explore.md`: "text: 'Founded neurodivergent-focused...'" |
  | `cv_priority` | integer | ∈ {1, 2, 3} | `explore.md`: "cv_priority (1-3) and website_show tags per bullet" |
  | `website_show` | boolean | Required | `explore.md`: "website_show: true" |
  | `star_ref` | string \| null | Must match `StarStory.id` | `explore.md`: "star_ref links bullets to star-stories.yaml entries" |
- **Invariants**: `cv_priority` ∈ {1, 2, 3}; if `cv_priority` == 3, `website_show` must be true.

### `StarStory`
- **Source-of-truth**: `content/star-stories.yaml`
- **Lifecycle owner**: User (manual edit)
- **Attributes**:
  | Attribute | Type | Invariant | Source Anchor |
  | :--- | :--- | :--- | :--- |
  | `id` | string | Unique slug | `explore.md`: "14 STAR stories (full format)" |
  | `situation` | string | Required | `explore.md`: "situation: >" |
  | `task` | string | Required | `explore.md`: "task: >" |
  | `action` | string | Required | `explore.md`: "action: >" |
  | `result` | string | Required | `explore.md`: "result: >" |
  | `metrics` | array of string | Optional | `explore.md`: "tags: - performance" |
- **Invariants**: `id` is unique and matches regex `^[a-z0-9-]+$`; all STAR components are non-empty.

### `Skill`
- **Source-of-truth**: `content/skills.yaml`
- **Lifecycle owner**: User (manual edit)
- **Attributes**:
  | Attribute | Type | Invariant | Source Anchor |
  | :--- | :--- | :--- | :--- |
  | `category` | string | Required | `explore.md`: "name: 'Primary'" |
  | `items` | array of string | Unique strings | `explore.md`: "skills: - 'C/C++'" |
- **Invariants**: `category` is non-empty; `items` contains unique strings.

### `Project`
- **Source-of-truth**: `content/projects.yaml`
- **Lifecycle owner**: User (manual edit)
- **Attributes**:
  | Attribute | Type | Invariant | Source Anchor |
  | :--- | :--- | :--- | :--- |
  | `id` | string | Unique slug | `explore.md`: "Project entries + variant tags" |
  | `name` | string | Required | `explore.md`: "name: 'Divergent Tabletop Wiki'" |
  | `description` | string | Required | `explore.md`: "description: general, systems, infrastructure" |
  | `url` | string \| null | Valid URL format | `explore.md`: "link: null" |
  | `technologies` | array of string | Optional | `explore.md`: "variant_tags: - general" |
  | `cv_priority` | integer | ∈ {1, 2, 3} | `explore.md`: "cv_priority (1-3)" |
  | `website_show` | boolean | Required | `explore.md`: "website_show: true" |
- **Invariants**: `id` is unique; `cv_priority` ∈ {1, 2, 3}.

### `Education`
- **Source-of-truth**: `content/education.yaml`
- **Lifecycle owner**: User (manual edit)
- **Attributes**:
  | Attribute | Type | Invariant | Source Anchor |
  | :--- | :--- | :--- | :--- |
  | `institution` | string | Required | `explore.md`: "institution: 'North-West University'" |
  | `degree` | string | Required | `explore.md`: "degree: 'B.Eng. Computer and Electronic Engineering'" |
  | `field` | string | Required | `explore.md`: "Focus on embedded systems..." |
  | `start_date` | string | ISO-8601 or "YYYY" | `explore.md`: "graduation_year: '2020'" |
  | `end_date` | string \| null | `start_date` <= `end_date` | `explore.md`: "graduation_year: '2020'" |
  | `cv_priority` | integer | ∈ {1, 2, 3} | `explore.md`: "cv_priority (1-3)" |
- **Invariants**: `start_date` <= `end_date` (if present).

## [RELATIONSHIP_GRAPH]

| From | Relationship | To | Cardinality | On-Delete | On-Cascade | Source Anchor |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `ExperienceBullet` | references | `StarStory` | N:1 | Set `star_ref` to `null` | None | `explore.md`: "star_ref links bullets to star-stories.yaml entries" |
| `Project` | uses | `Skill` | N:M | N/A (Denormalized) | None | `explore.md`: "variant_tags: - general" |

## [SCHEMA_TABLES]

### `content/config.yaml`
```yaml
# Schema: Config
name: string
title: string
contact:
  email: string
  phone: string | null
  linkedin: string | null
  github: string | null
  location: string | null
summary: string
```

### `content/experience.yaml`
```yaml
# Schema: Experience[]
- id: string
  company: string
  role: string
  start_date: string # ISO-8601 or "MMM YYYY"
  end_date: string | null
  bullets:
    - text: string
      cv_priority: integer # 1, 2, or 3
      website_show: boolean
      star_ref: string | null
```

### `content/star-stories.yaml`
```yaml
# Schema: StarStory[]
- id: string
  situation: string
  task: string
  action: string
  result: string
  metrics: 
    - string
```

### `content/skills.yaml`
```yaml
# Schema: Skill[]
- category: string
  items:
    - string
```

### `content/projects.yaml`
```yaml
# Schema: Project[]
- id: string
  name: string
  description: string
  url: string | null
  technologies:
    - string
  cv_priority: integer # 1, 2, or 3
  website_show: boolean
```

### `content/education.yaml`
```yaml
# Schema: Education[]
- institution: string
  degree: string
  field: string
  start_date: string
  end_date: string | null
  cv_priority: integer # 1, 2, or 3
```

## [STATE_TRANSITIONS]

### Content Curation State Machine (per `ExperienceBullet` / `Project`)
- **States**: `Draft`, `CV_Essential` (cv_priority=1), `CV_Secondary` (cv_priority=2), `Web_Only` (cv_priority=3).
- **Initial State**: `Draft`
- **Terminal States**: `CV_Essential`, `Web_Only`
- **Transitions**:
  | From | Event | Guard | To | Side Effects |
  | :--- | :--- | :--- | :--- | :--- |
  | `Draft` | Promote | `text` is complete and impactful | `CV_Essential` | Appears on all 3 Typst CV variants and Astro. |
  | `CV_Essential` | Demote | Space constraints require demotion | `CV_Secondary` | Appears only on long-format Typst CV and Astro. |
  | `CV_Secondary` | Archive | Relevance to target CV role is low | `Web_Only` | `website_show=true`, excluded from all Typst CV variants. |

### STAR Story Lifecycle State Machine
- **States**: `Ideation`, `Fleshed_Out`, `Validated`, `Archived`.
- **Initial State**: `Ideation`
- **Terminal States**: `Validated`, `Archived`
- **Transitions**:
  | From | Event | Guard | To | Side Effects |
  | :--- | :--- | :--- | :--- | :--- |
  | `Ideation` | Complete | All 4 STAR components are non-empty | `Fleshed_Out` | Ready for review. |
  | `Fleshed_Out` | Validate | Reviewed for clarity and quantifiable metrics | `Validated` | Safe to be referenced by `star_ref`. |
  | `Validated` | Archive | Story is outdated or superseded | `Archived` | Existing `star_ref` links become inactive. |

## [DATA_FLOW]

### Flow: CV Compilation (Typst)
1. **Source**: User edits canonical YAML files in `content/*.yaml`.
2. **Consumption**: Typst templates (`lib/template.typ`) use built-in `yaml("content/experience.yaml")` to load data.
3. **Filtering**: Typst script filters `bullets` where `cv_priority <= target_variant_max_priority` (e.g., Variant A = 1, Variant B = 2, Variant C = 3).
4. **Enrichment**: If `bullet.star_ref` is present, Typst looks up the corresponding `StarStory` in `star-stories.yaml` and appends/expands the STAR details.
5. **Render**: `cv.typ` calls `render_cv(cv_data, variant: "general")` to produce the final PDF.
- **Source Anchor**: `explore.md`: "Content must be strictly separated from layout logic — stored in `content/*.yaml`, consumed via Typst's built-in `yaml()`."

### Flow: Website Rendering (Astro)
1. **Source**: Astro build process reads the same `content/*.yaml` files (via `js-yaml` or similar).
2. **Filtering**: Astro renders all items where `website_show == true` (which includes all `cv_priority` 1, 2, and 3 items).
3. **Enrichment**: Astro expands `star_ref` links into full S/T/A/R sections on case study pages.
4. **Render**: Astro generates static HTML pages with no page limit.
- **Source Anchor**: `explore.md`: "YAML (`content/*.yaml`) is the single source of truth."

## [SOURCE_REGISTRY]

| ID | Type | Source / Path (Strictly Relative to Repo Root) | Relevance Note |
| :--- | :--- | :--- | :--- |
| SRC-001 | Constitution | `specs/constitution.md` | Defines architectural principles, tech stack, and testing protocols for the migration. |
| SRC-002 | Explore_MD | `specs/002-yaml-content-layer/explore.md` | Provides empirical findings on Typst 0.14.2 built-in `yaml()`, current `data.typ` structure, and ecosystem research. |
| SRC-003 | Codebase_File | `content/data.typ` | Current 298-line hardcoded data dictionary, target of migration. |
| SRC-004 | Codebase_File | `lib/template.typ` | Layout engine containing `_resolve()` and `_resolve_entries()` functions to be adapted. |
