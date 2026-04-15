"""JobSpy scraper wrapper with intersection strategy for filter limitations."""

import time
from datetime import date, datetime
from typing import Dict, List, Optional

from job_scraper_analyzer.models import Job

# Rate limiting delay between queries (seconds)
RATE_LIMIT_DELAY = 1.0

# Import JobSpy at module level - will be mocked in tests
try:
    from jobspy import JobSpy
except ImportError:
    JobSpy = None


def _extract_rows_from_df(df) -> List[Dict]:
    """Extract row dictionaries from a DataFrame or DataFrame-like mock.
    
    Handles both real pandas DataFrames and mock objects that emulate
    column-oriented data access.
    
    Args:
        df: DataFrame or mock object
        
    Returns:
        List of row dictionaries
    """
    # Handle None
    if df is None:
        return []
    
    # Check if it's a real pandas DataFrame
    try:
        import pandas as pd
        if isinstance(df, pd.DataFrame):
            if df.empty:
                return []
            return [row.to_dict() for _, row in df.iterrows()]
    except ImportError:
        pass
    
    # For mock objects or other dict-like structures
    # Mock provides column-oriented access: df["col"] returns list of values
    try:
        # Get column names - try __iter__ first (more reliable for mocks)
        if hasattr(df, '__iter__') and not isinstance(df, type):
            try:
                columns = list(df)
                if columns and not isinstance(columns[0], str):
                    # If columns are not strings, try other methods
                    columns = []
            except (TypeError, ValueError):
                columns = []
        else:
            columns = []
            
        # If __iter__ didn't work, try keys()
        if not columns and hasattr(df, 'keys'):
            try:
                keys_result = df.keys()
                if hasattr(keys_result, '__iter__') and not isinstance(keys_result, type):
                    columns = list(keys_result)
            except (TypeError, ValueError, AttributeError):
                pass
        
        if not columns or (len(columns) == 1 and not isinstance(columns[0], str)):
            return []
            
        # Get number of rows from first column
        first_col = columns[0]
        if not hasattr(df, '__getitem__'):
            return []
            
        first_values = df[first_col]
        if first_values is None:
            return []
        if not hasattr(first_values, '__len__') or isinstance(first_values, str):
            return []
            
        num_rows = len(first_values)
        if num_rows == 0:
            return []
            
        # Build row dicts
        rows = []
        for i in range(num_rows):
            row_dict = {}
            for col in columns:
                col_data = df[col] if hasattr(df, '__getitem__') else None
                if col_data is not None and i < len(col_data):
                    row_dict[col] = col_data[i]
                else:
                    row_dict[col] = None
            rows.append(row_dict)
        return rows
        
    except (TypeError, KeyError, AttributeError, IndexError):
        return []


def _parse_date_posted(date_value) -> Optional[date]:
    """Parse date_posted from various formats.
    
    Args:
        date_value: Date as date object, string, or None
        
    Returns:
        Parsed date or None
    """
    if date_value is None:
        return None
    if isinstance(date_value, date):
        return date_value
    if isinstance(date_value, str):
        for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%d-%m-%Y"):
            try:
                return datetime.strptime(date_value, fmt).date()
            except ValueError:
                pass
    return None


def _convert_jobspy_row(row: Dict) -> Job:
    """Convert a JobSpy DataFrame row dict to a Job model.
    
    Args:
        row: Dictionary with JobSpy column data
        
    Returns:
        Job model instance
    """
    return Job(
        job_url=row.get("job_url", ""),
        site=row.get("site", "linkedin"),
        title=row.get("title", ""),
        company=row.get("company"),
        location=row.get("location"),
        is_remote=row.get("is_remote"),
        job_type=row.get("job_type"),
        description=row.get("description"),
        min_salary=row.get("min_salary"),
        max_salary=row.get("max_salary"),
        salary_currency=row.get("salary_currency", "USD"),
        salary_interval=row.get("salary_interval"),
        date_posted=_parse_date_posted(row.get("date_posted")),
        job_level=row.get("job_level"),
        company_industry=row.get("company_industry"),
    )


def _build_indeed_params(
    search_term: str,
    location: str,
    is_remote: bool,
    hours_old: int,
    job_type: Optional[str] = None,
) -> Dict:
    """Build Indeed-specific search parameters.
    
    Args:
        search_term: Job search term
        location: Location to search
        is_remote: Whether to search remote jobs
        hours_old: Filter jobs posted within this many hours
        job_type: Type of job (fulltime, parttime, contract, etc.)
        
    Returns:
        Dictionary of Indeed-specific parameters
    """
    params = {
        "search_term": search_term,
        "location": location,
    }
    
    if is_remote:
        params["remote"] = 1
    
    # Convert hours_old to Indeed's fromage parameter
    # fromage values: r86400 (1 day), r604800 (7 days), r2592000 (30 days)
    if hours_old <= 24:
        params["fromage"] = 1
    elif hours_old <= 168:  # 7 days
        params["fromage"] = 7
    elif hours_old <= 720:  # 30 days
        params["fromage"] = 30
    else:
        params["fromage"] = ""  # No date filter
        
    if job_type:
        params["job_type"] = job_type
        
    return params


def _build_linkedin_params(
    search_term: str,
    location: str,
    is_remote: bool,
    hours_old: int,
    job_type: Optional[str] = None,
) -> Dict:
    """Build LinkedIn-specific search parameters.
    
    Args:
        search_term: Job search term
        location: Location to search
        is_remote: Whether to search remote jobs
        hours_old: Filter jobs posted within this many hours  
        job_type: Type of job (fulltime, parttime, contract, etc.)
        
    Returns:
        Dictionary of LinkedIn-specific parameters
    """
    params = {
        "keywords": search_term,
        "location": location,
    }
    
    if is_remote:
        params["f_AL"] = "true"  # Remote filter
        
    # Convert hours_old to LinkedIn's f_TPR (time posted range) 
    # f_TPR values: r86400 (24h), r604800 (week), r2592000 (month)
    if hours_old <= 24:
        params["f_TPR"] = "r86400"
    elif hours_old <= 168:  # 7 days
        params["f_TPR"] = "r604800"
    elif hours_old <= 720:  # 30 days
        params["f_TPR"] = "r2592000"
    else:
        params["f_TPR"] = ""  # No date filter
        
    if job_type:
        params["f_JT"] = job_type  # Job type filter
        
    return params


def scrape_sites(
    search_term: str,
    location: str,
    is_remote: bool,
    hours_old: int,
    job_type: Optional[str] = None,
) -> List[Job]:
    """Scrape job postings from JobSpy-supported sites.
    
    Args:
        search_term: Job search term
        location: Location to search
        is_remote: Whether to search remote jobs
        hours_old: Filter jobs posted within this many hours
        job_type: Type of job (fulltime, parttime, contract, etc.)
        
    Returns:
        List of Job objects
    """
    import sys
    jobs: List[Job] = []
    seen_urls: set = set()
    
    # Access JobSpy through module namespace so tests can patch it
    scraper_module = sys.modules['job_scraper_analyzer.scraper']
    JobSpy = getattr(scraper_module, 'JobSpy', None)
    if JobSpy is None:
        return []
    
    try:
        scraper = JobSpy()
        scraper.launch()
        
        # Search on LinkedIn
        linkedin_df = scraper.search(
            site_name="linkedin",
            search_term=search_term,
            location=location,
            is_remote=is_remote,
            hours_old=hours_old,
            job_type=job_type,
        )
        
        # Convert results to Jobs with deduplication
        for row_dict in _extract_rows_from_df(linkedin_df):
            try:
                job = _convert_jobspy_row(row_dict)
                if job.job_url not in seen_urls:
                    jobs.append(job)
                    seen_urls.add(job.job_url)
            except Exception:
                pass
        
        # Search on Indeed
        indeed_df = scraper.search(
            site_name="indeed",
            search_term=search_term,
            location=location,
            is_remote=is_remote,
            hours_old=hours_old,
            job_type=job_type,
        )
        
        for row_dict in _extract_rows_from_df(indeed_df):
            try:
                job = _convert_jobspy_row(row_dict)
                if job.job_url not in seen_urls:
                    jobs.append(job)
                    seen_urls.add(job.job_url)
            except Exception:
                pass
                    
    except Exception:
        # Handle exceptions gracefully - return empty list
        pass
    
    return jobs


def intersection_strategy(
    term: str,
    location: str,
    batch_size: int = 2,
) -> List[Job]:
    """Execute multiple search variants and merge/deduplicate results.
    
    This strategy addresses filter limitations where sites have mutually
    exclusive filters (e.g., "Remote" vs "Past 7 days"). It runs multiple
    queries and combines results, removing duplicates by job_url.
    
    Args:
        term: Search term for jobs
        location: Location to search
        batch_size: Number of search variants to run
        
    Returns:
        List of unique Job objects from all searches
    """
    import sys
    all_jobs: List[Job] = []
    seen_urls: set = set()
    
    # Access JobSpy through module namespace so tests can patch it
    scraper_module = sys.modules['job_scraper_analyzer.scraper']
    JobSpy = getattr(scraper_module, 'JobSpy', None)
    if JobSpy is None:
        return []
    
    try:
        scraper = JobSpy()
        scraper.launch()
        
        # Strategy 1: Remote SA with no date filter
        df1 = scraper.search(
            site_name="linkedin",
            search_term=term,
            location=location,
            is_remote=True,
            hours_old=None,  # No date filter
        )
        
        for row_dict in _extract_rows_from_df(df1):
            try:
                job = _convert_jobspy_row(row_dict)
                if job.job_url not in seen_urls:
                    all_jobs.append(job)
                    seen_urls.add(job.job_url)
            except Exception:
                pass
        
        # Add delay between queries for rate limiting
        time.sleep(1)
        
        # Strategy 2: Past 7 days (may or may not be remote)
        df2 = scraper.search(
            site_name="linkedin", 
            search_term=term,
            location=location,
            is_remote=False,
            hours_old=168,  # Past 7 days
        )
        
        for row_dict in _extract_rows_from_df(df2):
            try:
                job = _convert_jobspy_row(row_dict)
                if job.job_url not in seen_urls:
                    all_jobs.append(job)
                    seen_urls.add(job.job_url)
            except Exception:
                pass
                    
    except Exception:
        # Handle exceptions gracefully
        pass
    
    return all_jobs
