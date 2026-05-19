# Experience Master — Werner Bisschoff

This is the canonical source of truth for all employment experience. Each CV variant
(embedded / enterprise) curates from this document.

---

## 1. Divergent Tabletop | Cape Town, ZA
**Founder and Host** | Jul 2025 – Present

### Concise CV Bullets (as currently in cv/experience.tex)
- Founded and facilitate a neurodivergent-focused peer community, managing event operations and a WhatsApp-based community.
- Conflict resolution and management in a neurodiverse context.
- Applied systems thinking to solve community management challenges through software solutions.

### Detailed Engineering Notes (from wiki analysis)
- Architected a distributed knowledge-management infrastructure (Docs-as-Code Wiki) optimized via git-backed asynchronous markdown pipelines.
- Integrated the Rust-backed CRDT synchronization library y\underline{}ex via NIFs to handle real-time modifications; implemented an actor-based buffering model with sub-50ms state-sync latency.
- Designed a dynamic BEAM supervision tree with `:one_for_one` strategy to isolate concurrent page editing instances, ensuring 99.9% fault isolation.
- Implemented threshold-based buffer flush and scheduled heap hibernation (`hibernate_after`), reducing process memory footprints by ~60%.
- Built multi-tenant isolation using PostgreSQL Row-Level Security (RLS) and `SET LOCAL` transaction-scoped context injection.
- Used `Ecto.Multi` atomic chains and `Oban` transactional background workers for multi-stage backend edits.
- Built real-time collaborative editing via Phoenix LiveView + WebSockets + Phoenix.PubSub.
- Implemented per-page EditLock GenServer with heartbeat timeout and fair handover queue to prevent concurrent write conflicts.
- Applied Monotropic focus paradigms and Universal Design principles to minimize platform cognitive complexity.

---

## 2. FARO Africa | Cape Town, ZA
**Full-Stack Software Engineer** | Aug 2024 – Nov 2025

- Extended ERPNext using Python/JavaScript to improve workflows, pricing logic, and operational reporting (SQL) → reduced manual reporting time and improved data accuracy
- Built mobile application in Expo, including NFC (ISO 14443-4 APDUs) for e-paper price tags and card operations → enabled real-time price updates with fewer tagging errors
- Migrated internal mobile Retool workflows to Expo → improved performance and enhanced long-term maintainability
- Developed and maintained C# APIs supporting internal systems.
- Provisioned AWS infra with Pulumi and deployed services including Inngest and PayloadCMS.
- Diagnosed and resolved issues in a large existing ERPNext installation.
- Introduced LLM-assisted development workflows → improved debugging speed and code review throughput.

---

## 3. Ingenics Digital GmbH | Remote / Germany
**Embedded Software Engineer** | Mar 2023 – May 2024

- Designed an event-driven finite state machine for an I2C-based embedded system using C++ and FreeRTOS → created maintainable in-house architecture leading to fewer bugs and quicker development
- Developed ESP32 applications using C/C++ and ESP-IDF
- Integrated a configurable low-energy BLE stack for device communication
- Built Python-based tooling for serial/BLE communication, including client-facing test executables → accelerated testing and debugging workflows
- Created Python hardware mocks for rapid iteration and early-stage testing → enabled faster development cycles with fewer hardware dependencies
- Managed fast, reliable data interchange using a compact TinyFrame binary protocol
- Implemented asynchronous communication workflows with Python and Pytest
- Developed an active object within the QP Real-Time Embedded Framework (with QSPY) to simulate device behaviour
- Integrated a configurable BLE stack for device communication and implemented FOTA firmware updates over BLE

---

## 4. UMAN Technologies | Century City, Cape Town
**Software Developer** | Mar 2021 – Dec 2022

- Creating and maintaining Docker containers for development and CI/CD testing → improved development environment consistency
- Implementing and testing new services using RPC based on the SOME/IP protocol, as well as using perf to reduce performance bottlenecks
- Implementing IPC/RPC in existing C++ programs and Python scripts using Cap'n Proto and pycapnp
- Implementing a node tree to expose process-related variables and function calls to the IPC interface
- Analysing TCP/UDP traffic with Wireshark
- Leading a small team using AGILE development practices, including onboarding and mentoring new software developers

---

## 5. North-West University | Potchefstroom
**Junior Lecturer** | Feb 2020 – Dec 2020

- Lecturing Python and C++ programming for Introduction to Programming for first year IT students in both remote and in-person settings

---

## Education

**B.Eng. Computer and Electronic Engineering** | North-West University | Potchefstroom | 2020

- Focus on embedded systems, software engineering, and electronic design
- Developing an Android app with Kotlin to emulate an ISO 14443 protocol-based NFC payment system
- Developing microcontroller logic with C and the STM32 system as well as utilizing STM32CubeMX
- Implementing a PID controller with an Arduino to control a DC motor's voltage and speed
- Cleaning and analysing data from large spreadsheets with Python and Pandas, utilizing linear regression, correlation and machine learning

---

## Projects

### Divergent Tabletop Wiki | Community Knowledge Base | Jun 2025 – Present
- Built a community wiki using Astro, Elixir, and Docker for knowledge management
- Documented event frameworks, onboarding processes, and communication best practices
- Created tooling for content management and community operations

### Ingenics Digital GmbH | Event-Driven FSM for Embedded Systems | Mar 2023 – May 2024
- Designed event-driven finite state machine for I2C-based embedded system using C++ and FreeRTOS
- Solved complex state management challenges in real-time embedded environment
- Outcome: Maintainable in-house architecture leading to fewer bugs and quicker development cycles
