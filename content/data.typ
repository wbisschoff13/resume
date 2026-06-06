#let _experience_entries = (
  (
    role: (
      general: "Founder and Host",
      embedded: "Principal Systems Architect",
      enterprise: "Principal Systems Architect",
    ),
    company: "Divergent Tabletop",
    location: "Cape Town",
    start_date: "Jul 2025",
    end_date: none,
    variant_tags: ("general", "embedded", "enterprise"),
    description: (
      general: (
        [Founded and facilitate a neurodivergent-focused peer community, managing event operations and a WhatsApp-based community.],
        [Conflict resolution and management in a neurodiverse context.],
        [Applied systems thinking to solve community management challenges through software solutions.],
      ),
      embedded: (
        [Engineered and deployed a distributed knowledge-management infrastructure],
        [Integrated a CRDT synchronization layer (y_ex) to handle real-time modifications; implemented an actor-based buffering model that reduced state-sync latency to sub-50ms thresholds.],
        [Designed a dynamic BEAM supervision tree with a :one_for_one strategy to isolate concurrent page editing instances, ensuring 99.9% fault isolation and zero system-wide cascading crashes.],
        [Implemented a threshold-based buffer flush and scheduled heap hibernation (hibernate_after), reducing process memory footprints by ~60% under active network I/O concurrency.],
        [Applied Monotropic focus principles and Universal Design to minimize user information processing overhead and ensure highly predictable, deterministic information layout.],
      ),
      enterprise: (
        [Engineered and hosted an enterprise-grade documentation ecosystem],
        [Implemented a single-database multi-tenant separation engine using PostgreSQL Row-Level Security (RLS) and transaction-scoped local parameters (SET LOCAL), enforcing strict data silos across isolated groups.],
        [Designed an atomic asynchronous flush strategy using in-memory GenServer storage buffers, reducing database persistent write transactions by 85% during periods of high user interaction.],
        [Utilized Ecto.Multi atomic chains and Oban transactional background workers to ensure multi-stage backend edits execute completely or roll back safely.],
        [Applied Universal Design and Executive Functioning support models to product UX/UI; established highly structured, low-context asynchronous operational playbooks that minimized cognitive friction for contributors.],
      ),
    ),
  ),
  (
    role: (
      general: "Full-Stack Software Engineer",
      embedded: "Embedded Systems & Integration Engineer",
      enterprise: "Full-Stack ERPNext & Automation Engineer",
    ),
    company: "FARO Africa",
    location: "Cape Town",
    start_date: "Aug 2024",
    end_date: "Nov 2025",
    variant_tags: ("general", "embedded", "enterprise"),
    description: (
      general: (
        [Extended ERPNext using Python/JavaScript to improve workflows, pricing logic, and operational reporting (SQL) \u{2192} reduced manual reporting time and improved data accuracy],
        [Built mobile application in Expo, including NFC (ISO 14443-4 APDUs) for e-paper price tags and card operations \u{2192} enabled real-time price updates with fewer tagging errors],
        [Migrated internal mobile Retool workflows to Expo \u{2192} improved performance and enhanced long-term maintainability],
        [Developed and maintained C\# APIs supporting internal systems.],
        [Provisioned AWS infra with Pulumi and deployed services including Inngest and PayloadCMS.],
        [Diagnosed and resolved issues in a large existing ERPNext installation.],
        [Introduced LLM-assisted development workflows \u{2192} improved debugging speed and code review throughput, enabling faster iteration],
      ),
      embedded: (
        [Designed ISO 14443-4 NFC communication architectures for e-paper display nodes and secure card reader matrices.],
        [Engineered lock-free asynchronous device management services bridging hardware peripherals with application layers.],
        [Built Python-based hardware peripheral simulators to catch edge-case device state corruptions prior to flashing.],
        [Introduced LLM-assisted development workflows to improve debugging speed and code review throughput.],
      ),
      enterprise: (
        [Refactored and extended ERPNext via Python and JavaScript server hooks, optimizing pricing matrices and business intelligence reporting.],
        [Architected migration of internal Retool workflows to React Native/Expo mobile ecosystem, reducing vendor licensing overhead.],
        [Built custom NFC scanner communication utilities within Expo applications for instantaneous physical inventory syncs.],
        [Provisioned AWS infrastructure with Pulumi, deploying Inngest event-driven functions and PayloadCMS.],
        [Diagnosed and resolved issues in a large existing ERPNext installation; introduced LLM-assisted debugging workflows.],
      ),
    ),
  ),
  (
    role: (
      general: "Embedded Software Engineer",
      embedded: "Firmware Engineer (Contract)",
      enterprise: "Enterprise Infrastructure & Tooling Engineer",
    ),
    company: "Ingenics Digital GmbH (through ViVa Outsourcing)",
    location: "Remote Work",
    start_date: "Mar 2023",
    end_date: "May 2024",
    variant_tags: ("general", "embedded", "enterprise"),
    description: (
      general: (
        [Designed an event-driven finite state machine for an I2C-based embedded system using C++ and FreeRTOS \u{2192} created maintainable in-house architecture leading to fewer bugs and quicker development],
        [Developed ESP32 applications using C/C++ and ESP-IDF],
        [Integrated a configurable low-energy BLE stack for device communication],
        [Built Python-based tooling for serial/BLE communication, including client-facing test executables \u{2192} accelerated testing and debugging workflows],
        [Created Python hardware mocks for rapid iteration and early-stage testing \u{2192} enabled faster development cycles with fewer hardware dependencies],
        [Managed fast, reliable data interchange using a compact TinyFrame binary protocol],
        [Implemented asynchronous communication workflows with Python and Pytest],
        [Developed an active object within the QP Real-Time Embedded Framework (with QSPY) to simulate device behaviour],
        [Integrated a configurable BLE stack for device communication and implemented FOTA firmware updates over BLE],
      ),
      embedded: (
        [Architected deterministic finite state machines (FSM) on dual-core ESP32 using FreeRTOS for concurrent sensor arrays.],
        [Developed Cap'n Proto inter-process communication over serial lines, achieving sub-millisecond serialization latency.],
        [Implemented strict compile-time and runtime hardware state guards via rigorous assertions preventing fragmentation.],
      ),
      enterprise: (
        [Built modular Python utility structures and automation scripts for internal configuration schema validation.],
        [Designed data handling pipelines ensuring data transfer consistency across runtime platforms using declarative specifications.],
        [Developed Python hardware mocks enabling faster development cycles with fewer hardware dependencies.],
      ),
    ),
  ),
  (
    role: (
      general: "Software Developer",
      embedded: "Software Developer",
    ),
    company: "UMAN Technologies",
    location: "Century City, Cape Town",
    start_date: "Mar 2021",
    end_date: "Dec 2022",
    variant_tags: ("general", "embedded"),
    description: (
      general: (
        [Creating and maintaining Docker containers for development and CI/CD testing \u{2192} improved development environment consistency],
        [Implementing and testing new services using RPC based on the SOME/IP protocol, as well as using perf to reduce performance bottlenecks],
        [Implementing IPC/RPC in existing C++ programs and Python scripts using Cap'n Proto and pycapnp],
        [Implementing a node tree to expose process-related variables and function calls to the IPC interface],
        [Analysing TCP/UDP traffic with Wireshark],
        [Leading a small team using AGILE development practices, including onboarding and mentoring new software developers],
      ),
      embedded: (
        [Implemented RPC services using SOME/IP protocol and reduced performance bottlenecks with perf.],
        [Built IPC/RPC layers in C++ and Python using Cap'n Proto; designed node trees exposing process variables via IPC interface.],
      ),
    ),
  ),
  (
    role: (
      general: "Junior Lecturer",
      embedded: "Junior Lecturer",
      enterprise: "Junior Lecturer",
    ),
    company: "North-West University",
    location: "Potchefstroom",
    start_date: "Feb 2020",
    end_date: "Dec 2020",
    variant_tags: ("general", "embedded", "enterprise"),
    description: (
      general: (
        [Lecturing Python and C++ programming for Introduction to Programming for first year IT students in both remote and in-person settings],
      ),
      embedded: (
        [Lectured Python and C++ programming for Introduction to Programming for first year IT students.],
      ),
      enterprise: (
        [Lectured Python and C++ programming for Introduction to Programming for first year IT students.],
      ),
    ),
  ),
)

#let _education_entries = (
  (
    degree: "B.Eng. Computer and Electronic Engineering",
    institution: "North-West University",
    location: "Potchefstroom",
    graduation_year: "2020",
    details: (
      general: (
        [Focus on embedded systems, software engineering, and electronic design],
        [Developing an Android app with Kotlin to emulate an ISO 14443 protocol-based NFC payment system],
        [Developing microcontroller logic with C and the STM32 system as well as utilizing STM32CubeMX],
        [Implementing a PID controller with an Arduino to control a DC motor's voltage and speed],
        [Cleaning and analysing data from large spreadsheets with Python and Pandas, utilizing linear regression, correlation and machine learning],
      ),
      embedded: (
        [Focus on embedded systems, software engineering, and electronic design],
        [Developed NFC payment protocol emulator (Kotlin/Android), STM32 firmware (C), and PID motor controller (Arduino)],
      ),
      enterprise: (
        [Focus on embedded systems, software engineering, and electronic design],
        [Developed data analysis pipeline with Python/Pandas (linear regression, ML); built NFC payment emulator (Kotlin/Android)],
      ),
    ),
  ),
)

#let _skill_categories = (
  (category_name: "Systems Architecture", skills: ("Event-driven FSM", "RPC/IPC (Cap'n Proto, SOME/IP)", "State machines", "Node trees"), variant: "general"),
  (category_name: "Testing & Quality", skills: ("Unit testing (Pytest)", "Hardware mocks", "Test executables", "Code coverage analysis"), variant: "general"),
  (category_name: "Development Infrastructure", skills: ("Docker", "CI/CD", "Cloudflare", "Terraform", "Linux", "WSL2"), variant: "general"),
  (category_name: "Agentic Engineering & AI Integration", skills: ("Agentic workflows", "Claude Code", "Spec-Driven TDD", "Prompt Engineering"), variant: "general"),
  (category_name: "Workflow Automation", skills: ("ERPNext", "Python tooling", "Retool \u{2192} Expo migration"), variant: "general"),
  (category_name: "Languages", skills: ("C/C++", "Python", "JavaScript/TypeScript", "SQL", "Elixir"), variant: "general"),
  (category_name: "Embedded Systems", skills: ("ESP32/ESP-IDF", "FreeRTOS", "NimBLE", "QP RTOS", "TinyFrame protocol"), variant: "general"),
  (category_name: "Web Development", skills: ("ReactJS", "AstroJS", "Django REST API", "TailwindCSS", "Phoenix"), variant: "general"),
  (category_name: "Primary", skills: ("C++", "FreeRTOS", "ESP32/ESP-IDF", "NFC APDU (ISO 14443-4)"), variant: "embedded"),
  (category_name: "Secondary", skills: ("NimBLE", "UART/SPI/I2C", "TinyFrame", "Hardware-in-the-Loop (HIL) Testing"), variant: "embedded"),
  (category_name: "Foundational", skills: ("Assembly", "Digital Logic", "System Modeling"), variant: "embedded"),
  (category_name: "Other", skills: ("ERPNext (Integration-focused)", "Expo Mobile"), variant: "embedded"),
  (category_name: "Primary", skills: ("Python", "ERPNext/Frappe Framework", "Expo (React Native)", "Inngest"), variant: "enterprise"),
  (category_name: "Secondary", skills: ("AWS", "Pulumi (IaC)", "PostgreSQL (RLS)", "Docker"), variant: "enterprise"),
  (category_name: "Foundational", skills: ("SQL", "Object-Oriented Design", "Spec-Driven Development"), variant: "enterprise"),
  (category_name: "Other", skills: ("C++", "FreeRTOS (Low-level integration support)"), variant: "enterprise"),
)

#let _project_entries = (
  (
    name: "Divergent Tabletop Wiki",
    description: (
      general: ([Built a community wiki using Astro, Elixir, and Docker for knowledge management], [Documented event frameworks, onboarding processes, and communication best practices], [Created tooling for content management and community operations]),
    ),
    link: none,
    variant_tags: ("general", "embedded", "enterprise"),
  ),
  (
    name: "Ingenics Digital GmbH \u{2014} Event-Driven FSM for Embedded Systems",
    description: (
      general: ([Designed event-driven finite state machine for I2C-based embedded system using C++ and FreeRTOS], [Solved complex state management challenges in real-time embedded environment], [Outcome: Maintainable in-house architecture leading to fewer bugs and quicker development cycles]),
    ),
    link: none,
    variant_tags: ("general", "embedded"),
  ),
  (
    name: "MeepleInn",
    description: (
      general: ([Phoenix/Elixir web application for board game catalogue and event organization], [Comprehensive development tooling: Mise workflow, git hooks for quality checks, automatic migrations, Docker deployment]),
    ),
    link: none,
    variant_tags: ("general",),
  ),
  (
    name: "Divergent Tabletop Commons",
    description: (
      general: ([Elixir LiveView application for community wiki/knowledge base with collaborative editing], [Phoenix LiveView architecture with OTP supervision trees, context isolation, and modular wiki_web components], [CRDT using Y_ex for collaborative editing]),
    ),
    link: none,
    variant_tags: ("general",),
  ),
  (
    name: "Spec-Driven and Test-Driven Agentic Coding",
    description: (
      general: ([SDD framework for Factory Droid and Claude Code to create specification documents], [Prompts crafted with latest research into prompt- and context engineering], [Python script to automate Red-Green-Refactor cycles for tasks], [Working on a Rust-based TUI to have a user-friendly interface]),
    ),
    link: none,
    variant_tags: ("general",),
  ),
)

#let _cover_letter_data = (
  recipient_name: none,
  recipient_title: none,
  company: none,
  date: none,
  about_me: (
    general: [
      I am a software engineer with over 5 years of experience bridging hardware, full-stack development, and resilient system architecture. My approach combines deep technical expertise with a rigorous, AI-augmented methodology\u{2014}utilizing agentic workflows to ship reliable software at high velocity. With a background in Computer and Electronic Engineering (B.Eng.), I don't just write code; I design systems that last, from low-level firmware to cloud-native infrastructures.
    ],
    embedded: [
      I am writing to express my interest in the Senior Systems Engineering position at [Company]. I specialize in engineering deterministic, real-time software architectures (C/C++, FreeRTOS, Elixir/OTP) and secure, spec-driven communication protocols. Throughout my career, my focus has been on eliminating runtime faults and managing high-concurrency systems at the edge and data boundaries.
    ],
    enterprise: [
      I am writing to explore the Enterprise Systems Architect position at [Company]. I bring over 5 years of experience designing robust business automation engines, multi-tenant database infrastructures, and scalable custom extensions within the ERPNext/Frappe ecosystem.
    ],
  ),
  why_me: (
    general: (
      [
        Hard Engineering & System Design: My foundations are in complex, real-time systems. At Ingenics Digital, I designed an event-driven finite state machine for embedded systems using C++ and FreeRTOS, creating a maintainable architecture that reduced bugs and accelerated development cycles. Whether I am working with memory-constrained microcontrollers or distributed cloud services, I prioritize long-term maintainability and architectural integrity.
      ],
      [
        Strategic AI Integration: I treat AI as a powerful force multiplier for my existing engineering skills, applying it where it offers the greatest leverage while remaining fully capable of developing complex systems manually. I use Claude Code for surgical, interactive debugging and Droid by Factory for programmatic automation. This allows me to maintain high code quality and rigour while moving at the pace of a modern, high-impact environment, without incurring technical debt.
      ],
      [
        Full-Stack Versatility & Impact: My technical breadth is grounded in practical delivery. At FARO Africa, I extended ERPNext systems (Python/JS), built mobile features in Expo with NFC integration, and provisioned AWS infrastructure with Pulumi. This versatility is complemented by my "impact over process" philosophy\u{2014}demonstrated by my work founding Divergent Tabletop, where I apply systems thinking to solve real-world community challenges.
      ],
      [
        Resilient Infrastructure: Beyond application code, I am comfortable with the "plumbing" of modern software, including Docker for development and CI/CD. I am currently preparing to open-source my community wiki project, reflecting my commitment to shared knowledge and the Open Source ecosystem.
      ],
    ),
    embedded: (
      [
        Recently, as Principal Systems Architect for the open-source Divergent Tabletop ecosystem, I engineered a high-concurrency real-time wiki engine using Elixir with the y_ex CRDT library. By implementing a dynamic supervision tree and an actor-based memory buffering architecture, I achieved 99.9% fault isolation and reduced per-session memory overhead by 60%.
      ],
    ),
    enterprise: (
      [
        My recent work highlights my ability to transform complex real-world operational challenges into scalable, secure software architectures. As the Principal Systems Architect for the Divergent Tabletop documentation engine, I designed and deployed a single-database multi-tenant architecture utilizing PostgreSQL Row-Level Security (RLS) and transaction-scoped context injection. This strategy, combined with an in-memory transactional flushing architecture, safely reduced database write volumes by 85% under heavy user concurrency. Additionally, my background at FARO Africa includes leading the migration of business workflows from Retool into custom Expo mobile environments, significantly lowering operational latency and eliminating third-party licensing dependencies.
      ],
    ),
  ),
  how_i_work: (
    embedded: [
      I approach software through the lens of Spec-Driven Development (SDD) to ensure code correctness and maintain clear, robust architectures. I am looking forward to bringing this systems-level discipline to [Company]'s engineering team.
    ],
    enterprise: [
      I execute tasks using strict Spec-Driven Development frameworks to deliver highly maintainable codebases that align perfectly with business goals. I am eager to help optimize and scale [Company]'s enterprise core.
    ],
  ),
)

#let cv_data = (
  name: "Werner Bisschoff",
  email: "werner@bisschoff.dev",
  phone: "071 826 2066",
  location: "Cape Town, Western Cape, South Africa",
  position: "Systems Engineer",

  summary: (
    general: [
      Software engineer with 5+ years of experience bridging hardware and full-stack development. I combine technical depth in C++ and Python with a rigorous, agentic engineering methodology. My focus is on resilient system design and productivity-enhancing AI workflows, governed by security, processes, and specification-driven development.
    ],
    embedded: [
      Rigorous Systems Engineer with 5+ years of experience engineering real-time, event-driven software architectures (C/C++, FreeRTOS) and secure, deterministic communication protocols. Specializes in designing robust firmware, high-performance IPC mechanisms, and hardware-in-the-loop simulation frameworks. Governed by strict Spec-Driven Development (SDD) methodologies and automated validation pipelines to eliminate runtime faults in production environments.
    ],
    enterprise: [
      Strategic Enterprise Software Architect with 5+ years of experience engineering robust business automation platforms, custom ERP extensions, and scalable API layers. Expert in the Frappe/ERPNext ecosystem, asynchronous workflow systems, and cross-platform mobile application deployment (Expo/React Native). Proven track record of translating complex real-world operations into scalable, type-safe data schemas governed by strict Spec-Driven Development (SDD) paradigms.
    ],
  ),

  ai_policy: (
    [I treat AI as an agentic partner within a strict engineering framework, moving beyond "vibe-coding" to structured, audit-ready workflows:],
    [Spec-Driven Development (SDD): Prioritize context-heavy specifications to ensure alignment; AI-generated outputs are treated as hypotheses validated by human-led TDD.],
    [Data Security: Enforce mandatory sandboxing for all agentic projects; strictly prohibit credential access and utilize tool-based retrieval for scoped, anonymized data only.],
    [Engineering Rigour: All AI-assisted output undergoes rigorous human-in-the-loop review to ensure it meets enterprise quality and compliance benchmarks.],
    [Privacy by Design: AI workflows are architected to avoid direct database access; sensitive data remains behind scoped, tool-mediated retrieval with no standing credentials exposed to agents.],
  ),

  job_target: [
    Seeking a mid to senior software engineering role (remote preferred, hybrid max. 2 days/week on-site in Cape Town) with emphasis on embedded systems, backend services, or AI-assisted development workflows. Prefers small, focused teams with clear goals and engineering culture. Open to permanent or contract (3+ months) arrangements.
  ],

  experience_entries: _experience_entries,
  experience: _experience_entries,
  education_entries: _education_entries,
  education: _education_entries,
  skill_categories: _skill_categories,
  skills: _skill_categories,
  project_entries: _project_entries,
  cover_letter_data: _cover_letter_data,
)
