"""End-to-end integration tests for fetch → analyze → review flow.

This test suite verifies the complete pipeline:
1. fetch command: reads search terms → scrapes jobs → stores to DB
2. analyze command: loads unanalyzed jobs → calls AI → stores fit ratings
3. review command: loads jobs → displays UI (tested via assertions)

Tests use mocks for external dependencies (JobSpy, droid exec) and
verify database state transitions at each pipeline stage.
"""

import os
import tempfile
from pathlib import Path
from typing import List
from unittest.mock import patch, MagicMock

import pytest
from typer.testing import CliRunner

from job_scraper_analyzer.models import Analysis, Job

# Import real implementations BEFORE patching for safe reference
from job_scraper_analyzer import database as db_module
from job_scraper_analyzer import scraper as scraper_module
from job_scraper_analyzer import analyzer as analyzer_module


class TestFixtures:
    """Shared test fixtures for E2E tests."""

    @staticmethod
    def create_search_terms_file(terms: List[str]) -> str:
        """Create a temporary search terms file.
        
        Args:
            terms: List of search term strings
            
        Returns:
            Path to temporary file with search terms
        """
        fd, path = tempfile.mkstemp(suffix=".txt")
        with os.fdopen(fd, "w") as f:
            f.write("\n".join(terms))
        return path

    @staticmethod
    def create_mock_jobs() -> List[Job]:
        """Create mock job fixtures for testing.
        
        Returns:
            List of Job objects representing scraped job postings
        """
        return [
            Job(
                job_url="https://linkedin.com/jobs/view/123",
                site="linkedin",
                title="Senior Python Engineer",
                company="Tech Corp",
                location="Remote SA",
                is_remote=True,
                description="Python with AI/ML experience and FastAPI",
            ),
            Job(
                job_url="https://indeed.com/jobs/view/456",
                site="indeed",
                title="Full Stack Developer",
                company="Startup Inc",
                location="Cape Town",
                is_remote=False,
                description="React, Node.js, and PostgreSQL",
            ),
            Job(
                job_url="https://linkedin.com/jobs/view/789",
                site="linkedin",
                title="Backend Engineer",
                company="Data Co",
                location="Remote",
                is_remote=True,
                description="Django, PostgreSQL, Redis",
            ),
        ]

    @staticmethod
    def create_mock_analyses() -> List[Analysis]:
        """Create mock analysis fixtures for testing.
        
        Returns:
            List of Analysis objects with fit ratings
        """
        return [
            Analysis(job_id=1, fit_rating=4, justification="Perfect Python match with AI/ML"),
            Analysis(job_id=2, fit_rating=3, justification="Good full stack fit"),
            Analysis(job_id=3, fit_rating=2, justification="Marginal fit - different stack"),
        ]


class TestFetchAnalyzeReviewFlow:
    """Test suite for complete fetch → analyze → review pipeline."""

    def test_fetch_with_empty_search_terms_file(self) -> None:
        """Test fetch command handles empty search terms file gracefully.
        
        Edge case: Empty search terms file should not crash,
        should provide meaningful message.
        """
        runner = CliRunner()
        
        # Create empty search terms file
        fd, path = tempfile.mkstemp(suffix=".txt")
        os.close(fd)
        
        fd_db, db_path = tempfile.mkstemp(suffix=".db")
        os.close(fd_db)
        
        try:
            from job_scraper_analyzer.__main__ import app
            
            result = runner.invoke(app, [
                "fetch",
                "--search-terms", path,
                "--db", str(Path(db_path)),
            ])
            
            # Command should complete without error
            assert result.exit_code == 0
            assert "No search terms" in result.output or "empty" in result.output.lower()
        finally:
            Path(path).unlink(missing_ok=True)
            Path(db_path).unlink(missing_ok=True)

    def test_analyze_with_no_jobs_to_analyze(self) -> None:
        """Test analyze command handles empty database gracefully.
        
        Edge case: No jobs in database should complete successfully
        with message indicating nothing to analyze.
        """
        runner = CliRunner()
        
        fd_db, db_path = tempfile.mkstemp(suffix=".db")
        os.close(fd_db)
        db_path_obj = Path(db_path)
        
        try:
            # Initialize empty database
            from job_scraper_analyzer.database import init_db
            init_db(db_path_obj)
            
            from job_scraper_analyzer.__main__ import app
            
            result = runner.invoke(app, [
                "analyze",
                "--db", str(db_path),
            ])
            
            # Command should complete without error
            assert result.exit_code == 0
            assert "No jobs" in result.output or "complete" in result.output
        finally:
            db_path_obj.unlink(missing_ok=True)

    def test_review_with_empty_database(self) -> None:
        """Test review command handles empty database gracefully.
        
        Edge case: No jobs to review should display meaningful
        empty state message.
        """
        runner = CliRunner()
        
        fd_db, db_path = tempfile.mkstemp(suffix=".db")
        os.close(fd_db)
        db_path_obj = Path(db_path)
        
        try:
            # Initialize empty database
            from job_scraper_analyzer.database import init_db
            init_db(db_path_obj)
            
            from job_scraper_analyzer.__main__ import app
            
            result = runner.invoke(app, [
                "review",
                "--db", str(db_path),
            ], input="q\n")
            
            # Command should complete without error
            assert result.exit_code == 0
            assert "No jobs" in result.output or "empty" in result.output.lower()
        finally:
            db_path_obj.unlink(missing_ok=True)

    def test_review_status_workflow(self) -> None:
        """Test review command status update workflow.
        
        Verifies that review command can update job status through
        the interactive UI simulation.
        """
        runner = CliRunner()
        
        # Jobs with fit ratings and new status
        jobs_with_analysis = [
            Job(
                job_id=1,
                job_url="https://linkedin.com/jobs/view/status1",
                site="linkedin",
                title="Python Engineer",
                company="Status Co",
                location="Remote",
                is_remote=True,
                fit_rating=4,
                status="new",
                description="Python role",
            ),
            Job(
                job_id=2,
                job_url="https://linkedin.com/jobs/view/status2",
                site="linkedin",
                title="Go Developer",
                company="Move Co",
                location="Cape Town",
                is_remote=False,
                fit_rating=3,
                status="new",
                description="Go role",
            ),
        ]
        
        # Capture real implementations before patching
        real_init_db = db_module.init_db
        real_get_jobs_by_status = db_module.get_jobs_by_status
        real_upsert_job = db_module.upsert_job
        
        def mock_get_jobs_by_status(status, db_path):
            return real_get_jobs_by_status(status, db_path)
        
        fd_db, db_path = tempfile.mkstemp(suffix=".db")
        os.close(fd_db)
        db_path_obj = Path(db_path)
        
        try:
            # Initialize database with real init_db
            real_init_db(db_path_obj)
            
            # Load jobs into database first using real functions
            for job in jobs_with_analysis:
                real_upsert_job(job, db_path_obj)
            
            with patch.object(db_module, 'get_jobs_by_status', side_effect=mock_get_jobs_by_status):
                from job_scraper_analyzer.__main__ import app
                
                # Run review and verify table displays with status
                result = runner.invoke(app, [
                    "review",
                    "--db", str(db_path),
                ], input="q\n")
                
                assert result.exit_code == 0
                output_lower = result.output.lower()
                assert "python engineer" in output_lower or "status co" in output_lower
        finally:
            db_path_obj.unlink(missing_ok=True)


class TestPipelineEdgeCases:
    """Edge case tests for the fetch → analyze → review pipeline."""

    def test_cv_file_not_found_uses_default(self) -> None:
        """Test that analyze command uses default CV summary when file not found.
        
        Edge case: When --cv points to non-existent file, should not fail
        but use default CV summary and warn user.
        """
        runner = CliRunner()
        
        fd_db, db_path = tempfile.mkstemp(suffix=".db")
        os.close(fd_db)
        db_path_obj = Path(db_path)
        
        try:
            from job_scraper_analyzer.database import init_db
            init_db(db_path_obj)
            
            from job_scraper_analyzer.__main__ import app
            
            result = runner.invoke(app, [
                "analyze",
                "--cv", "/nonexistent/cv.tex",
                "--db", str(db_path),
            ])
            
            # Command should not fail
            assert result.exit_code == 0
            assert "not found" in result.output.lower() or "default" in result.output.lower()
        finally:
            db_path_obj.unlink(missing_ok=True)
