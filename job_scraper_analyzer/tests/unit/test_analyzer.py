"""Tests for droid exec AI analyzer for batch job fit rating.

RED PHASE: These tests define the expected behavior.
They will FAIL until the analyzer module is implemented.
"""

from datetime import date
from typing import List, Tuple
from unittest.mock import patch, MagicMock

import pytest

from job_scraper_analyzer.models import Job, Analysis


class TestAnalyzeJobs:
    """Test suite for analyze_jobs() batch processing."""

    def setup_test_jobs(self) -> List[Job]:
        """Helper to create test job fixtures."""
        return [
            Job(
                job_url="https://linkedin.com/jobs/view/analyst-1",
                site="linkedin",
                title="Senior Python Engineer",
                company="Tech Corp",
                location="Remote SA",
                is_remote=True,
                description="Looking for Python expert with AI/ML experience",
            ),
            Job(
                job_url="https://linkedin.com/jobs/view/analyst-2",
                site="indeed",
                title="Full Stack Developer",
                company="Startup Inc",
                location="Cape Town",
                is_remote=False,
                description="React and Node.js developer needed",
            ),
            Job(
                job_url="https://linkedin.com/jobs/view/analyst-3",
                site="google",
                title="Embedded Systems Engineer",
                company="Hardware Co",
                location="Remote",
                is_remote=True,
                description="C++ and ESP32 experience required",
            ),
        ]

    def test_analyze_jobs_batch_calls_droid_exec(self) -> None:
        """Test that analyze_jobs() calls droid exec for each batch.
        
        RED: analyze_jobs() must call `droid exec --auto low` for AI analysis.
        The implementation should batch jobs and invoke droid exec for each batch.
        """
        jobs = self.setup_test_jobs()
        cv_summary = "Senior software engineer with Python, JavaScript, C++ skills"
        
        # Mock subprocess.run to capture droid exec calls
        with patch("job_scraper_analyzer.analyzer.subprocess.run") as mock_run:
            # Configure mock to return a successful response
            mock_run.return_value = MagicMock(
                returncode=0,
                stdout='{"fit_rating": 4, "justification": "Perfect match for Python role"}',
                stderr=""
            )
            
            from job_scraper_analyzer.analyzer import analyze_jobs
            
            # Call analyze_jobs with small batch size to trigger multiple calls
            results = analyze_jobs(jobs, cv_summary, batch_size=2, db_path=None)
            
            # Verify droid exec was called (at least once per batch)
            assert mock_run.call_count >= 1, "droid exec should be called at least once per batch"
            
            # Verify the command structure includes droid exec
            for call in mock_run.call_args_list:
                args, kwargs = call
                command = args[0] if args else kwargs.get("args", [])
                assert "droid" in command, "Command should include droid"
                assert "exec" in command, "Command should include exec subcommand"

    def test_analyze_jobs_returns_analysis_results(self) -> None:
        """Test that analyze_jobs() returns a list of Analysis objects.
        
        RED: analyze_jobs() must return List[Analysis] with fit_rating and justification.
        """
        jobs = self.setup_test_jobs()
        cv_summary = "Senior software engineer with Python, JavaScript, C++ skills"
        
        with patch("job_scraper_analyzer.analyzer.subprocess.run") as mock_run:
            # Batch mode: single call returns JSON array with all results
            mock_responses = [
                '{"fit_rating": 4, "justification": "Perfect match for Python role"}\n{"fit_rating": 3, "justification": "Good match for full stack"}\n{"fit_rating": 2, "justification": "Marginal fit for embedded"}',
            ]
            mock_run.side_effect = [
                MagicMock(returncode=0, stdout=resp, stderr="")
                for resp in mock_responses
            ]
            
            from job_scraper_analyzer.analyzer import analyze_jobs
            
            results = analyze_jobs(jobs, cv_summary, batch_size=5, db_path=None)
            
            assert isinstance(results, list), "analyze_jobs should return a list"
            assert len(results) == 3, "Should return one Analysis per job"
            
            for analysis in results:
                assert isinstance(analysis, Analysis), "Results should be Analysis objects"
                assert analysis.fit_rating in [1, 2, 3, 4], "fit_rating should be 1-4"
                assert analysis.justification, "Each analysis should have a justification"

    def test_analyze_jobs_respects_batch_size(self) -> None:
        """Test that analyze_jobs() processes jobs in batches of the specified size.
        
        RED: Jobs should be grouped into batches of `batch_size`.
        """
        jobs = self.setup_test_jobs()
        cv_summary = "Senior software engineer"
        
        with patch("job_scraper_analyzer.analyzer.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                returncode=0,
                stdout='{"fit_rating": 3, "justification": "Good"}',
                stderr=""
            )
            
            from job_scraper_analyzer.analyzer import analyze_jobs
            
            # With 3 jobs and batch_size=2, we expect 2 droid exec calls
            analyze_jobs(jobs, cv_summary, batch_size=2, db_path=None)
            
            # If batching works, we should have 2 calls (first batch of 2, second batch of 1)
            assert mock_run.call_count == 2, "Should make 2 calls for batch_size=2 with 3 jobs"

    def test_analyze_jobs_stores_results_to_database(self) -> None:
        """Test that analyze_jobs() stores results to database when db_path provided.
        
        RED: When db_path is provided, analyze_jobs() should update job fit_ratings in DB.
        """
        import tempfile
        from pathlib import Path
        
        jobs = self.setup_test_jobs()
        cv_summary = "Senior software engineer"
        
        # Create temp database
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            temp_db = Path(f.name)
        
        try:
            # Initialize database with jobs
            from job_scraper_analyzer.database import init_db, upsert_job
            init_db(temp_db)
            for job in jobs:
                upsert_job(job, temp_db)
            
            with patch("job_scraper_analyzer.analyzer.subprocess.run") as mock_run:
                # Batch mode: single call returns JSON array with all results
                mock_run.return_value = MagicMock(
                    returncode=0,
                    stdout='{"fit_rating": 4, "justification": "Perfect match"}\n{"fit_rating": 3, "justification": "Good match"}\n{"fit_rating": 2, "justification": "Marginal fit"}',
                    stderr=""
                )
                
                from job_scraper_analyzer.analyzer import analyze_jobs
                from job_scraper_analyzer.database import get_jobs_by_status
                
                # Analyze jobs and store to DB
                analyze_jobs(jobs, cv_summary, batch_size=5, db_path=temp_db)
                
                # Verify jobs now have fit_rating in database
                analyzed_jobs = get_jobs_by_status("new", temp_db)
                
                # All analyzed jobs should now have fit_rating set
                for job in analyzed_jobs:
                    assert job.fit_rating is not None, f"Job {job.job_url} should have fit_rating after analysis"
        finally:
            if temp_db.exists():
                temp_db.unlink()


class TestBuildAnalysisPrompt:
    """Test suite for _build_analysis_prompt() helper."""

    def test_build_analysis_prompt_includes_cv_summary(self) -> None:
        """Test that the prompt includes the CV summary.
        
        RED: _build_analysis_prompt() should include cv_summary in the prompt.
        """
        job = Job(
            job_url="https://linkedin.com/jobs/view/test",
            site="linkedin",
            title="Python Engineer",
            company="Tech Corp",
            description="Looking for Python developer",
        )
        cv_summary = "Experienced Python developer with AI/ML skills"
        
        from job_scraper_analyzer.analyzer import _build_analysis_prompt
        
        prompt = _build_analysis_prompt(job, cv_summary)
        
        assert cv_summary in prompt, "Prompt should include the CV summary"
        assert "Python Engineer" in prompt, "Prompt should include job title"
        assert "Tech Corp" in prompt, "Prompt should include company name"
        assert "Looking for Python developer" in prompt, "Prompt should include job description"

    def test_build_analysis_prompt_requests_fit_rating(self) -> None:
        """Test that the prompt asks for a fit rating.
        
        RED: Prompt should ask for fit rating with options: Perfect, Good, Marginal, No Fit.
        """
        job = Job(
            job_url="https://linkedin.com/jobs/view/test",
            site="linkedin",
            title="Engineer",
            company="Co",
            description="Job desc",
        )
        
        from job_scraper_analyzer.analyzer import _build_analysis_prompt
        
        prompt = _build_analysis_prompt(job, "CV summary")
        
        assert "fit" in prompt.lower(), "Prompt should mention fit rating"
        # The rating options should be present
        assert any(opt in prompt for opt in ["Perfect", "Good", "Marginal", "No Fit"]), \
            "Prompt should include rating options"


class TestParseDroidResponse:
    """Test suite for _parse_droid_response() parsing logic."""

    def test_parse_fit_rating_from_response_json(self) -> None:
        """Test parsing JSON response from droid exec.
        
        RED: _parse_droid_response() should extract fit_rating (1-4) and justification.
        """
        response = '{"fit_rating": 4, "justification": "Perfect match for skills"}'
        
        from job_scraper_analyzer.analyzer import _parse_droid_response
        
        fit_rating, justification = _parse_droid_response(response)
        
        assert isinstance(fit_rating, int), "fit_rating should be an integer"
        assert fit_rating in [1, 2, 3, 4], "fit_rating should be between 1 and 4"
        assert justification == "Perfect match for skills", "justification should be extracted"

    def test_parse_fit_rating_good(self) -> None:
        """Test parsing a 'Good' fit rating response.
        
        RED: fit_rating should be 3 for 'Good' rating.
        """
        response = '{"fit_rating": 3, "justification": "Good match for the role"}'
        
        from job_scraper_analyzer.analyzer import _parse_droid_response
        
        fit_rating, justification = _parse_droid_response(response)
        
        assert fit_rating == 3, "fit_rating 3 corresponds to 'Good'"
        assert "Good match" in justification

    def test_parse_fit_rating_marginal(self) -> None:
        """Test parsing a 'Marginal' fit rating response.
        
        RED: fit_rating should be 2 for 'Marginal' rating.
        """
        response = '{"fit_rating": 2, "justification": "Partial overlap with skills"}'
        
        from job_scraper_analyzer.analyzer import _parse_droid_response
        
        fit_rating, justification = _parse_droid_response(response)
        
        assert fit_rating == 2, "fit_rating 2 corresponds to 'Marginal'"
        assert "Partial overlap" in justification

    def test_parse_fit_rating_no_fit(self) -> None:
        """Test parsing a 'No Fit' fit rating response.
        
        RED: fit_rating should be 1 for 'No Fit' rating.
        """
        response = '{"fit_rating": 1, "justification": "Significant mismatch"}'
        
        from job_scraper_analyzer.analyzer import _parse_droid_response
        
        fit_rating, justification = _parse_droid_response(response)
        
        assert fit_rating == 1, "fit_rating 1 corresponds to 'No Fit'"
        assert "mismatch" in justification.lower()

    def test_parse_droid_response_handles_text_ratings(self) -> None:
        """Test parsing responses where fit_rating is specified as text.
        
        RED: Should handle responses like "Perfect" -> 4, "Good" -> 3, etc.
        """
        # Response with text rating instead of number
        response = '{"fit_rating": "Perfect", "justification": "Ideal match"}'
        
        from job_scraper_analyzer.analyzer import _parse_droid_response
        
        fit_rating, justification = _parse_droid_response(response)
        
        assert fit_rating == 4, "Text 'Perfect' should map to fit_rating 4"
        assert "Ideal match" in justification


class TestAnalyzerEdgeCases:
    """Test suite for edge case handling in analyzer."""

    def test_analyze_jobs_handles_empty_job_list(self) -> None:
        """Test that analyze_jobs() handles empty job list gracefully.
        
        RED: Empty job list should return empty list, not raise an error.
        """
        from job_scraper_analyzer.analyzer import analyze_jobs
        
        results = analyze_jobs([], "CV summary", batch_size=5, db_path=None)
        
        assert results == [], "Empty job list should return empty results"

    def test_parse_droid_response_handles_malformed_json(self) -> None:
        """Test that _parse_droid_response() handles malformed JSON gracefully.
        
        RED: Malformed JSON should raise a clear error or return sensible defaults.
        """
        malformed_response = "This is not valid JSON"
        
        from job_scraper_analyzer.analyzer import _parse_droid_response
        
        with pytest.raises((ValueError, KeyError)):
            _parse_droid_response(malformed_response)

    def test_analyze_jobs_handles_droid_not_installed(self) -> None:
        """Test handling when droid command is not found.
        
        RED: Should raise a clear error when droid is not available.
        """
        jobs = [
            Job(
                job_url="https://linkedin.com/jobs/view/error",
                site="linkedin",
                title="Engineer",
                company="Co",
                description="Job",
            )
        ]
        
        with patch("job_scraper_analyzer.analyzer.subprocess.run") as mock_run:
            mock_run.side_effect = FileNotFoundError("droid: command not found")
            
            from job_scraper_analyzer.analyzer import analyze_jobs
            
            with pytest.raises(RuntimeError) as exc_info:
                analyze_jobs(jobs, "CV", batch_size=5, db_path=None)
            
            assert "droid" in str(exc_info.value).lower(), "Error should mention droid"

    def test_analyze_jobs_handles_rate_limiting(self) -> None:
        """Test that analyze_jobs() handles rate limiting from AI service.
        
        RED: When droid exec returns rate limit error, should retry or raise appropriate error.
        """
        jobs = [
            Job(
                job_url="https://linkedin.com/jobs/view/ratelimit",
                site="linkedin",
                title="Engineer",
                company="Co",
                description="Job",
            )
        ]
        
        with patch("job_scraper_analyzer.analyzer.subprocess.run") as mock_run:
            # First call fails with rate limit, second succeeds
            mock_run.side_effect = [
                MagicMock(returncode=429, stdout="", stderr="Rate limited"),
                MagicMock(
                    returncode=0,
                    stdout='{"fit_rating": 3, "justification": "Good"}',
                    stderr=""
                ),
            ]
            
            from job_scraper_analyzer.analyzer import analyze_jobs
            
            # Should either succeed after retry or raise rate limit error
            try:
                results = analyze_jobs(jobs, "CV", batch_size=5, db_path=None, max_retries=1)
                # If it succeeds, rate limiting was handled
                assert len(results) == 1
            except RuntimeError as e:
                # If it raises error, it should be about rate limiting
                assert "rate" in str(e).lower() or "429" in str(e)

    def test_analyze_jobs_includes_batch_id_for_tracking(self) -> None:
        """Test that analysis results include batch_id for audit tracking.
        
        RED: Each Analysis should have a batch_id for tracking which batch it came from.
        """
        jobs = [
            Job(
                job_url="https://linkedin.com/jobs/view/batch",
                site="linkedin",
                title="Engineer",
                company="Co",
                description="Job",
            )
        ]
        
        with patch("job_scraper_analyzer.analyzer.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                returncode=0,
                stdout='{"fit_rating": 4, "justification": "Perfect"}',
                stderr=""
            )
            
            from job_scraper_analyzer.analyzer import analyze_jobs
            
            results = analyze_jobs(jobs, "CV", batch_size=5, db_path=None)
            
            assert len(results) == 1
            assert results[0].batch_id is not None, "Analysis should have batch_id for tracking"
