# ui/styles/light_theme.py
"""
Light theme stylesheet for GST Processing Tool v5.0

This file contains the CSS-like stylesheet for PyQt5.
PyQt5 uses a subset of CSS called QSS (Qt Style Sheets).
"""

LIGHT_THEME = """
/* ============================================
   LIGHT THEME - GST Processing Tool v5.0
   ============================================ */

/* Main Window */
QMainWindow {
    background-color: #f5f5f5;
}

QWidget {
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 10pt;
    color: #333333;
}

/* Tab Widget */
QTabWidget::pane {
    border: 1px solid #cccccc;
    background-color: #ffffff;
    border-radius: 4px;
}

QTabBar::tab {
    background-color: #e0e0e0;
    color: #555555;
    padding: 10px 20px;
    margin-right: 2px;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
}

QTabBar::tab:selected {
    background-color: #ffffff;
    color: #1a73e8;
    font-weight: bold;
}

QTabBar::tab:hover:!selected {
    background-color: #d0d0d0;
}

/* Group Boxes */
QGroupBox {
    font-weight: bold;
    border: 1px solid #cccccc;
    border-radius: 6px;
    margin-top: 12px;
    padding-top: 10px;
    background-color: #ffffff;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 5px;
    color: #1a73e8;
}

/* Buttons */
QPushButton {
    background-color: #1a73e8;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #1557b0;
}

QPushButton:pressed {
    background-color: #0d47a1;
}

QPushButton:disabled {
    background-color: #cccccc;
    color: #888888;
}

/* Secondary Button Style */
QPushButton[secondary="true"] {
    background-color: #ffffff;
    color: #1a73e8;
    border: 1px solid #1a73e8;
}

QPushButton[secondary="true"]:hover {
    background-color: #e8f0fe;
}

/* Danger Button Style */
QPushButton[danger="true"] {
    background-color: #dc3545;
}

QPushButton[danger="true"]:hover {
    background-color: #c82333;
}

/* Line Edits */
QLineEdit {
    padding: 8px;
    border: 1px solid #cccccc;
    border-radius: 4px;
    background-color: #ffffff;
}

QLineEdit:focus {
    border: 2px solid #1a73e8;
}

QLineEdit:disabled {
    background-color: #f0f0f0;
    color: #888888;
}

/* Combo Boxes */
QComboBox {
    padding: 8px;
    border: 1px solid #cccccc;
    border-radius: 4px;
    background-color: #ffffff;
}

QComboBox:focus {
    border: 2px solid #1a73e8;
}

QComboBox::drop-down {
    border: none;
    padding-right: 10px;
}

QComboBox::down-arrow {
    width: 12px;
    height: 12px;
}

QComboBox QAbstractItemView {
    background-color: #ffffff;
    border: 1px solid #cccccc;
    selection-background-color: #e8f0fe;
    selection-color: #1a73e8;
}

/* Tables */
QTableWidget {
    background-color: #ffffff;
    alternate-background-color: #f9f9f9;
    border: 1px solid #cccccc;
    border-radius: 4px;
    gridline-color: #e0e0e0;
}

QTableWidget::item {
    padding: 8px;
}

QTableWidget::item:selected {
    background-color: #e8f0fe;
    color: #1a73e8;
}

QHeaderView::section {
    background-color: #f0f0f0;
    color: #333333;
    padding: 10px;
    border: none;
    border-right: 1px solid #e0e0e0;
    border-bottom: 1px solid #cccccc;
    font-weight: bold;
}

/* Checkboxes */
QCheckBox {
    spacing: 8px;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border: 2px solid #cccccc;
    border-radius: 3px;
    background-color: #ffffff;
}

QCheckBox::indicator:checked {
    background-color: #1a73e8;
    border-color: #1a73e8;
}

QCheckBox::indicator:hover {
    border-color: #1a73e8;
}

/* Progress Bar */
QProgressBar {
    border: 1px solid #cccccc;
    border-radius: 4px;
    text-align: center;
    background-color: #e0e0e0;
    height: 25px;
}

QProgressBar::chunk {
    background-color: #1a73e8;
    border-radius: 3px;
}

/* Text Edit (Log Panel) */
QTextEdit {
    background-color: #ffffff;
    border: 1px solid #cccccc;
    border-radius: 4px;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 9pt;
}

/* List Widget */
QListWidget {
    background-color: #ffffff;
    border: 1px solid #cccccc;
    border-radius: 4px;
}

QListWidget::item {
    padding: 8px;
    border-bottom: 1px solid #f0f0f0;
}

QListWidget::item:selected {
    background-color: #e8f0fe;
    color: #1a73e8;
}

QListWidget::item:hover {
    background-color: #f5f5f5;
}

/* Scroll Bars */
QScrollBar:vertical {
    background-color: #f5f5f5;
    width: 12px;
    border-radius: 6px;
}

QScrollBar::handle:vertical {
    background-color: #cccccc;
    border-radius: 6px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background-color: #aaaaaa;
}

QScrollBar:horizontal {
    background-color: #f5f5f5;
    height: 12px;
    border-radius: 6px;
}

QScrollBar::handle:horizontal {
    background-color: #cccccc;
    border-radius: 6px;
    min-width: 30px;
}

/* Status Bar */
QStatusBar {
    background-color: #f0f0f0;
    border-top: 1px solid #cccccc;
    color: #555555;
}

/* Labels */
QLabel {
    color: #333333;
}

QLabel[heading="true"] {
    font-size: 14pt;
    font-weight: bold;
    color: #1a73e8;
}

QLabel[subheading="true"] {
    font-size: 11pt;
    color: #555555;
}

QLabel[error="true"] {
    color: #dc3545;
    font-weight: bold;
}

QLabel[warning="true"] {
    color: #ffa500;
    font-weight: bold;
}

QLabel[success="true"] {
    color: #28a745;
    font-weight: bold;
}

/* Message Boxes / Dialogs */
QMessageBox {
    background-color: #ffffff;
}

QDialog {
    background-color: #ffffff;
}

/* Tool Tips */
QToolTip {
    background-color: #333333;
    color: #ffffff;
    border: none;
    padding: 5px;
    border-radius: 3px;
}

/* Splitter */
QSplitter::handle {
    background-color: #cccccc;
    border-radius: 2px;
}

QSplitter::handle:horizontal {
    width: 8px;
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #f5f5f5, stop:0.3 #cccccc, stop:0.5 #aaaaaa, stop:0.7 #cccccc, stop:1 #f5f5f5);
}

QSplitter::handle:hover {
    background-color: #1a73e8;
}

QSplitter::handle:horizontal:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #e8f0fe, stop:0.3 #1a73e8, stop:0.5 #1557b0, stop:0.7 #1a73e8, stop:1 #e8f0fe);
}
"""
