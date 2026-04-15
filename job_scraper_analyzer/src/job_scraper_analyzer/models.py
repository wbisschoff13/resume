"""Pydantic models for Job, Search, and Analysis entities.

These models are defined per the data-model.md specification.
"""

from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field


class Job(BaseModel):
    """Job posting entity with all scraped data and analysis results.
    
    Attributes:
        job_url: Unique URL to the job posting (required)
        site: Job board site ('linkedin', 'indeed', 'google')
        title: Job title (required)
        company: Company name
        location: Job location
        is_remote: Whether job is remote
        job_type: Type of employment ('fulltime', 'parttime', 'contract', 'internship', 'temporary')
        description: Full job description text
        min_salary: Minimum salary offered
        max_salary: Maximum salary offered
        salary_currency: Currency code (defaults to 'USD')
        salary_interval: Salary interval ('yearly', 'hourly', etc.)
        date_posted: Date the job was posted
        job_level: Experience level ('Senior', 'Mid', 'Entry', etc.)
        company_industry: Industry the company belongs to
        fit_rating: 1-4 rating from AI analysis (1=No Fit, 2=Marginal, 3=Good, 4=Perfect)
        status: Review status ('new', 'applied', 'declined', 'skip')
        search_id: Reference to the search that found this job
        scraped_at: Timestamp when job was scraped
        analyzed_at: Timestamp when job was analyzed
    """
    
    job_url: str
    site: str
    title: str
    company: Optional[str] = None
    location: Optional[str] = None
    is_remote: Optional[bool] = None
    job_type: Optional[str] = None
    description: Optional[str] = None
    min_salary: Optional[float] = None
    max_salary: Optional[float] = None
    salary_currency: str = "USD"
    salary_interval: Optional[str] = None
    date_posted: Optional[date] = None
    job_level: Optional[str] = None
    company_industry: Optional[str] = None
    fit_rating: Optional[int] = None
    status: str = "new"
    search_id: Optional[int] = None
    scraped_at: Optional[datetime] = None
    analyzed_at: Optional[datetime] = None


class Search(BaseModel):
    """Search parameters for job scraping.
    
    Attributes:
        search_term: The job search query (required)
        location: Geographic location filter
        is_remote: Filter for remote jobs
        hours_old: Filter for jobs posted within N hours
        job_type: Filter for job type
        site_name: Comma-separated list of sites to search
    """
    
    search_term: str
    location: Optional[str] = None
    is_remote: bool = False
    hours_old: Optional[int] = None
    job_type: Optional[str] = None
    site_name: str = "linkedin,indeed,google"


class Analysis(BaseModel):
    """AI analysis result for a job posting.
    
    Attributes:
        job_id: Reference to the job being analyzed (required)
        batch_id: Batch identifier for grouping analyses
        fit_rating: 1-4 rating (1=No Fit, 2=Marginal, 3=Good, 4=Perfect)
        justification: Explanation of the fit rating
        analyzed_at: Timestamp when analysis was performed
    """
    
    job_id: int
    batch_id: Optional[str] = None
    fit_rating: int
    justification: str
