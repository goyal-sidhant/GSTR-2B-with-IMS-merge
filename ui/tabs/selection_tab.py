# ui/tabs/selection_tab.py
"""
Selection Tab for GST Processing Tool v5.0

Contains:
- Preview statistics (compact, always visible at top)
- Client table with quick filter buttons
- Process button
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSizePolicy
)
from PyQt5.QtCore import pyqtSignal

from typing import List

from ui.widgets.preview_section import PreviewSection
from ui.widgets.client_table import ClientTable
from core.models import ClientInfo, PreviewData


class SelectionTab(QWidget):
    """
    Selection tab widget containing preview stats and client table.

    Signals:
        selection_changed: Emitted when client selection changes (count: int)
        filter_changed: Emitted when quick filter is applied (filter_type: str)
        process_requested: Emitted when process button is clicked
    """

    # Signals
    selection_changed = pyqtSignal(int)
    filter_changed = pyqtSignal(str)
    process_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        """Set up the tab UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # ---- Preview Section (compact statistics at top) ----
        self.preview_section = PreviewSection()
        layout.addWidget(self.preview_section)

        # ---- Client Table (takes most space) ----
        self.client_table = ClientTable()
        self.client_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.client_table.selection_changed.connect(self._on_selection_changed)
        self.client_table.filter_changed.connect(self.filter_changed.emit)
        layout.addWidget(self.client_table, stretch=1)

        # ---- Process Button (at bottom) ----
        self.process_btn = QPushButton("🚀 Start Processing")
        self.process_btn.setFixedHeight(45)
        self.process_btn.setEnabled(False)
        self.process_btn.clicked.connect(self.process_requested.emit)
        layout.addWidget(self.process_btn)

    def _on_selection_changed(self, count: int):
        """Handle selection change and update process button."""
        self.selection_changed.emit(count)
        self._update_process_button(count)

    def _update_process_button(self, selected_count: int):
        """Update process button state and text."""
        self.process_btn.setEnabled(selected_count > 0)
        if selected_count > 0:
            self.process_btn.setText(f"🚀 Start Processing ({selected_count} clients)")
        else:
            self.process_btn.setText("🚀 Start Processing")

    # ============================================
    # Public Methods - Preview Section
    # ============================================

    def update_preview(self, preview_data: PreviewData):
        """Update preview statistics display."""
        self.preview_section.update_preview(preview_data)

    def clear_preview(self):
        """Clear preview statistics."""
        self.preview_section.clear()

    # ============================================
    # Public Methods - Client Table
    # ============================================

    def set_clients(self, clients: List[ClientInfo]):
        """Set clients in the table."""
        self.client_table.set_clients(clients)

    def get_selected_clients(self) -> List[ClientInfo]:
        """Get list of selected clients."""
        return self.client_table.get_selected_clients()

    def get_all_clients(self) -> List[ClientInfo]:
        """Get all clients."""
        return self.client_table.get_all_clients()

    def get_selected_count(self) -> int:
        """Get count of selected clients."""
        return self.client_table.get_selected_count()

    def get_total_count(self) -> int:
        """Get total client count."""
        return self.client_table.get_total_count()

    def select_all(self):
        """Select all clients."""
        self.client_table._select_all()

    def deselect_all(self):
        """Deselect all clients."""
        self.client_table._deselect_all()

    def clear_table(self):
        """Clear the client table."""
        self.client_table.clear()

    # ============================================
    # Public Methods - Process Button
    # ============================================

    def set_process_button_enabled(self, enabled: bool):
        """Enable or disable the process button."""
        self.process_btn.setEnabled(enabled)

    # ============================================
    # Public Methods - Enable/Disable
    # ============================================

    def set_enabled(self, enabled: bool):
        """Enable or disable all widgets in the tab."""
        self.client_table.set_enabled(enabled)
        # Process button state depends on selection
        if enabled:
            self._update_process_button(self.get_selected_count())
        else:
            self.process_btn.setEnabled(False)
