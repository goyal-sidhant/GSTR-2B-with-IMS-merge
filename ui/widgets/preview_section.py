# ui/widgets/preview_section.py
"""
Preview Section Widget for GST Processing Tool v5.0

Shows before processing:
- Merge count
- Create count
- Copy count
- Extra files list
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
    QLabel, QListWidget, QFrame
)
from PyQt5.QtCore import Qt

from typing import List
from core.models import PreviewData


class PreviewSection(QGroupBox):
    """
    Preview section showing processing breakdown and extra files.
    """
    
    def __init__(self, parent=None):
        super().__init__("📊 Preview", parent)
        self._setup_ui()
    
    def _setup_ui(self):
        """Set up the widget UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 15, 10, 10)
        layout.setSpacing(10)
        
        # Counts row
        counts_layout = QHBoxLayout()
        counts_layout.setSpacing(20)
        
        # Merge count
        self.merge_frame = self._create_count_card("📁 Merge", "0", "#4caf50")
        counts_layout.addWidget(self.merge_frame)
        
        # Create count
        self.create_frame = self._create_count_card("📝 Create", "0", "#2196f3")
        counts_layout.addWidget(self.create_frame)
        
        # Copy count
        self.copy_frame = self._create_count_card("⚠️ Copy", "0", "#ff9800")
        counts_layout.addWidget(self.copy_frame)
        
        # Extra files count
        self.extra_frame = self._create_count_card("📄 Extra", "0", "#9e9e9e")
        counts_layout.addWidget(self.extra_frame)
        
        counts_layout.addStretch()
        layout.addLayout(counts_layout)
        
        # Extra files section (collapsible-like)
        self.extra_files_label = QLabel("⚠️ Extra Files (won't be processed):")
        self.extra_files_label.setStyleSheet("font-weight: bold; color: #ff9800;")
        self.extra_files_label.hide()
        layout.addWidget(self.extra_files_label)
        
        self.extra_files_list = QListWidget()
        self.extra_files_list.setMaximumHeight(80)
        self.extra_files_list.hide()
        layout.addWidget(self.extra_files_list)
    
    def _create_count_card(self, title: str, count: str, color: str) -> QFrame:
        """Create a count card widget."""
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: {color}20;
                border: 1px solid {color};
                border-radius: 6px;
                padding: 5px;
            }}
        """)
        
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(2)
        
        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet(f"font-size: 9pt; color: {color};")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Count
        count_label = QLabel(count)
        count_label.setObjectName("count")
        count_label.setStyleSheet(f"font-size: 16pt; font-weight: bold; color: {color};")
        count_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(count_label)
        
        frame.setFixedWidth(100)
        return frame
    
    def _update_card_count(self, frame: QFrame, count: int):
        """Update the count in a card."""
        count_label = frame.findChild(QLabel, "count")
        if count_label:
            count_label.setText(str(count))
    
    def update_preview(self, preview_data: PreviewData):
        """
        Update the preview display.
        
        Args:
            preview_data: PreviewData object with counts and extra files
        """
        # Update counts
        self._update_card_count(self.merge_frame, preview_data.merge_count)
        self._update_card_count(self.create_frame, preview_data.create_count)
        self._update_card_count(self.copy_frame, preview_data.copy_count)
        self._update_card_count(self.extra_frame, preview_data.extra_files_count)
        
        # Update extra files list
        self.extra_files_list.clear()
        
        if preview_data.extra_files:
            self.extra_files_label.show()
            self.extra_files_list.show()
            for filename in preview_data.extra_files:
                self.extra_files_list.addItem(f"• {filename}")
        else:
            self.extra_files_label.hide()
            self.extra_files_list.hide()
    
    def set_counts(self, merge: int, create: int, copy: int, extra: int):
        """
        Set counts directly.
        
        Args:
            merge: Merge count
            create: Create count
            copy: Copy count
            extra: Extra files count
        """
        self._update_card_count(self.merge_frame, merge)
        self._update_card_count(self.create_frame, create)
        self._update_card_count(self.copy_frame, copy)
        self._update_card_count(self.extra_frame, extra)
    
    def set_extra_files(self, files: List[str]):
        """
        Set extra files list.
        
        Args:
            files: List of extra file names
        """
        self.extra_files_list.clear()
        
        if files:
            self.extra_files_label.show()
            self.extra_files_list.show()
            for filename in files:
                self.extra_files_list.addItem(f"• {filename}")
        else:
            self.extra_files_label.hide()
            self.extra_files_list.hide()
    
    def clear(self):
        """Clear all preview data."""
        self._update_card_count(self.merge_frame, 0)
        self._update_card_count(self.create_frame, 0)
        self._update_card_count(self.copy_frame, 0)
        self._update_card_count(self.extra_frame, 0)
        self.extra_files_list.clear()
        self.extra_files_label.hide()
        self.extra_files_list.hide()
