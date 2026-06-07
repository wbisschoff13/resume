# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

<!-- MANAGED_BY: tools:init -->

## ⚙️ Project Execution Contract (MANDATORY)

This section defines **non-negotiable execution rules** for this repository.
These rules override global defaults if conflicts arise.

### Directory Handling (CRITICAL)

⚠️ **ALL directory changes MUST occur inside subshells**

**Required pattern:**

```bash
Bash((cd path && command))
```

**Rules:**

- Never run `cd` as a standalone command
- Never assume directory state persists between Bash invocations
- Prefer relative paths or tool-specific directory flags (`mise run -C`, `pnpm --prefix`, etc.)

Violations of this rule are considered **execution errors**, not style issues.

---

### 🛠️ mise as Execution API

This repository uses **mise** (https://mise.fyi) as the canonical interface for build, test, lint, and dev commands.

- **Use mise tasks** over direct tool invocation (e.g., `mise run build` instead of `pnpm build`)
- **`mise ls`** shows all available tasks
- **`mise run <task>`** executes a task

This rule exists to ensure consistency and debuggability across development environments.

**Standardized Commands:**

- `mise run setup` - Install dependencies and configure git hooks
- `mise run check` - Run all validation checks (format, lint, type-check, etc.)
- `mise run format` - Apply code formatting
- `mise run lint` - Run linters
- `mise run fix` - Apply all auto-fixes (format + lint)
- `mise run build` - Build production site
- `mise run dev` - Start development server
- `mise run clean` - Remove build artifacts
- `mise ls` - Show all available commands

---

### 🧠 State & Authority Model (MANDATORY)

This repository follows a strict authority hierarchy.

**Sources of Truth (Highest → Lowest):**

1. Task / Phase state (Markdown plans or Task-Master)
2. `/sync` results
3. Git commits
4. Claude internal TODOs (ephemeral)
5. Claude reasoning / summaries

**Rules:**

- Only top-level tasks or phases are authoritative
- Subtasks are execution guidance only
- Progress is written ONLY via `/sync`
- Commits MUST reflect synced state
- Subtasks are NOT authoritative and MUST NOT be synced
- Task completion implies all required subtasks are satisfied
- Execution tracking happens only via Claude TODOs

If ambiguity exists, the higher source always wins.

---

### ⚡ Fast-Lane Execution Contract

This repository supports a fast-lane workflow for bounded work.

**Allowed fast-lane entry points:**

- `/plan:fix`
- `/tm:fix`

**Fast-lane rules:**

- Exactly ONE top-level task
- No architectural decisions
- No cross-system changes
- No partial progress tracking
- Completion is atomic

If scope exceeds bounds → escalate immediately.

---

### 🔐 Git Commit Authority (MANDATORY)

**CRITICAL: Claude must NEVER automatically create commits unless the user explicitly prompts it to do so.** Even when all conditions below are met, commits require explicit user approval.

Claude may execute `git commit` **only** under ALL of the following conditions:

1. `/sync` has completed successfully
2. Authoritative state is updated:
   - Markdown task / phase marked complete OR
   - Task-Master task marked DONE
3. The user has explicitly approved the commit
4. The commit is scoped to exactly one task or phase
5. The commit message follows the required format

If ANY condition is not met:

- Claude MUST NOT commit
- Claude MUST stop and ask for guidance

#### Commit Message Formats

**Markdown task:**

```
Task: <task title>

* <concise summary>
```

**Task-Master task:**

```
TM-<ID>: <task title>

* <concise summary>
```

---

### Git Hooks

This repository uses git hooks to enforce code quality automatically:

- **Pre-commit:** Runs `mise run check` (validates formatting, linting, type-checking)
- **Pre-push:** Runs `mise run build` (verifies build succeeds)

Hooks are installed automatically by `mise run setup` and can be managed with:

- `mise run hooks` - Install git hooks manually
- `mise run uninstall-hooks` - Remove git hooks

**Skipping hooks:**

- Bypass pre-commit: `git commit --no-verify`
- Bypass pre-push: `git push --no-verify`

---

## Project Overview

This is an **AstroWind** template - a production-ready Astro 5.0 website with **Tailwind CSS 4.x + DaisyUI**, designed for fast, SEO-friendly static sites with blogging capabilities. It uses static site generation (SSG) with optional hybrid/server modes.

### Tech Stack Highlights

- **Astro 5.0** - Modern static site generator
- **Tailwind CSS 4.x** - CSS-first configuration with Lightning CSS engine (5x faster builds)
- **DaisyUI 5.x** - 40+ pre-built accessible components
- **Dark-only theme** - Custom theme with primary color `#599692`
- **CSS-first config** - No `tailwind.config.js`, configuration in `tailwind.css`

---

## Common Development Commands

**Note:** This repository uses mise for consistent development workflows. Both `mise run` and `pnpm` commands are shown below.

```bash
# === Setup ===
mise run setup        # Install dependencies (RECOMMENDED)
pnpm install          # Install dependencies only

# === Development ===
mise run dev          # Start dev server at localhost:4321
pnpm dev              # Start dev server (alternative)

# === Build & Preview ===
mise run build        # Build production site to ./dist/
pnpm build            # Build production site (alternative)
pnpm preview          # Preview production build locally

# === Code Quality (mise - RECOMMENDED) ===
mise run check        # Run ALL validation checks (format, lint, type-check)
mise run lint         # Run ESLint
mise run fix          # Apply all auto-fixes (format + lint)

# === Code Quality (pnpm - alternative) ===
pnpm check            # Run all checks (astro-check, eslint, prettier)
pnpm check:astro      # Type checking with Astro
pnpm check:eslint     # ESLint validation
pnpm check:prettier   # Prettier formatting check
pnpm fix              # Auto-fix ESLint and Prettier issues
pnpm fix:eslint       # Auto-fix ESLint issues
pnpm fix:prettier     # Auto-format with Prettier

# === Utility ===
mise run clean        # Remove build artifacts
mise ls               # Show all available mise tasks
```

---

## UI Development Tools

### Frontend Design Plugin (Claude Code)

This project leverages Claude Code's `frontend-design` skill for rapid, production-quality UI component development.

**What it does:**

- Generates distinctive, high-quality frontend interfaces
- Avoids generic AI aesthetics with unique design patterns
- Creates production-ready code following best practices

**When to use it:**

- Building custom UI components and widgets
- Creating landing pages and marketing sections
- Developing interactive interfaces and forms
- Designing custom theme toggle components
- Rapid prototyping of new UI ideas

**How to invoke:**

```
/frontend-design
```

Or simply ask Claude:

- "Build a hero section with the frontend-design plugin"
- "Create a contact form using frontend-design"
- "Design a theme toggle button with the frontend-design skill"

**Integration with AstroWind:**

- Works seamlessly with Tailwind CSS and Astro components
- Ideal for creating custom layouts beyond default AstroWind templates
- Particularly useful for theme system UI components (TM-002)
- Generates code that follows the project's existing design patterns

---

## Architecture & Key Concepts

### Content Collections (Astro 5.0)

The blog uses **Astro Content Collections** with type-safe Zod schemas:

- **Blog posts** are stored in `src/data/post/` (`.md` or `.mdx`)
- **Collection schema** defined in `src/content/config.ts`
- **Frontmatter fields**: `title`, `excerpt`, `image`, `category`, `tags`, `author`, `publishDate`, `updateDate`, `draft`, `metadata`

When adding blog posts:

- Place files in `src/data/post/`
- Follow the Zod schema in `src/content/config.ts`
- Use MDX for mixed Markdown + JSX content

### Custom Integration (`vendor/integration/`)

The custom **astrowind integration** loads `src/config.yaml` and provides a virtual module:

```typescript
import { SITE, I18N, METADATA, APP_BLOG, UI, ANALYTICS } from 'astrowind:config';
```

**Key responsibilities:**

- Loads site configuration from YAML
- Watches `src/config.yaml` for changes
- Updates `robots.txt` with sitemap reference after build
- Provides config via Vite virtual module

### Navigation Structure

Site navigation is centralized in `src/navigation.ts`:

- **headerData**: Main navigation links and actions
- **footerData**: Footer links, social links, legal links
- Uses helper functions from `src/utils/permalinks.ts` for consistent URL generation

### Page Architecture Pattern

Pages are assembled from **reusable widgets** in `src/components/widgets/`:

- Widget-based design (Header, Hero, Features, etc.)
- Layout hierarchy: `Layout.astro` → `PageLayout.astro` → page content
- Blog uses `MarkdownLayout.astro` for post rendering

### Styling System (Tailwind 4.x + DaisyUI)

**CSS-first configuration** in `src/assets/styles/tailwind.css`:

```css
@import 'tailwindcss';
@plugin "daisyui" {
  themes: --default;
}
@plugin "@tailwindcss/typography";
```

**Design tokens** via CSS variables in `@layer theme`:

- **DaisyUI theme tokens**: `--p` (primary), `--s` (secondary), `--a` (accent), `--n` (neutral)
- **Extended tokens**: `--aw-color-text-default`, `--aw-color-bg-page`, etc.
- **Colors**: Primary `#599692`, Secondary `#4a7d7a`, Background `#121212`
- **Dark-only**: Site uses dark mode exclusively (no light mode switcher)

**Component styling**:

- **DaisyUI classes**: Use `btn btn-primary`, `btn btn-secondary`, etc.
- **Custom Button component**: `src/components/ui/Button.astro` with variant props
- **Rounded-full**: Buttons maintain rounded appearance (`rounded-full` class added)
- **Typography**: `@tailwindcss/typography` plugin for blog content prose

**Custom animations**:

- `fade-in-up` keyframes defined in CSS
- Use `animate-fade-in-up` or `data-animate` attributes
- Intersect variant for scroll-triggered animations: `@variant intersect`

**No `tailwind.config.js`** - All configuration is in the CSS file following Tailwind 4.x conventions.

### Permalink System

URL generation is centralized in `src/utils/permalinks.ts`:

- `getPermalink()` - Generate page URLs
- `getBlogPermalink()` - Generate blog URLs
- `getAsset()` - Generate asset URLs
- Respects `trailingSlash` setting from `src/config.yaml`

---

## Configuration Files

### `src/config.yaml`

**Primary site configuration** - edit this for site metadata:

```yaml
site:
  name: 'Site Name'
  site: 'https://example.com'
  base: '/'
  trailingSlash: false

metadata:
  title:
    default: 'Default Title'
    template: '%s — Site Name'
  description: 'Site description'

apps:
  blog:
    isEnabled: true
    postsPerPage: 6
    post:
      permalink: '/blog/%slug%'

ui:
  theme: 'system' # system | light | dark | light:only | dark:only

analytics:
  vendors:
    googleAnalytics:
      id: null # or "G-XXXXXXXXXX"
```

### `astro.config.ts`

Key integrations:

- **@tailwindcss/vite** - Tailwind CSS 4.x Vite plugin (in `vite.plugins`)
- **DaisyUI** - Component library configured in CSS
- **MDX** - Markdown with JSX support
- **Sitemap** - Automatic sitemap generation
- **Astro Icon** - Tabler and Flat Color Icons
- **Partytown** - Offload analytics scripts
- **Astro-compress** - Asset optimization
- **Custom astrowind** - YAML config loading

**Note**: Tailwind is loaded via Vite plugin, not Astro integration. This is the Tailwind 4.x approach.

### `tsconfig.json`

- Path alias: `~/*` → `src/*`
- Strict null checks enabled
- Includes Astro types

---

## Important Development Notes

### Blog Routing

Blog uses **dynamic routing** with `prerender = true`:

- Main: `src/pages/[...blog]/index.astro`
- Categories: `src/pages/[...blog]/[category]/index.astro`
- Tags: `src/pages/[...blog]/[tag]/index.astro`
- Pagination: `src/pages/[...blog]/[...page].astro`

The blog only works with pre-rendering in the current version. SSR support is planned for AstroWind 2.0.

### SEO & Metadata

**SEO is built-in** via `@astrolib/seo` integration:

- Meta tags from `src/config.yaml`
- Open Graph and Twitter cards
- Sitemap auto-generation
- robots.txt auto-updated with sitemap reference

### Static Assets

- **`public/`** - Direct file serving (no transformation)
- **`src/assets/`** - Imported and optimized by Astro
- **Image domains** configured in `astro.config.ts` (currently `cdn.pixabay.com`)

### Component Organization

```
src/components/
├── blog/          # Blog-specific components
├── common/        # Shared UI components
├── ui/           # Reusable UI elements
├── widgets/      # Page sections/assemblers
├── CustomStyles.astro  # Custom CSS injection
├── Favicons.astro      # Favicon management
└── Logo.astro          # Site logo component
```

---

## RSS Feed

RSS feed is generated at `src/pages/rss.xml.ts` based on published blog posts. URL is automatically added to navigation and footer.

---

## Deployment

The site outputs static files to `dist/` and can be deployed to any static hosting:

- Netlify (`netlify.toml` included)
- Vercel (`vercel.json` included)
- GitHub Pages (set `base: '/repo-name'` in config.yaml)
- Docker (`Dockerfile` included)
