# ui/widgets/date_section.py
"""
Date Selection Section Widget for GST Processing Tool v5.0

This widget contains:
- Month dropdown
- Year dropdown
- Total clients input
- Not generated input
- Expected count display
"""

from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QGroupBox,
    QLabel, QComboBox, QLineEdit, QGridLayout
)
from PyQt5.QtCore import pyqtSignal, Qt

from utils.constants import FINANCIAL_YEAR_MONTHS, YEARS_RANGE
from utils.date_utils import get_current_month_year


class DateSection(QGroupBox):
    """
    Date and client count selection widget.
    
    Signals:
        values_changed: Emitted when any value changes
    """
    
    # Signals
    values_changed = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__("📅 Processing Period", parent)
        self._setup_ui()
        self._set_defaults()
    
    def _setup_ui(self):
        """Set up the widget UI."""
        layout = QGridLayout(self)
        layout.setContentsMargins(10, 15, 10, 10)
        layout.setSpacing(10)
        
        # Row 0: Month and Year
        layout.addWidget(QLabel("Month:"), 0, 0)
        
        self.month_combo = QComboBox()
        self.month_combo.addItems(FINANCIAL_YEAR_MONTHS)
        self.month_combo.setFixedWidth(100)
        self.month_combo.currentTextChanged.connect(self._on_values_changed)
        layout.addWidget(self.month_combo, 0, 1)
        
        layout.addWidget(QLabel("Year:"), 0, 2)
        
        self.year_combo = QComboBox()
        self.year_combo.addItems([str(y) for y in YEARS_RANGE])
        self.year_combo.setFixedWidth(100)
        self.year_combo.currentTextChanged.connect(self._on_values_changed)
        layout.addWidget(self.year_combo, 0, 3)
        
        # Spacer
        layout.setColumnStretch(4, 1)
        
        # Row 1: Client counts
        layout.addWidget(QLabel("Total Clients:"), 1, 0)
        
        self.total_clients_edit = QLineEdit()
        self.total_clients_edit.setFixedWidth(80)
        self.total_clients_edit.setPlaceholderText("0")
        self.total_clients_edit.textChanged.connect(self._on_values_changed)
        self.total_clients_edit.textChanged.connect(self._update_expected)
        layout.addWidget(self.total_clients_edit, 1, 1)
        
        layout.addWidget(QLabel("Not Generated:"), 1, 2)
        
        self.not_generated_edit = QLineEdit()
        self.not_generated_edit.setFixedWidth(80)
        self.not_generated_edit.setPlaceholderText("0")
        self.not_generated_edit.textChanged.connect(self._on_values_changed)
        self.not_generated_edit.textChanged.connect(self._update_expected)
        layout.addWidget(self.not_generated_edit, 1, 3)
        
        # Expected count (calculated)
        layout.addWidget(QLabel("Expected:"), 1, 5)
        
        self.expected_label = QLabel("0")
        self.expected_label.setStyleSheet("font-weight: bold; color: #1a73e8;")
        layout.addWidget(self.expected_label, 1, 6)
    
    def _set_defaults(self):
        """Set default values to current month/year."""
        current_month, current_year = get_current_month_year()
        
        # Set month
        index = self.month_combo.findText(current_month)
        if index >= 0:
            self.month_combo.setCurrentIndex(index)
        
        # Set year
        index = self.year_combo.findText(current_year)
        if index >= 0:
            self.year_combo.setCurrentIndex(index)
    
    def _on_values_changed(self):
        """Handle any value change."""
        self.values_changed.emit()
    
    def _update_expected(self):
        """Update the expected count calculation."""
        try:
            total = int(self.total_clients_edit.text() or 0)
            not_gen = int(self.not_generated_edit.text() or 0)
            expected = total - not_gen
            self.expected_label.setText(str(expected))
        except ValueError:
            self.expected_label.setText("Invalid")
    
    def get_month(self) -> str:
        """Get selected month."""
        return self.month_combo.currentText()
    
    def get_year(self) -> str:
        """Get selected year."""
        return self.year_combo.currentText()
    
    def get_total_clients(self) -> int:
        """Get total clients count."""
        try:
            return int(self.total_clients_edit.text() or 0)
        except ValueError:
            return 0
    
    def get_not_generated(self) -> int:
        """Get not generated count."""
        try:
            return int(self.not_generated_edit.text() or 0)
        except ValueError:
            return 0
    
    def get_expected_count(self) -> int:
        """Get expected count (total - not generated)."""
        return self.get_total_clients() - self.get_not_generated()
    
    def set_month(self, month: str):
        """Set the month."""
        index = self.month_combo.findText(month)
        if index >= 0:
            self.month_combo.setCurrentIndex(index)
    
    def set_year(self, year: str):
        """Set the year."""
        index = self.year_combo.findText(year)
        if index >= 0:
            self.year_combo.setCurrentIndex(index)
    
    def set_total_clients(self, count: int):
        """Set total clients count."""
        self.total_clients_edit.setText(str(count) if count else "")
    
    def set_not_generated(self, count: int):
        """Set not generated count."""
        self.not_generated_edit.setText(str(count) if count else "")
    
    def set_values(self, month: str = None, year: str = None, 
                   total: int = None, not_gen: int = None):
        """
        Set multiple values at once.
        
        Args:
            month: Month to set
            year: Year to set
            total: Total clients count
            not_gen: Not generated count
        """
        if month:
            self.set_month(month)
        if year:
            self.set_year(year)
        if total is not None:
            self.set_total_clients(total)
        if not_gen is not None:
            self.set_not_generated(not_gen)
    
    def set_enabled(self, enabled: bool):
        """Enable or disable the widget."""
        self.month_combo.setEnabled(enabled)
        self.year_combo.setEnabled(enabled)
        self.total_clients_edit.setEnabled(enabled)
        self.not_generated_edit.setEnabled(enabled)
