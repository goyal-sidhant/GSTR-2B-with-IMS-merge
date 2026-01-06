# ui/main_window.py
"""
Main Window for GST Processing Tool v5.0

REDESIGNED: Tab-based layout with tabs at header level
- HEADER: [Setup] [Selection] [Log] ... [Dark Mode]
- Setup Tab: Folder, Date, Comparison, Process button
- Selection Tab: Preview stats + Quick filters + Client table
- Log Tab: Progress + Log messages
"""

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QPushButton, QStatusBar, QMessageBox,
    QShortcut
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QKeySequence

from typing import Optional

from ui.tabs.setup_tab import SetupTab
from ui.tabs.selection_tab import SelectionTab
from ui.widgets.log_panel import LogPanel
from ui.widgets.summary_dialog import SummaryDialog, ConfirmDialog

from ui.styles.light_theme import LIGHT_THEME
from ui.styles.dark_theme import DARK_THEME

from core.file_processor import FileProcessor
from core.models import ProgressInfo, ProcessingSummary

from utils.constants import APP_TITLE, Shortcuts
from utils.logger import setup_logger


class ProcessingThread(QThread):
    """
    Worker thread for file processing.

    Runs processing in background to keep UI responsive.
    """

    # Signals
    progress_updated = pyqtSignal(ProgressInfo)
    processing_complete = pyqtSignal(ProcessingSummary)
    processing_error = pyqtSignal(str)

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
            def on_progress(progress: ProgressInfo):
                self.progress_updated.emit(progress)

            self.processor.set_progress_callback(on_progress)

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
    Main application window with tab-based layout.

    Header: [Setup] [Selection] [Log] tabs + [Dark Mode] button

    Setup Tab: Configuration settings
    Selection Tab: Preview stats + Client selection
    Log Tab: Progress + Log messages
    """

    # Tab indices
    TAB_SETUP = 0
    TAB_SELECTION = 1
    TAB_LOG = 2

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
        self._setup_connections()
        self._setup_shortcuts()
        self._apply_theme()

        # Connect logger to UI
        self.logger.set_ui_callback(self._on_log_message)

        self.logger.info("Application started")

    def _setup_ui(self):
        """Set up the main window UI with tabs at header level."""
        self.setWindowTitle(APP_TITLE)
        self.setMinimumSize(1000, 700)
        self.resize(1200, 800)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(0)

        # ============================================
        # HEADER: Tabs on left, Dark Mode on right
        # ============================================
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 5)
        header_layout.setSpacing(10)

        # Tab widget
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        header_layout.addWidget(self.tabs, stretch=1)

        # Dark mode button aligned with tabs
        self.theme_btn = QPushButton("🌙 Dark Mode")
        self.theme_btn.setFixedWidth(130)
        self.theme_btn.setFixedHeight(32)
        self.theme_btn.setProperty("secondary", True)
        self.theme_btn.clicked.connect(self._toggle_theme)
        header_layout.addWidget(self.theme_btn, alignment=Qt.AlignTop)

        main_layout.addLayout(header_layout)

        # ============================================
        # Create tabs
        # ============================================
        self.setup_tab = SetupTab()
        self.tabs.addTab(self.setup_tab, "⚙️ Setup")

        self.selection_tab = SelectionTab()
        self.tabs.addTab(self.selection_tab, "📋 Selection")

        self.log_panel = LogPanel()
        self.tabs.addTab(self.log_panel, "📜 Log")

        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")

    def _setup_connections(self):
        """Set up signal connections between tabs and main window."""
        # Setup tab signals
        self.setup_tab.folder_selected.connect(self._on_folder_selected)
        self.setup_tab.rescan_requested.connect(self._rescan_folder)
        self.setup_tab.values_changed.connect(self._on_values_changed)

        # Selection tab signals
        self.selection_tab.selection_changed.connect(self._on_selection_changed)
        self.selection_tab.filter_changed.connect(self._on_filter_changed)
        self.selection_tab.process_requested.connect(self._start_processing)

    def _setup_shortcuts(self):
        """Set up keyboard shortcuts."""
        # Browse folder
        QShortcut(QKeySequence(Shortcuts.BROWSE_FOLDER), self,
                  self.setup_tab.folder_section._on_browse_clicked)

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
                  self.selection_tab.select_all)

        # Deselect all
        QShortcut(QKeySequence(Shortcuts.DESELECT_ALL), self,
                  self.selection_tab.deselect_all)

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

    # ============================================
    # Event Handlers - Setup Tab
    # ============================================

    @pyqtSlot(str)
    def _on_folder_selected(self, folder_path: str):
        """Handle folder selection."""
        self.logger.info(f"Folder selected: {folder_path}")
        self.status_bar.showMessage("Scanning folder...")

        # Auto-detect info
        month, year, client_count = self.processor.auto_detect_folder_info(folder_path)

        if month and year:
            self.setup_tab.set_date_values(month=month, year=year, total=client_count)
            self.logger.info(f"Auto-detected: {month} {year}, {client_count} clients")

        # Scan folder and switch to Selection tab
        self._scan_folder()
        self.tabs.setCurrentIndex(self.TAB_SELECTION)

    def _rescan_folder(self):
        """Rescan the current folder."""
        folder_path = self.setup_tab.get_folder_path()
        if folder_path:
            self.logger.info("Rescanning folder...")
            self._scan_folder()

    def _scan_folder(self):
        """Scan folder and populate client table."""
        folder_path = self.setup_tab.get_folder_path()
        month = self.setup_tab.get_month()
        year = self.setup_tab.get_year()

        if not folder_path or not month or not year:
            return

        # Scan clients
        self._clients, self._extra_files = self.processor.scan_folder(
            folder_path, month, year
        )

        # Update selection tab
        self.selection_tab.set_clients(self._clients)

        # Update preview
        self._update_preview()

        # Update status
        self.status_bar.showMessage(
            f"Found {len(self._clients)} clients, {len(self._extra_files)} extra files"
        )

    def _on_values_changed(self):
        """Handle date/count value changes."""
        if self.setup_tab.get_folder_path():
            self._scan_folder()

    # ============================================
    # Event Handlers - Selection Tab
    # ============================================

    def _on_selection_changed(self, selected_count: int):
        """Handle client selection changes."""
        self._update_preview()

    def _on_filter_changed(self, filter_type: str):
        """Handle quick filter changes."""
        self.logger.info(f"Filter applied: {filter_type}")
        # Preview updates automatically via selection_changed signal

    def _update_preview(self):
        """Update the preview section with selected clients."""
        selected_clients = self.selection_tab.get_selected_clients()
        preview = self.processor.get_preview(selected_clients, self._extra_files)
        self.selection_tab.update_preview(preview)

    # ============================================
    # Processing
    # ============================================

    def _start_processing(self):
        """Start the processing operation."""
        selected_count = self.selection_tab.get_selected_count()
        if selected_count == 0:
            return

        # Get data
        folder_path = self.setup_tab.get_folder_path()
        month = self.setup_tab.get_month()
        year = self.setup_tab.get_year()
        selected_clients = self.selection_tab.get_selected_clients()
        comparison_files = self.setup_tab.get_comparison_files()

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
        self.tabs.setCurrentIndex(self.TAB_LOG)

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
        month_year = f"{self.setup_tab.get_month()} {self.setup_tab.get_year()}"
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
        self.setup_tab.set_enabled(enabled)
        self.selection_tab.set_enabled(enabled)
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
