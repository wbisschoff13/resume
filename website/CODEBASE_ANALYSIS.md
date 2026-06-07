# Codebase Analysis: Werner Bisschoff Portfolio Website

**Date:** 2026-04-07  
**Status:** Analysis Complete - No Changes Made  
**Purpose:** Identify inconsistencies, flaws, and areas for improvement for public portfolio presentation

---

## TL;DR

The codebase has **four major areas requiring attention** before public release:

1. **Content Architecture:** Mix of hardcoded content (pages) and unused content collection (src/data/post has template posts, src/content/ is nearly empty)
2. **Unused Code:** Significant dead code including duplicate components, unused utilities, and template artifacts
3. **Cleanliness:** Component naming duplication, scattered UI patterns, and inconsistent export patterns
4. **Missing Content Strategy:** No clear separation between "Notes" (blog) and static page content

---

## 1. Content Architecture Analysis

### 1.1 The Content Collection Problem

**Location:** `src/content/` vs `src/data/post/`

**Issue:** The AstroWind template uses **two different content mechanisms**:

| Path                    | Purpose                          | Status                  |
| ----------------------- | -------------------------------- | ----------------------- |
| `src/content/config.ts` | Defines `post` collection schema | **Empty collection**    |
| `src/data/post/*.md`    | Actual blog posts                | **Template demo posts** |

**Evidence:**

```typescript
// src/content/config.ts - defines the collection
const postCollection = defineCollection({
  loader: glob({ pattern: ['*.md', '*.mdx'], base: 'src/data/post' }),
  // ...
});
```

The content collection points to `src/data/post/` but `src/content/` folder is essentially empty (only contains `config.ts`).

**Problem:** This is a **hybrid approach** that creates confusion:

- Astro 5.0 content collections should live in `src/content/`
- The current setup uses `src/data/post/` as the actual content directory
- The `src/content/` folder serves no purpose

### 1.2 Hardcoded Content in Pages

All portfolio content is **hardcoded directly in Astro pages**:

| File                      | Content Type                    |
| ------------------------- | ------------------------------- |
| `src/pages/index.astro`   | Hero, About, Skills, Background |
| `src/pages/work.astro`    | Case studies array              |
| `src/pages/resume.astro`  | Experience, skills arrays       |
| `src/pages/contact.astro` | Form integration                |

**Problems:**

1. **No separation of concerns** - content mixed with markup
2. **Difficult to maintain** - editing requires touching component code
3. **Not portable** - cannot use headless CMS or migrate to different framework

### 1.3 Recommended Content Architecture

For a **clean static site without CMS**, the recommended approach:

```
src/
├── content/
│   ├── config.ts           # Schema definitions
│   ├── pages/             # Static pages content (about, services, etc.)
│   │   └── *.md           # Markdown files for static pages
│   └── posts/             # Blog posts (renamed from data/post)
│       └── *.md
├── pages/                 # Astro page components (thin wrappers)
│   ├── index.astro
│   ├── work.astro
│   └── resume.astro
└── data/                  # ONLY for non-content configuration
    └── config.yaml        # Site metadata
```

**Key Principles:**

- Content in Markdown files (`.md` or `.mdx`)
- Pages are thin wrappers that load content
- Configuration in `config.yaml` (already done correctly)
- No CMS = static content files are the right approach

### 1.4 Blog Posts Analysis

**Location:** `src/data/post/`

| File                                             | Status                            |
| ------------------------------------------------ | --------------------------------- |
| `astrowind-template-in-depth.mdx`                | **Template content** - draft:true |
| `how-to-customize-astrowind-to-your-brand.md`    | **Template content** - draft:true |
| `get-started-website-with-astro-tailwind-css.md` | **Template content** - draft:true |
| `landing.md`                                     | **Template content** - draft:true |
| `markdown-elements-demo-post.mdx`                | **Template content** - draft:true |
| `useful-resources-to-create-websites.md`         | **Template content** - draft:true |

**Issue:** All 6 posts are **template demo content**, not actual notes/blog posts. They all have `draft: true` so they're excluded from builds, but they remain in the repo as dead weight.

**Action Required:** Either delete these or replace with actual notes content.

---

## 2. Unused Code Analysis

### 2.1 Duplicate Components

**Critical Finding:** Component naming collision between `blog/` and `ui/` directories:

| Duplicate         | Files                                                                             |
| ----------------- | --------------------------------------------------------------------------------- |
| `Headline.astro`  | `src/components/blog/Headline.astro` AND `src/components/ui/Headline.astro`       |
| `Grid.astro`      | `src/components/blog/Grid.astro` (used) AND NOT in ui/                            |
| `GridItem.astro`  | `src/components/blog/GridItem.astro` (used) AND NOT in ui/                        |
| `List.astro`      | `src/components/blog/List.astro` (used) AND NOT in ui/                            |
| `ListItem.astro`  | `src/components/blog/ListItem.astro` (used) AND NOT in ui/                        |
| `ItemGrid.astro`  | `src/components/ui/ItemGrid.astro` (used) AND `src/components/ui/ItemGrid2.astro` |
| `ItemGrid2.astro` | `src/components/ui/ItemGrid2.astro` (used) - seems duplicate                      |

**Evidence:**

```
src/components/blog/
├── Grid.astro          # Grid of posts
├── GridItem.astro      # Single post in grid
├── List.astro          # List of posts
└── ListItem.astro      # Single post in list

src/components/ui/
├── ItemGrid.astro      # Generic item grid
├── ItemGrid2.astro     # Another item grid (duplication?)
```

### 2.2 Unused Utility Functions

**Location:** `src/utils/`

| Function                     | File                   | Usage                    | Status    |
| ---------------------------- | ---------------------- | ------------------------ | --------- |
| `toUiAmount()`               | `utils/utils.ts`       | **Never called**         | DEAD CODE |
| `getProjectRootDir()`        | `utils/directories.ts` | **Never called**         | DEAD CODE |
| `getRelativeUrlByFilePath()` | `utils/directories.ts` | **Never called**         | DEAD CODE |
| `findPostsBySlugs()`         | `utils/blog.ts`        | **Never called**         | DEAD CODE |
| `findPostsByIds()`           | `utils/blog.ts`        | **Never called**         | DEAD CODE |
| `findLatestPosts()`          | `utils/blog.ts`        | **Never called**         | DEAD CODE |
| `isRelatedPostsEnabled`      | `utils/blog.ts`        | Exported but check usage | SUSPECT   |
| `isBlogEnabled`, etc.        | `utils/blog.ts`        | Multiple exports         | SUSPECT   |

**Evidence:**

```bash
$ rg "toUiAmount" --files-with-matches
src/utils/utils.ts     # Only defined, never imported elsewhere

$ rg "getProjectRootDir" --files-with-matches
src/utils/directories.ts  # Only defined, never imported elsewhere
```

### 2.3 Unused Blog Routes

**Location:** `src/pages/[...blog]/`

| Route                      | Status                      |
| -------------------------- | --------------------------- |
| `category/[...page].astro` | **Active** - category pages |
| `tag/[...page].astro`      | **Active** - tag pages      |
| `index.astro`              | **Active** - blog list      |

**However in config.yaml:**

```yaml
tag:
  isEnabled: true
  pathname: 'tag'
  robots:
    index: false # Tags are disabled from indexing
```

The tag route exists but is disabled from indexing. This is intentional but creates dead code if tags are never used.

### 2.4 Unused Type Definitions

**Location:** `src/types.d.ts`

| Interface      | Usage      | Status    |
| -------------- | ---------- | --------- |
| `TeamMember`   | Never used | DEAD CODE |
| `Social`       | Never used | DEAD CODE |
| `Stat`         | Never used | DEAD CODE |
| `Price`        | Never used | DEAD CODE |
| `Testimonial`  | Never used | DEAD CODE |
| `Video`        | Never used | DEAD CODE |
| `Collapse`     | Never used | DEAD CODE |
| `Pricing`      | Never used | DEAD CODE |
| `Testimonials` | Never used | DEAD CODE |
| `Brands`       | Never used | DEAD CODE |
| `Features`     | Never used | DEAD CODE |
| `Steps`        | Never used | DEAD CODE |

**Evidence:** grep for each type name - none appear as imports in any file.

### 2.5 ItemGrid vs ItemGrid2

**Finding:** `ItemGrid.astro` and `ItemGrid2.astro` are nearly identical.

**ItemGrid.astro** (`src/components/ui/ItemGrid.astro`):

```astro
<div class="grid mx-auto gap-8 md:gap-y-12">
  {
    items.map(({ title, description, icon, callToAction, classes: itemClasses = {} }) => (
      <div class="intersect-once ...">
        <div class="flex flex-row max-w-md">
          <Icon name={icon || defaultIcon} class="w-7 h-7 mr-2" />
          <div>
            <h3>{title}</h3>
            <p set:html={description} />
          </div>
        </div>
      </div>
    ))
  }
</div>
```

**ItemGrid2.astro** (`src/components/ui/ItemGrid2.astro`):

```astro
<div class="grid gap-8 gap-x-12 sm:gap-y-8">
  {
    items.map(({ title, description, icon, callToAction, classes: itemClasses = {} }) => (
      <div class="relative flex flex-col">
        <Icon name={icon || defaultIcon} class="mb-2 w-10 h-10" />
        <div class="text-xl font-bold">{title}</div>
        <p set:html={description} />
      </div>
    ))
  }
</div>
```

**Differences:**

1. ItemGrid uses `flex-row` (icon left of text), ItemGrid2 uses `flex-col` (icon above text)
2. ItemGrid2 has intersection animation, ItemGrid does not
3. ItemGrid2 has different gap values

**Recommendation:** Consolidate into one component with a `layout` prop.

### 2.6 Unused Dependencies

From `package.json` - check for unused imports:

| Package                | Purpose            | Usage Status             |
| ---------------------- | ------------------ | ------------------------ |
| `limax`                | URL slugify        | Used in `permalinks.ts`  |
| `lodash.merge`         | Deep merge         | Used in `Metadata.astro` |
| `reading-time`         | Post reading time  | Used in `frontmatter.ts` |
| `mdast-util-to-string` | Markdown utilities | Used in `frontmatter.ts` |
| `unist-util-visit`     | AST traversal      | Used in `frontmatter.ts` |

All appear used. No unused dependencies found in package.json.

---

## 3. Clean Code Issues

### 3.1 Component Naming Duplication

**Problem:** Two `Headline.astro` components in different directories:

```
src/components/blog/Headline.astro      # Used in blog contexts
src/components/ui/Headline.astro       # Generic headline
```

**Confusion matrix:**
| File | Used Where |
|------|-----------|
| `blog/Headline.astro` | `MarkdownLayout.astro`, blog pages |
| `ui/Headline.astro` | Not used by any page component |

**Note:** `ui/Headline.astro` is never imported anywhere despite existing in the codebase.

### 3.2 Export Patterns Are Inconsistent

**Blog Utils (`src/utils/blog.ts`):**

```typescript
// Exports at bottom - exported after function definitions
export const isBlogEnabled = APP_BLOG.isEnabled;
export const fetchPosts = async (): Promise<Array<Post>> => { ... };
```

**Permalinks (`src/utils/permalinks.ts`):**

```typescript
// Exports scattered throughout - some at top, some at bottom
export const trimSlash = (s: string) => trim(trim(s, '/'));
export const cleanSlug = (text = '') => { ... };
// ... more exports interspersed
export const getPermalink = (slug = '', type = 'page'): string => { ... };
```

**Best Practice:** Group all exports at the top or bottom of the file, not interspersed with implementations.

### 3.3 JSON-LD Schema Duplication

**Location:** Multiple pages define same JSON-LD schemas inline:

| Page            | Schemas Defined                                                |
| --------------- | -------------------------------------------------------------- |
| `index.astro`   | Person, WebSite, FAQPage                                       |
| `contact.astro` | ContactPage                                                    |
| `resume.astro`  | JobPosting (per experience), EducationalOccupationalCredential |

**Issue:** Schemas are manually written and duplicated across pages. If Person schema changes, it must be updated in 3 places.

**Recommendation:** Extract to `src/utils/structured-data.ts`:

```typescript
export const personSchema = { ... };
export const websiteSchema = { ... };
export const contactSchema = { ... };
```

### 3.4 TypeScript Interface Comments

**Location:** `src/types.d.ts`

**Problem:** Most interfaces have minimal or no JSDoc comments:

```typescript
export interface Post {
  id: string; // A unique ID number that identifies a post.
  slug: string; // A post's unique slug...
  // ... several undocumented fields
}
```

**Recommendation:** Add JSDoc comments to all public-facing types, especially those exported from the module.

### 3.5 Hardcoded Strings

**Problem:** Multiple hardcoded strings that should be centralized:

| Location        | Hardcoded Values                                                      |
| --------------- | --------------------------------------------------------------------- |
| `index.astro`   | "B.Eng. Computer and Electronic Engineering", "North-West University" |
| `resume.astro`  | Same education strings duplicated                                     |
| `contact.astro` | Formspree endpoint hardcoded                                          |
| `config.yaml`   | site.name, site.site - but not used consistently                      |

**Recommendation:** Move all personal info to `src/config/contact.ts`:

```typescript
export const PERSONAL_INFO = {
  name: 'Werner Bisschoff',
  title: 'Software Engineer',
  email: 'contact@bisschoff.dev',
  location: 'Cape Town, South Africa',
  education: {
    degree: 'B.Eng. Computer and Electronic Engineering',
    school: 'North-West University',
    year: 2020,
  },
  // ...
};
```

### 3.6 Inline Styles and Scripts

**Location:** Multiple components

**Problem:** `<style>` blocks embedded in page files:

- `index.astro` - Hero animations CSS
- `resume.astro` - Print styles
- `work.astro` - Smooth scroll

**Recommendation:** Move shared styles to:

1. Global CSS (`src/assets/styles/tailwind.css`)
2. Component-specific CSS files (`*.module.css` via Vite)

### 3.7 Blog vs Notes Naming

**Problem:** The blog section is branded as "Notes" but code uses "blog" everywhere:

| Code                 | User-Facing                 |
| -------------------- | --------------------------- |
| `APP_BLOG`           | "Notes"                     |
| `getBlogPermalink()` | Returns `/notes`            |
| `BLOG_BASE`          | `/notes`                    |
| Navigation           | "Notes" link points to blog |

**Confusion:** Internal code uses "blog" but user-facing UI uses "Notes". This is technically fine (just naming), but creates cognitive load.

**Recommendation:** Either:

1. Rename internally to `APP_NOTES` and `NOTES_BASE` (breaking change)
2. Keep as-is (current approach is acceptable)

---

## 4. Astro Best Practices Analysis

### 4.1 Content Collections (Astro 5.0)

**Current State:**

- Schema defined in `src/content/config.ts` ✓
- Loader configured for `src/data/post` ✓
- But content lives in `src/data/post`, not `src/content/` ✗

**Astro 5.0 Best Practice:**

```typescript
// src/content/config.ts
// This is correct - but the base path is wrong
const postCollection = defineCollection({
  loader: glob({ pattern: ['*.md', '*.mdx'], base: 'src/content/posts' }),  // Should be src/content/posts
  schema: z.object({ ... }),
});

// Posts should live in src/content/posts/, NOT src/data/post/
```

### 4.2 Image Optimization

**Location:** `src/utils/images-optimization.ts`, `src/components/common/Image.astro`

**Analysis:** Well-implemented image optimization with:

- Multiple breakpoint generation ✓
- WebP format support ✓
- Unpic for external CDN images ✓
- Aspect ratio handling ✓

**Issue:** The `Image` component has many props - could be simplified:

```typescript
// Current: 15+ props
<Image
  src={image}
  alt={...}
  width={400}
  height={300}
  widths={[400, 900]}
  sizes="..."
  aspectRatio="16:9"
  loading="lazy"
  decoding="async"
  class="..."
  background="..."
/>
```

**Recommendation:** Use sensible defaults for most props and allow overrides only when needed.

### 4.3 Static vs SSR

**Current:** `output: 'static'` in `astro.config.ts`

This is correct for a portfolio site. No issues.

### 4.4 Routing Pattern

**Current:** Dynamic routes for blog

```
src/pages/[...blog]/
├── index.astro          # /notes
├── [...page].astro      # /notes/page/2
├── [category]/[...page].astro  # /notes/category/...
└── [tag]/[...page].astro       # /notes/tag/...
```

**Issue:** The tag route is enabled but `robots: index: false`. This is fine but the tag functionality is dead code if no posts use tags.

---

## 5. Security & Performance Observations

### 5.1 Security

**Positive:**

- No hardcoded secrets in git ✓
- Formspree endpoint is public-facing (intentional) ✓
- No client-side sensitive data exposure ✓

**Concern:**

- `config.yaml` contains `googleSiteVerificationId` - this is fine as public verification

### 5.2 Performance

**Positive:**

- Image optimization with multiple breakpoints ✓
- Lazy loading images ✓
- Font loading with `@fontsource` (self-hosted) ✓
- Static site generation (no server overhead) ✓
- Partytown for analytics offloading ✓

**Concern:**

- `sharp` dependency for image processing adds build time but is necessary

---

## 6. Recommendations Summary

### 6.1 High Priority

1. **Delete template blog posts** from `src/data/post/` or replace with real content
2. **Fix content collection location** - move posts to `src/content/posts/` if using Astro content collections properly
3. **Extract JSON-LD schemas** to shared utility file
4. **Consolidate ItemGrid/ItemGrid2** into single component with layout prop

### 6.2 Medium Priority

1. **Remove unused type definitions** from `src/types.d.ts`
2. **Remove dead code functions** (`toUiAmount`, `getProjectRootDir`, `getRelativeUrlByFilePath`)
3. **Delete unused Headline component** (`ui/Headline.astro`)
4. **Document component responsibilities** - clarify blog vs UI components

### 6.3 Low Priority

1. **Group exports** consistently at top/bottom of utility files
2. **Move inline styles** to CSS files
3. **Add JSDoc comments** to exported types
4. **Consider centralizing personal info** in `src/config/personal.ts`

---

## 7. Verification Commands

Before making changes, verify with:

```bash
# Check for unused exports (requires TypeScript)
pnpm check:astro

# Run lint
pnpm check:lint

# Build to verify no breakage
mise run build

# Check for circular dependencies
# (use depcruise or madge if needed)
```

---

## 8. File Inventory

### 8.1 Pages (6 files)

| File            | Content            | Hardcoded? |
| --------------- | ------------------ | ---------- |
| `index.astro`   | Hero, About        | Yes        |
| `work.astro`    | Case studies       | Yes        |
| `resume.astro`  | Experience, Skills | Yes        |
| `contact.astro` | Contact form       | Yes        |
| `404.astro`     | 404 page           | No         |
| `privacy.md`    | Privacy policy     | No         |
| `terms.md`      | Terms of service   | No         |

### 8.2 Components (30+ files)

**Layouts:**

- `Layout.astro` - Base layout
- `PageLayout.astro` - Page wrapper
- `MarkdownLayout.astro` - Blog post layout

**Blog Components:**

- `Grid.astro`, `GridItem.astro`
- `List.astro`, `ListItem.astro`
- `SinglePost.astro`
- `Pagination.astro`
- `RelatedPosts.astro`
- `Tags.astro`
- `Headline.astro`
- `ToBlogLink.astro`

**UI Components:**

- `Button.astro`
- `ItemGrid.astro`, `ItemGrid2.astro` (duplication!)
- `Headline.astro` (unused!)
- `Timeline.astro`
- `WidgetWrapper.astro`
- `Form.astro`
- `Background.astro`
- `DListItem.astro`

**Common Components:**

- `Image.astro`
- `Metadata.astro`
- `CommonMeta.astro`
- `StructuredData.astro`
- `SocialShare.astro`
- `ToggleTheme.astro`
- `ToggleMenu.astro`
- `SiteVerification.astro`
- `Analytics.astro`
- `BasicScripts.astro`
- `ApplyColorMode.astro`
- `Favicons.astro`
- `CustomStyles.astro`

**Animation:**

- `ScrollReveal.astro`
- `InteractiveElement.astro`

### 8.3 Utilities (8 files)

| File                     | Functions             | Status                   |
| ------------------------ | --------------------- | ------------------------ |
| `permalinks.ts`          | URL generation        | Active                   |
| `blog.ts`                | Blog data fetching    | Active (some dead)       |
| `images.ts`              | Image resolution      | Active                   |
| `images-optimization.ts` | Image processing      | Active                   |
| `utils.ts`               | Date formatting, trim | Active (toUiAmount dead) |
| `frontmatter.ts`         | Markdown plugins      | Active                   |
| `a11y.ts`                | Motion preferences    | Active                   |
| `motion.ts`              | Motion re-exports     | Active                   |
| `directories.ts`         | Path utilities        | **DEAD**                 |

---

## 9. Next Steps

1. **Decision Point:** Determine content strategy (keep current approach vs. restructure)
2. **Cleanup Pass:** Remove dead code first
3. **Consolidation Pass:** Merge duplicate components
4. **Content Pass:** Replace template posts with real content
5. **Documentation Pass:** Add code comments and README updates

---

_Analysis completed: 2026-04-07_
_Tool used: Manual code inspection + Gemini CLI (partial)_
