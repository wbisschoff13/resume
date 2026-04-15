"""LaTeX CV parser to extract plain text for AI context."""

import re
from pathlib import Path
from typing import Optional

# Pre-compiled regex patterns for LaTeX command stripping
_LATEX_CMD_WITH_BRACES = re.compile(r'\\[a-zA-Z]+\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}')
_LATEX_CMD_WITHOUT_BRACES = re.compile(r'\\[a-zA-Z]+')
_LATEX_NEWCOMMAND_DEF = re.compile(r"\\newcommand\{[^}]*\}\{[^}]*\}")
_LATEX_BEGIN_END = re.compile(r"\\(?:begin|end)\s*\{[^}]*\}")
_WHITESPACE_COLLAPSE = re.compile(r"[ \t]+")
_BLANK_LINES_COLLAPSE = re.compile(r"\n{3,}")
_SKILLSEP_NORMALIZE = re.compile(r"\\skillsep")


def _strip_latex_commands(text: str) -> str:
    """Strip LaTeX commands from text, preserving content in braces.
    
    Args:
        text: LaTeX text
        
    Returns:
        Plain text with commands stripped
    """
    # Extract content from all brace groups after a command
    def extract_cmd_content(match: re.Match) -> str:
        full = match.group(0)
        contents = re.findall(r'\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}', full)
        return " ".join(contents)
    
    # Iteratively strip commands until no change (handles nested commands)
    prev = text
    for _ in range(10):
        text = _LATEX_CMD_WITH_BRACES.sub(extract_cmd_content, text)
        if text == prev:
            break
        prev = text
    
    # Remove remaining commands without braces
    text = _LATEX_CMD_WITHOUT_BRACES.sub('', text)
    
    return text


def parse_latex_file(file_path: Path) -> str:
    """Extract plain text from a LaTeX file.
    
    Strips LaTeX commands and returns human-readable text content.
    
    Args:
        file_path: Path to the .tex file
        
    Returns:
        Plain text extracted from the LaTeX file
        
    Raises:
        FileNotFoundError: If the file does not exist
    """
    if not file_path.exists():
        raise FileNotFoundError(f"LaTeX file not found: {file_path}")
    
    content = file_path.read_text(encoding="utf-8")
    
    if not content.strip():
        return ""
    
    # Remove LaTeX command definitions like \newcommand{\skillsep}{...}
    content = _LATEX_NEWCOMMAND_DEF.sub('', content)
    
    # Remove skillsep macros and normalize whitespace
    content = _SKILLSEP_NORMALIZE.sub(" | ", content)
    
    # Strip all LaTeX commands, preserving content in braces
    content = _strip_latex_commands(content)
    
    # Remove remaining \begin{...} and \end{...} blocks
    content = _LATEX_BEGIN_END.sub('', content)
    
    # Normalize whitespace: collapse multiple spaces/tabs to single space
    content = _WHITESPACE_COLLAPSE.sub(' ', content)
    
    # Normalize newlines: collapse multiple blank lines to single newline
    content = _BLANK_LINES_COLLAPSE.sub('\n\n', content)
    
    # Remove leading/trailing whitespace from each line
    lines = [line.strip() for line in content.split("\n")]
    
    # Filter out empty lines at start/end
    while lines and not lines[0]:
        lines.pop(0)
    while lines and not lines[-1]:
        lines.pop()
    
    return "\n".join(lines)


def _parse_single_file(tex_file: Path) -> Optional[str]:
    """Parse a single .tex file and return plain text, or None on error.
    
    Args:
        tex_file: Path to the .tex file
        
    Returns:
        Plain text content or None if file cannot be read
    """
    try:
        text = parse_latex_file(tex_file)
        return text if text else None
    except (FileNotFoundError, UnicodeDecodeError):
        return None


def parse_cv_directory(cv_dir: Path) -> str:
    """Parse all .tex files in a CV directory and combine their text.
    
    Args:
        cv_dir: Path to directory containing .tex files
        
    Returns:
        Combined plain text from all .tex files in the directory
        
    Raises:
        FileNotFoundError: If the directory does not exist
        NotADirectoryError: If the path is not a directory
    """
    if not cv_dir.exists():
        raise FileNotFoundError(f"CV directory not found: {cv_dir}")
    
    if not cv_dir.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {cv_dir}")
    
    # Find all .tex files in the directory
    tex_files = sorted(cv_dir.glob("*.tex"))
    
    if not tex_files:
        return ""
    
    # Parse each file and combine results
    results = [
        text for tex_file in tex_files
        if (text := _parse_single_file(tex_file)) is not None
    ]
    
    # Combine all results with double newline separation
    return "\n\n".join(results)


def extract_cv_summary(text: str, max_length: int = 500) -> str:
    """Extract a summary from CV text, truncating to max_length.
    
    Truncates at word boundaries to avoid cutting words in the middle.
    
    Args:
        text: The full CV text
        max_length: Maximum length of the returned summary (default: 500)
        
    Returns:
        Truncated text that fits within max_length characters
    """
    if not text:
        return ""
    
    if len(text) <= max_length:
        return text
    
    # Find the last space before max_length to avoid cutting words
    truncated = text[:max_length]
    last_space = truncated.rfind(" ")
    
    if last_space > max_length * 0.8:
        # If space is found and it's not too far back, cut there
        return truncated[:last_space].strip()
    else:
        # Otherwise just cut at max_length
        return truncated.strip()
