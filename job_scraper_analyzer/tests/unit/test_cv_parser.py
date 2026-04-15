"""Tests for LaTeX CV parser to extract plain text for AI context.

RED PHASE: These tests define the expected behavior.
They will FAIL until the cv_parser module is implemented.
"""

from pathlib import Path
from typing import Generator

import pytest


class TestParseLatexFile:
    """Test suite for parse_latex_file() function."""

    @pytest.fixture
    def sample_latex_file(self, tmp_path: Path) -> Generator[Path, None, None]:
        """Create a sample LaTeX file for testing.
        
        Creates a file with common LaTeX commands that should be stripped.
        """
        content = r"""\cvsection{Summary}

\begin{cvparagraph}
  Software engineer with 5+ years of experience bridging hardware and full-stack development.
\end{cvparagraph}

\cvsection{Skills}

\begin{cvskills}  
  \cvskill{Languages}{  
    Python \skillsep
    C++ \skillsep
    JavaScript
  }
\end{cvskills}
"""
        file_path = tmp_path / "sample.tex"
        file_path.write_text(content, encoding="utf-8")
        yield file_path

    def test_parse_latex_file_extracts_text(self, sample_latex_file: Path) -> None:
        """Test that parse_latex_file() extracts plain text from LaTeX source.
        
        RED: parse_latex_file(file_path: Path) -> str must strip LaTeX commands
        and return human-readable text content.
        """
        from job_scraper_analyzer.cv_parser import parse_latex_file
        
        result = parse_latex_file(sample_latex_file)
        
        # The result should contain the meaningful text
        assert "Software engineer" in result, "Should extract text content"
        assert "5+ years" in result, "Should preserve description text"
        # Should NOT contain LaTeX commands
        assert "\\cvsection" not in result, "Should strip \\cvsection commands"
        assert "\\begin{" not in result, "Should strip \\begin{} blocks"
        assert "\\end{" not in result, "Should strip \\end{} blocks"

    def test_parse_latex_file_strips_commands(self, sample_latex_file: Path) -> None:
        """Test that LaTeX commands like \\textbf{}, \\href{} are stripped.
        
        RED: Common LaTeX formatting commands should be removed.
        """
        from job_scraper_analyzer.cv_parser import parse_latex_file
        
        result = parse_latex_file(sample_latex_file)
        
        assert "\\textbf" not in result, "Should strip \\textbf commands"
        assert "\\href" not in result, "Should strip \\href commands"
        assert "\\emph{" not in result, "Should strip \\emph commands"

    def test_parse_latex_file_handles_tex_file(self, tmp_path: Path) -> None:
        """Test that function accepts .tex file extension.
        
        RED: Function should work with .tex files.
        """
        from job_scraper_analyzer.cv_parser import parse_latex_file
        
        tex_file = tmp_path / "test.tex"
        tex_file.write_text(r"\cvsection{Test Section} Some content here", encoding="utf-8")
        
        result = parse_latex_file(tex_file)
        
        assert isinstance(result, str), "Should return a string"
        assert len(result) > 0, "Should return non-empty string for valid file"

    def test_parse_latex_file_raises_on_missing_file(self, tmp_path: Path) -> None:
        """Test that parse_latex_file() raises FileNotFoundError for missing files.
        
        RED: Function should raise appropriate error for missing files.
        """
        from job_scraper_analyzer.cv_parser import parse_latex_file
        
        missing_file = tmp_path / "nonexistent.tex"
        
        with pytest.raises(FileNotFoundError):
            parse_latex_file(missing_file)

    def test_parse_latex_file_handles_empty_file(self, tmp_path: Path) -> None:
        """Test that parse_latex_file() handles empty .tex files gracefully.
        
        RED: Empty files should return empty string.
        """
        from job_scraper_analyzer.cv_parser import parse_latex_file
        
        empty_file = tmp_path / "empty.tex"
        empty_file.write_text("", encoding="utf-8")
        
        result = parse_latex_file(empty_file)
        
        assert result == "", "Empty file should return empty string"

    def test_parse_latex_file_preserves_whitespace_for_readability(self, tmp_path: Path) -> None:
        """Test that whitespace is normalized for readability.
        
        RED: Multiple whitespace should be normalized but lines should be preserved.
        """
        from job_scraper_analyzer.cv_parser import parse_latex_file
        
        content = r"""First line
Second line

Third line"""
        file_path = tmp_path / "whitespace.tex"
        file_path.write_text(content, encoding="utf-8")
        
        result = parse_latex_file(file_path)
        
        assert "First line" in result
        assert "Second line" in result
        assert "Third line" in result


class TestParseCvDirectory:
    """Test suite for parse_cv_directory() function."""

    @pytest.fixture
    def cv_directory(self, tmp_path: Path) -> Generator[Path, None, None]:
        """Create a sample CV directory structure with multiple .tex files.
        
        Creates files for different CV sections that would be combined.
        """
        # Create cv subdirectory
        cv_dir = tmp_path / "cv"
        cv_dir.mkdir()
        
        # Summary section
        (cv_dir / "summary.tex").write_text(
            r"\cvsection{Summary}" + "\n" +
            r"\begin{cvparagraph}" + "\n" +
            r"  Experienced software engineer." + "\n" +
            r"\end{cvparagraph}",
            encoding="utf-8"
        )
        
        # Skills section
        (cv_dir / "skills.tex").write_text(
            r"\cvsection{Skills}" + "\n" +
            r"\begin{cvskills}" + "\n" +
            r"  \cvskill{Python}{ Django \skillsep Flask }" + "\n" +
            r"\end{cvskills}",
            encoding="utf-8"
        )
        
        # Experience section
        (cv_dir / "experience.tex").write_text(
            r"\cvsection{Experience}" + "\n" +
            r"\cventry{Engineer}{Company}{Location}{2020 -- 2024}{" + "\n" +
            r"  \begin{cvitems}" + "\n" +
            r"    \item Built scalable systems" + "\n" +
            r"  \end{cvitems}" + "\n" +
            r"}",
            encoding="utf-8"
        )
        
        yield cv_dir

    def test_parse_cv_directory_returns_combined_text(self, cv_directory: Path) -> None:
        """Test that parse_cv_directory() combines text from multiple .tex files.
        
        RED: parse_cv_directory(cv_dir: Path) -> str should read all .tex files
        in the directory and combine their text content.
        """
        from job_scraper_analyzer.cv_parser import parse_cv_directory
        
        result = parse_cv_directory(cv_directory)
        
        assert isinstance(result, str), "Should return a string"
        assert len(result) > 0, "Should return non-empty combined text"
        # Should contain content from multiple files
        assert "software engineer" in result.lower() or "engineer" in result.lower()
        assert "skills" in result.lower() or "python" in result.lower()

    def test_parse_cv_directory_parses_all_tex_files(self, cv_directory: Path) -> None:
        """Test that all .tex files in directory are processed.
        
        RED: Should find and parse summary.tex, skills.tex, experience.tex.
        """
        from job_scraper_analyzer.cv_parser import parse_cv_directory
        
        result = parse_cv_directory(cv_directory)
        
        # Content from summary.tex
        assert "experienced" in result.lower() or "software" in result.lower()
        # Content from skills.tex
        assert "python" in result.lower() or "django" in result.lower()
        # Content from experience.tex
        assert "engineer" in result.lower() or "company" in result.lower()

    def test_parse_cv_directory_strips_latex_commands(self, cv_directory: Path) -> None:
        """Test that combined text has LaTeX commands stripped.
        
        RED: The combined result should have all LaTeX markup removed.
        """
        from job_scraper_analyzer.cv_parser import parse_cv_directory
        
        result = parse_cv_directory(cv_directory)
        
        assert "\\cvsection" not in result, "Should strip \\cvsection commands"
        assert "\\begin{" not in result, "Should strip \\begin blocks"
        assert "\\end{" not in result, "Should strip \\end blocks"
        assert "\\cvskill" not in result, "Should strip \\cvskill commands"
        assert "\\cventry" not in result, "Should strip \\cventry commands"

    def test_parse_cv_directory_raises_on_missing_directory(self, tmp_path: Path) -> None:
        """Test that parse_cv_directory() raises error for missing directory.
        
        RED: Should raise FileNotFoundError or NotADirectoryError.
        """
        from job_scraper_analyzer.cv_parser import parse_cv_directory
        
        missing_dir = tmp_path / "nonexistent_cv"
        
        with pytest.raises((FileNotFoundError, NotADirectoryError)):
            parse_cv_directory(missing_dir)

    def test_parse_cv_directory_handles_empty_directory(self, tmp_path: Path) -> None:
        """Test that parse_cv_directory() handles directory with no .tex files.
        
        RED: Empty directory should return empty string.
        """
        from job_scraper_analyzer.cv_parser import parse_cv_directory
        
        empty_dir = tmp_path / "empty_cv"
        empty_dir.mkdir()
        
        result = parse_cv_directory(empty_dir)
        
        assert result == "", "Empty directory should return empty string"


class TestExtractCvSummary:
    """Test suite for extract_cv_summary() function."""

    def test_extract_cv_summary_truncates_to_max_length(self) -> None:
        """Test that extract_cv_summary() truncates text to max_length.
        
        RED: extract_cv_summary(text: str, max_length: int = 500) -> str
        should truncate text to approximately max_length characters.
        """
        from job_scraper_analyzer.cv_parser import extract_cv_summary
        
        long_text = "A" * 1000  # 1000 character text
        
        result = extract_cv_summary(long_text, max_length=500)
        
        assert len(result) <= 500, f"Result should be truncated to max_length, got {len(result)}"

    def test_extract_cv_summary_default_max_length_is_500(self) -> None:
        """Test that default max_length is 500 characters.
        
        RED: When max_length not specified, should default to 500.
        """
        from job_scraper_analyzer.cv_parser import extract_cv_summary
        
        long_text = "B" * 600
        
        result = extract_cv_summary(long_text)
        
        assert len(result) <= 500, "Default max_length should be 500"

    def test_extract_cv_summary_returns_unchanged_when_short(self) -> None:
        """Test that short text is returned unchanged.
        
        RED: Text shorter than max_length should be returned as-is.
        """
        from job_scraper_analyzer.cv_parser import extract_cv_summary
        
        short_text = "Short CV summary text"
        
        result = extract_cv_summary(short_text, max_length=500)
        
        assert result == short_text, "Short text should be returned unchanged"

    def test_extract_cv_summary_preserves_word_boundaries(self) -> None:
        """Test that truncation happens at word boundaries where possible.
        
        RED: Should not cut words in the middle when truncating.
        """
        from job_scraper_analyzer.cv_parser import extract_cv_summary
        
        text = "word1 word2 word3 word4 word5 word6 word7 word8 word9 word10"
        
        result = extract_cv_summary(text, max_length=50)
        
        # Should not end with a partial word
        if len(result) < len(text):
            assert result[-1].isalnum() or result.endswith(" "), \
                "Should truncate at word boundary"

    def test_extract_cv_summary_returns_string_type(self) -> None:
        """Test that extract_cv_summary() always returns a string.
        
        RED: Return type should always be str, even for edge cases.
        """
        from job_scraper_analyzer.cv_parser import extract_cv_summary
        
        result = extract_cv_summary("")
        
        assert isinstance(result, str), "Should always return a string"
        assert result == "", "Empty input should return empty string"

    def test_extract_cv_summary_with_very_long_words(self) -> None:
        """Test truncation with words longer than max_length.
        
        RED: Should handle words that exceed max_length individually.
        """
        from job_scraper_analyzer.cv_parser import extract_cv_summary
        
        # A single word longer than max_length
        long_word = "A" * 600
        
        result = extract_cv_summary(long_word, max_length=500)
        
        # Should return truncated version of the long word
        assert len(result) <= 500
        assert result.startswith("A")


class TestCvParserIntegration:
    """Integration tests for CV parser workflow."""

    def test_full_pipeline_parse_file_then_summarize(self, tmp_path: Path) -> None:
        """Test the full workflow: parse LaTeX file, then extract summary.
        
        RED: Full pipeline should work end-to-end.
        """
        from job_scraper_analyzer.cv_parser import parse_latex_file, extract_cv_summary
        
        # Create a test file
        tex_file = tmp_path / "test_cv.tex"
        content = (
            r"\cvsection{Summary}" + "\n" +
            r"Software engineer with extensive experience in Python, " +
            r"C++, and JavaScript. Skilled in web development, " +
            r"embedded systems, and cloud architecture. " +
            r"Looking for challenging opportunities."
        )
        tex_file.write_text(content, encoding="utf-8")
        
        # Parse the file
        parsed_text = parse_latex_file(tex_file)
        
        # Extract summary
        summary = extract_cv_summary(parsed_text, max_length=200)
        
        assert isinstance(summary, str)
        assert len(summary) <= 200
        # Key content should be preserved
        assert "software engineer" in summary.lower() or "python" in summary.lower()

    def test_cv_parser_with_real_cv_structure(self, tmp_path: Path) -> None:
        """Test with realistic CV section structure.
        
        RED: Should handle structure similar to actual CV files.
        """
        from job_scraper_analyzer.cv_parser import parse_latex_file, extract_cv_summary
        
        # Create files mimicking real CV structure
        cv_dir = tmp_path / "cv"
        cv_dir.mkdir()
        
        (cv_dir / "summary.tex").write_text(
            r"\cvsection{Summary}" + "\n" +
            r"\begin{cvparagraph}" + "\n" +
            r"  Software engineer with 5+ years experience." + "\n" +
            r"\end{cvparagraph}",
            encoding="utf-8"
        )
        
        (cv_dir / "skills.tex").write_text(
            r"\cvsection{Skills}" + "\n" +
            r"\begin{cvskills}" + "\n" +
            r"  \cvskill{Languages}{ Python \skillsep C++ \skillsep SQL }" + "\n" +
            r"  \cvskill{Frameworks}{ Django \skillsep React \skillsep Phoenix }" + "\n" +
            r"\end{cvskills}",
            encoding="utf-8"
        )
        
        from job_scraper_analyzer.cv_parser import parse_cv_directory
        
        combined = parse_cv_directory(cv_dir)
        summary = extract_cv_summary(combined, max_length=300)
        
        # Should extract key information
        assert len(summary) <= 300
        # Key terms should be present
        content_lower = summary.lower()
        has_skill_info = any(term in content_lower for term in ["python", "skill", "language"])


class TestCvParserEdgeCases:
    """Test suite for edge case handling in CV parser."""

    def test_handles_non_utf8_encoding(self, tmp_path: Path) -> None:
        """Test handling of files with various encodings.
        
        RED: Should handle common encodings gracefully.
        """
        from job_scraper_analyzer.cv_parser import parse_latex_file
        
        # Create file with UTF-8 content including special characters
        tex_file = tmp_path / "unicode.tex"
        content = r"\cvsection{Skills}" + "\nPython \skillsep C++ \skillsep JavaScript"
        tex_file.write_text(content, encoding="utf-8")
        
        result = parse_latex_file(tex_file)
        
        assert isinstance(result, str)
        assert "Python" in result

    def test_handles_nested_latex_commands(self, tmp_path: Path) -> None:
        """Test handling of nested or complex LaTeX structures.
        
        RED: Should strip deeply nested commands.
        """
        from job_scraper_analyzer.cv_parser import parse_latex_file
        
        tex_file = tmp_path / "nested.tex"
        content = (
            r"\cvsection{Experience}" + "\n" +
            r"\cventry{Engineer}{Company}{Location}{2020 -- 2024}{" + "\n" +
            r"  \begin{cvitems}" + "\n" +
            r"    \item Worked on \textbf{\emph{nested}} commands" + "\n" +
            r"  \end{cvitems}" + "\n" +
            r"}"
        )
        tex_file.write_text(content, encoding="utf-8")
        
        result = parse_latex_file(tex_file)
        
        assert "\\textbf" not in result
        assert "\\emph" not in result
        assert "nested" in result

    def test_handles_macros_like_skillsep(self, tmp_path: Path) -> None:
        """Test that custom macros like \\skillsep are handled.
        
        RED: Should either strip or normalize custom command definitions.
        """
        from job_scraper_analyzer.cv_parser import parse_latex_file
        
        tex_file = tmp_path / "macro.tex"
        # Simulate the skillsep macro definition and usage
        content = (
            r"\newcommand\skillsep{\enspace\textbar\enspace}" + "\n" +
            r"Python \skillsep C++ \skillsep JavaScript"
        )
        tex_file.write_text(content, encoding="utf-8")
        
        result = parse_latex_file(tex_file)
        
        # Should strip the \skillsep command but preserve the content
        assert "\\skillsep" not in result or "enspace" not in result
        assert "Python" in result
        assert "C++" in result or "C" in result
