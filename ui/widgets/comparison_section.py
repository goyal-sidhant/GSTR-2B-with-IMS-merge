# ui/widgets/comparison_section.py
"""
Comparison Section Widget for GST Processing Tool v5.0

Compact design for adding comparison reports.
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
    QPushButton, QListWidget, QListWidgetItem, QFileDialog,
    QLabel, QMessageBox, QSizePolicy
)
from PyQt5.QtCore import pyqtSignal, Qt

from pathlib import Path
from typing import List

from core.models import ComparisonReport
from utils.file_utils import extract_month_year_from_report
from utils.constants import MAX_COMPARISON_FILES


class ComparisonSection(QGroupBox):
    """
    Comparison reports management widget.

    Signals:
        reports_changed: Emitted when report list changes
    """

    # Signals
    reports_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__("Comparison Reports (Optional)", parent)
        self._reports: List[ComparisonReport] = []
        self._setup_ui()

    def _setup_ui(self):
        """Set up the widget UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 15, 10, 10)
        layout.setSpacing(8)

        # Header row with info and buttons
        header_layout = QHBoxLayout()
        header_layout.setSpacing(10)

        # Info label
        info_label = QLabel(f"Add previous reports for trend analysis (max {MAX_COMPARISON_FILES})")
        info_label.setStyleSheet("color: #6c757d; font-size: 9pt;")
        header_layout.addWidget(info_label)

        header_layout.addStretch()

        # Count label
        self.count_label = QLabel("0 reports")
        self.count_label.setStyleSheet("font-weight: bold; color: #495057;")
        header_layout.addWidget(self.count_label)

        layout.addLayout(header_layout)

        # Reports list (compact)
        self.reports_list = QListWidget()
        self.reports_list.setMinimumHeight(60)
        self.reports_list.setSelectionMode(QListWidget.SingleSelection)
        self.reports_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #dee2e6;
                border-radius: 4px;
                background-color: #f8f9fa;
            }
            QListWidget::item {
                padding: 4px 8px;
            }
            QListWidget::item:selected {
                background-color: #e3f2fd;
                color: #1565c0;
            }
        """)
        self.reports_list.itemSelectionChanged.connect(self._on_selection_changed)
        self.reports_list.itemDoubleClicked.connect(self._remove_item)
        layout.addWidget(self.reports_list, stretch=1)

        # Button row at bottom
        button_layout = QHBoxLayout()
        button_layout.setSpacing(8)

        self.add_btn = QPushButton("+ Add")
        self.add_btn.clicked.connect(self._add_report)
        button_layout.addWidget(self.add_btn)

        self.remove_btn = QPushButton("Remove")
        self.remove_btn.setProperty("secondary", True)
        self.remove_btn.setEnabled(False)
        self.remove_btn.clicked.connect(self._remove_selected)
        button_layout.addWidget(self.remove_btn)

        self.clear_btn = QPushButton("Clear All")
        self.clear_btn.setProperty("secondary", True)
        self.clear_btn.setEnabled(False)
        self.clear_btn.clicked.connect(self._clear_all)
        button_layout.addWidget(self.clear_btn)

        button_layout.addStretch()
        layout.addLayout(button_layout)

    def _add_report(self):
        """Add a comparison report file."""
        if len(self._reports) >= MAX_COMPARISON_FILES:
            QMessageBox.warning(
                self,
                "Maximum Reached",
                f"Maximum of {MAX_COMPARISON_FILES} comparison reports allowed."
            )
            return

        initial_dir = ""
        if self._reports:
            initial_dir = str(Path(self._reports[-1].file_path).parent)

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Previous GST Report",
            initial_dir,
            "Excel Files (*.xlsx);;All Files (*.*)"
        )

        if file_path:
            if any(r.file_path == file_path for r in self._reports):
                QMessageBox.information(
                    self, "Already Added", "This report is already in the list."
                )
                return

            path = Path(file_path)
            month, year = extract_month_year_from_report(path)

            report = ComparisonReport(
                file_path=file_path,
                file_name=path.name,
                month=month or "",
                year=year or ""
            )

            self._reports.append(report)
            self._update_list()
            self.reports_changed.emit()

    def _remove_selected(self):
        """Remove the selected report."""
        current_row = self.reports_list.currentRow()
        if current_row >= 0:
            self._reports.pop(current_row)
            self._update_list()
            self.reports_changed.emit()

    def _remove_item(self, item: QListWidgetItem):
        """Remove a report by double-clicking."""
        row = self.reports_list.row(item)
        if row >= 0:
            self._reports.pop(row)
            self._update_list()
            self.reports_changed.emit()

    def _clear_all(self):
        """Clear all reports."""
        if self._reports:
            reply = QMessageBox.question(
                self, "Clear All", "Remove all comparison reports?",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                self._reports.clear()
                self._update_list()
                self.reports_changed.emit()

    def _update_list(self):
        """Update the list widget display."""
        self.reports_list.clear()

        for report in self._reports:
            period = report.period if report.month else "Unknown"
            text = f"{period} - {report.file_name}"
            self.reports_list.addItem(text)

        count = len(self._reports)
        self.count_label.setText(f"{count} report{'s' if count != 1 else ''}")

        self.clear_btn.setEnabled(count > 0)
        self.add_btn.setEnabled(count < MAX_COMPARISON_FILES)

    def _on_selection_changed(self):
        """Handle selection change."""
        has_selection = self.reports_list.currentRow() >= 0
        self.remove_btn.setEnabled(has_selection)

    def get_report_paths(self) -> List[str]:
        """Get list of report file paths."""
        return [r.file_path for r in self._reports]

    def get_reports(self) -> List[ComparisonReport]:
        """Get list of report objects."""
        return self._reports.copy()

    def get_count(self) -> int:
        """Get number of reports."""
        return len(self._reports)

    def clear(self):
        """Clear all reports without confirmation."""
        self._reports.clear()
        self._update_list()

    def set_enabled(self, enabled: bool):
        """Enable or disable the widget."""
        self.add_btn.setEnabled(enabled and len(self._reports) < MAX_COMPARISON_FILES)
        self.remove_btn.setEnabled(enabled and self.reports_list.currentRow() >= 0)
        self.clear_btn.setEnabled(enabled and len(self._reports) > 0)
        self.reports_list.setEnabled(enabled)
