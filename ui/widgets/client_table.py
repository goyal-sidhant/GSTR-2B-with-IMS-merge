# ui/widgets/client_table.py
"""
Client Table Widget for GST Processing Tool v5.0

This is the main client selection table that shows:
- Checkbox for selection
- Client name
- State code
- File status (Both/GSTR Only/IMS Only)
- Category (Merge/Create/Copy)

Features:
- Select All / Deselect All buttons
- Shows selected count in title
- Color coding by category
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QPushButton, QCheckBox, QLabel, QAbstractItemView
)
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QColor, QBrush

from typing import List
from core.models import ClientInfo
from utils.constants import CategoryType, FileStatus


class ClientTable(QGroupBox):
    """
    Client selection table widget.
    
    Signals:
        selection_changed: Emitted when selection changes (selected_count: int)
    """
    
    # Signals
    selection_changed = pyqtSignal(int)
    
    # Column indices
    COL_CHECKBOX = 0
    COL_NAME = 1
    COL_STATE = 2
    COL_STATUS = 3
    COL_CATEGORY = 4
    
    def __init__(self, parent=None):
        super().__init__("Client Selection", parent)
        self._clients: List[ClientInfo] = []
        self._setup_ui()
    
    def _setup_ui(self):
        """Set up the widget UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 15, 10, 10)
        layout.setSpacing(10)
        
        # Header with buttons
        header_layout = QHBoxLayout()
        
        # Selected count label
        self.count_label = QLabel("0 of 0 selected")
        self.count_label.setStyleSheet("font-weight: bold;")
        header_layout.addWidget(self.count_label)
        
        header_layout.addStretch()
        
        # Select All button
        self.select_all_btn = QPushButton("Select All")
        self.select_all_btn.setFixedWidth(100)
        self.select_all_btn.setProperty("secondary", True)
        self.select_all_btn.clicked.connect(self._select_all)
        header_layout.addWidget(self.select_all_btn)
        
        # Deselect All button
        self.deselect_all_btn = QPushButton("Deselect All")
        self.deselect_all_btn.setFixedWidth(100)
        self.deselect_all_btn.setProperty("secondary", True)
        self.deselect_all_btn.clicked.connect(self._deselect_all)
        header_layout.addWidget(self.deselect_all_btn)
        
        layout.addLayout(header_layout)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "", "Client Name", "State", "Files", "Action"
        ])
        
        # Table settings
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.verticalHeader().setVisible(False)
        self.table.setSortingEnabled(True)  # Allow sorting by clicking headers
        
        # ============================================
        # COLUMN WIDTHS - ALL USER RESIZABLE
        # ============================================
        header = self.table.horizontalHeader()
        
        # Checkbox column - fixed (no need to resize)
        header.setSectionResizeMode(self.COL_CHECKBOX, QHeaderView.Fixed)
        self.table.setColumnWidth(self.COL_CHECKBOX, 40)
        
        # All other columns - Interactive (user can drag to resize)
        header.setSectionResizeMode(self.COL_NAME, QHeaderView.Interactive)
        header.setSectionResizeMode(self.COL_STATE, QHeaderView.Interactive)
        header.setSectionResizeMode(self.COL_STATUS, QHeaderView.Interactive)
        header.setSectionResizeMode(self.COL_CATEGORY, QHeaderView.Interactive)
        
        # Set default widths (user can resize these)
        self.table.setColumnWidth(self.COL_NAME, 200)    # Client Name
        self.table.setColumnWidth(self.COL_STATE, 70)    # State
        self.table.setColumnWidth(self.COL_STATUS, 100)  # Files
        self.table.setColumnWidth(self.COL_CATEGORY, 90) # Action
        
        # Allow last column to stretch to fill remaining space
        header.setStretchLastSection(True)
        
        # Make the header clickable for sorting
        header.setSectionsClickable(True)
        
        layout.addWidget(self.table)
    
    def set_clients(self, clients: List[ClientInfo]):
        """
        Populate the table with client data.
        
        Args:
            clients: List of ClientInfo objects
        """
        self._clients = clients
        self.table.setRowCount(len(clients))
        
        for row, client in enumerate(clients):
            # Checkbox
            checkbox = QCheckBox()
            checkbox.setChecked(client.selected)
            checkbox.stateChanged.connect(lambda state, r=row: self._on_checkbox_changed(r, state))
            
            checkbox_widget = QWidget()
            checkbox_layout = QHBoxLayout(checkbox_widget)
            checkbox_layout.addWidget(checkbox)
            checkbox_layout.setAlignment(Qt.AlignCenter)
            checkbox_layout.setContentsMargins(0, 0, 0, 0)
            self.table.setCellWidget(row, self.COL_CHECKBOX, checkbox_widget)
            
            # Client name
            name_item = QTableWidgetItem(client.name)
            name_item.setFlags(name_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row, self.COL_NAME, name_item)
            
            # State
            state_item = QTableWidgetItem(client.state)
            state_item.setFlags(state_item.flags() & ~Qt.ItemIsEditable)
            state_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, self.COL_STATE, state_item)
            
            # File status
            status_item = QTableWidgetItem(client.file_status)
            status_item.setFlags(status_item.flags() & ~Qt.ItemIsEditable)
            status_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, self.COL_STATUS, status_item)
            
            # Category with color coding
            category_item = QTableWidgetItem(client.category)
            category_item.setFlags(category_item.flags() & ~Qt.ItemIsEditable)
            category_item.setTextAlignment(Qt.AlignCenter)
            
            # Color coding
            if client.category == CategoryType.MERGE.value:
                category_item.setBackground(QBrush(QColor("#e8f5e9")))  # Light green
                category_item.setForeground(QBrush(QColor("#2e7d32")))  # Dark green
            elif client.category == CategoryType.CREATE.value:
                category_item.setBackground(QBrush(QColor("#e3f2fd")))  # Light blue
                category_item.setForeground(QBrush(QColor("#1565c0")))  # Dark blue
            elif client.category == CategoryType.COPY.value:
                category_item.setBackground(QBrush(QColor("#fff3e0")))  # Light orange
                category_item.setForeground(QBrush(QColor("#e65100")))  # Dark orange
            
            self.table.setItem(row, self.COL_CATEGORY, category_item)
        
        self._update_count()
    
    def _on_checkbox_changed(self, row: int, state: int):
        """Handle checkbox state change."""
        if row < len(self._clients):
            self._clients[row].selected = (state == Qt.Checked)
            self._update_count()
    
    def _update_count(self):
        """Update the selected count label."""
        total = len(self._clients)
        selected = sum(1 for c in self._clients if c.selected)
        self.count_label.setText(f"{selected} of {total} selected")
        
        # Update group box title
        self.setTitle(f"📋 Client Selection ({selected} of {total})")
        
        # Emit signal
        self.selection_changed.emit(selected)
    
    def _select_all(self):
        """Select all clients."""
        for row in range(self.table.rowCount()):
            checkbox_widget = self.table.cellWidget(row, self.COL_CHECKBOX)
            if checkbox_widget:
                checkbox = checkbox_widget.findChild(QCheckBox)
                if checkbox:
                    checkbox.setChecked(True)
    
    def _deselect_all(self):
        """Deselect all clients."""
        for row in range(self.table.rowCount()):
            checkbox_widget = self.table.cellWidget(row, self.COL_CHECKBOX)
            if checkbox_widget:
                checkbox = checkbox_widget.findChild(QCheckBox)
                if checkbox:
                    checkbox.setChecked(False)
    
    def get_selected_clients(self) -> List[ClientInfo]:
        """
        Get list of selected clients.
        
        Returns:
            List of selected ClientInfo objects
        """
        return [c for c in self._clients if c.selected]
    
    def get_all_clients(self) -> List[ClientInfo]:
        """
        Get all clients.
        
        Returns:
            List of all ClientInfo objects
        """
        return self._clients.copy()
    
    def get_selected_count(self) -> int:
        """Get count of selected clients."""
        return sum(1 for c in self._clients if c.selected)
    
    def get_total_count(self) -> int:
        """Get total client count."""
        return len(self._clients)
    
    def clear(self):
        """Clear the table."""
        self._clients = []
        self.table.setRowCount(0)
        self._update_count()
    
    def set_enabled(self, enabled: bool):
        """Enable or disable the widget."""
        self.table.setEnabled(enabled)
        self.select_all_btn.setEnabled(enabled)
        self.deselect_all_btn.setEnabled(enabled)
