# utils/constants.py
"""
Constants used throughout the GST Processing Tool v5.0

This file contains all fixed values that don't change during runtime.
Keeping them in one place makes it easy to update if needed.
"""

from enum import Enum

# =============================================================================
# FILE PATTERNS
# =============================================================================
# These patterns are used to identify and parse file names

# Pattern for GSTR-2B files
# Example: GSTR2B-ABC Corporation-27-May 2025.xlsx
# Groups: (1) Client Name, (2) State Code, (3) Month, (4) Year
GSTR2B_PATTERN = r'GSTR2B-(.+)-([^-]+)-(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+(\d{4})'

# Pattern for IMS Reco files
# Example: ImsReco-ABC Corporation-27-May 2025.xlsx
# Groups: (1) Client Name, (2) State Code
IMS_PATTERN = r'ImsReco-(.+)-([^-]+)-'

# =============================================================================
# MONTHS AND YEARS
# =============================================================================

# Standard month list
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# Financial year order (April to March) - used for dropdowns
FINANCIAL_YEAR_MONTHS = ["Apr", "May", "Jun", "Jul", "Aug", "Sep", 
                         "Oct", "Nov", "Dec", "Jan", "Feb", "Mar"]

# Years range for dropdown
YEARS_RANGE = list(range(2020, 2031))  # 2020 to 2030

# =============================================================================
# STATUS TYPES
# =============================================================================

class StatusType(Enum):
    """
    Status types for client processing results.
    Used for color coding and categorization.
    """
    SUCCESS = "Success"      # Successfully merged both files
    ERROR = "Error"          # Processing failed
    WARNING = "Warning"      # Processed but with issues (e.g., no IMS)
    CREATED = "Created"      # New GSTR-2B created from IMS
    NONE = "None"            # Default state

# =============================================================================
# ERROR CODES
# =============================================================================

class ErrorCode(Enum):
    """
    Error codes for identifying specific issues.
    Used to provide helpful error messages and suggestions.
    """
    FILE_NOT_FOUND = "file_not_found"
    FILENAME_PARSE_ERROR = "filename_parse_error"
    IMS_SHEET_MISSING = "ims_sheet_missing"
    CREATION_ERROR = "creation_error"
    FILE_LOCKED = "file_locked"
    GENERAL_ERROR = "general_error"

# =============================================================================
# CATEGORY TYPES (NEW in v5.0)
# =============================================================================

class CategoryType(Enum):
    """
    Categories for client files - determines what action will be taken.
    Displayed in the client table and preview section.
    """
    MERGE = "Merge"       # Has both GSTR-2B and IMS - will merge
    CREATE = "Create"     # Has only IMS - will create GSTR-2B
    COPY = "Copy"         # Has only GSTR-2B - will copy with warning

# =============================================================================
# FILE STATUS (for client table display)
# =============================================================================

class FileStatus(Enum):
    """
    File availability status for each client.
    Shown in the client table.
    """
    BOTH = "✓ Both"           # Has both GSTR-2B and IMS
    GSTR_ONLY = "GSTR Only"   # Has only GSTR-2B
    IMS_ONLY = "IMS Only"     # Has only IMS

# =============================================================================
# EXCEL COLORS (for report generation)
# =============================================================================

class ExcelColors:
    """
    Colors used in Excel report generation.
    Hex color codes without the # symbol.
    """
    ERROR_RED = "FFFF0000"      # Red for errors
    WARNING_ORANGE = "FFFFA500"  # Orange for warnings
    CREATED_BLUE = "FF87CEEB"    # Light blue for created files
    SUCCESS_GREEN = "FF90EE90"   # Light green for success
    HEADER_BLUE = "FF4472C4"     # Dark blue for headers
    
    # Tab colors (shorter format)
    TAB_BLUE = "4472C4"
    TAB_GREEN = "70AD47"
    TAB_ORANGE = "FFA500"

# =============================================================================
# REPORT SHEET NAMES
# =============================================================================

class SheetNames:
    """
    Names for sheets in the generated Excel report.
    """
    SUMMARY = "Summary"
    DETAILED_REPORT = "Detailed Report"
    ERROR_DETAILS = "Error Details"
    EXTRA_FILES = "Extra Files"
    
    # Comparison sheets (only if comparison reports added)
    MONTHLY_TRENDS = "Monthly Trends"
    ERROR_ANALYTICS = "Error Analytics"
    EFFICIENCY_DASHBOARD = "Efficiency Dashboard"
    CLIENT_JOURNEY = "Client Journey Tracker"
    EXECUTIVE_DASHBOARD = "Executive Dashboard"
    ACTION_ITEMS = "Action Items"

# =============================================================================
# APPLICATION SETTINGS
# =============================================================================

# Maximum number of comparison reports allowed
MAX_COMPARISON_FILES = 12

# Log file name
LOG_FILE_NAME = "gst_tool.log"

# Application info
APP_NAME = "GST Processing Tool"
APP_VERSION = "5.0"
APP_TITLE = f"{APP_NAME} v{APP_VERSION}"

# =============================================================================
# KEYBOARD SHORTCUTS
# =============================================================================

class Shortcuts:
    """
    Keyboard shortcut definitions.
    """
    BROWSE_FOLDER = "Ctrl+O"
    RESCAN_FOLDER = "Ctrl+R"
    START_PROCESSING = "Ctrl+Return"  # Ctrl+Enter
    REFRESH = "F5"
    SELECT_ALL = "Ctrl+A"
    DESELECT_ALL = "Ctrl+D"
    TOGGLE_THEME = "Ctrl+T"
    QUIT = "Ctrl+Q"
