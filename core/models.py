# core/models.py
"""
Data models for GST Processing Tool v5.0

This file contains all the data structures (classes) used throughout the app.
These are like "containers" that hold related information together.

Using dataclasses makes these easy to create and use.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from pathlib import Path
from datetime import datetime

from utils.constants import StatusType, CategoryType, FileStatus


@dataclass
class ClientInfo:
    """
    Information about a single client.
    
    This holds all the data about one client that appears in the client table.
    
    Attributes:
        name: Client name (e.g., "ABC Corporation")
        state: State code (e.g., "27" for Maharashtra)
        has_gstr2b: Whether GSTR-2B file exists
        has_ims: Whether IMS Reco file exists
        status: Processing status message
        issue_type: Type of issue (None, Warning, Error, Created)
        error_code: Specific error code if failed
        selected: Whether client is selected for processing (NEW in v5.0)
        category: Processing category - Merge/Create/Copy (NEW in v5.0)
    """
    name: str
    state: str
    has_gstr2b: bool = False
    has_ims: bool = False
    status: str = ""
    issue_type: str = "None"
    error_code: str = ""
    selected: bool = True  # NEW: Default to selected
    category: str = ""     # NEW: Will be set to Merge/Create/Copy
    
    @property
    def client_key(self) -> str:
        """Get unique identifier for this client."""
        return f"{self.name}-{self.state}"
    
    @property
    def file_status(self) -> str:
        """Get file availability status for display."""
        if self.has_gstr2b and self.has_ims:
            return FileStatus.BOTH.value
        elif self.has_gstr2b:
            return FileStatus.GSTR_ONLY.value
        else:
            return FileStatus.IMS_ONLY.value
    
    def determine_category(self) -> str:
        """Determine and set the processing category."""
        if self.has_gstr2b and self.has_ims:
            self.category = CategoryType.MERGE.value
        elif self.has_ims:
            self.category = CategoryType.CREATE.value
        else:
            self.category = CategoryType.COPY.value
        return self.category


@dataclass
class ProcessingResult:
    """
    Result of a file processing operation.
    
    Returned after processing each client or the entire batch.
    
    Attributes:
        success: Whether the operation succeeded
        message: Description of what happened
        error_code: Specific error code if failed
        output_path: Path to the output file/folder
        details: Additional details dictionary
    """
    success: bool
    message: str
    error_code: Optional[str] = None
    output_path: Optional[Path] = None
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ValidationResult:
    """
    Result of file validation before processing.
    
    Returned after scanning the input folder.
    
    Attributes:
        is_valid: Whether validation passed
        error_message: Error message if validation failed
        warnings: List of warning messages
        file_counts: Dictionary of file counts
        issues: List of issue descriptions
        extra_files: List of extra file names (NEW in v5.0)
    """
    is_valid: bool
    error_message: str = ""
    warnings: List[str] = field(default_factory=list)
    file_counts: Dict[str, int] = field(default_factory=dict)
    issues: List[str] = field(default_factory=list)
    extra_files: List[str] = field(default_factory=list)  # NEW


@dataclass
class SummaryData:
    """
    Summary statistics for processing.
    
    Holds all the counts displayed in reports and UI.
    
    Attributes:
        clients_with_gstr2b: Count of clients with GSTR-2B files
        clients_with_ims: Count of clients with IMS files
        clients_with_both: Count of clients with both files
        clients_gstr_only: Count with only GSTR-2B
        clients_ims_only: Count with only IMS
        files_processed: Successfully processed count
        files_created: Newly created GSTR-2B count
        files_with_errors: Error count
        extra_files_count: Extra files found
        selected_count: Clients selected for processing (NEW)
    """
    clients_with_gstr2b: int = 0
    clients_with_ims: int = 0
    clients_with_both: int = 0
    clients_gstr_only: int = 0
    clients_ims_only: int = 0
    files_processed: int = 0
    files_created: int = 0
    files_with_errors: int = 0
    extra_files_count: int = 0
    selected_count: int = 0  # NEW


@dataclass
class PreviewData:
    """
    Preview data shown before processing starts (NEW in v5.0).
    
    This is shown in the Preview section and confirmation dialog.
    
    Attributes:
        merge_count: Clients that will have files merged
        create_count: Clients that will have GSTR-2B created
        copy_count: Clients that will have GSTR-2B copied only
        extra_files: List of extra file names
        total_selected: Total clients selected
    """
    merge_count: int = 0
    create_count: int = 0
    copy_count: int = 0
    extra_files: List[str] = field(default_factory=list)
    total_selected: int = 0
    
    @property
    def extra_files_count(self) -> int:
        """Get count of extra files."""
        return len(self.extra_files)


@dataclass
class ComparisonReport:
    """
    Information about a comparison report file (NEW in v5.0).
    
    Used in the Comparison section to track added reports.
    
    Attributes:
        file_path: Full path to the report file
        file_name: Just the file name for display
        month: Month extracted from filename
        year: Year extracted from filename
        period: Combined "MMM YYYY" string
    """
    file_path: str
    file_name: str = ""
    month: str = ""
    year: str = ""
    
    def __post_init__(self):
        """Set file_name from file_path if not provided."""
        if not self.file_name and self.file_path:
            self.file_name = Path(self.file_path).name
    
    @property
    def period(self) -> str:
        """Get period string."""
        if self.month and self.year:
            return f"{self.month} {self.year}"
        return "Unknown"


@dataclass
class ReportData:
    """
    All data needed to generate the Excel report.
    
    Attributes:
        client_data: List of all client info
        summary: Summary statistics
        extra_files: List of extra file names
        month_year: Processing period string
        comparison_data: Data from comparison reports
        processing_timestamp: When processing was done
    """
    client_data: List[ClientInfo]
    summary: SummaryData
    extra_files: List[str]
    month_year: str
    comparison_data: List[Dict[str, Any]] = field(default_factory=list)
    processing_timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class ComparisonData:
    """
    Parsed data from a historical report for comparison.
    
    Attributes:
        month: Month from the report
        year: Year from the report
        period: Combined period string
        file_path: Path to the original file
        metrics: Summary data from the report
        clients: Client info from the report
        error_patterns: List of error types found
    """
    month: str
    year: str
    period: str
    file_path: str
    metrics: SummaryData
    clients: List[ClientInfo] = field(default_factory=list)
    error_patterns: List[str] = field(default_factory=list)


@dataclass
class ProgressInfo:
    """
    Progress information for UI updates (NEW in v5.0).
    
    Used to update the progress bar and status.
    
    Attributes:
        current: Current item number
        total: Total items to process
        client_name: Current client being processed
        message: Status message
        percentage: Calculated percentage
    """
    current: int = 0
    total: int = 0
    client_name: str = ""
    message: str = ""
    
    @property
    def percentage(self) -> int:
        """Calculate percentage complete."""
        if self.total > 0:
            return int((self.current / self.total) * 100)
        return 0
    
    @property
    def progress_text(self) -> str:
        """Get progress text like '15 of 78'."""
        return f"{self.current} of {self.total}"


@dataclass 
class ProcessingSummary:
    """
    Final summary after processing completes (NEW in v5.0).
    
    Shown in the completion dialog.
    
    Attributes:
        merged: Count of successfully merged files
        created: Count of newly created files
        copied: Count of copied files (no IMS)
        errors: Count of errors
        output_folder: Path to output folder
        report_path: Path to generated report
        duration_seconds: How long processing took
    """
    merged: int = 0
    created: int = 0
    copied: int = 0
    errors: int = 0
    output_folder: Optional[Path] = None
    report_path: Optional[Path] = None
    duration_seconds: float = 0.0
    
    @property
    def total_processed(self) -> int:
        """Total files processed (excluding errors)."""
        return self.merged + self.created + self.copied
    
    @property
    def has_errors(self) -> bool:
        """Check if there were any errors."""
        return self.errors > 0
    
    @property
    def duration_text(self) -> str:
        """Get human-readable duration."""
        if self.duration_seconds < 60:
            return f"{self.duration_seconds:.1f} seconds"
        else:
            minutes = int(self.duration_seconds // 60)
            seconds = int(self.duration_seconds % 60)
            return f"{minutes}m {seconds}s"
