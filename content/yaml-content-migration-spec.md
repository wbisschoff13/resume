# YAML Content Layer — Migration Spec

> **Goal:** Replace the current hardcoded `content/data.typ` + `content/master-list.md` duality with a single YAML-based canonical content layer.
> **Consumers:** Typst (CV PDF, 3 variants filtered by priority) + Astro (website, unconstrained).
> **Editor:** LLM (you). The YAML files are what you write to when Werner says "update my resume."
> **Source of truth:** `content/experience.yaml`, `content/star-stories.yaml`, `content/config.yaml`
> **Stakeholder:** Life OS Assistant (spec author). Dev Agent (executor): implement the Typst import changes and YAML files. Werner: content owner.
> **Branch:** `feat/001-typst-cv-migration/yaml-content-migration` (create new)

---

## Why This Change

| Problem | Solution |
|---------|----------|
| `data.typ` and `master-list.md` duplicate the same content in different formats | One YAML file, both consume from it |
| Updating a bullet requires touching multiple files | Edit one YAML file |
| Typst hardcodes data in Typst syntax, not portable | YAML is language-agnostic, parseable by Astro too |
| No curation metadata exists | `cv_priority`, `website_show` tags in YAML |
| No single place to see "everything I've done" | The YAML is the catalog |

---

## File Structure

```
resume/
├── content/
│   ├── config.yaml              # Personal info, links, cert, job target, ai_policy
│   ├── experience.yaml          # All roles, all bullets, all variants
│   ├── star-stories.yaml        # 14 STAR stories (full format)
│   ├── skills.yaml              # Skills by category + variant
│   ├── projects.yaml            # Project entries
│   └── education.yaml           # Education entries
├── content/data.typ             # BECOMES a thin import layer: reads YAML and re-exports
├── cv.typ                       # Unchanged (entry point)
├── lib/template.typ             # MINOR UPDATE: change field names from old data dict to new
├── cv_embedded.typ              # Entry point for embedded variant (if still needed)
├── cover_letter.typ             # Unchanged (reads from data.typ as before)
└── website/                     # (future — Astro project reads same YAML)
    └── src/content/             # Symlink or import from ../../content/*.yaml
```

---

## YAML Schemas

### 1. `content/config.yaml`

```yaml
# Personal information — used by both CV and website
name: "Werner Bisschoff"
email: "werner@bisschoff.dev"
phone: "071 826 2066"
location: "Cape Town, Western Cape, South Africa"
github: "wbisschoff13"
website: "https://werner.bisschoff.dev"
linkedin: "wbisschoff13"

# Position title per variant
position:
  general: "Software Engineer"
  systems: "Hybrid Edge/Systems Engineer"
  infrastructure: "Cloud Infrastructure Engineer / Platform Developer"

# Summary per variant
summary:
  general: |
    Software engineer with 5+ years of experience bridging hardware and
    full-stack development. I combine technical depth in C++ and Python
    with a rigorous, agentic engineering methodology. My focus is on resilient
    system design and productivity-enhancing AI workflows, governed by security,
    processes, and specification-driven development.
  systems: |
    Hybrid Edge/Systems Engineer with 5+ years of experience architecting
    end-to-end telemetry systems spanning edge compute to backend integration.
    Specializes in C/C++ and FreeRTOS for deterministic real-time scheduling,
    Python for automation and hardware-in-the-loop validation, and Elixir/OTP
    for distributed platform infrastructure.
  infrastructure: |
    Cloud Infrastructure Engineer / Platform Developer with 5+ years of
    experience designing high-availability infrastructure across Linux systems
    administration, Docker containerization, and Pulumi infrastructure-as-code.
    Proven track record in PostgreSQL performance tuning, multi-tenant data
    isolation, and building resilient automation and deployment pipelines.

# AI policy (shown on website, omitted from CV due to space)
ai_policy:
  - "I treat AI as an agentic partner within a strict engineering framework, moving beyond 'vibe-coding' to structured, audit-ready workflows."
  - "Spec-Driven Development (SDD): Prioritize context-heavy specifications to ensure alignment; AI-generated outputs are treated as hypotheses validated by human-led TDD."
  - "Data Security: Enforce mandatory sandboxing for all agentic projects; strictly prohibit credential access and utilize tool-based retrieval for scoped, anonymized data only."
  - "Engineering Rigour: All AI-assisted output undergoes rigorous human-in-the-loop review."
  - "Privacy by Design: AI workflows are architected to avoid direct database access."

# Job target
job_target: |
  Seeking a mid to senior software engineering role (remote preferred, hybrid
  max. 2 days/week on-site in Cape Town) with emphasis on embedded systems,
  backend services, or AI-assisted development workflows.

# Certification
certification: "AWS Certified Solutions Architect – Associate (In Progress — Target: 6 Weeks)"
```

### 2. `content/experience.yaml`

The core change. Each role has all bullets for all variants. Each bullet carries curation tags.

```yaml
roles:
  - company: "Divergent Tabletop"
    location: "Cape Town"
    start_date: "Jul 2025"
    end_date: null  # null = present
    roles:
      general: "Founder and Host"
      systems: "Principal Systems Architect"
      infrastructure: "Principal Systems Architect"
    bullets:
      # --- GENERAL ---
      - text: "Founded neurodivergent-focused peer community; manage event operations and WhatsApp-based community platform."
        variant: general
        cv_priority: 1
        website_show: true
        star_ref: null
      - text: "Applied systems thinking to solve community management challenges through software solutions."
        variant: general
        cv_priority: 2
        website_show: true
        star_ref: null
      # --- SYSTEMS ---
      - text: "Engineered a distributed real-time data engine utilizing Elixir/OTP and conflict-free replicated data types (CRDT models). Deployed in-memory GenServer storage buffers with threshold-based flush mechanics, reducing direct database write transactions by approximately 85% under sustained edit workloads."
        variant: systems
        cv_priority: 1
        website_show: true
        star_ref: 11
      - text: "Integrated a Rust-backed CRDT synchronization layer (y_ex) using actor-based concurrency, achieving sub-50ms convergence latency across distributed editing sessions through deterministic state reconciliation and binary delta serialization."
        variant: systems
        cv_priority: 1
        website_show: true
        star_ref: 11
      - text: "Designed a dynamic BEAM supervision tree with one_for_one isolation, encapsulating each page editing session in its own process subtree to prevent cascading failures and guarantee per-session state integrity."
        variant: systems
        cv_priority: 1
        website_show: true
        star_ref: null
      # --- INFRASTRUCTURE ---
      - text: "Engineered and hosted an enterprise-grade documentation ecosystem."
        variant: infrastructure
        cv_priority: 1
        website_show: true
        star_ref: null
      - text: "Implemented a single-database multi-tenant separation engine using PostgreSQL Row-Level Security (RLS) and transaction-scoped local parameters (SET LOCAL), enforcing strict data silos across isolated groups."
        variant: infrastructure
        cv_priority: 1
        website_show: true
        star_ref: null
      - text: "Designed an atomic asynchronous flush strategy using in-memory GenServer storage buffers, reducing database persistent write transactions by 85% during periods of high user interaction."
        variant: infrastructure
        cv_priority: 2
        website_show: true
        star_ref: null
      - text: "Utilized Ecto.Multi atomic chains and Oban transactional background workers to ensure multi-stage backend edits execute completely or roll back safely."
        variant: infrastructure
        cv_priority: 2
        website_show: true
        star_ref: null
      - text: "Applied Universal Design and Executive Functioning support models to product UX/UI; established highly structured, low-context asynchronous operational playbooks that minimized cognitive friction for contributors."
        variant: infrastructure
        cv_priority: 3
        website_show: true
        star_ref: null

  - company: "FARO Africa"
    location: "Cape Town"
    start_date: "Aug 2024"
    end_date: "Nov 2025"
    roles:
      general: "Full-Stack Software Engineer"
      systems: "Embedded Systems & Integration Engineer"
      infrastructure: "Full-Stack ERPNext & Automation Engineer"
    bullets:
      # --- GENERAL ---
      - text: "Extended ERPNext using Python/JavaScript to improve workflows, pricing logic, and operational reporting (SQL) → reduced manual reporting time and improved data accuracy."
        variant: general
        cv_priority: 1
        website_show: true
        star_ref: null
      - text: "Built mobile application in Expo, including NFC (ISO 14443-4 APDUs) for e-paper price tags and card operations → enabled real-time price updates with fewer tagging errors."
        variant: general
        cv_priority: 1
        website_show: true
        star_ref: 7
      - text: "Migrated internal mobile Retool workflows to Expo → improved performance and enhanced long-term maintainability."
        variant: general
        cv_priority: 2
        website_show: true
        star_ref: null
      - text: "Provisioned AWS infrastructure with Pulumi; deployed Inngest and PayloadCMS services."
        variant: general
        cv_priority: 3
        website_show: true
        star_ref: null
      - text: "Diagnosed and resolved issues in a large existing ERPNext installation."
        variant: general
        cv_priority: 3
        website_show: true
        star_ref: null
      - text: "Introduced LLM-assisted development workflows → improved debugging speed and code review throughput, enabling faster iteration."
        variant: general
        cv_priority: 2
        website_show: true
        star_ref: null
      # --- SYSTEMS ---
      - text: "Designed ISO 14443-4 NFC communication architectures for e-paper display nodes and secure card reader matrices."
        variant: systems
        cv_priority: 1
        website_show: true
        star_ref: 7
      - text: "Engineered lock-free asynchronous device management services bridging hardware peripherals with application layers."
        variant: systems
        cv_priority: 2
        website_show: true
        star_ref: null
      - text: "Built Python-based hardware peripheral simulators to catch edge-case device state corruptions prior to flashing."
        variant: systems
        cv_priority: 1
        website_show: true
        star_ref: null
      # --- INFRASTRUCTURE ---
      - text: "Identified poor UX as root cause of recurring user errors — pushed back against training gap framing, proposed user research to validate, and drove UX improvements that reduced task completion time and error rates."
        variant: infrastructure
        cv_priority: 1
        website_show: true
        star_ref: 9
      - text: "Refactored and extended ERPNext via Python and JavaScript server hooks, optimizing pricing matrices and BI reporting."
        variant: infrastructure
        cv_priority: 2
        website_show: true
        star_ref: null
      - text: "Architected migration of internal Retool workflows to Expo/React Native, reducing vendor licensing overhead."
        variant: infrastructure
        cv_priority: 2
        website_show: true
        star_ref: null
      - text: "Built custom NFC scanner utilities within Expo for instantaneous physical inventory syncs."
        variant: infrastructure
        cv_priority: 3
        website_show: true
        star_ref: 7
      - text: "Provisioned and maintained a secure virtualized Linux infrastructure environment using Docker Compose for container isolation and writing custom backup and monitoring scripts."
        variant: infrastructure
        cv_priority: 3
        website_show: true
        star_ref: null
      - text: "Diagnosed and resolved issues in a large existing ERPNext installation; introduced LLM-assisted debugging workflows."
        variant: infrastructure
        cv_priority: 3
        website_show: true
        star_ref: null

  - company: "Ingenics Digital GmbH (through ViVa Outsourcing)"
    location: "Remote"
    start_date: "Mar 2023"
    end_date: "May 2024"
    roles:
      general: "Embedded Software Engineer"
      systems: "Firmware Engineer (Contract)"
      infrastructure: "Enterprise Infrastructure & Tooling Engineer"
    bullets:
      # --- GENERAL ---
      - text: "Designed event-driven FSM for I2C-based embedded system (C++/FreeRTOS) → maintainable architecture, fewer bugs."
        variant: general
        cv_priority: 1
        website_show: true
        star_ref: 5
      - text: "Developed ESP32 applications (C/C++, ESP-IDF) with configurable BLE stack, TinyFrame protocol, and FOTA updates."
        variant: general
        cv_priority: 2
        website_show: true
        star_ref: 6
      - text: "Built Python tooling for serial/BLE communication, hardware mocks, and pytest async workflows → accelerated testing."
        variant: general
        cv_priority: 1
        website_show: true
        star_ref: null
      - text: "Developed active object within QP Real-Time Embedded Framework (QSPY) to simulate device behaviour."
        variant: general
        cv_priority: 3
        website_show: true
        star_ref: null
      # --- SYSTEMS ---
      - text: "Architected deterministic FSMs on dual-core ESP32 using FreeRTOS for concurrent sensor arrays."
        variant: systems
        cv_priority: 1
        website_show: true
        star_ref: 5
      - text: "Developed Cap'n Proto IPC over serial lines, achieving sub-millisecond serialization latency."
        variant: systems
        cv_priority: 2
        website_show: true
        star_ref: null
      # --- INFRASTRUCTURE ---
      - text: "Built modular Python utility structures and automation scripts for internal configuration schema validation."
        variant: infrastructure
        cv_priority: 2
        website_show: true
        star_ref: null
      - text: "Designed data handling pipelines ensuring data transfer consistency across runtime platforms using declarative specifications."
        variant: infrastructure
        cv_priority: 3
        website_show: true
        star_ref: null
      - text: "Developed Python hardware mocks enabling faster development cycles with fewer hardware dependencies."
        variant: infrastructure
        cv_priority: 1
        website_show: true
        star_ref: null

  - company: "UMAN Technologies"
    location: "Cape Town"
    start_date: "Mar 2021"
    end_date: "Dec 2022"
    roles:
      general: "Software Developer"
      systems: "Software Developer"
      infrastructure: "Infrastructure & Tooling Developer"
    bullets:
      # --- GENERAL ---
      - text: "Implemented SOME/IP RPC services; optimized performance bottlenecks with perf."
        variant: general
        cv_priority: 2
        website_show: true
        star_ref: 1
      - text: "Built IPC/RPC layers (C++/Python) using Cap'n Proto; led small team using Agile practices."
        variant: general
        cv_priority: 2
        website_show: true
        star_ref: null
      # --- SYSTEMS ---
      - text: "Used perf profiling and flamegraphs to trace a performance bottleneck to JSON serialization and verbose logging in a SOME/IP request handling loop. Eliminated unnecessary logging via config toggle reducing latency by approximately 80%, then drove an architecture redesign to phase out JSON entirely."
        variant: systems
        cv_priority: 1
        website_show: true
        star_ref: 1
      - text: "Sole owner of an IPC service layer — studied existing node schema, designed node structures and data contracts, and implemented the communication layer enabling the frontend to consume the service."
        variant: systems
        cv_priority: 1
        website_show: true
        star_ref: 4
      - text: "Built Python-based SOME/IP hardware mocks simulating request/response behavior; integrated into CI so automated tests ran without physical hardware."
        variant: systems
        cv_priority: 1
        website_show: true
        star_ref: 3
      # --- INFRASTRUCTURE ---
      - text: "Proactively created a Docker development container replicating the exact hardware environment — including VLAN and networking configuration — reducing setup time from hours to under an hour and enabling remote teams to develop without physical hardware."
        variant: infrastructure
        cv_priority: 1
        website_show: true
        star_ref: 2
      - text: "Built Python hardware mocks simulating SOME/IP behavior; integrated into CI to enable automated testing without physical hardware, improving test coverage and developer productivity."
        variant: infrastructure
        cv_priority: 1
        website_show: true
        star_ref: 3

  - company: "North-West University"
    location: "Potchefstroom"
    start_date: "Feb 2020"
    end_date: "Dec 2020"
    roles:
      general: "Junior Lecturer"
      systems: "Junior Lecturer"
      infrastructure: "Junior Lecturer"
    bullets:
      - text: "Lectured Python and C++ programming for Introduction to Programming for first year IT students in both remote and in-person settings."
        variant: general
        cv_priority: 1
        website_show: true
        star_ref: null
```

### 3. `content/skills.yaml`

```yaml
categories:
  - name: "Primary"
    variant: general
    skills:
      - "C/C++"
      - "Python"
      - "FreeRTOS"
      - "ESP32/ESP-IDF"
      - "NFC APDU (ISO 14443-4)"
  - name: "Secondary"
    variant: general
    skills:
      - "NimBLE"
      - "UART/SPI/I2C"
      - "TinyFrame"
      - "BLE"
      - "Hardware-in-the-Loop Testing"
  - name: "Foundational"
    variant: general
    skills:
      - "SQL"
      - "Docker"
      - "CI/CD"
      - "Git"
      - "Linux"
  - name: "Other"
    variant: general
    skills:
      - "React"
      - "Phoenix"
      - "AWS"
      - "Pulumi"
      - "ERPNext"

  - name: "Primary Competencies"
    variant: systems
    skills:
      - "C"
      - "C++"
      - "FreeRTOS"
      - "ESP32/ESP-IDF"
      - "NFC APDU (ISO 14443-4)"
  - name: "Secondary Competencies"
    variant: systems
    skills:
      - "NimBLE"
      - "Bare-Metal Runtimes"
      - "UART/SPI/I2C"
      - "Hardware-in-the-Loop (HIL) Testing"
  - name: "Foundational Systems"
    variant: systems
    skills:
      - "Linux IPC"
      - "Bash"
      - "Python (pytest, Custom Automation Frameworks)"
      - "Assembly"
      - "System Modeling"
  - name: "Cross-Domain Integration"
    variant: systems
    skills:
      - "ERPNext (Integration-focused)"
      - "Docker"
      - "Spec-Driven Development (SDD)"

  - name: "Primary Competencies"
    variant: infrastructure
    skills:
      - "Python"
      - "Docker"
      - "Docker Compose"
      - "AWS (Solutions Architect – In Progress)"
      - "PostgreSQL (Row-Level Security, Index Tuning, Connection Pooling)"
  - name: "Secondary Platforms"
    variant: infrastructure
    skills:
      - "ERPNext/Frappe Framework"
      - "Elixir/OTP"
      - "Asynchronous Workflow Engines (Inngest, Oban)"
  - name: "Data Layer Infrastructure"
    variant: infrastructure
    skills:
      - "SQL"
      - "Ecto.Multi"
  - name: "Systems & Automation"
    variant: infrastructure
    skills:
      - "Pulumi (IaC)"
      - "Linux Systems Administration"
      - "CI/CD Pipelines"
      - "Bash Scripting"
      - "Network Proxies"
      - "SSH Networking"
      - "Spec-Driven Development (SDD)"
```

### 4. `content/education.yaml`

```yaml
entries:
  - degree: "B.Eng. Computer and Electronic Engineering"
    institution: "North-West University"
    location: "Potchefstroom"
    graduation_year: "2020"
    details:
      general:
        - "Focus on embedded systems, software engineering, and electronic design"
        - "NFC payment emulator (Kotlin/Android), STM32 firmware (C), PID motor controller (Arduino)"
        - "Data analysis with Python/pandas using linear regression, correlation and machine learning"
      systems:
        - "Focus on embedded systems, software engineering, and electronic design"
        - "Developed NFC payment protocol emulator (Kotlin/Android), STM32 firmware (C), PID motor controller (Arduino)"
      infrastructure:
        - "Focus on embedded systems, software engineering, and electronic design"
        - "Developed data analysis pipeline with Python/pandas (linear regression, ML); built NFC payment emulator (Kotlin/Android)"
```

### 5. `content/projects.yaml`

```yaml
entries:
  - name: "Divergent Tabletop Wiki"
    description:
      general:
        - "Built a community wiki using Astro, Elixir, and Docker for knowledge management"
        - "Documented event frameworks, onboarding processes, and communication best practices"
        - "Created tooling for content management and community operations"
      systems:
        - "Engineered a real-time collaborative wiki engine using Elixir/OTP and CRDT"
        - "Implemented PostgreSQL RLS for multi-tenant isolation"
      infrastructure:
        - "Deployed with Docker Compose and managed CI/CD pipelines"
        - "Provisioned cloud infrastructure for community platform"
    link: null  # use actual URL when available
    variant_tags:
      - general
      - systems
      - infrastructure

  - name: "Ingenics Digital GmbH — Event-Driven FSM for Embedded Systems"
    description:
      general:
        - "Designed event-driven finite state machine for I2C-based embedded system using C++ and FreeRTOS"
        - "Solved complex state management challenges in real-time embedded environment"
        - "Outcome: Maintainable in-house architecture leading to fewer bugs and quicker development cycles"
      systems:
        - "Architected deterministic FSM on dual-core ESP32 using FreeRTOS for concurrent sensor arrays"
    link: null
    variant_tags:
      - general
      - systems
```

### 6. `content/star-stories.yaml`

Schema — one entry per story:

```yaml
stories:
  - id: 1
    title: "SOME/IP Performance Investigation"
    company: "UMAN Technologies"
    lps:
      primary: "Dive Deep"
      secondary: "Ownership"
    situation: >
      Our C++ library for customer hardware had severe latency issues —
      customers couldn't use the software at all.
    task: >
      I was tasked to investigate and fix the performance bottleneck.
    action: >
      I used perf to profile the hot paths during live requests, generated
      flamegraphs, and traced the problem to JSON serialization in the
      request handling loop. Verbose logging on every JSON operation made
      it worse. I disabled the unnecessary logging via a config toggle as
      a first step. I then participated in the design discussion and helped
      drive the effort to phase out JSON entirely through a complete
      architecture redesign for dynamic payload creation. I self-taught the
      SOME/IP protocol from specs to ensure the new approach was
      spec-compliant.
    result: >
      Removing verbose logging alone improved some request calls by 80%.
      The full architecture redesign eliminated the bottleneck long-term,
      restoring full functionality for customers.
    tags:
      - performance
      - embedded
      - cpp
      - someip
```

Include all 14 stories matching `content/star-stories.md`. Keep the same content; just reformat into YAML.

---

## Typst Migration Plan

### Step 1: Create the YAML files (content/*.yaml)

Write all 6 YAML files by extracting data from:
- `content/data.typ` (experience, education, skills, projects, config)
- `content/master-list.md` (cv_priority, website_show, star_ref curation metadata)
- `content/star-stories.md` (14 full stories)

The `cv_priority` field is NEW — it curates what fits on one page. Rules:
- **priority 1** = essential, always include in CV
- **priority 2** = include if space permits after priority 1 bullets
- **priority 3** = website-only (CV too long)

### Step 2: Simplify `content/data.typ`

The old `data.typ` is 298 lines of hardcoded data. Replace it with a thin YAML-import layer:

```typst
// content/data.typ — now a thin YAML import layer
// The canonical data lives in content/*.yaml

#import "@preview/yaml:0.2.0": yaml

// Read raw data from YAML files
#let _raw_config = yaml("content/config.yaml")
#let _raw_experience = yaml("content/experience.yaml")
#let _raw_education = yaml("content/education.yaml")
#let _raw_skills = yaml("content/skills.yaml")
#let _raw_projects = yaml("content/projects.yaml")

// Helper: filter bullets for a variant and max priority
#let _filter_bullets(bullets, variant, max_priority: 3) = {
  bullets
    .filter(b => b.variant == variant)
    .filter(b => b.cv_priority <= max_priority)
    .map(b => b.text)
}

// Helper: build experience entries for a variant
#let _build_experience(roles, variant) = {
  roles.map(r => (
    role: r.roles.at(variant),
    company: r.company,
    location: r.location,
    start_date: r.start_date,
    end_date: r.end_date,
    description: _filter_bullets(r.bullets, variant),
  ))
}

// Build education for variant
#let _build_education(entries, variant) = {
  entries.map(e => (
    degree: e.degree,
    institution: e.institution,
    location: e.location,
    graduation_year: e.graduation_year,
    details: e.details.at(variant, default: e.details.at("general")),
  ))
}

// Build skills for variant
#let _build_skills(categories, variant) = {
  categories.filter(c => c.variant == variant)
}

// Build projects for variant
#let _build_projects(entries, variant) = {
  entries.filter(e =>
    "variant_tags" in e and variant in e.variant_tags
  ).map(e => (
    name: e.name,
    description: e.description.at(variant, default: ()),
    link: e.link,
  ))
}

// Export: data dictionary matching old schema
// The template calls data.at("experience"), data.at("summary"), etc.
#let raw_data = {
  // This is populated per-variant below
  (
    name: _raw_config.name,
    email: _raw_config.email,
    phone: _raw_config.phone,
    location: _raw_config.location,
    github: _raw_config.github,
    website: _raw_config.website,
    linkedin: _raw_config.linkedin,
    position: _raw_config.position,
    summary: _raw_config.summary,
    certification: _raw_config.certification,
    ai_policy: _raw_config.ai_policy,
    job_target: _raw_config.job_target,
    // Will be resolved per variant
  )
}

// Variant-specific exports — these match what cv.typ imports
// The template already calls _resolve(data, variant) which handles dictionaries
// So we can either:
// A) Export the raw data and let _resolve handle variant selection
// B) Export pre-built variant dicts

#let cv_data = {
  // Re-exports the full data dictionary; template._resolve handles variant lookups.
  // Experience, etc. are stored as raw YAML lists, the template resolves them.
  raw_data + (
    experience: _raw_experience.roles,
    education: _raw_education.entries,
    skills: _raw_skills.categories,
    projects: _raw_projects.entries,
  )
}

// NOTE: The template.typ _resolve function already handles
// variant-aware dictionaries. For experience entries, the template
// expects a list of dicts with (role, company, ...). Currently the
// template calls _resolve_entries which resolves role and description
// by variant. The YAML layer replaces that: role comes from roles.general/systems/infra,
// description comes from filtered bullets.
```

**IMPORTANT:** The template's `_resolve_entries` function expects `role` and `description` fields to be variant-aware dictionaries. The new data layer needs to either:
- (A) Keep the existing template logic and have `data.typ` pre-build variant-resolved lists — simpler, fewer template changes
- (B) Change the template to use the flatter YAML structure — cleaner long-term

**Recommendation: Option A** — keep template changes minimal. Have `data.typ` pre-build variant-resolved lists before exporting. That way `template.typ` barely changes.

```typst
// Pre-resolved export for each variant (Option A)
// cv.typ calls: render_cv(cv_data, variant: "general")
// cv_data already has variant-resolved experience, education, skills, etc.

#let cv_data = {
  // The template already calls _resolve on position, summary (variant-aware dicts)
  // For experience lists, we pre-resolve them before export
  let all_roles = _raw_experience.roles
  
  raw_data + (
    experience_entries_general: _build_experience(all_roles, "general"),
    experience_entries_systems: _build_experience(all_roles, "systems"),
    experience_entries_infra: _build_experience(all_roles, "infrastructure"),
    education_general: _build_education(_raw_education.entries, "general"),
    education_systems: _build_education(_raw_education.entries, "systems"),
    education_infra: _build_education(_raw_education.entries, "infrastructure"),
    skills_general: _build_skills(_raw_skills.categories, "general"),
    skills_systems: _build_skills(_raw_skills.categories, "systems"),
    skills_infra: _build_skills(_raw_skills.categories, "infrastructure"),
  )
}
```

Actually, let me think about this more carefully. The current template `template.typ` already has a function `_resolve(value, variant)` that handles the variant lookup pattern. And the data dict uses the same pattern — `summary` is a dict with variant keys, `position` is a dict with variant keys.

The `_resolve_entries` function in the template also resolves `role` and `description` by variant when those fields are dictionaries.

So the minimal-change approach is:
1. Keep the YAML data structured similarly to the current Typst data
2. Template.typ barely changes — `_resolve` and `_resolve_entries` already handle variant lookup
3. `data.typ` just becomes an import layer that reads YAML and exports in the same shape

Let me simplify the approach. The migration should be mechanical, not introducing new complexity.

Actually, I think the cleanest approach is simpler than I'm making it. Let me think about what the dev agent needs to know:

1. Create YAML files from existing data
2. Update `content/data.typ` to read YAML instead of hardcoding
3. Minor template adjustments if needed

The key new thing is the `cv_priority` and `website_show` fields that don't exist currently. But I can handle that.

Actually, I think I'm overcomplicating the spec document. Let me write it clearly with the recommendation and let the dev agent figure out the exact Typst implementation details. The point of the spec is to describe the architecture and the migration steps, not to write the Typst code.

Let me simplify the document.<｜end▁of▁thinking｜>

<｜｜DSML｜｜tool_calls>
<｜｜DSML｜｜invoke name="write_file">
<｜｜DSML｜｜parameter name="content" string="true"># YAML Content Layer — Architecture & Migration Spec

> **Purpose:** Move from dual-sourced content (`data.typ` + `master-list.md`) to a single YAML-based canonical layer that both Typst (CV PDF) and Astro (website) consume.
> **Status:** Approved. Ready for dev agent execution.
> **Branch:** `feat/001-typst-cv-migration/yaml-content-migration` (create new)
> **Depends on:** No open PRs — start fresh from `main`.

---

## Why

| Problem | Solution |
|---------|----------|
| `data.typ` and `master-list.md` duplicate the same data in different formats | One YAML file, both consume it |
| No curation metadata exists — can't distinguish "must fit on CV" from "nice to have on website" | `cv_priority` (1-3) and `website_show` tags per bullet |
| Data locked in Typst syntax, not portable to Astro | YAML is language-agnostic |
| Editing requires touching multiple files | Edit one YAML file |

---

## Architecture

```
                    ┌─────────────────────────┐
                    │  content/*.yaml          │
                    │  (canonical source of     │
                    │   truth — all data +      │
                    │   curation tags)          │
                    └───────────┬──────────────┘
                                │
                ┌───────────────┴───────────────┐
                │                               │
        ┌───────▼───────┐               ┌───────▼───────┐
        │  data.typ     │               │  Astro        │
        │  (thin YAML    │               │  (reads YAML  │
        │   import layer)│               │   directly)   │
        └───────┬───────┘               └───────┬───────┘
                │                               │
        ┌───────▼───────┐               ┌───────▼───────┐
        │  template.typ  │               │  Website HTML │
        │  (variant      │               │  (everything, │
        │   filtering +   │               │   no page     │
        │   pagination)   │               │   limit)      │
        └───────┬───────┘               └───────────────┘
                │
        ┌───────▼───────┐
        │  cv.pdf       │
        │  (1 page,     │
        │  priority-    │
        │  filtered)    │
        └───────────────┘
```

- **CV (.pdf):** filters by `variant` + `cv_priority <= 2`, fits to one page
- **Website (.html):** shows everything above `website_show = true`, expanded with STAR details

---

## File Structure

```
resume/
├── content/
│   ├── config.yaml              # Name, links, summary (per variant), cert, job target
│   ├── experience.yaml          # All roles, all bullets per variant, curation tags
│   ├── star-stories.yaml        # 14 STAR stories (full S/T/A/R per story)
│   ├── skills.yaml              # Skills by category + variant
│   ├── projects.yaml            # Project entries + variant tags
│   └── education.yaml           # Education + per-variant detail lines
├── content/data.typ             # REPLACED — now imports YAML and re-exports
├── content/master-list.md       # DELETE — superseded by YAML (or regenerate from it)
├── cv.typ                       # UNCHANGED — still calls render_cv(cv_data, variant)
├── lib/template.typ             # MINOR UPDATE — field name alignment if needed
├── cover_letter.typ             # UNCHANGED
└── website/                     # FUTURE — Astro reads same YAML files
```

---

## Curation Strategy: `cv_priority` + `website_show`

Every bullet in `experience.yaml` carries two curation tags:

| Field | Values | Meaning |
|-------|--------|---------|
| `cv_priority` | 1, 2, 3 | 1=essential (on every CV variant), 2=include if space permits, 3=website only |
| `website_show` | true / false | Show on website (no page limit, so most are true) |

**CV compilation logic per variant:**
1. Filter bullets by `variant` (general/systems/infrastructure)
2. Include all `cv_priority: 1` bullets
3. Add `cv_priority: 2` bullets until page is full
4. Drop anything that doesn't fit one page
5. Never include `cv_priority: 3` in CV

**Website logic:**
- Show all `website_show: true` bullets
- Expand STAR-referenced bullets with full S/T/A/R narrative
- No page limit

---

## Curation Metadata for All Bullets

Each bullet in `experience/roles[].bullets[]` gets these fields (currently exist only in master-list.md as ad-hoc cross-references):

```yaml
- text: "Used perf profiling and flamegraphs to trace a performance bottleneck..."
  variant: systems
  cv_priority: 1              # NEW — essential for systems CV
  website_show: true          # NEW — show on website
  star_ref: 1                 # LINKS to star-stories.yaml story id: 1
```

Rules for assigning `cv_priority`:
- **priority 1** — strongest impact metric, core differentiator, primary technical achievement
- **priority 2** — good supporting detail, shows breadth, fills space
- **priority 3** — operational/maintenance work, interesting but not essential for recruiter scan

All existing bullets from `data.typ` and `master-list.md` must be migrated with appropriate tags.

---

## Migration Steps (for dev agent)

### Step 1: Create 6 YAML files from existing data

| YAML file | Source | Notes |
|-----------|--------|-------|
| `config.yaml` | `data.typ` cv_data block (name, email, phone, location, github, linkedin, position, summary, certification, ai_policy, job_target) | Also pull website URL from cv_data |
| `experience.yaml` | `data.typ` `_experience_entries` + `master-list.md` bullet text and cross-refs | Add `cv_priority` and `website_show` based on master-list priority order (first bullets = higher priority) |
| `star-stories.yaml` | `star-stories.md` | Same content, reformat to YAML list |
| `skills.yaml` | `data.typ` `_skill_categories` | Same structure, format to YAML |
| `projects.yaml` | `data.typ` `_project_entries` | Include variant_tags |
| `education.yaml` | `data.typ` `_education_entries` | Include per-variant details |

### Step 2: Replace `content/data.typ`

Current: 298 lines of hardcoded Typst data.
New: A thin YAML-import layer that:
1. Reads all 6 YAML files using `yaml()` function
2. Builds experience entry lists (filtered by variant + priority)
3. Re-exports everything in the shape `template.typ` expects

**Typst YAML import options:**
- **Preferred:** `#import "@preview/yaml:0.2.0": yaml` (community package)
- **Fallback:** Typst 0.12+ has built-in `yaml()` — check `typst --version` first
- Use whichever works reliably

### Step 3: Minor `template.typ` adjustments

The template currently expects `experience_entries` to be a list with variant-resolved fields. After migration:
- Data comes from YAML, filtered by cv_priority
- The field naming might differ slightly — align template if needed
- Test all 3 variants compile identically

### Step 4: Delete `content/master-list.md`

This file is superseded by the YAML layer. After verifying everything compiles:
- `git rm content/master-list.md`
- Or keep as a regenerated reference doc driven by a script

### Step 5: Verify

- Run `mise run check` (regression test)
- `typst compile cv.typ` — compare output PDF visually with current
- `typst compile cv_embedded.typ` — verify same
- `typst compile cover_letter.typ` — verify unchanged

---

## CV Priority Assignments (Draft)

For the dev agent as a starting point. These can be tuned.

### Divergent Tabletop
- **Priority 1:** Founding mission + all systems bullets (CRDT, sub-50ms, supervision tree)
- **Priority 2:** Additional infra bullets (buffer strategy, Ecto.Multi, RLS)
- **Priority 3:** Universal Design bullet

### FARO Africa
- **Priority 1:** ERPNext extension + NFC app + UX improvement (STAR 9) + LLM workflows + Python simulators (systems)
- **Priority 2:** Retool migration + AWS provisioning + BLE tooling
- **Priority 3:** General maintenance bullets + NFC scanner utility + Docker infra

### Ingenics Digital
- **Priority 1:** FSM framework (STAR 5) + Python tooling + WBUS3 protocol (STAR 6)
- **Priority 2:** ESP32 dev + BLE stack + Cap'n Proto IPC + HW mocks (infra)
- **Priority 3:** QP active object + ESP32 concurrent (systems)

### UMAN Technologies
- **Priority 1:** SOME/IP perf (STAR 1, 80% metric) + IPC layer (STAR 4) + HW mocks (STAR 3) + Docker container (STAR 2)
- **Priority 2:** General SOME/IP + Cap'n Proto + Agile lead
- **Priority 3:** (none — all bullets here are strong)

### North-West University
- **Priority 1:** Only one bullet. Always include in general.
- **Priority 3:** For systems/infrastructure variants (omit from CV to save space)

---

## Future: Website Integration

Not part of this migration, but the architecture enables it cleanly:

```
website/                        # Astro project
├── src/content/                # Astro content collections
│   ├── experience.yaml         # symlink -> ../../content/experience.yaml
│   ├── star-stories.yaml       # symlink -> ../../content/star-stories.yaml
│   └── ...
```

Astro reads the same YAML. The website renders every bullet where `website_show: true`, and expands `star_ref` links into full S/T/A/R sections on case study pages.

---

## Acceptance Criteria

- [ ] All 6 YAML files created with correct data from existing sources
- [ ] `data.typ` imports YAML and exports same shape as before
- [ ] `cv.typ --variant general` compiles to PDF with priority 1+2 bullets
- [ ] `cv.typ --variant systems` compiles to PDF with priority 1+2 bullets
- [ ] `cv.typ --variant infrastructure` compiles to PDF with priority 1+2 bullets
- [ ] `cover_letter.typ` still compiles unchanged
- [ ] `mise run check` passes
- [ ] Visual diff shows no regressions vs previous PDF output
- [ ] `master-list.md` removed
- [ ] All 14 STAR stories migrated to `star-stories.yaml`
