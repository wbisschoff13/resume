# Exploration: Job Scraper and Analyzer

---

## [PROBLEM_DEFINITION]
[Statement]: Create a Python-based CLI tool using `uv` and `mise` to scrape job postings from LinkedIn, Indeed, and Google, analyze their fit against a user's CV using AI (`droid exec`), and provide a review interface for job applications.
[Scope]: 
- Scraping from Indeed, LinkedIn, and Google via `JobSpy`.
- Multi-term searches from a text file.
- Geolocation: Remote (South Africa) and Hybrid/Office (Cape Town).
- Handling filter limitations: Intersecting "Remote" and "Past 7 days" searches for sites with mutually exclusive filters.
- Data persistence: SQLite database.
- AI Analysis: Batching (5-10 jobs) and rating fit ("No fit" to "Perfect fit") using `droid exec`.
- Review UI: Interactive CLI to mark jobs as "applied", "declined", or "skip".
[Exclusions]: 
- Automatic job application (only marking status).
- GUI (CLI only).
[Context]: User is a senior software engineer with 5+ years experience in Full-stack, Embedded, and AI workflows, based in Cape Town.

---

## [CONSTITUTIONAL_CONSTRAINTS]
[Constraint_List]:
- [CONST_001]: Use `uv` for Python project management. — Source: User Requirement
- [CONST_002]: Use `mise` for environment management. — Source: User Requirement
- [CONST_003]: Use `JobSpy` for scraping. — Source: User Requirement
- [CONST_004]: Use `droid exec` for AI analysis. — Source: User Requirement
- [CONST_005]: Target Remote SA and Hybrid/Office Cape Town. — Source: User Requirement

---

## [RESEARCH_FINDINGS]

### [CODEBASE_ANALYSIS]
[Existing_Patterns]:
- The project is a new `uv` project.
- CV details are stored in LaTeX format (`cv/*.tex`).
[Technical_Debt]:
- None (greenfield).
[Reusable_Components]:
- LaTeX CV content can be parsed/extracted to provide context for AI analysis.

### [DOMAIN_RESEARCH]
[Industry_Standards]:
- Job scraping often involves handling rate limits and IP blocking (JobSpy supports proxies).
- SQLite is standard for local data persistence in small tools.
[Reference_Implementations]:
- `JobSpy` README provides clear usage for `scrape_jobs`.
[Anti_Patterns]:
- Heavy scraping without delays or proxies (LinkedIn is restrictive).
- Passing too much data per LLM call (batching 5-10 is reasonable).

### [TECHNICAL_FEASIBILITY]
[Tooling]:
- `JobSpy`: Mature library for aggregating Indeed, LinkedIn, Glassdoor, etc.
- `droid exec`: Powerful non-interactive AI agent for data analysis.
- `sqlite3`: Built-in Python library for DB.
- `typer` or `click`: Modern CLI frameworks for Python.
[Integration_Points]:
- `JobSpy` integration via `scrape_jobs` function.
- `droid exec` integration via subprocess calls with CV and JD context.
[Performance_Considerations]:
- `linkedin_fetch_description` is slow as it makes O(n) requests.
- Scraping should be concurrent (JobSpy does this internally for sites, but we might run terms in parallel).
[Security_Implications]:
- Protecting API keys for `droid` (handled by environment variables).

### [FINDINGS_SUMMARY]
- [FIND_001]: Indeed and LinkedIn have mutually exclusive filters. Indeed: `hours_old` vs `is_remote`. LinkedIn: `hours_old` vs `easy_apply`. — Source: JobSpy README/Source — Excerpt: `If hours_old is provided, composite filter for job_type/is_remote is not possible.`
- [FIND_002]: `droid exec` supports non-interactive mode with autonomy levels. — Source: `droid exec --help` — Excerpt: `Execute a single command (non-interactive mode)`
- [FIND_003]: User CV covers Full-stack (Python, JS, C#), Embedded (C++, ESP32), and AI workflows. — Source: `cv/summary.tex`, `cv/skills.tex`

### [KEY_EVIDENCE]
[Evidence_001]:
- [Related_Finding]: [FIND_001]
- [Type]: Code_Snippet
- [Source]: `JobSpy/jobspy/indeed/__init__.py`
- [Content]:
  ```python
  def _build_filters(self):
      # ...
      if self.scraper_input.hours_old:
          # ...
      elif self.scraper_input.job_type or self.scraper_input.is_remote:
          # ...
  ```
- [Why_This_Matters]: Confirms the need for manual intersection of results to get "Past 7 days" + "Remote".

[Evidence_002]:
- [Related_Finding]: [FIND_002]
- [Type]: Documentation_Quote
- [Source]: `droid exec --help`
- [Content]:
  ```
  --auto low                 Low-risk operations
  --auto medium              Development operations
  --auto high                Production operations
  ```
- [Why_This_Matters]: Allows safe execution of analysis prompts without interactive overhead.

---

## [OPTION_ANALYSIS]

### [OPTION_1]
[Overview]: A unified Python CLI tool built with `uv`, `typer`, and `sqlite3`, using `JobSpy` for data acquisition and `droid exec` for analysis.
[Research_Basis]: [FIND_001], [FIND_002], [FIND_003]
[Architecture_Summary]:
- **CLI Layer**: `typer` app with `fetch`, `analyze`, and `review` commands.
- **Persistence Layer**: `sqlite3` database with `jobs` and `search_metadata` tables.
- **Scraper Service**: Wrapper around `JobSpy` that implements the "Intersection Strategy" (Remote search + Recent search).
- **Analysis Service**: Batches jobs, reads CV context, and invokes `droid exec` with a prompt template.
- **Review Service**: Interactive loop to display jobs and update DB status.

[Dependencies]:
- `python-jobspy` — Availability: Stable
- `typer` — Availability: Stable
- `pydantic` (for data validation) — Availability: Stable
- `rich` (for CLI UI) — Availability: Stable

[Pros]:
- Highly modular and verifiable.
- Minimal external dependencies beyond scraping and AI.
- Leverages existing `droid` toolchain.

[Cons]:
- LinkedIn/Indeed scraping may require proxies for reliability.
- Intersecting results increases scraping time.

[Risks]:
- [RISK_001]: Rate limiting by LinkedIn. — Mitigation: Use `linkedin_fetch_description` sparingly or use proxies.
- [RISK_002]: AI analysis cost/token usage. — Mitigation: Use batching and concise prompts.

[Constraint_Fit]:
- [CONST_001]: Compliant — Using `uv`.
- [CONST_002]: Compliant — Using `mise`.
- [CONST_003]: Compliant — Using `JobSpy`.
- [CONST_004]: Compliant — Using `droid exec`.
- [CONST_005]: Compliant — Search logic covers both.

[Complexity]: Medium — Implementing robust scraping logic and AI prompt engineering.
[Time_To_Implement]: Medium — ~2-3 days for a polished tool.
[Operational_Risk]: Low — Local tool, no server-side state.
[Maintainability]: High — Structured Python with clear service boundaries.

---

## [SINGLE_OPTION_JUSTIFICATION]
[Dominance_Evidence]: The user's requirements are very specific regarding the stack (`uv`, `mise`, `JobSpy`, `droid exec`) and the logic (intersection of filters, batching). Option 1 directly maps these requirements into a standard Python CLI architecture.
[Alternatives_Rejected]:
- Using a different scraper: Rejected because `JobSpy` was explicitly requested.
- Using a different AI: Rejected because `droid exec` was explicitly requested.
- Using a simpler JSON file instead of SQLite: Rejected to better handle job status updates and future scalability.

---

## [PRIMARY_RECOMMENDATION]
[Selected_Option]: [OPTION_1]
[Justification]: Directly fulfills all user requirements while providing a robust foundation for future enhancements.
[Tradeoff_Summary]: Complexity of intersection logic is accepted to overcome site-specific filter limitations.
[Residual_Risks]:
- [RISK_001]: Rate limiting — Mitigated by user's expectation of slow `linkedin_fetch_description`.

---

## [DECISION_READINESS]
[PRD_Readiness_Checklist]:
- [x] Problem space fully mapped
- [x] All viable approaches identified and evaluated
- [x] Technical feasibility validated (or risks documented)
- [x] Integration points identified
- [x] Constraints accounted for in all options
- [x] Recommendation supported by evidence

---

## [CLARIFICATION_LOG]
[Questions]:
- [Q_001]:
  - [Question]: Should search terms be provided as a simple line-separated text file?
  - [Status]: Non-Blocking
  - [Impact]: Input format for `fetch` command.
  - [Related_Options]: All
- [Q_002]:
  - [Question]: Does the user already have proxies configured, or should the tool include proxy rotation logic?
  - [Status]: Non-Blocking
  - [Impact]: Reliability of LinkedIn scraping.
  - [Related_Options]: All

---

## [SOURCE_REGISTRY]

| ID | Type | Source | Relevance |
|----|------|--------|-----------|
| [SRC_001] | Documentation | `JobSpy/README.md` | Core scraping library details. |
| [SRC_002] | Tool_Output | `droid exec --help` | AI analysis tool capabilities. |
| [SRC_003] | Codebase_File | `JobSpy/jobspy/indeed/__init__.py` | Confirmation of filter limitations. |
| [SRC_004] | Codebase_File | `W_Bisschoff_CV.tex` | Context for AI analysis. |

---

## [SEMANTIC_ANCHORS]
- `specs/001-job-scraper-analyzer/explore.md`
- `[OPTION_1]`
- `[CONST_001]`, `[CONST_002]`, `[CONST_003]`, `[CONST_004]`, `[CONST_005]`
- `[RISK_001]`, `[RISK_002]`
- `[FIND_001]`, `[FIND_002]`, `[FIND_003]`
- `[Q_001]`, `[Q_002]`
- `[SRC_001]`, `[SRC_002]`, `[SRC_003]`, `[SRC_004]`
- `[Evidence_001]`, `[Evidence_002]`
