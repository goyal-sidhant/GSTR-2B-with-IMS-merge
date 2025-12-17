# ui/main_window.py
"""
Main Window for GST Processing Tool v5.0

REDESIGNED: Split-screen layout
- LEFT: Settings (folder, date, preview, comparison)
- RIGHT: Client table (resizable columns)
- Middle: Draggable splitter
"""

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QPushButton, QStatusBar, QMessageBox,
    QShortcut, QApplication, QSplitter, QFrame, QGroupBox,
    QScrollArea, QSizePolicy
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QKeySequence

from pathlib import Path
from typing import Optional

from ui.widgets.folder_section import FolderSection
from ui.widgets.date_section import DateSection
from ui.widgets.client_table import ClientTable
from ui.widgets.preview_section import PreviewSection
from ui.widgets.comparison_section import ComparisonSection
from ui.widgets.log_panel import LogPanel
from ui.widgets.summary_dialog import SummaryDialog, ConfirmDialog

from ui.styles.light_theme import LIGHT_THEME
from ui.styles.dark_theme import DARK_THEME

from core.file_processor import FileProcessor
from core.models import ClientInfo, PreviewData, ProgressInfo, ProcessingSummary

from utils.constants import APP_TITLE, Shortcuts
from utils.logger import setup_logger, get_logger


class ProcessingThread(QThread):
    """
    Worker thread for file processing.
    
    Runs processing in background to keep UI responsive.
    """
    
    # Signals
    progress_updated = pyqtSignal(ProgressInfo)
    processing_complete = pyqtSignal(ProcessingSummary)
    processing_error = pyqtSignal(str)
    log_message = pyqtSignal(str, str, str)  # timestamp, level, message
    
    def __init__(self, processor: FileProcessor, input_path: str, 
                 month: str, year: str, clients: list, comparison_files: list):
        super().__init__()
        self.processor = processor
        self.input_path = input_path
        self.month = month
        self.year = year
        self.clients = clients
        self.comparison_files = comparison_files
    
    def run(self):
        """Run processing in thread."""
        try:
            # Set up progress callback
            def on_progress(progress: ProgressInfo):
                self.progress_updated.emit(progress)
            
            self.processor.set_progress_callback(on_progress)
            
            # Run processing
            summary = self.processor.process_files(
                self.input_path,
                self.month,
                self.year,
                self.clients,
                self.comparison_files
            )
            
            self.processing_complete.emit(summary)
            
        except Exception as e:
            self.processing_error.emit(str(e))


class MainWindow(QMainWindow):
    """
    Main application window with split-screen layout.
    
    LEFT PANEL: Settings
    - Folder selection
    - Date selection
    - Preview counts
    - Comparison reports
    - Process button
    
    RIGHT PANEL: Client table
    - Resizable columns
    - Checkbox selection
    - Select all / Deselect all buttons
    """
    
    def __init__(self):
        super().__init__()
        
        # Initialize logger
        self.logger = setup_logger()
        
        # Initialize processor
        self.processor = FileProcessor()
        
        # State
        self._is_dark_mode = False
        self._clients: list = []
        self._extra_files: list = []
        self._processing_thread: Optional[ProcessingThread] = None
        
        # Set up UI
        self._setup_ui()
        self._setup_shortcuts()
        self._apply_theme()
        
        # Connect logger to UI
        self.logger.set_ui_callback(self._on_log_message)
        
        self.logger.info("Application started")
    
    def _setup_ui(self):
        """Set up the main window UI with split-screen layout."""
        self.setWindowTitle(APP_TITLE)
        self.setMinimumSize(1000, 700)
        self.resize(1200, 800)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Header with theme toggle
        header_layout = QHBoxLayout()
        header_layout.addStretch()
        
        self.theme_btn = QPushButton("🌙 Dark Mode")
        self.theme_btn.setFixedWidth(130)
        self.theme_btn.setProperty("secondary", True)
        self.theme_btn.clicked.connect(self._toggle_theme)
        header_layout.addWidget(self.theme_btn)
        
        main_layout.addLayout(header_layout)
        
        # Tab widget
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        main_layout.addWidget(self.tabs)
        
        # Create tabs
        self._create_processing_tab()
        self._create_log_tab()
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
    
    def _create_processing_tab(self):
        """Create the Processing tab with split layout."""
        processing_widget = QWidget()
        layout = QHBoxLayout(processing_widget)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(0)
        
        # ============================================
        # SPLITTER - Divides left and right panels
        # ============================================
        splitter = QSplitter(Qt.Horizontal)
        splitter.setHandleWidth(8)
        splitter.setChildrenCollapsible(False)
        
        # ============================================
        # LEFT PANEL - Settings
        # ============================================
        left_panel = self._create_left_panel()
        splitter.addWidget(left_panel)
        
        # ============================================
        # RIGHT PANEL - Client Table
        # ============================================
        right_panel = self._create_right_panel()
        splitter.addWidget(right_panel)
        
        # Set initial sizes (35% left, 65% right)
        splitter.setSizes([350, 650])
        
        # Set stretch factors (right panel gets more space when resizing)
        splitter.setStretchFactor(0, 0)  # Left panel - fixed ratio
        splitter.setStretchFactor(1, 1)  # Right panel - expandable
        
        layout.addWidget(splitter)
        
        self.tabs.addTab(processing_widget, "📁 Processing")
    
    def _create_left_panel(self) -> QWidget:
        """Create the left panel with settings."""
        # Scroll area for left panel (in case window is small)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setMinimumWidth(300)
        scroll.setMaximumWidth(450)
        
        # Container widget
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(10, 10, 15, 10)
        layout.setSpacing(15)
        
        # ---- Folder Section ----
        self.folder_section = FolderSection()
        self.folder_section.folder_selected.connect(self._on_folder_selected)
        self.folder_section.rescan_requested.connect(self._rescan_folder)
        layout.addWidget(self.folder_section)
        
        # ---- Date Section ----
        self.date_section = DateSection()
        self.date_section.values_changed.connect(self._on_values_changed)
        layout.addWidget(self.date_section)
        
        # ---- Preview Section ----
        self.preview_section = PreviewSection()
        layout.addWidget(self.preview_section)
        
        # ---- Comparison Section ----
        self.comparison_section = ComparisonSection()
        layout.addWidget(self.comparison_section)
        
        # ---- Process Button ----
        self.process_btn = QPushButton("🚀 Start Processing")
        self.process_btn.setFixedHeight(50)
        self.process_btn.setEnabled(False)
        self.process_btn.clicked.connect(self._start_processing)
        layout.addWidget(self.process_btn)
        
        # Push everything to top
        layout.addStretch()
        
        scroll.setWidget(container)
        return scroll
    
    def _create_right_panel(self) -> QWidget:
        """Create the right panel with client table."""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # ---- Client Table (takes most space) ----
        self.client_table = ClientTable()
        self.client_table.selection_changed.connect(self._on_selection_changed)
        layout.addWidget(self.client_table, stretch=1)
        
        return container
    
    def _create_log_tab(self):
        """Create the Log tab."""
        self.log_panel = LogPanel()
        self.tabs.addTab(self.log_panel, "📋 Log")
    
    def _setup_shortcuts(self):
        """Set up keyboard shortcuts."""
        # Browse folder
        QShortcut(QKeySequence(Shortcuts.BROWSE_FOLDER), self, 
                  self.folder_section._on_browse_clicked)
        
        # Rescan folder
        QShortcut(QKeySequence(Shortcuts.RESCAN_FOLDER), self,
                  self._rescan_folder)
        
        # Start processing
        QShortcut(QKeySequence(Shortcuts.START_PROCESSING), self,
                  self._start_processing)
        
        # Refresh (same as rescan)
        QShortcut(QKeySequence(Shortcuts.REFRESH), self,
                  self._rescan_folder)
        
        # Select all
        QShortcut(QKeySequence(Shortcuts.SELECT_ALL), self,
                  self.client_table._select_all)
        
        # Deselect all
        QShortcut(QKeySequence(Shortcuts.DESELECT_ALL), self,
                  self.client_table._deselect_all)
        
        # Toggle theme
        QShortcut(QKeySequence(Shortcuts.TOGGLE_THEME), self,
                  self._toggle_theme)
        
        # Quit
        QShortcut(QKeySequence(Shortcuts.QUIT), self,
                  self.close)
    
    def _apply_theme(self):
        """Apply current theme."""
        if self._is_dark_mode:
            self.setStyleSheet(DARK_THEME)
            self.theme_btn.setText("☀️ Light Mode")
        else:
            self.setStyleSheet(LIGHT_THEME)
            self.theme_btn.setText("🌙 Dark Mode")
    
    def _toggle_theme(self):
        """Toggle between light and dark themes."""
        self._is_dark_mode = not self._is_dark_mode
        self._apply_theme()
        self.logger.info(f"Theme changed to {'dark' if self._is_dark_mode else 'light'} mode")
    
    @pyqtSlot(str)
    def _on_folder_selected(self, folder_path: str):
        """Handle folder selection."""
        self.logger.info(f"Folder selected: {folder_path}")
        self.status_bar.showMessage("Scanning folder...")
        
        # Auto-detect info
        month, year, client_count = self.processor.auto_detect_folder_info(folder_path)
        
        if month and year:
            self.date_section.set_values(month=month, year=year, total=client_count)
            self.logger.info(f"Auto-detected: {month} {year}, {client_count} clients")
        
        # Scan folder
        self._scan_folder()
    
    def _rescan_folder(self):
        """Rescan the current folder."""
        folder_path = self.folder_section.get_path()
        if folder_path:
            self.logger.info("Rescanning folder...")
            self._scan_folder()
    
    def _scan_folder(self):
        """Scan folder and populate client table."""
        folder_path = self.folder_section.get_path()
        month = self.date_section.get_month()
        year = self.date_section.get_year()
        
        if not folder_path or not month or not year:
            return
        
        # Scan clients
        self._clients, self._extra_files = self.processor.scan_folder(
            folder_path, month, year
        )
        
        # Update client table
        self.client_table.set_clients(self._clients)
        
        # Update preview
        self._update_preview()
        
        # Update status
        self.status_bar.showMessage(
            f"Found {len(self._clients)} clients, {len(self._extra_files)} extra files"
        )
        
        # Enable/disable process button
        self._update_process_button()
    
    def _on_values_changed(self):
        """Handle date/count value changes."""
        # Rescan if folder is selected
        if self.folder_section.get_path():
            self._scan_folder()
    
    def _on_selection_changed(self, selected_count: int):
        """Handle client selection changes."""
        self._update_preview()
        self._update_process_button()
    
    def _update_preview(self):
        """Update the preview section."""
        preview = self.processor.get_preview(self._clients, self._extra_files)
        self.preview_section.update_preview(preview)
    
    def _update_process_button(self):
        """Update process button state and text."""
        selected = self.client_table.get_selected_count()
        self.process_btn.setEnabled(selected > 0)
        self.process_btn.setText(f"🚀 Start Processing ({selected} clients)")
    
    def _start_processing(self):
        """Start the processing operation."""
        if not self.process_btn.isEnabled():
            return
        
        # Get data
        folder_path = self.folder_section.get_path()
        month = self.date_section.get_month()
        year = self.date_section.get_year()
        selected_clients = self.client_table.get_selected_clients()
        comparison_files = self.comparison_section.get_report_paths()
        
        # Get preview counts
        preview = self.processor.get_preview(selected_clients, self._extra_files)
        
        # Show confirmation dialog
        confirm = ConfirmDialog(
            merge_count=preview.merge_count,
            create_count=preview.create_count,
            copy_count=preview.copy_count,
            extra_files=self._extra_files,
            month_year=f"{month} {year}",
            parent=self
        )
        
        if confirm.exec_() != ConfirmDialog.Accepted:
            return
        
        # Switch to Log tab
        self.tabs.setCurrentIndex(1)
        
        # Disable UI
        self._set_ui_enabled(False)
        self.status_bar.showMessage("Processing...")
        
        # Reset progress
        self.log_panel.reset_progress()
        self.log_panel.clear_log()
        
        # Start processing thread
        self._processing_thread = ProcessingThread(
            self.processor,
            folder_path,
            month,
            year,
            selected_clients,
            comparison_files
        )
        
        self._processing_thread.progress_updated.connect(self._on_progress_updated)
        self._processing_thread.processing_complete.connect(self._on_processing_complete)
        self._processing_thread.processing_error.connect(self._on_processing_error)
        
        self._processing_thread.start()
    
    @pyqtSlot(ProgressInfo)
    def _on_progress_updated(self, progress: ProgressInfo):
        """Handle progress updates from processing thread."""
        self.log_panel.update_progress(progress)
        self.status_bar.showMessage(
            f"Processing: {progress.current}/{progress.total} | "
            f"{progress.client_name}"
        )
    
    @pyqtSlot(ProcessingSummary)
    def _on_processing_complete(self, summary: ProcessingSummary):
        """Handle processing completion."""
        # Re-enable UI
        self._set_ui_enabled(True)
        
        # Update log panel
        self.log_panel.set_complete()
        
        # Update status bar
        self.status_bar.showMessage(
            f"Complete | Merged: {summary.merged} | Created: {summary.created} | "
            f"Copied: {summary.copied} | Errors: {summary.errors}"
        )
        
        # Show summary dialog
        month_year = f"{self.date_section.get_month()} {self.date_section.get_year()}"
        dialog = SummaryDialog(summary, month_year, self)
        dialog.exec_()
    
    @pyqtSlot(str)
    def _on_processing_error(self, error_message: str):
        """Handle processing error."""
        self._set_ui_enabled(True)
        self.status_bar.showMessage("Processing failed")
        
        self.logger.error(f"Processing failed: {error_message}")
        
        QMessageBox.critical(
            self,
            "Processing Error",
            f"An error occurred during processing:\n\n{error_message}"
        )
    
    def _on_log_message(self, timestamp: str, level: str, message: str):
        """Handle log messages from logger."""
        self.log_panel.add_log_message(timestamp, level, message)
    
    def _set_ui_enabled(self, enabled: bool):
        """Enable or disable UI elements during processing."""
        self.folder_section.set_enabled(enabled)
        self.date_section.set_enabled(enabled)
        self.client_table.set_enabled(enabled)
        self.comparison_section.set_enabled(enabled)
        self.process_btn.setEnabled(enabled and self.client_table.get_selected_count() > 0)
        self.theme_btn.setEnabled(enabled)
    
    def closeEvent(self, event):
        """Handle window close event."""
        # Check if processing is running
        if self._processing_thread and self._processing_thread.isRunning():
            reply = QMessageBox.question(
                self,
                "Processing in Progress",
                "Processing is still running. Are you sure you want to quit?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.No:
                event.ignore()
                return
        
        # Log session end
        self.logger.session_end()
        
        event.accept()
