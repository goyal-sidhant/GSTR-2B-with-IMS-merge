# utils/file_utils.py
"""
File utility functions for GST Processing Tool v5.0

Contains helper functions for:
- Checking file names against patterns
- Extracting client info from file names
- Finding extra files
- Organizing files by client
"""

import re
from pathlib import Path
from typing import List, Tuple, Optional, Set, Dict
from collections import defaultdict

from utils.constants import GSTR2B_PATTERN, IMS_PATTERN


def check_file_month(filename: str, target_month: str, target_year: str) -> bool:
    """
    Check if a file name contains the specified month and year.
    
    The file name format expected: 
    Something-Something-MMM YYYY.xlsx or Something-MMM YYYY (N).xlsx
    
    Args:
        filename: The file name (without path) to check
        target_month: Three-letter month (e.g., "May")
        target_year: Four-digit year (e.g., "2025")
    
    Returns:
        True if the file matches the month and year
    
    Example:
        check_file_month("GSTR2B-ABC Corp-27-May 2025.xlsx", "May", "2025")
        Returns: True
    """
    # Pattern looks for: -MMM YYYY at the end (optionally with (N) suffix)
    pattern = r'-(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+(\d{4})(\s*\(\d+\))?'
    match = re.search(pattern, filename)
    
    if match:
        month_in_file = match.group(1)
        year_in_file = match.group(2)
        return month_in_file == target_month and year_in_file == target_year
    
    return False


def extract_client_info(filename: str, file_type: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Extract client name and state code from a file name.
    
    Args:
        filename: The file name to parse
        file_type: Either "GSTR2B" or "IMS"
    
    Returns:
        Tuple of (client_name, state_code) or (None, None) if parsing fails
    
    Example:
        extract_client_info("GSTR2B-ABC Corporation-27-May 2025.xlsx", "GSTR2B")
        Returns: ("ABC Corporation", "27")
    """
    if file_type == "GSTR2B":
        pattern = GSTR2B_PATTERN
    else:  # IMS
        pattern = IMS_PATTERN
    
    match = re.search(pattern, filename)
    
    if match:
        client_name = match.group(1)
        # Remove any (N) suffix from client name (duplicate file indicator)
        client_name = re.sub(r'\s*\(\d+\)\s*$', '', client_name)
        state = match.group(2)
        return client_name, state
    
    return None, None


def extract_month_year_from_report(report_file: Path) -> Tuple[Optional[str], Optional[str]]:
    """
    Extract month and year from a report file name.
    
    Args:
        report_file: Path to the report file
    
    Returns:
        Tuple of (month, year) or (None, None) if not found
    
    Example:
        Path("GSTR-2B Processing Report May 2025.xlsx")
        Returns: ("May", "2025")
    """
    try:
        pattern = r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+(\d{4})'
        match = re.search(pattern, report_file.stem)
        if match:
            return match.group(1), match.group(2)
    except Exception:
        pass
    return None, None


def find_extra_files(input_path: Path, month: str, year: str) -> List[str]:
    """
    Find files in the folder that don't match expected patterns.
    
    These are files that won't be processed - the user should know about them.
    
    Args:
        input_path: Path to the input folder
        month: Target month
        year: Target year
    
    Returns:
        List of extra file names
    
    Example:
        Returns: ["Copy of GSTR2B-ABC.xlsx", "Notes.xlsx", "random.xlsx"]
    """
    extra_files = []
    all_files = list(input_path.glob("*.xlsx"))
    
    for file in all_files:
        filename = file.stem
        
        # Check if it's a valid GSTR-2B file for this month/year
        is_gstr2b = filename.startswith("GSTR2B-") and check_file_month(filename, month, year)
        
        # Check if it's a valid ImsReco file
        is_ims = filename.startswith("ImsReco-")
        
        # If it's neither, it's an extra file
        if not is_gstr2b and not is_ims:
            extra_files.append(file.name)
    
    return extra_files


def get_best_file(files: List[Path]) -> Optional[Path]:
    """
    From a list of similar files, pick the best one.
    
    If there are duplicate files (with (1), (2) suffix), prefer the numbered one
    as it's usually the newer/corrected version.
    
    Args:
        files: List of file paths
    
    Returns:
        The best file to use, or None if list is empty
    """
    if not files:
        return None
    
    # Look for files with " (1)", " (2)" etc. in the name
    duplicate_files = [f for f in files if re.search(r'\(\d+\)', f.stem)]
    
    if duplicate_files:
        # Return the first duplicate (usually "(1)" suffix)
        return duplicate_files[0]
    
    # If no duplicates, return the original file
    return files[0]


def create_output_folders(parent_dir: Path, month_year: str, timestamp: str) -> Tuple[Path, Path, Path]:
    """
    Create the output folder structure for processed files.
    
    Creates:
    - Main output folder
    - Processed Files subfolder (for merged files)
    - Created GSTR-2B Files subfolder (for newly created files)
    
    Args:
        parent_dir: Parent directory where output folder will be created
        month_year: String like "May 2025"
        timestamp: Timestamp string like "14062025_103045"
    
    Returns:
        Tuple of (main_folder, processed_folder, created_folder) paths
    """
    # Main output folder
    output_main_folder = parent_dir / f"GSTR-2B with IMS {month_year}_{timestamp}"
    output_main_folder.mkdir(exist_ok=True)
    
    # Subfolder for processed (merged) files
    processed_folder = output_main_folder / "Processed Files"
    processed_folder.mkdir(exist_ok=True)
    
    # Subfolder for newly created GSTR-2B files
    created_folder = output_main_folder / "Created GSTR-2B Files"
    created_folder.mkdir(exist_ok=True)
    
    return output_main_folder, processed_folder, created_folder


def organize_files_by_client(files: List[Path], file_type: str) -> Dict[str, List[Path]]:
    """
    Group files by client key (name-state combination).
    
    Args:
        files: List of file paths
        file_type: Either "GSTR2B" or "IMS"
    
    Returns:
        Dictionary mapping client_key to list of files
    
    Example:
        {
            "ABC Corp-27": [Path("GSTR2B-ABC Corp-27-May 2025.xlsx")],
            "XYZ Ltd-29": [Path("GSTR2B-XYZ Ltd-29-May 2025.xlsx")]
        }
    """
    client_files = defaultdict(list)
    
    for f in files:
        client_name, state = extract_client_info(f.stem, file_type)
        if client_name and state:
            key = f"{client_name}-{state}"
            client_files[key].append(f)
    
    return dict(client_files)


def get_unique_clients(gstr_files: Dict[str, List[Path]], 
                       ims_files: Dict[str, Path]) -> Set[str]:
    """
    Get all unique client keys from both GSTR-2B and IMS files.
    
    Args:
        gstr_files: Dictionary of GSTR-2B files by client
        ims_files: Dictionary of IMS files by client
    
    Returns:
        Set of all unique client keys
    """
    return set(gstr_files.keys()) | set(ims_files.keys())


def get_client_key(client_name: str, state: str) -> str:
    """
    Create a unique client key from name and state.
    
    Args:
        client_name: Client name
        state: State code
    
    Returns:
        Client key in format "ClientName-State"
    """
    return f"{client_name}-{state}"


def parse_client_key(client_key: str) -> Tuple[str, str]:
    """
    Parse a client key back into name and state.
    
    Args:
        client_key: Key in format "ClientName-State"
    
    Returns:
        Tuple of (client_name, state)
    """
    # Split on last hyphen only (client name might contain hyphens)
    parts = client_key.rsplit("-", 1)
    if len(parts) == 2:
        return parts[0], parts[1]
    return client_key, ""
