# Implementation Tasks: jobspy

## [PHASE_1]: Project Bootstrap
[Phase_Goal]: Initialize `uv` project with mise environment and minimal dependencies

### [TASKS]
- [x] [T001] Initialize uv project with mise environment and minimal dependencies
  - [Task_Type]: Infra_Batch
  - [Execution_Mode]: IMMEDIATE
  - [Verification]: `cd job_scraper_analyzer && uv run python -c "import job_scraper_analyzer; print('OK')"`
  - [Estimated_Time]: 30 minutes
  - [Risk_Level]: low
  - [Effort]: S
  - [Files_Touched]:
    - job_scraper_analyzer/pyproject.toml
    - job_scraper_analyzer/.mise.toml
    - job_scraper_analyzer/src/job_scraper_analyzer/__init__.py
    - job_scraper_analyzer/src/job_scraper_analyzer/__main__.py
  - [Task_Details]:
    - [SETUP] Create pyproject.toml with uv build backend, dependencies: typer, pydantic, rich, jobspy
    - [SETUP] Create .mise.toml with python 3.10+ environment
    - [SETUP] Create src/job_scraper_analyzer/__init__.py with __version__ and package exports
    - [SETUP] Create src/job_scraper_analyzer/__main__.py with typer CLI app skeleton
    - [SETUP] Add JobSpy as submodule reference and src-based import structure
    - [ACCEPTANCE] Package imports successfully, `uv run python -c 'import job_scraper_analyzer'` returns OK

---

## [PHASE_2]: Database Layer
[Phase_Goal]: Implement SQLite schema and CRUD operations

### [TASKS]
- [x] [T002] Implement Pydantic models for Job, Search, and Analysis entities
  - [Task_Type]: Domain_Batch
  - [Execution_Mode]: TDD
  - [Test_Strategy]: Sociable_Unit
  - [Verification]: `cd job_scraper_analyzer && uv run pytest tests/unit/test_models.py -v`
  - [Estimated_Time]: 45 minutes
  - [Risk_Level]: low
  - [Effort]: S
  - [Files_Touched]:
    - job_scraper_analyzer/src/job_scraper_analyzer/models.py
    - job_scraper_analyzer/tests/unit/test_models.py
  - [Task_Details]:
    - [RED] Write failing test: `test_job_model_validates_required_fields()` with assertion that missing job_url raises ValidationError
    - [RED] Write failing test: `test_job_model_default_status_is_new()` with assertion that status defaults to 'new'
    - [GREEN] Implement Job model with Pydantic BaseModel matching data-model.md schema
    - [GREEN] Implement Search model with all filter parameters
    - [GREEN] Implement Analysis model linking job_id to fit_rating and justification
    - [REFACTOR] Add field validators for URL format, enum constraints on site/status/fit_rating
    - [EDGE_CASES] Handle optional fields with None defaults, salary intervals, date parsing
    - [ACCEPTANCE] All model tests pass, Pydantic validation works for all enum constraints

- [x] [T003] Implement SQLite database layer with CRUD operations
  - [Task_Type]: Domain_Batch
  - [Execution_Mode]: TDD
  - [Test_Strategy]: Sociable_Unit
  - [Verification]: `cd job_scraper_analyzer && uv run pytest tests/unit/test_database.py -v`
  - [Estimated_Time]: 60 minutes
  - [Dependency]: T002
  - [Risk_Level]: medium
  - [Effort]: M
  - [Files_Touched]:
    - job_scraper_analyzer/src/job_scraper_analyzer/database.py
    - job_scraper_analyzer/tests/unit/test_database.py
  - [Task_Details]:
    - [RED] Write failing test: `test_database_creates_jobs_table()` with assertion that table exists after init_db()
    - [RED] Write failing test: `test_upsert_job_inserts_new_job()` with assertion that job appears in database
    - [RED] Write failing test: `test_upsert_job_updates_existing_job()` with assertion that duplicate job_url updates instead of inserts
    - [GREEN] Implement init_db() creating tables: jobs, searches, analyses with indexes per data-model.md
    - [GREEN] Implement upsert_job(job: Job) -> int inserting or updating on job_url UNIQUE constraint
    - [GREEN] Implement get_jobs_by_status(status: str) -> List[Job] query with status filter
    - [GREEN] Implement get_jobs_needing_analysis(limit: int) -> List[Job] returning unanalyzed jobs
    - [REFACTOR] Use context manager for sqlite3.Connection, extract SQL to constants
    - [EDGE_CASES] Handle database locked errors with retry, malformed dates gracefully
    - [ACCEPTANCE] Database tests pass, jobs persist across connection cycles

---

## [PHASE_3]: Scraper Service
[Phase_Goal]: Implement JobSpy wrapper with intersection strategy for filter limitations

### [TASKS]
- [x] [T005] Implement JobSpy scraper wrapper with intersection strategy for filter limitations
  - [Task_Type]: Feature_Batch
  - [Execution_Mode]: TDD
  - [Test_Strategy]: Sociable_Unit
  - [Verification]: `cd job_scraper_analyzer && uv run pytest tests/unit/test_scraper.py -v`
  - [Estimated_Time]: 90 minutes
  - [Dependency]: T003
  - [Risk_Level]: high
  - [Effort]: L
  - [Files_Touched]:
    - job_scraper_analyzer/src/job_scraper_analyzer/scraper.py
    - job_scraper_analyzer/tests/unit/test_scraper.py
  - [Task_Details]:
    - [RED] Write failing test: `test_scrape_sites_returns_job_list()` with mock JobSpy returning sample DataFrame
    - [RED] Write failing test: `test_intersection_strategy_merges_results()` with two search variants and deduplication assertion
    - [GREEN] Implement scrape_jobs(search_term: str, location: str, is_remote: bool, hours_old: int) -> List[Job] calling JobSpy
    - [GREEN] Implement intersection_strategy(term: str, location: str) -> List[Job] executing multiple queries and merging
    - [GREEN] Implement _convert_jobspy_row(row: dict) -> Job mapping JobSpy DataFrame columns to Job model
    - [REFACTOR] Extract site-specific filter logic to _build_indeed_params, _build_linkedin_params helpers
    - [EDGE_CASES] Handle rate limiting (add delays), empty results, JobSpy exceptions gracefully
    - [ACCEPTANCE] Scraper tests pass, intersection strategy merges Remote SA and Past 7 days correctly

---

## [PHASE_4]: CV Parser
[Phase_Goal]: Extract plain text from LaTeX CV files for AI context

### [TASKS]
- [/] [T004] Implement LaTeX CV parser to extract plain text for AI context
  - [Task_Type]: Feature_Batch
  - [Execution_Mode]: TDD
  - [Test_Strategy]: Sociable_Unit
  - [Verification]: `cd job_scraper_analyzer && uv run pytest tests/unit/test_cv_parser.py -v`
  - [Estimated_Time]: 45 minutes
  - [Dependency]: T001
  - [Risk_Level]: low
  - [Effort]: S
  - [Files_Touched]:
    - job_scraper_analyzer/src/job_scraper_analyzer/cv_parser.py
    - job_scraper_analyzer/tests/unit/test_cv_parser.py
  - [Task_Details]:
    - [RED] Write failing test: `test_parse_latex_file_extracts_text()` with assertion that plain text is extracted from sample.tex
    - [RED] Write failing test: `test_parse_cv_directory_returns_combined_text()` with assertion that multiple files combine correctly
    - [GREEN] Implement parse_latex_file(file_path: Path) -> str stripping LaTeX commands, extracting text
    - [GREEN] Implement parse_cv_directory(cv_dir: Path) -> str combining summary, skills, experience, education sections
    - [GREEN] Implement extract_cv_summary(text: str, max_length: int = 500) -> str truncating to fit AI prompt limits
    - [REFACTOR] Use regex to strip common LaTeX commands: \section{}, \textbf{}, \href{}, etc.
    - [EDGE_CASES] Handle missing files gracefully, encoding issues, empty sections
    - [ACCEPTANCE] CV parser tests pass, extracts human-readable text from W_Bisschoff_CV.tex structure

---

## [PHASE_5]: Analyzer Service
[Phase_Goal]: Batch jobs and invoke `droid exec` for fit rating

### [TASKS]
- [ ] [T006] Implement droid exec AI analyzer for batch job fit rating
  - [Task_Type]: Feature_Batch
  - [Execution_Mode]: TDD
  - [Test_Strategy]: Sociable_Unit
  - [Verification]: `cd job_scraper_analyzer && uv run pytest tests/unit/test_analyzer.py -v`
  - [Estimated_Time]: 60 minutes
  - [Dependency]: T003,T004
  - [Risk_Level]: medium
  - [Effort]: M
  - [Files_Touched]:
    - job_scraper_analyzer/src/job_scraper_analyzer/analyzer.py
    - job_scraper_analyzer/tests/unit/test_analyzer.py
  - [Task_Details]:
    - [RED] Write failing test: `test_analyze_jobs_batch_calls_droid_exec()` with mock subprocess assertion
    - [RED] Write failing test: `test_parse_fit_rating_from_response()` with sample AI response parsing assertion
    - [GREEN] Implement analyze_jobs(jobs: List[Job], cv_summary: str, batch_size: int = 5) -> List[Analysis] calling droid exec
    - [GREEN] Implement _build_analysis_prompt(job: Job, cv_summary: str) -> str creating prompt per research.md template
    - [GREEN] Implement _parse_droid_response(response: str) -> Tuple[int, str] extracting fit_rating (1-4) and justification
    - [REFACTOR] Add retry logic for droid exec failures, batch_id tracking for analysis audits
    - [EDGE_CASES] Handle malformed AI responses, droid not installed, rate limiting from AI service
    - [ACCEPTANCE] Analyzer tests pass, batch size of 5-10 jobs per droid exec invocation works

---

## [PHASE_6]: CLI Application
[Phase_Goal]: Implement `fetch`, `analyze`, and `review` commands with interactive UI

### [TASKS]
- [ ] [T007] Implement CLI application with fetch, analyze, and review commands
  - [Task_Type]: Feature_Batch
  - [Execution_Mode]: TDD
  - [Test_Strategy]: Integration
  - [Verification]: `cd job_scraper_analyzer && uv run pytest tests/integration/test_cli.py -v`
  - [Estimated_Time]: 75 minutes
  - [Dependency]: T005,T006
  - [Risk_Level]: medium
  - [Effort]: M
  - [Files_Touched]:
    - job_scraper_analyzer/src/job_scraper_analyzer/cli.py
    - job_scraper_analyzer/tests/integration/test_cli.py
  - [Task_Details]:
    - [RED] Write failing test: `test_fetch_command_scrapes_and_stores()` with ClickRunner invoking CLI
    - [RED] Write failing test: `test_review_command_displays_interactive_ui()` with assertion that rich table renders
    - [GREEN] Implement fetch command: reads search terms file, calls scraper, stores to DB
    - [GREEN] Implement analyze command: loads unanalyzed jobs, calls analyzer, updates DB with fit ratings
    - [GREEN] Implement review command: interactive CLI with Rich table, keyboard navigation, status updates
    - [REFACTOR] Use typer.App with subcommands, add --verbose flag, --search-terms-file option
    - [EDGE_CASES] Handle empty search terms, no jobs to analyze, keyboard interrupts in review mode
    - [ACCEPTANCE] CLI tests pass, all three commands functional with proper error handling

---

## [PHASE_7]: Integration Test
[Phase_Goal]: End-to-end test of fetch → analyze → review flow

### [TASKS]
- [ ] [T008] Implement end-to-end integration test for fetch → analyze → review flow
  - [Task_Type]: Feature_Batch
  - [Execution_Mode]: IMMEDIATE
  - [Verification]: `cd job_scraper_analyzer && uv run pytest tests/integration/test_e2e.py -v`
  - [Estimated_Time]: 45 minutes
  - [Dependency]: T007
  - [Risk_Level]: low
  - [Effort]: S
  - [Files_Touched]:
    - job_scraper_analyzer/tests/integration/test_e2e.py
  - [Task_Details]:
    - [SETUP] Create test fixtures for search terms file and mock JobSpy responses
    - [EXECUTE] Run full pipeline: fetch → analyze → review with mocked dependencies
    - [ASSERT] Verify jobs exist in DB after fetch, fit_ratings populated after analyze, status changes after review
    - [EDGE_CASES] Test with empty database, single job, batch boundary conditions
    - [ACCEPTANCE] E2E test passes, full pipeline functional with test doubles

---

## [IMPLEMENTATION_STRATEGY]
[Execution_Order]: T001 → T002 → T003 → T004 → T005 → T006 → T007 → T008

[Critical_Dependency_Chains]:
- T003 (Database) must precede T005 (Scraper) which stores to DB
- T003 (Database) must precede T006 (Analyzer) which stores results
- T004 (CV Parser) should complete before T006 (Analyzer) since analyzer needs CV context
- T007 (CLI) depends on all prior phases

[Risk_Hotspots]:
- [RISK_001]: LinkedIn rate limiting — Mitigation: Use `--auto low` for droid, add delays between scrapes
- [RISK_002]: Filter mutual exclusivity — Mitigation: Intersection strategy implemented in scraper.py
- [RISK_003]: `droid exec` token usage — Mitigation: Batch sizes of 5-10 jobs

[Merge_Conflict_Boundaries]:
- No merge conflicts expected (single developer)

[NEXT_ACTION]:
Run `/spec.cycle` to start the TDD implementation cycle.