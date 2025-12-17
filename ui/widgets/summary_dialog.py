# ui/widgets/summary_dialog.py
"""
Summary Dialog Widget for GST Processing Tool v5.0

Shown after processing completes with:
- Success/Error status
- Processing statistics
- Buttons: Open Output Folder, View Report, OK
"""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QGridLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

import os
import platform
import subprocess
from pathlib import Path

from core.models import ProcessingSummary


class SummaryDialog(QDialog):
    """
    Processing summary dialog shown after completion.
    """
    
    def __init__(self, summary: ProcessingSummary, month_year: str, parent=None):
        super().__init__(parent)
        self.summary = summary
        self.month_year = month_year
        self._setup_ui()
    
    def _setup_ui(self):
        """Set up the dialog UI."""
        self.setWindowTitle("Processing Complete")
        self.setMinimumWidth(400)
        self.setModal(True)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Header with icon
        header_layout = QHBoxLayout()
        
        if self.summary.has_errors:
            icon_text = "⚠️"
            title_text = "Processing Complete (with issues)"
            title_color = "#ff9800"
        else:
            icon_text = "✅"
            title_text = "Processing Complete!"
            title_color = "#28a745"
        
        icon_label = QLabel(icon_text)
        icon_label.setFont(QFont("Segoe UI", 24))
        header_layout.addWidget(icon_label)
        
        title_label = QLabel(title_text)
        title_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        title_label.setStyleSheet(f"color: {title_color};")
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        layout.addLayout(header_layout)
        
        # Period info
        period_label = QLabel(f"📅 {self.month_year} Processing Summary")
        period_label.setStyleSheet("font-size: 11pt; color: #666666;")
        layout.addWidget(period_label)
        
        # Separator
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("background-color: #cccccc;")
        layout.addWidget(line)
        
        # Statistics grid
        stats_grid = QGridLayout()
        stats_grid.setSpacing(10)
        
        stats = [
            ("✓ Files Merged:", self.summary.merged, "#28a745"),
            ("✓ Files Created:", self.summary.created, "#2196f3"),
            ("⚠ Copied (No IMS):", self.summary.copied, "#ff9800"),
            ("✗ Errors:", self.summary.errors, "#dc3545"),
        ]
        
        for row, (label, value, color) in enumerate(stats):
            label_widget = QLabel(label)
            label_widget.setStyleSheet("font-size: 10pt;")
            stats_grid.addWidget(label_widget, row, 0)
            
            value_widget = QLabel(str(value))
            value_widget.setStyleSheet(f"font-size: 10pt; font-weight: bold; color: {color};")
            value_widget.setAlignment(Qt.AlignRight)
            stats_grid.addWidget(value_widget, row, 1)
        
        layout.addLayout(stats_grid)
        
        # Total processed
        total_label = QLabel(f"Total Processed: {self.summary.total_processed}")
        total_label.setStyleSheet("font-weight: bold; font-size: 11pt;")
        layout.addWidget(total_label)
        
        # Duration
        duration_label = QLabel(f"⏱️ Duration: {self.summary.duration_text}")
        duration_label.setStyleSheet("color: #666666;")
        layout.addWidget(duration_label)
        
        # Report path
        if self.summary.report_path:
            report_frame = QFrame()
            report_frame.setStyleSheet("""
                QFrame {
                    background-color: #f0f0f0;
                    border: 1px solid #cccccc;
                    border-radius: 4px;
                    padding: 5px;
                }
            """)
            report_layout = QVBoxLayout(report_frame)
            report_layout.setContentsMargins(10, 5, 10, 5)
            
            report_title = QLabel("📊 Report saved to:")
            report_title.setStyleSheet("font-weight: bold;")
            report_layout.addWidget(report_title)
            
            report_name = QLabel(self.summary.report_path.name)
            report_name.setStyleSheet("color: #1a73e8;")
            report_name.setWordWrap(True)
            report_layout.addWidget(report_name)
            
            layout.addWidget(report_frame)
        
        # Separator
        line2 = QFrame()
        line2.setFrameShape(QFrame.HLine)
        line2.setStyleSheet("background-color: #cccccc;")
        layout.addWidget(line2)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        # Open Output Folder button
        self.open_folder_btn = QPushButton("📁 Open Output Folder")
        self.open_folder_btn.clicked.connect(self._open_output_folder)
        button_layout.addWidget(self.open_folder_btn)
        
        # View Report button
        self.view_report_btn = QPushButton("📊 View Report")
        self.view_report_btn.clicked.connect(self._open_report)
        if not self.summary.report_path:
            self.view_report_btn.setEnabled(False)
        button_layout.addWidget(self.view_report_btn)
        
        button_layout.addStretch()
        
        # OK button
        self.ok_btn = QPushButton("OK")
        self.ok_btn.setFixedWidth(80)
        self.ok_btn.clicked.connect(self.accept)
        self.ok_btn.setDefault(True)
        button_layout.addWidget(self.ok_btn)
        
        layout.addLayout(button_layout)
    
    def _open_output_folder(self):
        """Open the output folder in file explorer."""
        if self.summary.output_folder and self.summary.output_folder.exists():
            self._open_path(self.summary.output_folder)
    
    def _open_report(self):
        """Open the report file."""
        if self.summary.report_path and self.summary.report_path.exists():
            self._open_path(self.summary.report_path)
    
    def _open_path(self, path: Path):
        """
        Open a file or folder in the system default application.
        
        Args:
            path: Path to open
        """
        try:
            if platform.system() == "Windows":
                os.startfile(str(path))
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["open", str(path)])
            else:  # Linux
                subprocess.run(["xdg-open", str(path)])
        except Exception as e:
            print(f"Could not open path: {e}")


class ConfirmDialog(QDialog):
    """
    Confirmation dialog shown before processing starts.
    """
    
    def __init__(self, merge_count: int, create_count: int, copy_count: int,
                 extra_files: list, month_year: str, parent=None):
        super().__init__(parent)
        self.merge_count = merge_count
        self.create_count = create_count
        self.copy_count = copy_count
        self.extra_files = extra_files
        self.month_year = month_year
        self._setup_ui()
    
    def _setup_ui(self):
        """Set up the dialog UI."""
        self.setWindowTitle("Confirm Processing")
        self.setMinimumWidth(380)
        self.setModal(True)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Title
        total = self.merge_count + self.create_count + self.copy_count
        title_label = QLabel(f"Ready to process {total} clients for {self.month_year}")
        title_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        layout.addWidget(title_label)
        
        # Breakdown
        breakdown_frame = QFrame()
        breakdown_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border: 1px solid #e0e0e0;
                border-radius: 4px;
            }
        """)
        breakdown_layout = QVBoxLayout(breakdown_frame)
        breakdown_layout.setContentsMargins(15, 10, 15, 10)
        
        items = [
            (f"📁 Will Merge:", self.merge_count, "#28a745"),
            (f"📝 Will Create:", self.create_count, "#2196f3"),
            (f"⚠️ Will Copy:", self.copy_count, "#ff9800"),
        ]
        
        for label, count, color in items:
            row = QHBoxLayout()
            row.addWidget(QLabel(label))
            row.addStretch()
            count_label = QLabel(f"{count} clients")
            count_label.setStyleSheet(f"font-weight: bold; color: {color};")
            row.addWidget(count_label)
            breakdown_layout.addLayout(row)
        
        layout.addWidget(breakdown_frame)
        
        # Extra files warning
        if self.extra_files:
            warning_label = QLabel(f"⚠️ {len(self.extra_files)} extra files will be skipped:")
            warning_label.setStyleSheet("color: #ff9800; font-weight: bold;")
            layout.addWidget(warning_label)
            
            for filename in self.extra_files[:3]:  # Show first 3
                file_label = QLabel(f"  • {filename}")
                file_label.setStyleSheet("color: #666666; font-size: 9pt;")
                layout.addWidget(file_label)
            
            if len(self.extra_files) > 3:
                more_label = QLabel(f"  ... and {len(self.extra_files) - 3} more")
                more_label.setStyleSheet("color: #666666; font-size: 9pt; font-style: italic;")
                layout.addWidget(more_label)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setProperty("secondary", True)
        cancel_btn.setFixedWidth(100)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        button_layout.addStretch()
        
        start_btn = QPushButton("✓ Start Processing")
        start_btn.setFixedWidth(140)
        start_btn.clicked.connect(self.accept)
        start_btn.setDefault(True)
        button_layout.addWidget(start_btn)
        
        layout.addLayout(button_layout)
