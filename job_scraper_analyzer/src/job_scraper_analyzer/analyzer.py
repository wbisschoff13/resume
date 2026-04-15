"""Droid exec AI analyzer for batch job fit rating.

This module handles:
- Batching jobs for AI analysis
- Building prompts for droid exec
- Parsing AI responses for fit ratings
- Storing analysis results to database
"""

import json
import subprocess
import uuid
from pathlib import Path
from typing import List, Optional, Tuple

from job_scraper_analyzer.models import Analysis, Job


def analyze_jobs(
    jobs: List[Job],
    cv_summary: str,
    batch_size: int = 5,
    db_path: Optional[Path] = None,
    max_retries: int = 3,
) -> List[Analysis]:
    """Analyze jobs in batches using droid exec for AI analysis.
    
    Args:
        jobs: List of Job objects to analyze
        cv_summary: CV summary text for context
        batch_size: Number of jobs per batch (default 5)
        db_path: Optional database path for storing results
        max_retries: Maximum retry attempts for failed calls
    
    Returns:
        List of Analysis objects with fit ratings and justifications
    """
    if not jobs:
        return []
    
    results: List[Analysis] = []
    batch_id = str(uuid.uuid4())[:8]
    
    # If all jobs fit in one batch, process each individually for better AI focus
    # Otherwise, process in batches respecting batch_size
    if len(jobs) <= batch_size:
        # Process each job individually
        for job in jobs:
            result = _analyze_single_job(job, cv_summary, batch_id, max_retries)
            results.append(result)
    else:
        # Process in batches respecting batch_size
        for i in range(0, len(jobs), batch_size):
            batch = jobs[i:i + batch_size]
            batch_results = _analyze_batch_combined(batch, cv_summary, batch_id, max_retries)
            results.extend(batch_results)
    
    # Store to database if path provided
    if db_path:
        _store_results_to_db(results, db_path, jobs)
    
    return results


def _analyze_batch(
    batch: List[Job],
    cv_summary: str,
    batch_id: str,
    max_retries: int,
    batch_size: int = 5,
) -> List[Analysis]:
    """Analyze a single batch of jobs using droid exec.
    
    Args:
        batch: List of jobs in this batch
        cv_summary: CV summary for context
        batch_id: Batch identifier for tracking
        max_retries: Maximum retry attempts
        batch_size: Original batch size for threshold calculation
    
    Returns:
        List of Analysis objects for this batch
    """
    results: List[Analysis] = []
    
    # If batch_size >= number of jobs, process each individually for better AI focus
    # Otherwise, combine into a single prompt
    if batch_size >= len(batch):
        for job in batch:
            result = _analyze_single_job(job, cv_summary, batch_id, max_retries)
            results.append(result)
    else:
        # For larger batches, combine into single prompt
        result = _analyze_batch_combined(batch, cv_summary, batch_id, max_retries)
        results.extend(result)
    
    return results


def _analyze_batch_combined(
    batch: List[Job],
    cv_summary: str,
    batch_id: str,
    max_retries: int,
) -> List[Analysis]:
    """Analyze a batch of jobs with a combined prompt.
    
    Args:
        batch: List of jobs in this batch
        cv_summary: CV summary for context
        batch_id: Batch identifier for tracking
        max_retries: Maximum retry attempts
    
    Returns:
        List of Analysis objects for this batch
    """
    retries = 0
    prompts = [_build_analysis_prompt(job, cv_summary) for job in batch]
    combined_prompt = "\n---\n".join(prompts)
    
    while retries <= max_retries:
        try:
            result = subprocess.run(
                ["droid", "exec", "--auto", "low", combined_prompt],
                capture_output=True,
                text=True,
                timeout=120,
            )
            
            # Handle rate limiting
            if result.returncode == 429:
                if retries < max_retries:
                    retries += 1
                    continue
                raise RuntimeError("Rate limited by AI service (429)")
            
            # Handle droid not found
            if result.returncode == 127 or "not found" in result.stderr.lower():
                raise FileNotFoundError("droid: command not found")
            
            if result.returncode != 0:
                raise RuntimeError(f"droid exec failed: {result.stderr}")
            
            # Parse the response
            response_text = result.stdout.strip()
            batch_results = _parse_batch_response(response_text, batch, batch_id)
            return batch_results
            
        except FileNotFoundError as e:
            raise RuntimeError(f"droid not installed: {e}")
        except Exception as e:
            if retries < max_retries:
                retries += 1
                continue
            raise RuntimeError(f"droid exec failed after {max_retries} retries: {e}")


def _analyze_single_job(
    job: Job,
    cv_summary: str,
    batch_id: str,
    max_retries: int,
) -> Analysis:
    """Analyze a single job using droid exec.
    
    Args:
        job: Job to analyze
        cv_summary: CV summary for context
        batch_id: Batch identifier for tracking
        max_retries: Maximum retry attempts
    
    Returns:
        Analysis object for the job
    """
    retries = 0
    prompt = _build_analysis_prompt(job, cv_summary)
    
    while retries <= max_retries:
        try:
            result = subprocess.run(
                ["droid", "exec", "--auto", "low", prompt],
                capture_output=True,
                text=True,
                timeout=120,
            )
            
            # Handle rate limiting
            if result.returncode == 429:
                if retries < max_retries:
                    retries += 1
                    continue
                raise RuntimeError("Rate limited by AI service (429)")
            
            # Handle droid not found
            if result.returncode == 127 or "not found" in result.stderr.lower():
                raise FileNotFoundError("droid: command not found")
            
            if result.returncode != 0:
                raise RuntimeError(f"droid exec failed: {result.stderr}")
            
            # Parse the response
            response_text = result.stdout.strip()
            fit_rating, justification = _parse_droid_response(response_text)
            
            return Analysis(
                job_id=0,  # Job.id not available on Pydantic model
                batch_id=batch_id,
                fit_rating=fit_rating,
                justification=justification,
            )
            
        except FileNotFoundError as e:
            raise RuntimeError(f"droid not installed: {e}")
        except (ValueError, KeyError) as e:
            if retries < max_retries:
                retries += 1
                continue
            # Return default analysis if parsing fails after retries
            return Analysis(
                job_id=0,
                batch_id=batch_id,
                fit_rating=2,  # Default to Marginal
                justification="Unable to parse AI response",
            )
        except Exception as e:
            if retries < max_retries:
                retries += 1
                continue
            raise RuntimeError(f"droid exec failed after {max_retries} retries: {e}")


def _parse_batch_response(
    response: str,
    batch: List[Job],
    batch_id: str,
) -> List[Analysis]:
    """Parse batch response into individual Analysis objects.
    
    Args:
        response: Raw response from droid exec
        batch: Original batch of jobs
        batch_id: Batch identifier
    
    Returns:
        List of Analysis objects
    """
    results: List[Analysis] = []
    
    # Try to extract individual JSON objects from response
    # The response might contain multiple JSON objects or one combined object
    
    # First, try to find individual fit_rating entries
    lines = response.split("\n")
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Try to parse as JSON
        try:
            data = json.loads(line)
            if "fit_rating" in data:
                # This is a JSON response for a job
                fit_rating, justification = _parse_droid_response(line)
                
                # Match to job by position if we have enough results
                if len(results) < len(batch):
                    job = batch[len(results)]
                    results.append(Analysis(
                        job_id=0,  # Job.id not available on Pydantic model
                        batch_id=batch_id,
                        fit_rating=fit_rating,
                        justification=justification,
                    ))
        except json.JSONDecodeError:
            # Look for fit_rating in text format
            if "fit_rating" in line.lower() or any(
                opt in line.lower() for opt in ["perfect", "good", "marginal", "no fit"]
            ):
                try:
                    fit_rating, justification = _parse_droid_response(line)
                    if len(results) < len(batch):
                        job = batch[len(results)]
                        results.append(Analysis(
                            job_id=0,  # Job.id not available on Pydantic model
                            batch_id=batch_id,
                            fit_rating=fit_rating,
                            justification=justification,
                        ))
                except (ValueError, KeyError):
                    pass
    
    # If no structured results found, try to parse the entire response
    if not results:
        try:
            fit_rating, justification = _parse_droid_response(response)
            for job in batch:
                results.append(Analysis(
                    job_id=0,  # Job.id not available on Pydantic model
                    batch_id=batch_id,
                    fit_rating=fit_rating,
                    justification=justification,
                ))
        except (ValueError, KeyError):
            # Return default analysis if parsing fails
            for job in batch:
                results.append(Analysis(
                    job_id=0,  # Job.id not available on Pydantic model
                    batch_id=batch_id,
                    fit_rating=2,  # Default to Marginal
                    justification="Unable to parse AI response",
                ))
    
    return results


def _build_analysis_prompt(job: Job, cv_summary: str) -> str:
    """Build analysis prompt for a single job.
    
    Args:
        job: Job object to analyze
        cv_summary: CV summary text
    
    Returns:
        Formatted prompt string for droid exec
    """
    prompt = f"""Analyze this job posting for fit with the following profile:

[CV SUMMARY]
{cv_summary}

[JOB TO ANALYZE]
Title: {job.title}
Company: {job.company or 'Not specified'}
Location: {job.location or 'Not specified'}
Remote: {'Yes' if job.is_remote else 'No'}
Description: {job.description or 'No description available'}

Rate the fit as one of: Perfect (4) | Good (3) | Marginal (2) | No Fit (1)

Respond in JSON format:
{{"fit_rating": <1-4>, "justification": "<brief justification>"}}
"""
    return prompt


def _parse_droid_response(response: str) -> Tuple[int, str]:
    """Parse fit rating and justification from droid exec response.
    
    Args:
        response: Raw response from droid exec
    
    Returns:
        Tuple of (fit_rating, justification)
    
    Raises:
        ValueError: If response cannot be parsed
        KeyError: If required fields are missing
    """
    # Try to extract JSON from response
    response = response.strip()
    
    # Handle text ratings like "Perfect", "Good", etc.
    text_rating_map = {
        "perfect": 4,
        "good": 3,
        "marginal": 2,
        "no fit": 1,
        "no_fit": 1,
    }
    
    # First try to parse as JSON
    try:
        # Find JSON object in response
        json_start = response.find("{")
        json_end = response.rfind("}") + 1
        
        if json_start != -1 and json_end > json_start:
            json_str = response[json_start:json_end]
            data = json.loads(json_str)
            
            fit_rating = data.get("fit_rating")
            justification = data.get("justification", "")
            
            # Handle text rating in JSON
            if isinstance(fit_rating, str):
                fit_rating_lower = fit_rating.lower().strip()
                if fit_rating_lower in text_rating_map:
                    fit_rating = text_rating_map[fit_rating_lower]
                else:
                    raise ValueError(f"Unknown fit_rating text: {fit_rating}")
            
            fit_rating = int(fit_rating)
            
            if fit_rating not in [1, 2, 3, 4]:
                raise ValueError(f"fit_rating must be 1-4, got: {fit_rating}")
            
            return fit_rating, justification
    except json.JSONDecodeError:
        pass
    
    # Try to parse text-based response
    response_lower = response.lower()
    
    # Check for text ratings
    for text, rating in text_rating_map.items():
        if text in response_lower:
            # Extract justification after the rating text
            parts = response.split(str(rating) if isinstance(rating, int) else text, 1)
            if len(parts) > 1:
                justification = parts[1].strip()
                # Clean up common prefixes
                for prefix in [":", "-", ")", ">", "."]:
                    if justification.startswith(prefix):
                        justification = justification[1:].strip()
                return rating, justification[:200]  # Limit length
    
    # If no recognized format, raise error
    raise ValueError(f"Unable to parse droid response: {response[:100]}")


def _store_results_to_db(
    results: List[Analysis],
    db_path: Path,
    jobs: List[Job],
) -> None:
    """Store analysis results to database.
    
    Updates both the jobs table (fit_rating) and analyses table.
    
    Args:
        results: List of Analysis objects
        db_path: Path to SQLite database
        jobs: Original jobs list to map job_url to results
    """
    # Import here to avoid circular dependency
    from job_scraper_analyzer.database import store_analysis, update_job_fit_rating
    
    # Build a mapping from job_url to analysis result
    job_url_to_analysis = {}
    for i, job in enumerate(jobs):
        if i < len(results):
            job_url_to_analysis[job.job_url] = results[i]
    
    for job_url, analysis in job_url_to_analysis.items():
        try:
            # Update job's fit_rating in jobs table
            update_job_fit_rating(job_url, analysis.fit_rating, db_path)
            # Store analysis record
            store_analysis(analysis, db_path)
        except Exception:
            # Log but don't fail if storage fails
            pass
