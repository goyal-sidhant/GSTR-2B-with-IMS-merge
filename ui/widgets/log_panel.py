# ui/widgets/log_panel.py
"""
Log Panel Widget for GST Processing Tool v5.0

Shows:
- Progress bar with current status
- Live log messages with timestamps
- Color-coded log levels
- Clear button
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTextEdit, 
    QHBoxLayout, QPushButton
)
from PyQt5.QtWidgets import QGroupBox, QLabel, QProgressBar
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QTextCursor, QTextCharFormat, QColor

from core.models import ProgressInfo

class LogPanel(QWidget):
    """Log panel widget for displaying processing logs."""
    
    # Signal for thread-safe logging
    log_signal = pyqtSignal(str, str)  # message, level
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        
        # Connect signal to slot for thread-safe updates
        self.log_signal.connect(self._add_log_safe)
    
    def _setup_ui(self):
        """Set up the widget UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Progress section
        progress_group = QGroupBox("📈 Progress")
        progress_layout = QVBoxLayout(progress_group)
        progress_layout.setContentsMargins(10, 15, 10, 10)
        
        # Status label
        self.status_label = QLabel("Ready to process")
        self.status_label.setStyleSheet("font-weight: bold; font-size: 11pt;")
        progress_layout.addWidget(self.status_label)
        
        # Progress bar with percentage
        progress_row = QHBoxLayout()
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("%v / %m")
        progress_row.addWidget(self.progress_bar, stretch=1)
        
        self.percent_label = QLabel("0%")
        self.percent_label.setFixedWidth(50)
        self.percent_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.percent_label.setStyleSheet("font-weight: bold; font-size: 12pt;")
        progress_row.addWidget(self.percent_label)
        
        progress_layout.addLayout(progress_row)
        layout.addWidget(progress_group)
        
        # Log section
        log_group = QGroupBox("📋 Log")
        log_layout = QVBoxLayout(log_group)
        log_layout.setContentsMargins(10, 15, 10, 10)
        
        # Log text area
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setLineWrapMode(QTextEdit.NoWrap)
        log_layout.addWidget(self.log_text)
        
        # Clear button
        button_row = QHBoxLayout()
        button_row.addStretch()
        
        self.clear_btn = QPushButton("Clear Log")
        self.clear_btn.setFixedWidth(100)
        self.clear_btn.setProperty("secondary", True)
        self.clear_btn.clicked.connect(self.clear_log)
        button_row.addWidget(self.clear_btn)
        
        log_layout.addLayout(button_row)
        layout.addWidget(log_group, stretch=1)
    
    @pyqtSlot(str, str, str)
    def add_log_message(self, timestamp: str, level: str, message: str):
        """
        Add a log message to the display.
        
        Args:
            timestamp: Time string (HH:MM:SS)
            level: Log level (INFO, WARNING, ERROR, DEBUG)
            message: Log message
        """

        # Emit to main thread slot which handles UI updates
        self.log_signal.emit(message, level)

        # Format the message
        formatted = f"{timestamp} | {level:7s} | {message}"
        
        # Get cursor and move to end
        cursor = self.log_text.textCursor()
        cursor.movePosition(QTextCursor.End)
        
        # Set format based on level
        fmt = QTextCharFormat()
        
        if level == "ERROR":
            fmt.setForeground(QColor("#dc3545"))  # Red
            fmt.setFontWeight(700)  # Bold
        elif level == "WARNING":
            fmt.setForeground(QColor("#ff9800"))  # Orange
        elif level == "INFO":
            if "✓" in message:
                fmt.setForeground(QColor("#28a745"))  # Green for success
            elif "✗" in message:
                fmt.setForeground(QColor("#dc3545"))  # Red for failure
            else:
                fmt.setForeground(QColor("#333333"))  # Default
        elif level == "DEBUG":
            fmt.setForeground(QColor("#6c757d"))  # Gray
        else:
            fmt.setForeground(QColor("#333333"))
        
        # Insert text with formatting
        cursor.setCharFormat(fmt)
        cursor.insertText(formatted + "\n")
        
        # Scroll to bottom
        self.log_text.setTextCursor(cursor)
        self.log_text.ensureCursorVisible()

    def _add_log_safe(self, message: str, level: str = "INFO"):
        """Actually add the log message (called in main thread)."""
        from datetime import datetime

        timestamp = datetime.now().strftime("%H:%M:%S")

        # Color based on level
        colors = {
            "INFO": "#4fc3f7",
            "SUCCESS": "#81c784",
            "WARNING": "#ffb74d",
            "ERROR": "#e57373"
        }
        color = colors.get(level, "#ffffff")

        formatted = f'<span style="color: #888;">[{timestamp}]</span> <span style="color: {color};">[{level}]</span> {message}'

        self.log_text.append(formatted)
        self.log_text.moveCursor(QTextCursor.End)
    
    def update_progress(self, progress: ProgressInfo):
        """
        Update progress display.
        
        Args:
            progress: ProgressInfo object
        """
        self.progress_bar.setMaximum(progress.total)
        self.progress_bar.setValue(progress.current)
        self.progress_bar.setFormat(f"{progress.current} / {progress.total}")
        self.percent_label.setText(f"{progress.percentage}%")
        
        if progress.client_name:
            self.status_label.setText(f"Processing: {progress.client_name}")
        elif progress.message:
            self.status_label.setText(progress.message)
    
    def set_status(self, message: str):
        """
        Set status label text.
        
        Args:
            message: Status message
        """
        self.status_label.setText(message)
    
    def set_progress(self, current: int, total: int):
        """
        Set progress bar values.
        
        Args:
            current: Current value
            total: Maximum value
        """
        self.progress_bar.setMaximum(total)
        self.progress_bar.setValue(current)
        self.progress_bar.setFormat(f"{current} / {total}")
        
        if total > 0:
            percent = int((current / total) * 100)
            self.percent_label.setText(f"{percent}%")
        else:
            self.percent_label.setText("0%")
    
    def reset_progress(self):
        """Reset progress bar to initial state."""
        self.progress_bar.setValue(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setFormat("0 / 0")
        self.percent_label.setText("0%")
        self.status_label.setText("Ready to process")
    
    def set_complete(self):
        """Set progress to complete state."""
        self.progress_bar.setValue(self.progress_bar.maximum())
        self.percent_label.setText("100%")
        self.status_label.setText("✓ Processing Complete!")
        self.status_label.setStyleSheet(
            "font-weight: bold; font-size: 11pt; color: #28a745;"
        )
    
    def clear_log(self):
        """Clear the log text."""
        self.log_text.clear()
    
    def get_log_text(self) -> str:
        """Get all log text."""
        return self.log_text.toPlainText()
