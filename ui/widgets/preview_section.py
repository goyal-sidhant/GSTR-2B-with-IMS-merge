# ui/widgets/preview_section.py
"""
Preview Section Widget for GST Processing Tool v5.0

Compact horizontal stats bar showing:
- Merge count
- Create count
- Copy count
- Extra files count
"""

from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QLabel, QFrame, QSizePolicy
)
from PyQt5.QtCore import Qt

from core.models import PreviewData


class PreviewSection(QFrame):
    """
    Compact preview section showing processing breakdown.
    Horizontal layout with colored badges that spread evenly.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)
        self.setFixedHeight(50)
        self.setStyleSheet("""
            PreviewSection {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 6px;
            }
        """)
        self._setup_ui()

    def _setup_ui(self):
        """Set up the widget UI."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 8, 15, 8)
        layout.setSpacing(15)

        # Stats label
        stats_label = QLabel("Statistics:")
        stats_label.setStyleSheet("font-weight: bold; color: #495057;")
        layout.addWidget(stats_label)

        # Merge badge
        self.merge_badge = self._create_badge("Merge", "0", "#198754", "#d1e7dd")
        layout.addWidget(self.merge_badge)

        # Create badge
        self.create_badge = self._create_badge("Create", "0", "#0d6efd", "#cfe2ff")
        layout.addWidget(self.create_badge)

        # Copy badge
        self.copy_badge = self._create_badge("Copy", "0", "#fd7e14", "#ffe5d0")
        layout.addWidget(self.copy_badge)

        # Extra badge
        self.extra_badge = self._create_badge("Extra", "0", "#6c757d", "#e9ecef")
        layout.addWidget(self.extra_badge)

        # Stretch to push badges to the left but not too far
        layout.addStretch(1)

    def _create_badge(self, label: str, count: str, text_color: str, bg_color: str) -> QWidget:
        """Create a compact badge widget."""
        container = QWidget()
        container.setStyleSheet(f"""
            QWidget {{
                background-color: {bg_color};
                border-radius: 4px;
            }}
        """)

        badge_layout = QHBoxLayout(container)
        badge_layout.setContentsMargins(12, 4, 12, 4)
        badge_layout.setSpacing(8)

        # Label
        label_widget = QLabel(f"{label}:")
        label_widget.setStyleSheet(f"color: {text_color}; font-weight: 500; background: transparent;")
        badge_layout.addWidget(label_widget)

        # Count
        count_widget = QLabel(count)
        count_widget.setObjectName("count")
        count_widget.setStyleSheet(f"color: {text_color}; font-weight: bold; font-size: 14pt; background: transparent;")
        badge_layout.addWidget(count_widget)

        return container

    def _update_badge_count(self, badge: QWidget, count: int):
        """Update the count in a badge."""
        count_label = badge.findChild(QLabel, "count")
        if count_label:
            count_label.setText(str(count))

    def update_preview(self, preview_data: PreviewData):
        """Update the preview display."""
        self._update_badge_count(self.merge_badge, preview_data.merge_count)
        self._update_badge_count(self.create_badge, preview_data.create_count)
        self._update_badge_count(self.copy_badge, preview_data.copy_count)
        self._update_badge_count(self.extra_badge, preview_data.extra_files_count)

    def set_counts(self, merge: int, create: int, copy: int, extra: int):
        """Set counts directly."""
        self._update_badge_count(self.merge_badge, merge)
        self._update_badge_count(self.create_badge, create)
        self._update_badge_count(self.copy_badge, copy)
        self._update_badge_count(self.extra_badge, extra)

    def clear(self):
        """Clear all preview data."""
        self._update_badge_count(self.merge_badge, 0)
        self._update_badge_count(self.create_badge, 0)
        self._update_badge_count(self.copy_badge, 0)
        self._update_badge_count(self.extra_badge, 0)
