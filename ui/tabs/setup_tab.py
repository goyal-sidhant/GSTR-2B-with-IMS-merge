# ui/tabs/setup_tab.py
"""
Setup Tab for GST Processing Tool v5.0

Contains:
- Folder selection
- Date/period selection
- Comparison reports management
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QSizePolicy
)
from PyQt5.QtCore import pyqtSignal

from ui.widgets.folder_section import FolderSection
from ui.widgets.date_section import DateSection
from ui.widgets.comparison_section import ComparisonSection


class SetupTab(QWidget):
    """
    Setup tab widget containing configuration options.

    Signals:
        folder_selected: Emitted when folder is selected (path: str)
        rescan_requested: Emitted when rescan is requested
        values_changed: Emitted when date/count values change
    """

    # Signals
    folder_selected = pyqtSignal(str)
    rescan_requested = pyqtSignal()
    values_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        """Set up the tab UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 15, 10, 10)
        layout.setSpacing(15)

        # ---- Folder Section ----
        self.folder_section = FolderSection()
        self.folder_section.folder_selected.connect(self.folder_selected.emit)
        self.folder_section.rescan_requested.connect(self.rescan_requested.emit)
        layout.addWidget(self.folder_section)

        # ---- Date Section ----
        self.date_section = DateSection()
        self.date_section.values_changed.connect(self.values_changed.emit)
        layout.addWidget(self.date_section)

        # ---- Comparison Section (expandable) ----
        self.comparison_section = ComparisonSection()
        self.comparison_section.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(self.comparison_section, stretch=1)

    # ============================================
    # Public Methods - Folder Section
    # ============================================

    def get_folder_path(self) -> str:
        """Get the current folder path."""
        return self.folder_section.get_path()

    def set_folder_path(self, path: str):
        """Set the folder path."""
        self.folder_section.set_path(path)

    # ============================================
    # Public Methods - Date Section
    # ============================================

    def get_month(self) -> str:
        """Get selected month."""
        return self.date_section.get_month()

    def get_year(self) -> str:
        """Get selected year."""
        return self.date_section.get_year()

    def set_date_values(self, month: str = None, year: str = None,
                        total: int = None, not_gen: int = None):
        """Set date section values."""
        self.date_section.set_values(month, year, total, not_gen)

    # ============================================
    # Public Methods - Comparison Section
    # ============================================

    def get_comparison_files(self) -> list:
        """Get list of comparison report paths."""
        return self.comparison_section.get_report_paths()

    # ============================================
    # Public Methods - Enable/Disable
    # ============================================

    def set_enabled(self, enabled: bool):
        """Enable or disable all widgets in the tab."""
        self.folder_section.set_enabled(enabled)
        self.date_section.set_enabled(enabled)
        self.comparison_section.set_enabled(enabled)
