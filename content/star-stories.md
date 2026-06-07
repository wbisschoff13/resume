# Amazon LP Cheatsheet — Draft

## Leadership Principles: Story Index

### 1. Insist on the Highest Standards
> **Definition:** Leaders keep standards that ensure every deliverable is the best it can possibly be — even if it means spending more time or resources to get there.

**Stories:**
- **Story 8** (FARO) — Testing Framework: Established automated testing with no allocated time, working around ERPNext/Frappe faults, backfilling tests for critical functionality. Tests run on all PRs via GitHub CI.
- **Story 10** (Divergent Tabletop) — SDD Framework: Created a spec-driven development framework to add determinism to AI-assisted coding, reducing wasted iterations.
- **Story 14** (Divergent Tabletop) — Astro Website & Accessibility: Built WCAG-compliant website with keyboard navigation, Lighthouse performance optimization, and a forced-scroll trigger warning tool.

**Quick pick:** Story 8 (Testing Framework)

---

### 2. Bias for Action
> **Definition:** Leaders take initiative and move fast. They know that delaying decisions costs more than making the wrong call and learning from it.

**Stories:**
- **Story 2** (UMAN) — Docker Development Container: Proactively created a Dockerfile to replicate the hardware environment for remote teams, reducing setup from hours to under an hour.
- **Story 6** (Ingenics) — WBUS3 Protocol: Acquired ESP32 devices and implemented a proprietary protocol on top of I2C without being asked.
- **Story 7** (FARO) — NFC/E-ink Label App: Took on an R&D project to reverse engineer a proprietary e-ink display as a solo contributor.
- **Story 13** (Divergent Tabletop) — Events Rotation System: Designed a rotation system and player aids to run multi-table events solo.

**Quick pick:** Story 2 (Docker Container) — has clear stakeholder pushback and measurable result

---

### 3. Deliver Results
> **Definition:** Leaders focus on outcomes. They set ambitious goals, track metrics, and deliver despite obstacles.

**Stories:**
- **Story 3** (UMAN) — SOME/IP Hardware Mocks: Built Python mocks that were adopted by the team and integrated into CI, enabling automated tests without physical hardware.
- **Story 5** (Ingenics) — FSM Framework: Designed and delivered a C++ FSM framework that the customer used for their own products.
- **Story 6** (Ingenics) — WBUS3 Protocol: Implemented the full protocol and testing framework, enabling the customer to continue development reliably.
- **Story 7** (FARO) — NFC/E-ink Label App: Built a fully functional label creation app as an R&D deliverable.
- **Story 11** (Divergent Tabletop) — Kintree CRDT Architecture: Delivered a CRDT-based collaborative editing system with zero lock conflicts.

**Quick pick:** Story 5 (FSM Framework) — customer built products on top of it

---

### 4. Dive Deep
> **Definition:** Leaders go below the surface. They find root causes, understand systems end-to-end, and know the details that matter.

**Stories:**
- **Story 1** (UMAN) — SOME/IP Performance Investigation: Used perf and flamegraphs to trace a bottleneck to JSON serialization + verbose logging, achieving 80% improvement.
- **Story 11** (Divergent Tabletop) — Kintree CRDT Architecture: Deep technical design of CRDT storage, dual-schema PostgreSQL, and O(1) Registry lookups.

**Quick pick:** Story 1 (SOME/IP Performance) — has the 80% metric and concrete technical depth

---

### 5. Learn and Be Curious
> **Definition:** Leaders never stop learning. They ask questions, explore new areas, and stay ahead of trends.

**Stories:**
- **Story 3** (UMAN) — SOME/IP Hardware Mocks: Self-taught SOME/IP protocol from specs.
- **Story 5** (Ingenics) — FSM Framework: Learned C++ (templates, RAII, smart pointers) to implement a dynamic event-driven FSM.
- **Story 7** (FARO) — NFC/E-ink Label App: Reverse engineered a proprietary NFC protocol through trial and error.
- **Story 12** (Divergent Tabletop) — Self-taught Elixir/Phoenix: Chose and learned Elixir for FP benefits, immutability, and Phoenix/LiveView for real-time capabilities.

**Quick pick:** Story 12 (Self-taught Elixir) — shows commitment to learning a new paradigm

---

### 6. Earn Trust
> **Definition:** Leaders build credibility through competence, communication, and follow-through. Others trust them to do what they say.

**Stories:**
- **Story 9** (FARO) — UX Improvements: Identified the root cause of user errors as UX, not training. Argued for the investment and delivered results that changed how the team viewed the problem.

**Quick pick:** Story 9 (UX Improvements) — shows you can influence and convince stakeholders

---

### 7. Have Backbone; Disagree and Commit
> **Definition:** Leaders speak up when they disagree, even if it's uncomfortable. Once a decision is made, they commit fully and make it work.

**Stories:**
- **Story 9** (FARO) — UX Improvements: Pushed back on the "training gap" framing, argued that UX was the root cause, and held your position until the team adopted the changes.

**Quick pick:** Story 9 (UX Improvements) — same story covers Earn Trust + Have Backbone

---

### 8. Ownership
> **Definition:** Leaders take end-to-end responsibility. They don't say "that's not my job" — they own problems from start to finish.

**Stories:**
- **Story 1** (UMAN) — SOME/IP Performance Investigation: Took the investigation task and drove it to resolution (80% improvement + architecture redesign).
- **Story 4** (UMAN) — IPC Service Implementation: Sole owner of the IPC layer from schema study through implementation.
- **Story 8** (FARO) — Testing Framework: Championed testing with no allocated time, built it, and maintained it.
- **Story 10** (Divergent Tabletop) — SDD Framework: Created your own development methodology from scratch.
- **Story 13** (Divergent Tabletop) — Events Rotation System: Owned the entire event running experience, from rotation to player aids.

**Quick pick:** Story 10 (SDD Framework) — shows ownership of a personal initiative that solved a real problem

---

---

## Format Guide
```
SITUATION: What was the context?
TASK:      What was your specific responsibility?
ACTION:    What did YOU do? (focus on you, not the team)
RESULT:    What measurable outcome happened?
```

---

## UMAN

### 1. Dive Deep — SOME/IP Performance Investigation

**LPs:** Dive Deep (primary), Ownership (secondary)

```
SITUATION: Our C++ library for customer hardware had severe latency
          issues — customers couldn't use the software at all.

TASK:     I was tasked to investigate and fix the performance bottleneck.

ACTION:   I used perf to profile the hot paths during live requests,
          generated flamegraphs, and traced the problem to JSON
          serialization in the request handling loop. Verbose logging
          on every JSON operation made it worse. I disabled the
          unnecessary logging via a config toggle as a first step.
          I then participated in the design discussion and helped drive
          the effort to phase out JSON entirely through a complete
          architecture redesign for dynamic payload creation.
          I self-taught the SOME/IP protocol from specs to ensure
          the new approach was spec-compliant.

RESULT:   Removing verbose logging alone improved some request calls
          by 80%. The full architecture redesign eliminated the bottleneck
          long-term, restoring full functionality for customers.
```

---

### 2. Bias for Action — Docker Development Container

**LPs:** Bias for Action (primary), Deliver Results (secondary)

```
SITUATION: Remote teams were developing software for an embedded Linux
          hardware system. Each developer set up their own environment
          manually, leading to inconsistencies and slow onboarding.

TASK:     Enable the team to develop and test reliably without physical
          hardware, regardless of local setup.

ACTION:   I proactively created a Dockerfile that replicated the exact
          hardware environment — including VLAN setup and networking
          configuration — matching production precisely. I had to
          convince a skeptical team member who preferred pushing images
          to a remote service, arguing for a simpler local-first approach.

RESULT:   Setup time reduced from hours to under an hour. Remote teams
          could run and test the full system without physical hardware.
          Onboarding new engineers became significantly faster.
```

---

### 3. Deliver Results — SOME/IP Hardware Mocks

**LPs:** Deliver Results (primary), Learn and Be Curious (secondary)

```
SITUATION: Physical hardware wasn't always available for testing.
          Automated tests couldn't run at all.

TASK:     Enable automated testing without access to real hardware.

ACTION:   I built Python mocks that simulated SOME/IP requests and
          responses, creating a test harness that replicated hardware
          behavior. I ensured the mocks were integrated into CI so
          tests ran automatically against them.

RESULT:   The mocks were adopted by the team and integrated into CI.
          Automated tests could run without physical hardware,
          improving test coverage and developer productivity.
```

---

### 4. Ownership — IPC Service Implementation

**LPs:** Ownership (primary), Deliver Results (secondary)

```
SITUATION: Customers needed to dynamically add our service to the
          hardware box and interact with it via IPC.

TASK:     Design and implement the IPC layer for our SOME/IP simulation
          service — specifically, what nodes to expose and what data
          they would contain — so the frontend could consume it.

ACTION:   I was the sole owner of our service's IPC implementation.
          I studied the existing node schema and designed how to expose
          our service, defining the node structure and data contracts.
          There were a few iterations early on — I had some initial
          misunderstandings about how it should work — but I worked
          through them and wrote the code to make our service available
          to the frontend.

RESULT:   The IPC layer was implemented and customers could successfully
          integrate our service into the hardware box.
```

---

## INGENICS

### 5. Deliver Results — Finite State Machine Framework

**LPs:** Deliver Results (primary), Learn and Be Curious (secondary)

```
SITUATION: A customer needed a robust, event-driven finite state machine
          for industrial IoT devices. The existing C-based approach
          (built on the QP framework) wasn't robust or memory-safe
          enough for their requirements.

TASK:     Design and implement a finite state machine framework that
          the customer could use for their specific systems.

ACTION:   I chose C++ over C for memory safety and designed the entire
          framework — including event handler registration, state
          transition logic, and example implementations — so the customer
          could adapt it to any set of states, transitions, and event
          handlers. I learned C++ features (templates, RAII, smart
          pointers) to implement a dynamic event-driven FSM that
          wouldn't rely on the C-style void pointer shortcuts.

RESULT:   The customer built on top of the framework for their
          customer-facing products. The FSM provided a robust,
          memory-safe foundation for their industrial IoT systems.
```

---

### 6. Deliver Results / Bias for Action — WBUS3 Protocol Implementation

**LPs:** Deliver Results (primary), Bias for Action (secondary)

```
SITUATION: The customer needed a proprietary WBUS3 protocol implemented
          on top of I2C for their embedded system. Manual testing was
          the only approach available.

TASK:     Implement the WBUS3 protocol and create a testing framework
          to enable reliable development.

ACTION:   I acquired ESP32 devices and implemented the WBUS3 protocol
          on the target MCU. WBUS3 added flow control, an interrupt
          line, and reset logic on top of standard I2C. I also created
          unit tests and hardware request mocks so the customer could
          test without physical hardware.

RESULT:   The customer used the testing framework to continue WBUS3
          development more reliably. Testing no longer depended on
          manual hardware access.
```

---

---

## FARO

### 7. Learn and Be Curious — NFC/E-ink Label App (R&D)

**LPs:** Learn and Be Curious (primary), Bias for Action (secondary), Deliver Results (tertiary)

```
SITUATION: A startup fashion retailer wanted to use e-paper price tags
          for shelf markdowns instead of manual paper tags. We had
          partial knowledge of the APDU commands needed, but not the
          exact image format the proprietary device expected.

TASK:     Figure out how to generate an e-ink compatible image and
          send raw data over APDU to the proprietary e-ink display,
          as part of an R&D project.

ACTION:   I reverse engineered the image format through extensive
          trial and error and documentation research. The protocol
          required a specific "binnng" process where data had to
          be sent in a particular way. I used my prior experience
          with NFC and APDU protocols to build an Expo app on Android
          that generated the correct image and transmitted it to the
          display. I worked solo given my specific background.

RESULT:   I built a fully functional label creation app that could
          generate e-ink compatible images and send them to the
          proprietary display. The R&D project explored whether
          e-paper price tags were viable for the retailer.
```

---

### 8. Insist on Highest Standards / Ownership — Testing Framework

**LPs:** Insist on Highest Standards (primary), Ownership (secondary), Deliver Results (tertiary)

```
SITUATION: No automated tests existed. The ERPNext/Frappe testing suite
          had reproducibility issues — it modified the database, so
          running the suite twice produced different results.

TASK:     Establish automated testing for the codebase.

ACTION:   I championed the creation of a testing framework despite
          no allocated time for it. I worked around the Frappe
          testing suite's faults — fixing CI configuration where needed
          — and created regression and integration tests for the
          most critical functionality, backfilling tests for
          existing code.

RESULT:   Tests were integrated into GitHub CI and ran on all PRs.
          The team now had automated regression coverage for critical
          paths.
```

---

### 9. Have Backbone / Earn Trust / Insist on Highest Standards — UX Improvements

**LPs:** Have Backbone (primary), Earn Trust (secondary), Insist on Highest Standards (tertiary)

```
SITUATION: Internal warehouse tools were hard to use — requiring
          many taps to navigate to common actions. There had been
          frequent user error reports. The tech team attributed this
          to a "training gap," but I identified it as a UX problem.
          Changes were initially resisted as "unnecessary."

TASK:     Improve the UX of internal tools during a Retool-to-Expo
          migration.

ACTION:   I pushed back on the "training gap" framing, arguing the
          root cause was poor UX design. I proposed interviewing ground
          staff to validate my hypothesis, then made initial
          improvements based on gut calls to demonstrate value.
          I took ownership of the UX design for the new versions
          and argued for the investment.

RESULT:   The team eventually adopted the UX changes. Fewer taps
          reduced task completion time and user error rates dropped
          — validating that the problem was UX, not training.
```

---

---

## DIVERGENT TABLETOP

### 10. Insist on Highest Standards / Ownership — SDD Framework

**LPs:** Insist on Highest Standards (primary), Ownership (secondary)

```
SITUATION: AI-assisted development often produced outputs misaligned
          with my vision — requiring many iterations to reach
          satisfaction. I was doing "vibe coding" without deterministic
          guardrails to keep AI on track.

TASK:     Create a development framework that would add determinism
          to agentic coding, ensuring AI worked on the right problems
          and stayed aligned with the intended outcome.

ACTION:   I designed a Spec-Driven Development (SDD) framework that
          combines Acceptance Test Driven Development, Test Driven
          Development, and Test Driven Agentic Development. The
          framework provides structured specifications before coding,
          creating checkpoints that surface misalignments and
          inefficiencies before they become problems.

RESULT:   Using SDD, I caught inefficiencies and misalignment early
          across multiple projects. The framework improved my
          agentic coding efficiency by reducing wasted iterations
          and keeping AI output aligned with goals.
```

### 11. Dive Deep / Deliver Results — Kintree CRDT Architecture

**LPs:** Dive Deep (primary), Deliver Results (secondary)

```
SITUATION: When designing the collaborative wiki, the initial approach
          of edit locking could lock users out of pages and introduce
          wait times. I wanted to avoid that friction from a user
          experience perspective.

TASK:     Design a collaborative editing system that allowed multiple
          users to edit simultaneously without lock conflicts.

ACTION:   I chose CRDT (Conflict-free Replicated Data Types) via the
          y_ex library (Rust-backed) to handle concurrent edits without
          requiring locks. I designed the PostgreSQL schema with dual
          storage — a CRDT field for editing and a raw text field to
          enable fast full-text search and future AI moderation
          capabilities. I used Elixir's Registry for O(1) lookup to
          map page IDs to EditLock GenServer PIDs, allowing efficient
          process address resolution without bottlenecks.

RESULT:   The CRDT approach eliminated edit lock conflicts entirely.
          Multiple users can edit simultaneously, with the dual storage
          schema enabling both efficient search and AI integration
          without requiring a separate search engine.
```

---

### 12. Learn and Be Curious — Self-taught Elixir/Phoenix

**LPs:** Learn and Be Curious (primary)

```
SITUATION: I needed a technology stack suited for a collaborative,
          concurrent, real-time wiki. I had no prior experience
          with Elixir.

TASK:     Choose and learn a technology stack that would provide
          functional programming benefits, robustness, and efficient
          real-time capabilities for the Kintree wiki.

ACTION:   I chose Elixir for its emphasis on functional programming
          and immutable data — reducing bugs from unforeseen state
          changes. Phoenix was recommended as a robust concurrent
          framework, and LiveView because it uses WebSockets
          natively, eliminating the need for a separate REST API.
          I self-taught the entire stack and built Kintree from scratch.

RESULT:   I built a production-grade collaborative wiki engine
          using self-taught Elixir/Phoenix/LiveView, handling
          concurrent real-time editing without a separate API layer.
```

---

### 13. Ownership / Bias for Action — Events Rotation System

**LPs:** Ownership (primary), Bias for Action (secondary)

```
SITUATION: As the sole host of multi-table board game events, I faced
          the challenge of teaching games at multiple tables while
          managing member flow and keeping events running smoothly.

TASK:     Solve the problem of managing multiple tables and teaching
          games as a single host.

ACTION:   I designed a rotation system using a card-dealing approach
          for quick member shuffling. I created custom player aids
          — simplified reference materials for game rules — so
          attendees could self-teach without relying solely on me.
          When possible, I trained volunteers to host one table,
          further distributing the teaching burden.

RESULT:   Events ran smoothly despite having a single host.
          Player aids reduced my direct teaching time, and the
          rotation system kept the event flowing without bottlenecks.
```

---

### 14. Insist on Highest Standards — Astro Website & Accessibility

**LPs:** Insist on Highest Standards (primary)

```
SITUATION: I built the Divergent Tabletop community website using Astro.
          The community includes a vent and support group where trigger
          warnings and spoilers needed appropriate handling.

TASK:     Ensure the website met accessibility standards and had proper
          content warnings for sensitive discussions.

ACTION:   I built the website with WCAG compliance as a target,
          ensuring keyboard-based navigation and readability. I created
          a "read more" forced-scroll tool for trigger warnings and
          spoilers — handling edge cases like invisible Unicode
          characters that display differently than their character
          count suggests. I optimized for Lighthouse performance to
          ensure fast load times.

RESULT:   The website met accessibility standards with keyboard
          navigation support. The trigger warning tool was implemented
          for the community's sensitive content needs.
```

---

---

## LP Coverage Tracker

| Leadership Principle | UMAN | Ingenics | FARO | Divergent Tabletop | Status |
|---|---|---|---|---|---|
| Insist on Highest Standards | — | — | ✅ (8) | ✅ (10, 14) | ✅ |
| Bias for Action | ✅ (2) | ✅ (6) | ✅ (7) | ✅ (13) | ✅ |
| Deliver Results | ✅ (3) | ✅ (5, 6) | ✅ (7) | ✅ (11) | ✅ |
| Dive Deep | ✅ (1) | — | — | ✅ (11) | ✅ |
| Learn and Be Curious | ✅ (3) | ✅ (5) | ✅ (7) | ✅ (12) | ✅ |
| Earn Trust | — | — | ✅ (9) | — | ✅ |
| Have Backbone; Disagree and Commit | — | — | ✅ (9) | — | ✅ |
| Ownership | ✅ (4) | — | ✅ (8) | ✅ (10, 13) | ✅ |

## Summary: Recommended Stories by LP

| Leadership Principle | Primary Story | Company | Secondary Story | Company |
|---|---|---|---|---|
| Insist on the Highest Standards | Testing Framework | FARO | SDD Framework | Divergent Tabletop |
| Bias for Action | Docker Container | UMAN | Events Rotation System | Divergent Tabletop |
| Deliver Results | FSM Framework | Ingenics | SOME/IP Hardware Mocks | UMAN |
| Dive Deep | SOME/IP Performance | UMAN | Kintree CRDT Architecture | Divergent Tabletop |
| Learn and Be Curious | Self-taught Elixir | Divergent Tabletop | NFC/E-ink Label App | FARO |
| Earn Trust | UX Improvements | FARO | — | — |
| Have Backbone; Disagree and Commit | UX Improvements | FARO | — | — |
| Ownership | SDD Framework | Divergent Tabletop | SOME/IP Performance | UMAN |

*(You have 2+ strong stories for every LP — above are the recommended picks)*

---

## Notes

- All stories use the STAR method (Situation, Task, Action, Result)
- Focus on "I" not "we" — own your contributions
- Quantify results where possible (80%, hours to minutes, etc.)
- You don't need all 8 LPs for every interview — 2 strong stories per LP is sufficient
- Review these before your interview and practice saying them out loud
