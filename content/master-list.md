# Experience Master — Werner Bisschoff

This is the canonical source of truth for all CV content.
Each CV variant (general / systems / infrastructure) curates from this document.
**STAR stories** (Amazon LP format) are in `content/star-stories.md` and cross-referenced below.

> **ATS guard:** Never include Expo, React Native, or front-end/mobile frameworks on the infrastructure variant.
> These trigger front-end ATS classification, preventing platform/infrastructure role matching.
> The general and systems variants may include them where contextually relevant (e.g., NFC scanner utilities).

---

## 1. Divergent Tabletop | Cape Town, ZA

### General / Systems / Infrastructure
- **Role (general):** Founder and Host
- **Role (systems):** Principal Systems Architect
- **Role (infrastructure):** Principal Systems Architect
- **Dates:** Jul 2025 – Present

#### General bullets
- Founded neurodivergent-focused peer community; manage event operations and WhatsApp-based community platform.
- Applied systems thinking to solve community management challenges through software solutions.

#### Systems bullets
- Engineered a distributed real-time data engine utilizing Elixir/OTP and conflict-free replicated data types (CRDT models). Deployed in-memory GenServer storage buffers with threshold-based flush mechanics, reducing direct database write transactions by approximately 85% under sustained edit workloads.
- Integrated a Rust-backed CRDT synchronization layer (y_ex) using actor-based concurrency, achieving sub-50ms convergence latency across distributed editing sessions through deterministic state reconciliation and binary delta serialization.
- Designed a dynamic BEAM supervision tree with one_for_one isolation, encapsulating each page editing session in its own process subtree to prevent cascading failures and guarantee per-session state integrity.

#### Infrastructure bullets
- Engineered and hosted an enterprise-grade documentation ecosystem.
- Implemented a single-database multi-tenant separation engine using PostgreSQL Row-Level Security (RLS) and transaction-scoped local parameters (SET LOCAL), enforcing strict data silos across isolated groups.
- Designed an atomic asynchronous flush strategy using in-memory GenServer storage buffers, reducing database persistent write transactions by 85% during periods of high user interaction.
- Utilized Ecto.Multi atomic chains and Oban transactional background workers to ensure multi-stage backend edits (e.g., structural document renaming and incoming backlink indexing) execute completely or roll back safely.
- Applied Universal Design and Executive Functioning support models to product UX/UI; established highly structured, low-context asynchronous operational playbooks that minimized cognitive friction for contributors.

---

## 2. FARO Africa | Cape Town, ZA

- **Role (general):** Full-Stack Software Engineer
- **Role (systems):** Embedded Systems & Integration Engineer
- **Role (infrastructure):** Full-Stack ERPNext & Automation Engineer
- **Dates:** Aug 2024 – Nov 2025

#### General bullets
- Extended ERPNext using Python/JavaScript to improve workflows, pricing logic, and operational reporting (SQL) → reduced manual reporting time and improved data accuracy.
- Built mobile application in Expo, including NFC (ISO 14443-4 APDUs) for e-paper price tags and card operations → enabled real-time price updates with fewer tagging errors.
- Migrated internal mobile Retool workflows to Expo → improved performance and enhanced long-term maintainability.
- Provisioned AWS infrastructure with Pulumi; deployed Inngest and PayloadCMS services.
- Diagnosed and resolved issues in a large existing ERPNext installation.
- Introduced LLM-assisted development workflows → improved debugging speed and code review throughput, enabling faster iteration.

#### Systems bullets
- Designed ISO 14443-4 NFC communication architectures for e-paper display nodes and secure card reader matrices.
- Engineered lock-free asynchronous device management services bridging hardware peripherals with application layers.
- Built Python-based hardware peripheral simulators to catch edge-case device state corruptions prior to flashing.
- Introduced LLM-assisted development workflows to improve debugging speed and code review throughput.

#### Infrastructure bullets
- [STAR 9] Identified poor UX as root cause of recurring user errors — pushed back against "training gap" framing, proposed user research to validate, and drove UX improvements that reduced task completion time and error rates.
- Refactored and extended ERPNext via Python and JavaScript server hooks, optimizing pricing matrices and BI reporting.
- Architected migration of internal Retool workflows to Expo/React Native, reducing vendor licensing overhead.
- Built custom NFC scanner utilities within Expo for instantaneous physical inventory syncs.
- Provisioned and maintained a secure virtualized Linux infrastructure environment using Docker Compose for container isolation and writing custom backup and monitoring scripts.
- Diagnosed and resolved issues in a large existing ERPNext installation; introduced LLM-assisted debugging workflows.

---

## 3. Ingenics Digital GmbH | Remote / Germany

- **Role (general):** Embedded Software Engineer
- **Role (systems):** Firmware Engineer (Contract)
- **Role (infrastructure):** Enterprise Infrastructure & Tooling Engineer
- **Dates:** Mar 2023 – May 2024

#### General bullets
- Designed event-driven FSM for I2C-based embedded system (C++/FreeRTOS) → maintainable architecture, fewer bugs.
- Developed ESP32 applications (C/C++, ESP-IDF) with configurable BLE stack, TinyFrame protocol, and FOTA updates.
- Built Python tooling for serial/BLE communication, hardware mocks, and pytest async workflows → accelerated testing.
- Developed active object within QP Real-Time Embedded Framework (QSPY) to simulate device behaviour.

#### Systems bullets
- Architected deterministic FSMs on dual-core ESP32 using FreeRTOS for concurrent sensor arrays.
- Developed Cap'n Proto IPC over serial lines, achieving sub-millisecond serialization latency.

#### Infrastructure bullets
- Built modular Python utility structures and automation scripts for internal configuration schema validation.
- Designed data handling pipelines ensuring data transfer consistency across runtime platforms using declarative specifications.
- Developed Python hardware mocks enabling faster development cycles with fewer hardware dependencies.

---

## 4. UMAN Technologies | Century City, Cape Town

- **Role (general):** Software Developer
- **Role (systems):** Software Developer
- **Role (infrastructure):** Infrastructure & Tooling Developer
- **Dates:** Mar 2021 – Dec 2022
- **STAR stories:** 1 (Dive Deep — SOME/IP perf), 2 (Bias for Action — Docker), 3 (Deliver Results — HW mocks), 4 (Ownership — IPC)

#### General bullets
- Implemented SOME/IP RPC services; optimized performance bottlenecks with perf.
- Built IPC/RPC layers (C++/Python) using Cap'n Proto; led small team using Agile practices.

#### Systems bullets
- [STAR 1] Used perf profiling and flamegraphs to trace a performance bottleneck to JSON serialization and verbose logging in a SOME/IP request handling loop. Eliminated unnecessary logging via config toggle reducing latency by ~80%, then drove an architecture redesign to phase out JSON entirely.
- [STAR 4] Sole owner of an IPC service layer — studied existing node schema, designed node structures and data contracts, and implemented the communication layer enabling the frontend to consume the service.
- [STAR 3] Built Python-based SOME/IP hardware mocks that simulated request/response behavior; integrated into CI so automated tests ran without physical hardware.

#### Infrastructure bullets
- [STAR 2] Proactively created a Docker development container replicating the exact hardware environment — including VLAN and networking configuration — reducing setup time from hours to under an hour and enabling remote teams to develop without physical hardware.
- [STAR 3] Built Python hardware mocks simulating SOME/IP behavior; integrated into CI to enable automated testing without physical hardware, improving test coverage and developer productivity.

---

## 5. North-West University | Potchefstroom

- **Role (general):** Junior Lecturer
- **Role (systems):** Junior Lecturer
- **Role (infrastructure):** Junior Lecturer
- **Dates:** Feb 2020 – Dec 2020
- **Used in variants:** general only (dropped from systems and infrastructure during page-trimming)

#### General
- Lectured Python and C++ programming for Introduction to Programming for first year IT students in both remote and in-person settings.

---

## Education

**B.Eng. Computer and Electronic Engineering** | North-West University | Potchefstroom | 2020

#### General
- Focus on embedded systems, software engineering, and electronic design
- NFC payment emulator (Kotlin/Android), STM32 firmware (C), PID motor controller (Arduino)
- Data analysis with Python/pandas using linear regression, correlation and machine learning

#### Systems
- Focus on embedded systems, software engineering, and electronic design
- Developed NFC payment protocol emulator (Kotlin/Android), STM32 firmware (C), PID motor controller (Arduino)

#### Infrastructure
- Focus on embedded systems, software engineering, and electronic design
- Developed data analysis pipeline with Python/pandas (linear regression, ML); built NFC payment emulator (Kotlin/Android)

---

## Skills

### General
- **Primary:** C/C++, Python, FreeRTOS, ESP32/ESP-IDF, NFC APDU (ISO 14443-4)
- **Secondary:** NimBLE, UART/SPI/I2C, TinyFrame, BLE, Hardware-in-the-Loop Testing
- **Foundational:** SQL, Docker, CI/CD, Git, Linux
- **Other:** React, Phoenix, AWS, Pulumi, ERPNext

### Systems
- **Primary Competencies:** C, C++, FreeRTOS, ESP32/ESP-IDF, NFC APDU (ISO 14443-4)
- **Secondary Competencies:** NimBLE, Bare-Metal Runtimes, UART/SPI/I2C, Hardware-in-the-Loop (HIL) Testing
- **Foundational Systems:** Linux IPC, Bash, Python (pytest, Custom Automation Frameworks), Assembly, System Modeling
- **Cross-Domain Integration:** ERPNext (Integration-focused), Docker, Spec-Driven Development (SDD)

### Infrastructure
- **Primary Competencies:** Python, Docker, Docker Compose, AWS (Solutions Architect – In Progress), PostgreSQL (Row-Level Security, Index Tuning, Connection Pooling)
- **Secondary Platforms:** ERPNext/Frappe Framework, Elixir/OTP, Asynchronous Workflow Engines (Inngest, Oban)
- **Data Layer Infrastructure:** SQL, Ecto.Multi
- **Systems & Automation:** Pulumi (IaC), Linux Systems Administration, CI/CD Pipelines, Bash Scripting, Network Proxies, SSH Networking, Spec-Driven Development (SDD)

---

## Projects

### Divergent Tabletop Wiki | Community Knowledge Base | Jun 2025 – Present
- Built a community wiki using Astro, Elixir, and Docker for knowledge management
- Documented event frameworks, onboarding processes, and communication best practices
- Created tooling for content management and community operations

### Ingenics Digital GmbH | Event-Driven FSM for Embedded Systems | Mar 2023 – May 2024
- Designed event-driven finite state machine for I2C-based embedded system using C++ and FreeRTOS
- Solved complex state management challenges in real-time embedded environment
- **Outcome:** Maintainable in-house architecture leading to fewer bugs and quicker development cycles
