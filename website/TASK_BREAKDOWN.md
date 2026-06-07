# Portfolio Website — Task Breakdown Summary

**Generated**: 2025-01-22
**Source PRD**: thoughts/prds/2025-01-22_portfolio-website-prd.md
**Total Tasks**: 10
**Total Subtasks**: 27

---

## Task Overview

### Complexity Distribution

- **High Complexity**: 0 tasks
- **Medium Complexity**: 5 tasks (IDs: 2, 3, 5, 6, 8, 9, 10)
- **Low Complexity**: 5 tasks (IDs: 1, 4, 7)

### Priority Distribution

- **High Priority**: 6 tasks
- **Medium Priority**: 4 tasks

### Dependency Graph

```
TM-001 (Configure AstroWind base)
  ↓
TM-002 (Implement theme system)
  ↓
TM-003 (Build navigation)
  ↓
TM-004 (Homepage) ─────────────────────┐
TM-005 (Work page) ────────────────────┤
TM-006 (Resume page) ───────────────────┤
TM-007 (Contact page) ──────────────────┤
  ↓                                     ↓
TM-008 (Notes blog) ────────────────────┤
TM-009 (SEO optimization) ──────────────┤
  ↓                                     ↓
TM-010 (Accessibility & Performance) ←─┘
```

---

## Detailed Task List

### TM-001: Configure AstroWind base and cleanup

**Complexity**: ●○○○○ (2/10) - Low
**Priority**: High
**Dependencies**: None
**Blocks**: TM-002, TM-008, TM-009

**Subtasks**:

1. Clone AstroWind template and install dependencies
2. Clean up unused files and configure site metadata

**Implementation**:

- Delete: `src/pages/pricing.astro`, `src/pages/services.astro`, `src/pages/landing/*`
- Keep: `src/pages/homes/personal.astro` as reference
- Update `src/config.yaml`:
  - Site name: "Werner Bisschoff"
  - URL: "https://werner.bisschoff.dev"
  - Title: "Werner Bisschoff — Foundations & Velocity Engineer"
  - `trailingSlash: false`

**Test Strategy**:

- Verify build runs: `npm run build`
- Confirm deleted pages return 404
- Check metadata renders in browser tab title

---

### TM-002: Implement theme system with CSS variables

**Complexity**: ●●●○○ (5/10) - Medium
**Priority**: High
**Dependencies**: TM-001
**Blocks**: TM-003

**Subtasks**:

1. Define CSS variables and import typography
2. Implement client-side theme toggle logic
3. Add localStorage persistence for theme preference

**Implementation**:

- Edit `src/components/CustomStyles.astro`
- Define CSS variables for 3 themes:
  - **Option A (Default)**: Background `#121212`, Text `#F4F4F4/#E0E0E0`, Accent `#599692` or `#BFA181`
  - **Option B**: Background `#0F172A`, Text `#E5E7EB`, Accent `#22D3EE` or `#60A5FA`
  - **Option C**: Background `#121212`, Text `#E0E0E0`, Accent `#D4A574` or `#599692`
- Import fonts: Inter Variable, Inconsolata
- Add theme toggle script with localStorage persistence
- Ensure no pure black (`#000000`) used
- **Tip**: Use Claude's `frontend-design` skill (`/frontend-design`) to rapidly prototype and refine theme UI components

**Test Strategy**:

- Visually inspect all 3 themes using toggle
- Verify localStorage persists on reload
- Check CSS variables update via DevTools
- Validate contrast ratios meet WCAG AA (4.5:1 normal, 3:1 large)

---

### TM-003: Build responsive navigation and layout structure

**Complexity**: ●●●●○ (6/10) - Medium
**Priority**: High
**Dependencies**: TM-002
**Blocks**: TM-004, TM-005, TM-006, TM-007

**Subtasks**:

1. Update navigation configuration with 4-item menu
2. Implement responsive mobile menu
3. Configure footer with social links and email

**Implementation**:

- Edit `src/navigation.ts`:
  - Links: Work, Resume, Notes, Contact
  - Footer: Social links (LinkedIn, GitHub), Email
  - Remove: Pricing, Services navigation items
- Implement mobile hamburger menu (< 1024px)
- Add sticky header on scroll (desktop only)
- Configure footer with social links

**Test Strategy**:

- Verify navigation displays 4 items correctly
- Test mobile menu toggle functionality
- Check sticky header behavior on desktop
- Verify footer links work

---

### TM-004: Develop Homepage with Hero and Positioning

**Complexity**: ●●●○○ (3/10) - Low
**Priority**: High
**Dependencies**: TM-003
**Blocks**: TM-010

**Subtasks**:

1. Create Hero section with positioning and CTAs
2. Add featured case study and AI workflow section

**Implementation**:

- Create `src/pages/index.astro`
- Hero title: "I build the foundations teams need to ship reliable software fast. B.Eng. Computer and Electronic Engineering."
- Hero tagline: "Testing infrastructure. Development tooling. System architecture. I add the structure and safety nets that let teams move fast confidently."
- Primary CTA: "Start a conversation" (→ Contact)
- Secondary CTA: "View my work" (→ Work)
- Featured case study (1 of 3)
- AI workflow section: "I use AI to accelerate quality—not replace it. Code reviews, test generation, and refactoring—all validated through disciplined review."

**Test Strategy**:

- Verify hero content displays correctly
- Test CTA links navigate to correct pages
- Check featured case study visible
- Confirm B.Eng. mentioned in hero

---

### TM-005: Create Work page and Case Study content

**Complexity**: ●●●●○ (4/10) - Medium
**Priority**: High
**Dependencies**: TM-003
**Blocks**: TM-010

**Subtasks**:

1. Build Work page with 3 case study cards
2. Write detailed case study content (Problem → Constraints → Solution → Outcome)
3. Create case study detail pages or anchor navigation

**Implementation**:

- Create `src/pages/work.astro`
- Display 3 case studies:
  1. Event-Driven FSM for Embedded Systems
  2. Development Workflow Modernization
  3. Test Infrastructure from Scratch
- Each case: Title, Problem, Constraints, Solution, Outcome
- Links to full details (separate pages or anchors)

**Case Study 1 Content**:

- Problem: "Complex I2C-based embedded system needing reliable state management"
- Constraints: "Real-time requirements, FreeRTOS, C++"
- Solution: "Designed event-driven finite state machine architecture"
- Outcome: "Maintainable in-house FSM, fewer bugs, quicker development cycles"

**Case Study 2 Content**:

- Problem: "Internal Retool workflows were slow and unmaintainable"
- Constraints: "Needed better performance and developer experience"
- Solution: "Migrated to Expo, introduced LLM-assisted development workflow"
- Outcome: "Significantly improved performance, maintainability, and debugging speed"

**Case Study 3 Content**:

- Problem: "No test coverage, risky deployments, slow iteration"
- Constraints: "Needed rapid development cycle without breaking things"
- Solution: "Built Python tooling, hardware mocks, test executables from scratch"
- Outcome: "Faster iteration, fewer production bugs"

**Test Strategy**:

- Verify 3 case studies display
- Test links to full details work
- Check Problem → Constraints → Solution → Outcome structure visible

---

### TM-006: Implement Resume page with timeline and skills

**Complexity**: ●●●●○ (4/10) - Medium
**Priority**: Medium
**Dependencies**: TM-003
**Blocks**: TM-010

**Subtasks**:

1. Build Resume page using personal.astro as reference
2. Add experience timeline and education sections
3. Group skills by capability (not flat list)

**Implementation**:

- Create `src/pages/resume.astro`
- Use `src/pages/homes/personal.astro` as structural reference
- Experience section: Timeline/Steps widget format
- Education: B.Eng. Computer and Electronic Engineering prominent
- Skills grouped by capability:
  - Systems Architecture
  - Testing & Quality
  - Development Infrastructure
  - Workflow Automation
  - Languages
  - Embedded Systems
  - Web Development
- PDF download button
- Email: werner@bisschoff.dev

**Test Strategy**:

- Verify experience timeline displays correctly
- Check B.Eng. prominent
- Confirm skills grouped by capability
- Test PDF download works
- Verify print layout (print preview)

---

### TM-007: Build Contact page with form validation

**Complexity**: ●●●○○ (3/10) - Low
**Priority**: Medium
**Dependencies**: TM-003
**Blocks**: TM-010

**Subtasks**:

1. Create Contact page with form and email
2. Implement form validation (required fields, email format)
3. Add social links (LinkedIn, GitHub)

**Implementation**:

- Create `src/pages/contact.astro`
- Contact form fields: Name, Email, Message
- Form validation: Required fields, email format
- Form submissions → werner@bisschoff.dev
- Display email: werner@bisschoff.dev
- Social links: LinkedIn (wbisschoff13), GitHub (wbisschoff13)
- No phone number (email only)

**Test Strategy**:

- Verify form validation works (required fields, email format)
- Test form submission succeeds
- Confirm email displays correctly
- Check social links work

---

### TM-008: Setup Notes blog and content collections

**Complexity**: ●●●○○ (5/10) - Medium
**Priority**: Medium
**Dependencies**: TM-001
**Blocks**: TM-010

**Subtasks**:

1. Configure Astro Content Collections for blog posts
2. Create Notes page with placeholder or post listing
3. Verify RSS feed generation

**Implementation**:

- Blog posts: `src/data/post/*.md` or `.mdx`
- Zod schema validation: Required fields (`title`, `publishDate`), Optional (`excerpt`, `image`, `category`, `tags`, `author`, `updateDate`, `draft`)
- Create `src/pages/notes/index.astro`
- If empty: Display placeholder "More coming soon..." or "Practical notes on software engineering, architecture, and development tools. Check back soon."
- RSS feed auto-generated at `/rss.xml`

**Test Strategy**:

- Verify Zod schema validates at build time
- Check placeholder message displays when empty
- Confirm RSS feed generates at `/rss.xml`
- Test blog post URLs: `/notes/{slug}`

---

### TM-009: Optimize SEO, Metadata, and Sitemap

**Complexity**: ●●●○○ (5/10) - Medium
**Priority**: Medium
**Dependencies**: TM-001
**Blocks**: TM-010

**Subtasks**:

1. Configure meta tags and Open Graph
2. Verify sitemap and robots.txt generation
3. Add Schema.org structured data for blog posts

**Implementation**:

- Update `src/config.yaml`:
  - Site name: "Werner Bisschoff"
  - Site URL: "https://werner.bisschoff.dev"
  - Default title: "Werner Bisschoff — Foundations & Velocity Engineer"
  - Title template: `%s — Werner Bisschoff`
  - Description: "Software engineer who builds the foundations teams need to ship reliable software fast. Testing infrastructure. Development tooling. System architecture."
  - Open Graph configuration
  - Twitter card configuration
- Verify sitemap: `/sitemap.xml` (auto-generated via @astrolib/seo)
- Verify robots.txt: Updated with sitemap reference
- Schema.org markup for blog posts

**Test Strategy**:

- Verify meta tags render correctly (view source)
- Check sitemap accessible at `/sitemap.xml`
- Confirm robots.txt references sitemap
- Validate Open Graph tags (use Facebook debugger)
- Test Twitter card preview (use Twitter card validator)

---

### TM-010: Accessibility audit and Performance tuning

**Complexity**: ●●●●●● (7/10) - Medium
**Priority**: High
**Dependencies**: TM-004, TM-005, TM-006, TM-007, TM-008, TM-009
**Blocks**: None

**Subtasks**:

1. Run Lighthouse audit and fix performance issues
2. Conduct manual accessibility testing (keyboard, screen reader, color contrast)
3. Test cross-browser compatibility and responsive design
4. Fix any critical issues found

**Implementation**:

- **Lighthouse targets**: 90+ Performance, Accessibility, Best Practices, SEO
- **Core Web Vitals**:
  - First Contentful Paint (FCP): < 1.5s
  - Largest Contentful Paint (LCP): < 2.5s
  - Cumulative Layout Shift (CLS): < 0.1
- **Accessibility testing**:
  - Screen reader: NVDA/VoiceOver
  - Keyboard-only navigation
  - Color blindness simulators
  - Mobile devices (touch targets minimum 44x44px)
- **Color contrast**: Minimum 4.5:1 (normal), 3:1 (large)
- **Cross-browser testing**: Chrome, Firefox, Safari (desktop + mobile)

**Test Strategy**:

- Run Lighthouse audit (target 90+ all categories)
- Test keyboard navigation (all interactive elements)
- Test with screen reader (NVDA/VoiceOver)
- Test color contrast (WebAIM Contrast Checker)
- Test on mobile devices
- Test in Chrome, Firefox, Safari

---

## Risk Assessment

All tasks have been assessed for risk:

| Risk Level | Tasks                                                                  | Testing Approach                      |
| ---------- | ---------------------------------------------------------------------- | ------------------------------------- |
| **High**   | None                                                                   | N/A                                   |
| **Medium** | TM-007 (Contact form)                                                  | Integration test after implementation |
| **Low**    | TM-001, TM-002, TM-003, TM-004, TM-005, TM-006, TM-008, TM-009, TM-010 | Visual regression or manual testing   |

**Note**: Most tasks are Low Risk (content presentation, visual styling). Only TM-007 (contact form) has Medium Risk due to form validation and submission logic.

---

## Implementation Order

**Phase 1: Foundation (Days 1-2)**

1. TM-001: Configure AstroWind base
2. TM-002: Implement theme system
3. TM-003: Build navigation

**Phase 2: Core Pages (Days 3-4)** 4. TM-004: Homepage 5. TM-005: Work page + Case Studies 6. TM-006: Resume page 7. TM-007: Contact page

**Phase 3: Content & SEO (Day 5)** 8. TM-008: Notes blog 9. TM-009: SEO optimization

**Phase 4: Quality Assurance (Day 5)** 10. TM-010: Accessibility & Performance audit

---

## Commands Reference

```bash
# View all tasks
task-master list

# View task details
task-master show <id>

# Start working on a task
task-master set-status --id=<id> --status=in-progress

# Mark subtask complete
task-master set-status --id=<id> --subtask=<subtaskId> --status=done

# Mark task complete
task-master set-status --id=<id> --status=done

# View next recommended task
task-master next
```

---

**Task Generation Complete**

All 10 tasks have been generated from the PRD with:

- Clear dependencies
- Complexity ratings
- Implementation details
- Test strategies
- Subtask breakdowns

Ready for execution via `/tm:implement`.
