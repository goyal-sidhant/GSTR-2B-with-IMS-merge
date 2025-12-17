# ui/widgets/folder_section.py
"""
Folder Selection Section Widget for GST Processing Tool v5.0

This widget contains:
- Folder path display
- Browse button
- Rescan button
"""

from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QGroupBox,
    QLineEdit, QPushButton, QFileDialog
)
from PyQt5.QtCore import pyqtSignal


class FolderSection(QGroupBox):
    """
    Folder selection widget with Browse and Rescan functionality.
    
    Signals:
        folder_selected: Emitted when a folder is selected (path: str)
        rescan_requested: Emitted when rescan button is clicked
    """
    
    # Signals
    folder_selected = pyqtSignal(str)
    rescan_requested = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__("📁 Input Folder", parent)
        self._setup_ui()
    
    def _setup_ui(self):
        """Set up the widget UI."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 15, 10, 10)
        layout.setSpacing(10)
        
        # Folder path input
        self.path_edit = QLineEdit()
        self.path_edit.setPlaceholderText("Select a folder containing GSTR-2B and IMS Reco files...")
        self.path_edit.setReadOnly(True)
        layout.addWidget(self.path_edit, stretch=1)
        
        # Browse button
        self.browse_btn = QPushButton("Browse")
        self.browse_btn.setToolTip("Select input folder (Ctrl+O)")
        self.browse_btn.setFixedWidth(100)
        self.browse_btn.clicked.connect(self._on_browse_clicked)
        layout.addWidget(self.browse_btn)
        
        # Rescan button
        self.rescan_btn = QPushButton("↻ Rescan")
        self.rescan_btn.setToolTip("Rescan folder contents (Ctrl+R)")
        self.rescan_btn.setFixedWidth(100)
        self.rescan_btn.setEnabled(False)  # Disabled until folder is selected
        self.rescan_btn.clicked.connect(self._on_rescan_clicked)
        layout.addWidget(self.rescan_btn)
    
    def _on_browse_clicked(self):
        """Handle browse button click."""
        # Open folder selection dialog
        folder_path = QFileDialog.getExistingDirectory(
            self,
            "Select Input Folder",
            self.path_edit.text() or "",
            QFileDialog.ShowDirsOnly
        )
        
        if folder_path:
            self.set_path(folder_path)
            self.folder_selected.emit(folder_path)
    
    def _on_rescan_clicked(self):
        """Handle rescan button click."""
        if self.path_edit.text():
            self.rescan_requested.emit()
    
    def set_path(self, path: str):
        """
        Set the folder path.
        
        Args:
            path: Folder path to display
        """
        self.path_edit.setText(path)
        self.rescan_btn.setEnabled(bool(path))
    
    def get_path(self) -> str:
        """
        Get the current folder path.
        
        Returns:
            Current folder path
        """
        return self.path_edit.text()
    
    def clear(self):
        """Clear the folder path."""
        self.path_edit.clear()
        self.rescan_btn.setEnabled(False)
    
    def set_enabled(self, enabled: bool):
        """
        Enable or disable the widget.
        
        Args:
            enabled: Whether to enable the widget
        """
        self.path_edit.setEnabled(enabled)
        self.browse_btn.setEnabled(enabled)
        self.rescan_btn.setEnabled(enabled and bool(self.path_edit.text()))
