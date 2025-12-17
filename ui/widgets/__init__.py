# ui/widgets/__init__.py
"""
Custom UI widgets for GST Processing Tool v5.0

Each widget is a self-contained component that can be reused.
"""

from ui.widgets.folder_section import FolderSection
from ui.widgets.date_section import DateSection
from ui.widgets.client_table import ClientTable
from ui.widgets.preview_section import PreviewSection
from ui.widgets.comparison_section import ComparisonSection
from ui.widgets.log_panel import LogPanel
from ui.widgets.summary_dialog import SummaryDialog, ConfirmDialog

__all__ = [
    'FolderSection',
    'DateSection',
    'ClientTable',
    'PreviewSection',
    'ComparisonSection',
    'LogPanel',
    'SummaryDialog',
    'ConfirmDialog'
]
