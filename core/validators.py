# core/validators.py
"""
File validation logic for GST Processing Tool v5.0

This module handles:
- Validating input folder contents
- Auto-detecting folder information
- Providing helpful error messages and suggestions
"""

from pathlib import Path
from typing import Tuple, List, Dict, Optional
from collections import Counter

from core.models import ValidationResult, ClientInfo, PreviewData
from utils.file_utils import (
    check_file_month, 
    extract_client_info, 
    find_extra_files,
    organize_files_by_client
)
from utils.constants import CategoryType
from utils.logger import get_logger


class FileValidator:
    """
    Handles validation of input files and folders.
    """
    
    def __init__(self):
        self.logger = get_logger()
    
    def validate_folder(self, input_path: Path, month: str, year: str,
                       total_clients: int = 0, not_generated: int = 0) -> ValidationResult:
        """
        Validate the input folder and its contents.
        
        Args:
            input_path: Path to the input folder
            month: Selected month
            year: Selected year
            total_clients: Expected total client count
            not_generated: Count of clients without files
        
        Returns:
            ValidationResult with status and details
        """
        self.logger.info(f"Validating folder: {input_path}")
        
        # Check if folder exists
        if not input_path.exists():
            self.logger.error("Input folder does not exist")
            return ValidationResult(
                is_valid=False,
                error_message="Input folder does not exist!"
            )
        
        # Check if month and year are selected
        if not month or not year:
            self.logger.error("Month or year not selected")
            return ValidationResult(
                is_valid=False,
                error_message="Please select month and year!"
            )
        
        # Find all relevant files
        all_gstr2b_files = [f for f in input_path.glob("GSTR2B-*.xlsx")
                           if check_file_month(f.stem, month, year)]
        all_ims_files = list(input_path.glob("ImsReco-*.xlsx"))
        extra_files = find_extra_files(input_path, month, year)
        
        self.logger.info(f"Found {len(all_gstr2b_files)} GSTR-2B files, {len(all_ims_files)} IMS files")
        
        # Organize by client
        gstr_clients = set()
        ims_clients = set()
        
        for f in all_gstr2b_files:
            client_name, state = extract_client_info(f.stem, "GSTR2B")
            if client_name and state:
                gstr_clients.add(f"{client_name}-{state}")
        
        for f in all_ims_files:
            client_name, state = extract_client_info(f.stem, "IMS")
            if client_name and state:
                ims_clients.add(f"{client_name}-{state}")
        
        # Identify issues and warnings
        issues = []
        warnings = []
        
        # Check file counts against expected
        if total_clients > 0:
            expected_count = total_clients - not_generated
            if len(gstr_clients) != expected_count:
                diff = len(gstr_clients) - expected_count
                if diff > 0:
                    warnings.append(f"Found {diff} more GSTR-2B files than expected ({len(gstr_clients)} vs {expected_count})")
                else:
                    warnings.append(f"Found {abs(diff)} fewer GSTR-2B files than expected ({len(gstr_clients)} vs {expected_count})")
        
        # Check for clients with only IMS files
        ims_only = ims_clients - gstr_clients
        if ims_only:
            warnings.append(f"{len(ims_only)} clients have only IMS Reco files (GSTR-2B will be created)")
            self.logger.info(f"IMS-only clients: {len(ims_only)}")
        
        # Check for clients with only GSTR-2B files
        gstr_only = gstr_clients - ims_clients
        if gstr_only:
            warnings.append(f"{len(gstr_only)} clients have only GSTR-2B files (no IMS Reco)")
            self.logger.info(f"GSTR-only clients: {len(gstr_only)}")
        
        # Check for extra files
        if extra_files:
            warnings.append(f"{len(extra_files)} extra files found that won't be processed")
            self.logger.warning(f"Extra files found: {len(extra_files)}")
        
        # Build file counts dictionary
        file_counts = {
            'gstr2b_files': len(gstr_clients),
            'ims_files': len(ims_clients),
            'extra_files': len(extra_files),
            'ims_only': len(ims_only),
            'gstr_only': len(gstr_only),
            'both': len(gstr_clients & ims_clients)
        }
        
        # Validation passes if no critical issues
        is_valid = len(issues) == 0
        
        if is_valid:
            self.logger.info("Validation passed")
        else:
            self.logger.error(f"Validation failed: {issues}")
        
        return ValidationResult(
            is_valid=is_valid,
            error_message="\n".join(issues) if issues else "",
            warnings=warnings,
            file_counts=file_counts,
            issues=issues,
            extra_files=extra_files
        )
    
    def scan_clients(self, input_path: Path, month: str, year: str) -> List[ClientInfo]:
        """
        Scan folder and return list of ClientInfo objects.
        
        This is used to populate the client table in the UI.
        
        Args:
            input_path: Path to input folder
            month: Selected month
            year: Selected year
        
        Returns:
            List of ClientInfo objects for all found clients
        """
        self.logger.info(f"Scanning clients for {month} {year}")
        
        # Find all files
        all_gstr2b_files = [f for f in input_path.glob("GSTR2B-*.xlsx")
                           if check_file_month(f.stem, month, year)]
        all_ims_files = list(input_path.glob("ImsReco-*.xlsx"))
        
        # Organize by client
        gstr_by_client = organize_files_by_client(all_gstr2b_files, "GSTR2B")
        
        ims_by_client = {}
        for f in all_ims_files:
            client_name, state = extract_client_info(f.stem, "IMS")
            if client_name and state:
                key = f"{client_name}-{state}"
                ims_by_client[key] = f
        
        # Get all unique clients
        all_client_keys = set(gstr_by_client.keys()) | set(ims_by_client.keys())
        
        # Create ClientInfo for each
        clients = []
        for client_key in sorted(all_client_keys):
            parts = client_key.rsplit("-", 1)
            name = parts[0] if len(parts) > 0 else client_key
            state = parts[1] if len(parts) > 1 else ""
            
            client = ClientInfo(
                name=name,
                state=state,
                has_gstr2b=client_key in gstr_by_client,
                has_ims=client_key in ims_by_client,
                selected=True  # Default selected
            )
            client.determine_category()  # Set category based on files
            clients.append(client)
        
        self.logger.info(f"Found {len(clients)} unique clients")
        return clients
    
    def get_preview_data(self, clients: List[ClientInfo], 
                         extra_files: List[str]) -> PreviewData:
        """
        Generate preview data from client list.
        
        Args:
            clients: List of ClientInfo objects
            extra_files: List of extra file names
        
        Returns:
            PreviewData for display in UI
        """
        # Count only selected clients
        selected_clients = [c for c in clients if c.selected]
        
        merge_count = sum(1 for c in selected_clients 
                        if c.category == CategoryType.MERGE.value)
        create_count = sum(1 for c in selected_clients 
                         if c.category == CategoryType.CREATE.value)
        copy_count = sum(1 for c in selected_clients 
                        if c.category == CategoryType.COPY.value)
        
        return PreviewData(
            merge_count=merge_count,
            create_count=create_count,
            copy_count=copy_count,
            extra_files=extra_files,
            total_selected=len(selected_clients)
        )
    
    def auto_detect_folder_info(self, folder_path: str) -> Tuple[Optional[str], Optional[str], Optional[int]]:
        """
        Auto-detect month, year, and client count from folder contents.
        
        Args:
            folder_path: Path to the folder
        
        Returns:
            Tuple of (month, year, client_count) or (None, None, None)
        """
        self.logger.info(f"Auto-detecting folder info: {folder_path}")
        
        try:
            input_path = Path(folder_path)
            if not input_path.exists():
                return None, None, None
            
            # Find all GSTR-2B files
            gstr2b_files = list(input_path.glob("GSTR2B-*.xlsx"))
            
            if not gstr2b_files:
                self.logger.warning("No GSTR-2B files found")
                return None, None, 0
            
            # Extract months and years from files
            import re
            months_years = []
            for file in gstr2b_files:
                match = re.search(
                    r'-(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+(\d{4})',
                    file.stem
                )
                if match:
                    months_years.append((match.group(1), match.group(2)))
            
            if not months_years:
                return None, None, 0
            
            # Get the most common month/year combination
            most_common = Counter(months_years).most_common(1)[0][0]
            detected_month, detected_year = most_common
            
            # Count unique clients for the detected month/year
            unique_clients = set()
            for file in gstr2b_files:
                if check_file_month(file.stem, detected_month, detected_year):
                    client_name, state = extract_client_info(file.stem, "GSTR2B")
                    if client_name and state:
                        unique_clients.add(f"{client_name}-{state}")
            
            client_count = len(unique_clients)
            
            self.logger.info(f"Detected: {detected_month} {detected_year}, {client_count} clients")
            return detected_month, detected_year, client_count
            
        except Exception as e:
            self.logger.error(f"Auto-detection failed: {e}")
            return None, None, None
    
    def get_error_details(self, error_code: str, context: str = "") -> Dict[str, any]:
        """
        Get detailed error message and suggested fixes.
        
        Args:
            error_code: The error code
            context: Additional context about the error
        
        Returns:
            Dictionary with description, suggestions, and formatted message
        """
        error_details = {
            "file_not_found": {
                "description": "Required file is missing from the input folder",
                "suggestions": [
                    "Check if the file was accidentally moved or deleted",
                    "Verify the file naming convention matches the expected format",
                    "Ensure the month/year in filename is correct"
                ]
            },
            "filename_parse_error": {
                "description": "Cannot extract client information from filename",
                "suggestions": [
                    "Check filename follows format: GSTR2B-ClientName-State-MMM YYYY",
                    "Ensure there are no special characters in client name",
                    "Verify state code is correct (no spaces or special characters)"
                ]
            },
            "ims_sheet_missing": {
                "description": "IMS sheet not found in IMS Reco file",
                "suggestions": [
                    "Open the IMS Reco file manually and check sheet names",
                    "Rename the data sheet to 'IMS' if it exists with different name",
                    "Regenerate the IMS Reco file if it's corrupted"
                ]
            },
            "creation_error": {
                "description": "Failed to create new GSTR-2B file from IMS Reco",
                "suggestions": [
                    "Check if you have write permissions in the output folder",
                    "Ensure the IMS Reco file is not corrupted",
                    "Verify there's enough disk space available"
                ]
            },
            "file_locked": {
                "description": "File is currently open in another application",
                "suggestions": [
                    "Close Excel or any other application that might have the file open",
                    "Check if the file is being used by another process",
                    "Restart the application if the issue persists"
                ]
            }
        }
        
        if error_code in error_details:
            details = error_details[error_code]
            formatted = f"{details['description']}\n\nSuggested fixes:\n"
            formatted += "\n".join(f"• {fix}" for fix in details['suggestions'])
            
            return {
                "description": details["description"],
                "suggestions": details["suggestions"],
                "formatted_message": formatted
            }
        else:
            return {
                "description": f"Unexpected error: {context}",
                "suggestions": [
                    "Check the error details above",
                    "Try processing individual files",
                    "Contact support if issue persists"
                ],
                "formatted_message": f"Unexpected error: {context}\n\n" +
                                   "Suggested fixes:\n• Check the error details above\n" +
                                   "• Try processing individual files\n" +
                                   "• Contact support if issue persists"
            }
