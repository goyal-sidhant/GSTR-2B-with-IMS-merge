# utils/date_utils.py
"""
Date and time utility functions for GST Processing Tool v5.0

Contains helper functions for:
- Getting current date/time in various formats
- Parsing month/year strings
- Financial year calculations
"""

import datetime
from typing import Tuple, Optional


def get_current_month_year() -> Tuple[str, str]:
    """
    Get the current month and year.
    
    Returns:
        Tuple of (month, year) where month is 3-letter abbreviation
    
    Example:
        Returns: ("Jun", "2025")
    """
    now = datetime.datetime.now()
    return now.strftime("%b"), str(now.year)


def format_timestamp() -> str:
    """
    Get formatted timestamp for file naming.
    
    Format: DDMMYYYY_HHMMSS
    
    Returns:
        Timestamp string like "14062025_103045"
    """
    return datetime.datetime.now().strftime("%d%m%Y_%H%M%S")


def format_datetime() -> str:
    """
    Get formatted datetime for display purposes.
    
    Format: DD/MM/YYYY HH:MM:SS AM/PM
    
    Returns:
        Datetime string like "14/06/2025 10:30:45 AM"
    """
    return datetime.datetime.now().strftime("%d/%m/%Y %I:%M:%S %p")


def format_log_timestamp() -> str:
    """
    Get formatted timestamp for log entries.
    
    Format: HH:MM:SS
    
    Returns:
        Time string like "10:30:45"
    """
    return datetime.datetime.now().strftime("%H:%M:%S")


def format_log_datetime() -> str:
    """
    Get formatted datetime for log file entries.
    
    Format: YYYY-MM-DD HH:MM:SS
    
    Returns:
        Datetime string like "2025-06-14 10:30:45"
    """
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def parse_month_year(month_year_str: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Parse month and year from a string.
    
    Expected format: "MMM YYYY" (e.g., "Jan 2024")
    
    Args:
        month_year_str: String in format "MMM YYYY"
    
    Returns:
        Tuple of (month, year) or (None, None) if parsing fails
    """
    valid_months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    
    try:
        parts = month_year_str.strip().split()
        if len(parts) == 2:
            month = parts[0]
            year = parts[1]
            
            # Validate month and year
            if month in valid_months and len(year) == 4 and year.isdigit():
                return month, year
    except Exception:
        pass
    
    return None, None


def get_financial_year(month: str, year: int) -> str:
    """
    Get financial year string based on month and year.
    
    In India, financial year runs from April to March.
    So May 2025 is in FY 2025-26, but Feb 2025 is in FY 2024-25.
    
    Args:
        month: Three-letter month abbreviation
        year: Year as integer
    
    Returns:
        Financial year string like "2025-26"
    
    Example:
        get_financial_year("May", 2025) returns "2025-26"
        get_financial_year("Feb", 2025) returns "2024-25"
    """
    # Months that belong to the previous financial year
    prev_fy_months = ["Jan", "Feb", "Mar"]
    
    if month in prev_fy_months:
        # FY started in previous calendar year
        return f"{year-1}-{str(year)[2:]}"
    else:
        # FY started in current calendar year
        return f"{year}-{str(year+1)[2:]}"


def month_to_number(month: str) -> int:
    """
    Convert month abbreviation to number (1-12).
    
    Args:
        month: Three-letter month abbreviation
    
    Returns:
        Month number (1-12) or 0 if invalid
    
    Example:
        month_to_number("Jan") returns 1
        month_to_number("Dec") returns 12
    """
    month_map = {
        "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4,
        "May": 5, "Jun": 6, "Jul": 7, "Aug": 8,
        "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12
    }
    return month_map.get(month, 0)


def number_to_month(month_num: int) -> str:
    """
    Convert month number to abbreviation.
    
    Args:
        month_num: Month number (1-12)
    
    Returns:
        Three-letter month abbreviation or empty string if invalid
    """
    month_list = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun",
                  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    
    if 1 <= month_num <= 12:
        return month_list[month_num]
    return ""


def get_previous_month_year(month: str, year: str) -> Tuple[str, str]:
    """
    Get the previous month and year.
    
    Args:
        month: Current month abbreviation
        year: Current year string
    
    Returns:
        Tuple of (previous_month, previous_year)
    
    Example:
        get_previous_month_year("Jan", "2025") returns ("Dec", "2024")
    """
    month_num = month_to_number(month)
    year_int = int(year)
    
    if month_num == 1:  # January
        return "Dec", str(year_int - 1)
    else:
        return number_to_month(month_num - 1), year


def sort_periods(periods: list) -> list:
    """
    Sort a list of period strings chronologically.
    
    Args:
        periods: List of strings like ["May 2025", "Apr 2025", "Jun 2025"]
    
    Returns:
        Sorted list: ["Apr 2025", "May 2025", "Jun 2025"]
    """
    def period_key(period_str):
        month, year = parse_month_year(period_str)
        if month and year:
            return (int(year), month_to_number(month))
        return (0, 0)
    
    return sorted(periods, key=period_key)
