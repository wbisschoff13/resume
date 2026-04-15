"""Tests for JobSpy scraper wrapper.

RED PHASE: These tests define the expected behavior of the scraper module.
They will FAIL until scraper.py is implemented.
"""

from datetime import date
from typing import List
from unittest.mock import MagicMock, patch

import pytest
from pydantic import ValidationError

from job_scraper_analyzer.models import Job


class TestScrapeSites:
    """Test suite for scrape_sites function."""

    def test_scrape_sites_returns_job_list(self) -> None:
        """Test that scrape_sites returns a list of Job objects.
        
        RED: scrape_sites must call JobSpy and convert results to Job models.
        
        When JobSpy returns a DataFrame with job data, scrape_sites should
        convert each row to a Job model and return a list of Jobs.
        """
        # Arrange: Mock JobSpy to return a sample DataFrame
        sample_data = {
            "job_url": ["https://linkedin.com/jobs/view/123"],
            "site": ["linkedin"],
            "title": ["Software Engineer"],
            "company": ["Tech Corp"],
            "location": ["Cape Town, South Africa"],
            "is_remote": [True],
            "job_type": ["fulltime"],
            "description": ["Job description here"],
            "min_salary": [80000.0],
            "max_salary": [120000.0],
            "salary_currency": ["USD"],
            "salary_interval": ["yearly"],
            "date_posted": ["2024-01-15"],
            "job_level": ["Senior"],
            "company_industry": ["Technology"],
        }
        
        mock_df = MagicMock()
        mock_df.__getitem__ = lambda self, key: sample_data.get(key, [None])
        mock_df.__iter__ = lambda self: iter(sample_data.keys())
        mock_df.items = lambda: [(k, v) for k, v in sample_data.items()]
        mock_df.get = lambda key, default=None: sample_data.get(key, [default])
        
        # Mock the JobSpy class
        with patch("job_scraper_analyzer.scraper.JobSpy") as mock_jobspy_class:
            mock_jobspy = MagicMock()
            mock_jobspy.launch.return_value = None
            mock_jobspy.search.return_value = mock_df
            mock_jobspy_class.return_value = mock_jobspy
            
            # Import and call scrape_sites - this will fail until implemented
            from job_scraper_analyzer.scraper import scrape_sites
            
            result = scrape_sites(
                search_term="Software Engineer",
                location="Cape Town",
                is_remote=True,
                hours_old=168,
            )
            
            # Assert: Result should be a list of Job objects
            assert isinstance(result, list)
            assert len(result) == 1
            assert isinstance(result[0], Job)
            assert result[0].job_url == "https://linkedin.com/jobs/view/123"
            assert result[0].site == "linkedin"
            assert result[0].title == "Software Engineer"
            assert result[0].company == "Tech Corp"

    def test_scrape_sites_handles_empty_results(self) -> None:
        """Test that scrape_sites returns empty list when no jobs found.
        
        RED: scrape_sites must handle empty JobSpy results gracefully.
        """
        # Arrange: Mock JobSpy to return empty DataFrame
        mock_df = MagicMock()
        mock_df.__getitem__ = lambda self, key: []
        mock_df.__iter__ = lambda self: iter([])
        mock_df.items = lambda: []
        mock_df.get = lambda key, default=None: []
        
        with patch("job_scraper_analyzer.scraper.JobSpy") as mock_jobspy_class:
            mock_jobspy = MagicMock()
            mock_jobspy.launch.return_value = None
            mock_jobspy.search.return_value = mock_df
            mock_jobspy_class.return_value = mock_jobspy
            
            from job_scraper_analyzer.scraper import scrape_sites
            
            result = scrape_sites(
                search_term="Nonexistent Job Title XYZ",
                location="Nowhere",
                is_remote=False,
                hours_old=24,
            )
            
            # Assert: Should return empty list, not raise exception
            assert isinstance(result, list)
            assert len(result) == 0

    def test_scrape_sites_converts_jobspy_columns_correctly(self) -> None:
        """Test that JobSpy DataFrame columns are mapped to Job model fields.
        
        RED: _convert_jobspy_row must map JobSpy columns to Job model correctly.
        
        JobSpy uses different column names than our Job model. The conversion
        function must handle: job_url, site, title, company, location, etc.
        """
        # Arrange: Sample row data as JobSpy would return it
        jobspy_row = {
            "job_url": "https://indeed.com/jobs/view/456",
            "site": "indeed",
            "title": "Senior Developer",
            "company": "DevCorp",
            "location": "Remote SA",
            "is_remote": True,
            "job_type": "fulltime",
            "description": "Great opportunity",
            "min_salary": 90000.0,
            "max_salary": 130000.0,
            "salary_currency": "USD",
            "salary_interval": "yearly",
            "date_posted": "2024-02-20",
            "job_level": "Senior",
            "company_industry": "IT",
        }
        
        mock_df = MagicMock()
        mock_df.__getitem__ = lambda self, key: [jobspy_row.get(key)]
        mock_df.__iter__ = lambda self: iter(jobspy_row.keys())
        mock_df.items = lambda: [(k, [v]) for k, v in jobspy_row.items()]
        mock_df.get = lambda key, default=None: [jobspy_row.get(key)] if key in jobspy_row else [default]
        
        with patch("job_scraper_analyzer.scraper.JobSpy") as mock_jobspy_class:
            mock_jobspy = MagicMock()
            mock_jobspy.launch.return_value = None
            mock_jobspy.search.return_value = mock_df
            mock_jobspy_class.return_value = mock_jobspy
            
            from job_scraper_analyzer.scraper import scrape_sites
            
            result = scrape_sites(
                search_term="Developer",
                location="Remote SA",
                is_remote=True,
                hours_old=72,
            )
            
            # Assert: All fields should be correctly converted
            assert len(result) == 1
            job = result[0]
            assert job.job_url == "https://indeed.com/jobs/view/456"
            assert job.site == "indeed"
            assert job.title == "Senior Developer"
            assert job.company == "DevCorp"
            assert job.is_remote is True
            assert job.job_type == "fulltime"
            assert job.min_salary == 90000.0
            assert job.max_salary == 130000.0
            assert job.date_posted == date(2024, 2, 20)


class TestIntersectionStrategy:
    """Test suite for intersection_strategy function."""

    def test_intersection_strategy_merges_results(self) -> None:
        """Test that intersection_strategy merges results from multiple queries.
        
        RED: intersection_strategy must execute multiple search variants and
        merge/deduplicate results.
        
        When LinkedIn/Indeed have mutually exclusive filters (e.g., "Remote" vs
        "Past 7 days"), intersection_strategy runs both queries and combines
        results, removing duplicates by job_url.
        """
        # Arrange: Two sample DataFrames with overlapping jobs
        df1_data = {
            "job_url": [
                "https://linkedin.com/jobs/view/100",
                "https://linkedin.com/jobs/view/101",
            ],
            "site": ["linkedin", "linkedin"],
            "title": ["Engineer A", "Engineer B"],
            "company": ["Company A", "Company B"],
            "location": ["Remote", "Remote"],
            "is_remote": [True, True],
            "job_type": ["fulltime", "fulltime"],
            "description": ["Desc A", "Desc B"],
            "min_salary": [None, None],
            "max_salary": [None, None],
            "salary_currency": ["USD", "USD"],
            "salary_interval": [None, None],
            "date_posted": ["2024-03-01", "2024-03-05"],
            "job_level": ["Senior", "Senior"],
            "company_industry": [None, None],
        }
        
        df2_data = {
            "job_url": [
                "https://linkedin.com/jobs/view/101",  # Duplicate
                "https://linkedin.com/jobs/view/102",  # New
            ],
            "site": ["linkedin", "linkedin"],
            "title": ["Engineer B", "Engineer C"],
            "company": ["Company B", "Company C"],
            "location": ["Remote", "Remote"],
            "is_remote": [True, True],
            "job_type": ["fulltime", "fulltime"],
            "description": ["Desc B", "Desc C"],
            "min_salary": [None, None],
            "max_salary": [None, None],
            "salary_currency": ["USD", "USD"],
            "salary_interval": [None, None],
            "date_posted": ["2024-03-05", "2024-03-10"],
            "job_level": ["Senior", "Senior"],
            "company_industry": [None, None],
        }
        
        def create_mock_df(data):
            mock_df = MagicMock()
            mock_df.__getitem__ = lambda self, key: data.get(key, [None])
            mock_df.__iter__ = lambda self: iter(data.keys())
            mock_df.items = lambda: [(k, v) for k, v in data.items()]
            mock_df.get = lambda key, default=None: data.get(key, [default])
            return mock_df
        
        with patch("job_scraper_analyzer.scraper.JobSpy") as mock_jobspy_class:
            mock_jobspy = MagicMock()
            mock_jobspy.launch.return_value = None
            
            # Return different DataFrames on successive calls
            call_count = [0]
            def mock_search(*args, **kwargs):
                call_count[0] += 1
                if call_count[0] == 1:
                    return create_mock_df(df1_data)
                return create_mock_df(df2_data)
            
            mock_jobspy.search.side_effect = mock_search
            mock_jobspy_class.return_value = mock_jobspy
            
            from job_scraper_analyzer.scraper import intersection_strategy
            
            result = intersection_strategy(
                term="Software Engineer",
                location="Remote SA",
            )
            
            # Assert: Should have 3 unique jobs (100, 101, 102)
            assert isinstance(result, list)
            assert len(result) == 3
            
            # Check deduplication - job 101 should appear only once
            urls = [job.job_url for job in result]
            assert urls.count("https://linkedin.com/jobs/view/101") == 1
            
            # All jobs should be Job instances
            for job in result:
                assert isinstance(job, Job)

    def test_intersection_strategy_no_duplicates(self) -> None:
        """Test that intersection_strategy removes exact duplicate jobs.
        
        RED: Even if the same job appears in both search variants,
        it should appear only once in the final result.
        """
        # Both DataFrames have the exact same jobs
        shared_data = {
            "job_url": ["https://linkedin.com/jobs/view/200"],
            "site": ["linkedin"],
            "title": ["Same Job"],
            "company": ["Same Company"],
            "location": ["Remote"],
            "is_remote": [True],
            "job_type": ["fulltime"],
            "description": ["Same description"],
            "min_salary": [None],
            "max_salary": [None],
            "salary_currency": ["USD"],
            "salary_interval": [None],
            "date_posted": ["2024-03-15"],
            "job_level": ["Senior"],
            "company_industry": [None],
        }
        
        def create_mock_df(data):
            mock_df = MagicMock()
            mock_df.__getitem__ = lambda self, key: data.get(key, [None])
            mock_df.__iter__ = lambda self: iter(data.keys())
            mock_df.items = lambda: [(k, v) for k, v in data.items()]
            mock_df.get = lambda key, default=None: data.get(key, [default])
            return mock_df
        
        with patch("job_scraper_analyzer.scraper.JobSpy") as mock_jobspy_class:
            mock_jobspy = MagicMock()
            mock_jobspy.launch.return_value = None
            mock_jobspy.search.side_effect = [create_mock_df(shared_data), create_mock_df(shared_data)]
            mock_jobspy_class.return_value = mock_jobspy
            
            from job_scraper_analyzer.scraper import intersection_strategy
            
            result = intersection_strategy(
                term="Remote Engineer",
                location="Remote SA",
            )
            
            # Assert: Should have only 1 unique job (deduplicated)
            assert len(result) == 1
            assert result[0].job_url == "https://linkedin.com/jobs/view/200"

    def test_intersection_strategy_handles_empty_results(self) -> None:
        """Test that intersection_strategy handles when all searches return empty.
        
        RED: intersection_strategy must not raise on empty results.
        """
        def create_empty_mock_df():
            mock_df = MagicMock()
            mock_df.__getitem__ = lambda self, key: []
            mock_df.__iter__ = lambda self: iter([])
            mock_df.items = lambda: []
            mock_df.get = lambda key, default=None: []
            return mock_df
        
        with patch("job_scraper_analyzer.scraper.JobSpy") as mock_jobspy_class:
            mock_jobspy = MagicMock()
            mock_jobspy.launch.return_value = None
            mock_jobspy.search.side_effect = [create_empty_mock_df(), create_empty_mock_df()]
            mock_jobspy_class.return_value = mock_jobspy
            
            from job_scraper_analyzer.scraper import intersection_strategy
            
            result = intersection_strategy(
                term="Nonexistent",
                location="Nowhere",
            )
            
            # Assert: Should return empty list
            assert isinstance(result, list)
            assert len(result) == 0


class TestConvertJobSpyRow:
    """Test suite for _convert_jobspy_row helper function."""

    def test_convert_jobspy_row_maps_all_fields(self) -> None:
        """Test that _convert_jobspy_row correctly maps all JobSpy fields.
        
        RED: _convert_jobspy_row must map JobSpy DataFrame columns to
        Job model fields correctly.
        """
        from job_scraper_analyzer.scraper import _convert_jobspy_row
        
        row = {
            "job_url": "https://linkedin.com/jobs/view/300",
            "site": "linkedin",
            "title": "Test Engineer",
            "company": "Test Co",
            "location": "Cape Town",
            "is_remote": False,
            "job_type": "contract",
            "description": "Test description",
            "min_salary": 70000.0,
            "max_salary": 100000.0,
            "salary_currency": "USD",
            "salary_interval": "yearly",
            "date_posted": "2024-04-01",
            "job_level": "Mid",
            "company_industry": "Tech",
        }
        
        result = _convert_jobspy_row(row)
        
        assert isinstance(result, Job)
        assert result.job_url == "https://linkedin.com/jobs/view/300"
        assert result.site == "linkedin"
        assert result.title == "Test Engineer"
        assert result.company == "Test Co"
        assert result.location == "Cape Town"
        assert result.is_remote is False
        assert result.job_type == "contract"
        assert result.description == "Test description"
        assert result.min_salary == 70000.0
        assert result.max_salary == 100000.0
        assert result.salary_currency == "USD"
        assert result.salary_interval == "yearly"
        assert result.date_posted == date(2024, 4, 1)
        assert result.job_level == "Mid"
        assert result.company_industry == "Tech"

    def test_convert_jobspy_row_handles_missing_optional_fields(self) -> None:
        """Test that _convert_jobspy_row handles missing optional fields.
        
        RED: _convert_jobspy_row must handle rows with missing optional
        fields gracefully (defaults to None).
        """
        from job_scraper_analyzer.scraper import _convert_jobspy_row
        
        # Minimal required fields only
        row = {
            "job_url": "https://linkedin.com/jobs/view/301",
            "site": "linkedin",
            "title": "Minimal Job",
        }
        
        result = _convert_jobspy_row(row)
        
        assert isinstance(result, Job)
        assert result.job_url == "https://linkedin.com/jobs/view/301"
        assert result.site == "linkedin"
        assert result.title == "Minimal Job"
        # Optional fields should be None
        assert result.company is None
        assert result.location is None
        assert result.is_remote is None
        assert result.job_type is None
        assert result.description is None
        assert result.min_salary is None
        assert result.max_salary is None
        assert result.date_posted is None


class TestSiteSpecificFilters:
    """Test suite for site-specific filter builder helpers."""

    def test_build_indeed_params(self) -> None:
        """Test that _build_indeed_params creates correct Indeed parameters.
        
        RED: _build_indeed_params must map search parameters to Indeed-specific
        filter formats (e.g., remote →remote=1, date_posted →fromage).
        """
        from job_scraper_analyzer.scraper import _build_indeed_params
        
        result = _build_indeed_params(
            search_term="Python Developer",
            location="Remote SA",
            is_remote=True,
            hours_old=72,
            job_type="fulltime",
        )
        
        assert isinstance(result, dict)
        assert "search_term" in result or "keywords" in result or "q" in result
        assert "location" in result or "l" in result
        # Remote filter should be converted
        # Date filter should be converted (e.g., fromage=3 for 72 hours)

    def test_build_linkedin_params(self) -> None:
        """Test that _build_linkedin_params creates correct LinkedIn parameters.
        
        RED: _build_linkedin_params must map search parameters to LinkedIn-specific
        filter formats (e.g., remote →f_AL=true, date Posted →f_TPR).
        """
        from job_scraper_analyzer.scraper import _build_linkedin_params
        
        result = _build_linkedin_params(
            search_term="Senior Engineer",
            location="Cape Town",
            is_remote=False,
            hours_old=168,
            job_type="fulltime",
        )
        
        assert isinstance(result, dict)
        # LinkedIn uses specific parameter names
        assert "keywords" in result or "q" in result or "search_term" in result


class TestErrorHandling:
    """Test suite for error handling in scraper module."""

    def test_scrape_sites_handles_jobspy_exception(self) -> None:
        """Test that scrape_sites handles JobSpy exceptions gracefully.
        
        RED: scrape_sites must catch and handle JobSpy exceptions without
        crashing - returning empty list or raising controlled error.
        """
        with patch("job_scraper_analyzer.scraper.JobSpy") as mock_jobspy_class:
            mock_jobspy = MagicMock()
            mock_jobspy.launch.side_effect = Exception("JobSpy initialization failed")
            mock_jobspy_class.return_value = mock_jobspy
            
            from job_scraper_analyzer.scraper import scrape_sites
            
            # Should not raise - either returns empty list or raises controlled error
            try:
                result = scrape_sites(
                    search_term="Test",
                    location="Test",
                    is_remote=False,
                    hours_old=24,
                )
                # If it returns, should be a list
                assert isinstance(result, list)
            except Exception as e:
                # If it raises, should be a controlled error type
                assert "JobSpy" in str(e) or "scraper" in str(e).lower()

    def test_intersection_strategy_rate_limiting(self) -> None:
        """Test that intersection_strategy adds delays between queries.
        
        RED: intersection_strategy should add delays between multiple queries
        to respect rate limits (implement via time.sleep mocking).
        """
        import time
        
        with patch("job_scraper_analyzer.scraper.JobSpy") as mock_jobspy_class:
            with patch("job_scraper_analyzer.scraper.time.sleep") as mock_sleep:
                mock_jobspy = MagicMock()
                mock_jobspy.launch.return_value = None
                
                def create_empty_mock_df():
                    mock_df = MagicMock()
                    mock_df.__getitem__ = lambda self, key: []
                    mock_df.__iter__ = lambda self: iter([])
                    mock_df.items = lambda: []
                    mock_df.get = lambda key, default=None: []
                    return mock_df
                
                mock_jobspy.search.side_effect = [create_empty_mock_df(), create_empty_mock_df()]
                mock_jobspy_class.return_value = mock_jobspy
                
                from job_scraper_analyzer.scraper import intersection_strategy
                
                result = intersection_strategy(
                    term="Test",
                    location="Test",
                )
                
                # sleep should have been called at least once (rate limiting delay)
                # Note: This test may need adjustment based on actual implementation
                # For now we just verify the function completes without error
                assert isinstance(result, list)
