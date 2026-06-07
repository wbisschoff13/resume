#let _experience_entries = (
  (
    role: (
      general: "Founder and Host",
      systems: "Principal Systems Architect",
      infrastructure: "Principal Systems Architect",
    ),
    company: "Divergent Tabletop",
    location: "Cape Town",
    start_date: "Jul 2025",
    end_date: none,
    variant_tags: ("general", "systems", "infrastructure"),
    description: (
      general: (
        [Founded neurodivergent-focused peer community; manage event operations and WhatsApp-based community platform.],
        [Applied systems thinking to solve community management challenges through software solutions.],
      ),
      systems: (
        [Engineered a distributed real-time data engine utilizing Elixir/OTP and conflict-free replicated data types (CRDT models). Deployed in-memory GenServer storage buffers with threshold-based flush mechanics, reducing direct database write transactions by approximately 85% under sustained edit workloads.],
        [Integrated a Rust-backed CRDT synchronization layer (y_ex) using actor-based concurrency, achieving sub-50ms convergence latency across distributed editing sessions through deterministic state reconciliation and binary delta serialization.],
        [Designed a dynamic BEAM supervision tree with one_for_one isolation, encapsulating each page editing session in its own process subtree to prevent cascading failures and guarantee per-session state integrity.],
      ),
      infrastructure: (
        [Implemented a single-database multi-tenant separation engine using PostgreSQL Row-Level Security (RLS) and transaction-scoped local parameters (SET LOCAL), enforcing strict data silos across isolated groups.],
        [Designed an atomic asynchronous flush strategy using in-memory GenServer storage buffers, reducing database persistent write transactions by 85% during periods of high user interaction.],
        [Utilized Ecto.Multi atomic chains and Oban transactional background workers to ensure multi-stage backend edits (e.g., structural document renaming and incoming backlink indexing) execute completely or roll back safely.],
      ),
    ),
  ),
  (
    role: (
      general: "Full-Stack Software Engineer",
      systems: "Embedded Systems & Integration Engineer",
      infrastructure: "Full-Stack ERPNext & Automation Engineer",
    ),
    company: "FARO Africa",
    location: "Cape Town",
    start_date: "Aug 2024",
    end_date: "Nov 2025",
    variant_tags: ("general", "systems", "infrastructure"),
    description: (
      general: (
        [Extended ERPNext using Python/JavaScript to improve workflows, pricing logic, and operational reporting (SQL) → reduced manual reporting time and improved data accuracy.],
        [Built mobile application in Expo, including NFC (ISO 14443-4 APDUs) for e-paper price tags and card operations → enabled real-time price updates with fewer tagging errors.],
        [Migrated internal mobile Retool workflows to Expo → improved performance and enhanced long-term maintainability.],
        [Provisioned AWS infrastructure with Pulumi; deployed Inngest and PayloadCMS services.],
        [Diagnosed and resolved issues in a large existing ERPNext installation.],
        [Introduced LLM-assisted development workflows → improved debugging speed and code review throughput, enabling faster iteration.],
      ),
      systems: (
        [Designed ISO 14443-4 NFC communication architectures for e-paper display nodes and secure card reader matrices.],
        [Engineered lock-free asynchronous device management services bridging hardware peripherals with application layers.],
        [Built Python-based hardware peripheral simulators to catch edge-case device state corruptions prior to flashing.],
        [Introduced LLM-assisted development workflows to improve debugging speed and code review throughput.],
      ),
      infrastructure: (
        [Refactored and extended ERPNext via Python and JavaScript server hooks, optimizing pricing matrices and BI reporting.],
        [Architected migration of internal Retool workflows to Expo/React Native, reducing vendor licensing overhead.],
        [Provisioned and maintained a secure virtualized Linux infrastructure environment using Docker Compose for container isolation and writing custom backup and monitoring scripts.],
        [Diagnosed and resolved issues in a large existing ERPNext installation; introduced LLM-assisted debugging workflows.],
      ),
    ),
  ),
  (
    role: (
      general: "Embedded Software Engineer",
      systems: "Firmware Engineer (Contract)",
      infrastructure: "Enterprise Infrastructure & Tooling Engineer",
    ),
    company: "Ingenics Digital GmbH (through ViVa Outsourcing)",
    location: "Remote",
    start_date: "Mar 2023",
    end_date: "May 2024",
    variant_tags: ("general", "systems", "infrastructure"),
    description: (
      general: (
        [Designed event-driven FSM for I2C-based embedded system (C++/FreeRTOS) → maintainable architecture, fewer bugs.],
        [Developed ESP32 applications (C/C++, ESP-IDF) with configurable BLE stack, TinyFrame protocol, and FOTA updates.],
        [Built Python tooling for serial/BLE communication, hardware mocks, and pytest async workflows → accelerated testing.],
        [Developed active object within QP Real-Time Embedded Framework (QSPY) to simulate device behaviour.],
      ),
      systems: (
        [Architected deterministic FSMs on dual-core ESP32 using FreeRTOS for concurrent sensor arrays.],
        [Developed Cap'n Proto IPC over serial lines, achieving sub-millisecond serialization latency.],
      ),
      infrastructure: (
        [Designed data handling pipelines ensuring data transfer consistency across runtime platforms using declarative specifications.],
        [Developed Python hardware mocks enabling faster development cycles with fewer hardware dependencies.],
      ),
    ),
  ),
  (
    role: (
      general: "Software Developer",
      systems: "Software Developer",
      infrastructure: "Infrastructure & Tooling Developer",
    ),
    company: "UMAN Technologies",
    location: "Cape Town",
    start_date: "Mar 2021",
    end_date: "Dec 2022",
    variant_tags: ("general", "systems", "infrastructure"),
    description: (
      general: (
        [Implemented SOME/IP RPC services; optimized performance bottlenecks with perf.],
        [Built IPC/RPC layers (C++/Python) using Cap'n Proto; led small team using Agile practices.],
      ),
      systems: (
        [Used perf profiling and flamegraphs to trace a performance bottleneck to JSON serialization and verbose logging in a SOME/IP request handling loop. Eliminated unnecessary logging via config toggle reducing latency by approximately 80%, then drove an architecture redesign to phase out JSON entirely.],
        [Sole owner of an IPC service layer — studied existing node schema, designed node structures and data contracts, and implemented the communication layer enabling the frontend to consume the service.],
        [Built Python-based SOME/IP hardware mocks simulating request/response behavior; integrated into CI so automated tests ran without physical hardware.],
      ),
      infrastructure: (
        [Proactively created a Docker development container replicating the exact hardware environment — including VLAN and networking configuration — reducing setup time from hours to under an hour and enabling remote teams to develop without physical hardware.],
      ),
    ),
  ),
  (
    role: (
      general: "Junior Lecturer",
      systems: "Junior Lecturer",
      infrastructure: "Junior Lecturer",
    ),
    company: "North-West University",
    location: "Potchefstroom",
    start_date: "Feb 2020",
    end_date: "Dec 2020",
    variant_tags: ("general",),
    description: (
      general: (
        [Lectured Python and C++ programming for Introduction to Programming for first year IT students in both remote and in-person settings.],
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
        [NFC payment emulator (Kotlin/Android), STM32 firmware (C), PID motor controller (Arduino)],
        [Data analysis with Python/pandas using linear regression, correlation and machine learning],
      ),
      systems: (
        [Focus on embedded systems, software engineering, and electronic design],
        [Developed NFC payment protocol emulator (Kotlin/Android), STM32 firmware (C), PID motor controller (Arduino)],
      ),
      infrastructure: (
        [Focus on embedded systems, software engineering, and electronic design],
        [Developed data analysis pipeline with Python/pandas (linear regression, ML); built NFC payment emulator (Kotlin/Android)],
      ),
    ),
  ),
)

#let _skill_categories = (
  (category_name: "Primary", skills: ("C/C++", "Python", "FreeRTOS", "ESP32/ESP-IDF", "NFC APDU (ISO 14443-4)"), variant: "general"),
  (category_name: "Secondary", skills: ("NimBLE", "UART/SPI/I2C", "TinyFrame", "BLE", "Hardware-in-the-Loop Testing"), variant: "general"),
  (category_name: "Foundational", skills: ("SQL", "Docker", "CI/CD", "Git", "Linux"), variant: "general"),
  (category_name: "Other", skills: ("React", "Phoenix", "AWS", "Pulumi", "ERPNext"), variant: "general"),
  (category_name: "Primary Competencies", skills: ("C", "C++", "FreeRTOS", "ESP32/ESP-IDF", "NFC APDU (ISO 14443-4)"), variant: "systems"),
  (category_name: "Secondary Competencies", skills: ("NimBLE", "Bare-Metal Runtimes", "UART/SPI/I2C", "Hardware-in-the-Loop (HIL) Testing"), variant: "systems"),
  (category_name: "Foundational Systems", skills: ("Linux IPC", "Bash", "Python (pytest, Custom Automation Frameworks)", "Assembly", "System Modeling"), variant: "systems"),
  (category_name: "Cross-Domain Integration", skills: ("ERPNext (Integration-focused)", "Docker", "Spec-Driven Development (SDD)"), variant: "systems"),
  (category_name: "Primary Competencies", skills: ("Python", "Docker", "Docker Compose", "AWS (Solutions Architect – In Progress)", "PostgreSQL (Row-Level Security, Index Tuning, Connection Pooling)"), variant: "infrastructure"),
  (category_name: "Secondary Platforms", skills: ("ERPNext/Frappe Framework", "Elixir/OTP", "Asynchronous Workflow Engines (Inngest, Oban)"), variant: "infrastructure"),
  (category_name: "Data Layer Infrastructure", skills: ("SQL", "Ecto.Multi"), variant: "infrastructure"),
  (category_name: "Systems & Automation", skills: ("Pulumi (IaC)", "Linux Systems Administration", "CI/CD Pipelines", "Bash Scripting", "Network Proxies", "SSH Networking", "Spec-Driven Development (SDD)"), variant: "infrastructure"),

)

#let _project_entries = (
  (
    name: "Divergent Tabletop Wiki",
    description: (
      general: ([Built a community wiki using Astro, Elixir, and Docker for knowledge management], [Documented event frameworks, onboarding processes, and communication best practices], [Created tooling for content management and community operations]),
    ),
    link: none,
    variant_tags: ("general", "systems", "infrastructure"),
  ),
  (
    name: "Ingenics Digital GmbH \u{2014} Event-Driven FSM for Embedded Systems",
    description: (
      general: ([Designed event-driven finite state machine for I2C-based embedded system using C++ and FreeRTOS], [Solved complex state management challenges in real-time embedded environment], [Outcome: Maintainable in-house architecture leading to fewer bugs and quicker development cycles]),
    ),
    link: none,
    variant_tags: ("general", "systems"),
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
    systems: [
      I am writing to express my interest in the Senior Systems Engineering position at [Company]. I specialize in engineering deterministic, real-time software architectures (C/C++, FreeRTOS, Elixir/OTP) and secure, spec-driven communication protocols. Throughout my career, my focus has been on eliminating runtime faults and managing high-concurrency systems at the edge and data boundaries.
    ],
    infrastructure: [
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
    systems: (
      [
        Recently, as Principal Systems Architect for the open-source Divergent Tabletop ecosystem, I engineered a high-concurrency real-time wiki engine using Elixir with the y_ex CRDT library. By implementing a dynamic supervision tree and an actor-based memory buffering architecture, I achieved 99.9% fault isolation and reduced per-session memory overhead by 60%.
      ],
    ),
    infrastructure: (
      [
        My recent work highlights my ability to transform complex real-world operational challenges into scalable, secure software architectures. As the Principal Systems Architect for the Divergent Tabletop documentation engine, I designed and deployed a single-database multi-tenant architecture utilizing PostgreSQL Row-Level Security (RLS) and transaction-scoped context injection. This strategy, combined with an in-memory transactional flushing architecture, safely reduced database write volumes by 85% under heavy user concurrency. Additionally, my background at FARO Africa includes leading the migration of business workflows from Retool into custom Expo mobile environments, significantly lowering operational latency and eliminating third-party licensing dependencies.
      ],
    ),
  ),
  how_i_work: (
    systems: [
      I approach software through the lens of Spec-Driven Development (SDD) to ensure code correctness and maintain clear, robust architectures. I am looking forward to bringing this systems-level discipline to [Company]'s engineering team.
    ],
    infrastructure: [
      I execute tasks using strict Spec-Driven Development frameworks to deliver highly maintainable codebases that align perfectly with business goals. I am eager to help optimize and scale [Company]'s enterprise core.
    ],
  ),
)

#let cv_data = (
  name: "Werner Bisschoff",
  email: "werner@bisschoff.dev",
  phone: "071 826 2066",
  location: "Cape Town, Western Cape, South Africa",
  github: "wbisschoff13",
  website: "https://werner.bisschoff.dev",
  linkedin: "wbisschoff13",
  position: (
    general: "Software Engineer",
    systems: "Hybrid Edge/Systems Engineer",
    infrastructure: "Cloud Infrastructure Engineer / Platform Developer",
  ),

  summary: (
    general: [
      Software engineer with 5+ years of experience bridging hardware and full-stack development. I combine technical depth in C++ and Python with a rigorous, agentic engineering methodology. My focus is on resilient system design and productivity-enhancing AI workflows, governed by security, processes, and specification-driven development.
    ],
    systems: [
      Hybrid Edge/Systems Engineer with 5+ years of experience architecting end-to-end telemetry systems spanning edge compute to backend integration. Specializes in C/C++ and FreeRTOS for deterministic real-time scheduling, Python for automation and hardware-in-the-loop validation, and Elixir/OTP for distributed platform infrastructure.
    ],
    infrastructure: [
      Cloud Infrastructure Engineer / Platform Developer with 5+ years of experience designing high-availability infrastructure across Linux systems administration, Docker containerization, and Pulumi infrastructure-as-code. Proven track record in PostgreSQL performance tuning, multi-tenant data isolation, and building resilient automation and deployment pipelines.
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

  certification: "AWS Certified Solutions Architect – Associate (In Progress — Target: 6 Weeks)",

  experience: _experience_entries,
  education: _education_entries,
  skills: _skill_categories,
  cover_letter_data: _cover_letter_data,
)
