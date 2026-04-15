"""CLI entry point for job_scraper_analyzer."""

from pathlib import Path
from typing import List, Optional

import typer
from rich.console import Console
from rich.table import Table

from job_scraper_analyzer import analyzer, cv_parser, database, scraper
from job_scraper_analyzer.models import Analysis, Job

# Default database path
DEFAULT_DB_PATH = Path.home() / ".local" / "share" / "job-scraper-analyzer" / "jobs.db"

app = typer.Typer(
    name="job-scraper-analyzer",
    help="Job Scraper Analyzer with AI fit rating",
)
console = Console()


def _ensure_db_path(db_path: Optional[Path] = None) -> Path:
    """Ensure database path exists, create parent directories if needed."""
    if db_path is None:
        db_path = DEFAULT_DB_PATH
    db_path.parent.mkdir(parents=True, exist_ok=True)
    return db_path


@app.command()
def fetch(
    search_terms_file: str = typer.Option(..., "--search-terms", help="Path to search terms file"),
    location: str = typer.Option("Remote", "--location", help="Job location"),
    is_remote: bool = typer.Option(True, "--remote/--no-remote", help="Remote job filter"),
    hours_old: int = typer.Option(168, "--hours-old", help="Jobs from last N hours"),
    db_path: Optional[Path] = typer.Option(None, "--db", help="Database path"),
) -> None:
    """Fetch jobs from job boards."""
    db_path = _ensure_db_path(db_path)
    
    # Initialize database
    database.init_db(db_path)
    
    # Read search terms file
    search_terms_path = Path(search_terms_file)
    if not search_terms_path.exists():
        typer.echo(f"Error: Search terms file not found: {search_terms_file}")
        raise typer.Exit(1)
    
    search_terms = search_terms_path.read_text().strip().split("\n")
    search_terms = [term.strip() for term in search_terms if term.strip()]
    
    if not search_terms:
        typer.echo("No search terms found in file.")
        return
    
    # Scrape jobs with all search terms combined (single scrape call)
    # The scraper will iterate through sites internally
    all_jobs: List[Job] = []
    seen_urls: set = set()  # Deduplicate by job_url
    for term in search_terms:
        typer.echo(f"Fetching jobs for: {term} in {location}...")
        
        # Scrape jobs from all sites
        jobs = scraper.scrape_sites(term, location, is_remote, hours_old)
        
        # Only add jobs we haven't seen (deduplicate by URL)
        for job in jobs:
            if job.job_url not in seen_urls:
                all_jobs.append(job)
                seen_urls.add(job.job_url)
        
        typer.echo(f"  Found {len(jobs)} jobs for '{term}'")
    
    # Store all jobs (one scrape call per term, upsert per job)
    for job in all_jobs:
        database.upsert_job(job, db_path)
    
    typer.echo(f"Total: {len(all_jobs)} jobs fetched and stored.")


@app.command()
def analyze(
    batch_size: int = typer.Option(5, "--batch-size", help="Jobs per analysis batch"),
    cv_path: str = typer.Option("W_Bisschoff_CV.tex", "--cv", help="Path to CV file"),
    db_path: Optional[Path] = typer.Option(None, "--db", help="Database path"),
) -> None:
    """Analyze jobs with AI fit rating."""
    db_path = _ensure_db_path(db_path)
    
    # Parse CV for summary
    cv_file = Path(cv_path)
    if cv_file.exists():
        cv_text = cv_parser.parse_latex_file(cv_file)
        cv_summary = cv_parser.extract_cv_summary(cv_text)
    else:
        cv_summary = "Senior Software Engineer with experience in Python, Full-stack development, and AI/ML."
        typer.echo(f"CV file not found at {cv_path}, using default summary.")
    
    # Load jobs needing analysis
    jobs = database.get_jobs_needing_analysis(limit=batch_size, db_path=db_path)
    
    if not jobs:
        typer.echo("No jobs to analyze.")
        return
    
    typer.echo(f"Analyzing {len(jobs)} jobs with batch size: {batch_size}")
    
    # Analyze jobs
    analyses = analyzer.analyze_jobs(jobs, cv_summary, batch_size=batch_size, db_path=db_path)
    
    typer.echo(f"Analysis complete. {len(analyses)} jobs analyzed.")


@app.command()
def review(
    db_path: Optional[Path] = typer.Option(None, "--db", help="Database path"),
) -> None:
    """Review and manage job analysis results."""
    db_path = _ensure_db_path(db_path)
    
    # Load all jobs
    jobs = database.get_jobs_by_status(status="new", db_path=db_path)
    
    if not jobs:
        console.print("[yellow]No jobs to review.[/yellow]")
        return
    
    # Create Rich table for display
    table = Table(title="Job Applications")
    table.add_column("ID", style="cyan", width=3)
    table.add_column("Title", style="green")
    table.add_column("Company", style="yellow")
    table.add_column("Location", style="blue")
    table.add_column("Fit", style="magenta", width=4)
    table.add_column("Status", style="white")
    
    for i, job in enumerate(jobs, 1):
        fit_display = str(job.fit_rating) if job.fit_rating else "-"
        table.add_row(
            str(i),
            job.title or "N/A",
            job.company or "N/A",
            job.location or "N/A",
            fit_display,
            job.status,
        )
    
    console.print(table)
    console.print("\n[cyan]Controls:[/cyan] a=applied, d=declined, s=skip, q=quit")
    console.print("[dim]Use arrow keys to navigate, Enter to select action.[/dim]")


if __name__ == "__main__":
    app()
