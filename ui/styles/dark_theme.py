# ui/styles/dark_theme.py
"""
Dark theme stylesheet for GST Processing Tool v5.0

Dark mode for comfortable viewing during long sessions.
"""

DARK_THEME = """
/* ============================================
   DARK THEME - GST Processing Tool v5.0
   ============================================ */

/* Main Window */
QMainWindow {
    background-color: #1e1e1e;
}

QWidget {
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 10pt;
    color: #e0e0e0;
    background-color: #1e1e1e;
}

/* Tab Widget */
QTabWidget::pane {
    border: 1px solid #3d3d3d;
    background-color: #252526;
    border-radius: 4px;
}

QTabBar::tab {
    background-color: #2d2d2d;
    color: #aaaaaa;
    padding: 10px 20px;
    margin-right: 2px;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
}

QTabBar::tab:selected {
    background-color: #252526;
    color: #4fc3f7;
    font-weight: bold;
}

QTabBar::tab:hover:!selected {
    background-color: #3d3d3d;
}

/* Group Boxes */
QGroupBox {
    font-weight: bold;
    border: 1px solid #3d3d3d;
    border-radius: 6px;
    margin-top: 12px;
    padding-top: 10px;
    background-color: #252526;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 5px;
    color: #4fc3f7;
}

/* Buttons */
QPushButton {
    background-color: #0078d4;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #1084d8;
}

QPushButton:pressed {
    background-color: #006cbd;
}

QPushButton:disabled {
    background-color: #3d3d3d;
    color: #666666;
}

/* Secondary Button Style */
QPushButton[secondary="true"] {
    background-color: transparent;
    color: #4fc3f7;
    border: 1px solid #4fc3f7;
}

QPushButton[secondary="true"]:hover {
    background-color: #2d3748;
}

/* Danger Button Style */
QPushButton[danger="true"] {
    background-color: #dc3545;
}

QPushButton[danger="true"]:hover {
    background-color: #e04555;
}

/* Line Edits */
QLineEdit {
    padding: 8px;
    border: 1px solid #3d3d3d;
    border-radius: 4px;
    background-color: #2d2d2d;
    color: #e0e0e0;
}

QLineEdit:focus {
    border: 2px solid #4fc3f7;
}

QLineEdit:disabled {
    background-color: #1e1e1e;
    color: #666666;
}

/* Combo Boxes */
QComboBox {
    padding: 8px;
    border: 1px solid #3d3d3d;
    border-radius: 4px;
    background-color: #2d2d2d;
    color: #e0e0e0;
}

QComboBox:focus {
    border: 2px solid #4fc3f7;
}

QComboBox::drop-down {
    border: none;
    padding-right: 10px;
}

QComboBox QAbstractItemView {
    background-color: #2d2d2d;
    border: 1px solid #3d3d3d;
    selection-background-color: #0078d4;
    selection-color: #ffffff;
}

/* Tables */
QTableWidget {
    background-color: #252526;
    alternate-background-color: #2d2d2d;
    border: 1px solid #3d3d3d;
    border-radius: 4px;
    gridline-color: #3d3d3d;
    color: #e0e0e0;
}

QTableWidget::item {
    padding: 8px;
}

QTableWidget::item:selected {
    background-color: #0078d4;
    color: #ffffff;
}

QHeaderView::section {
    background-color: #2d2d2d;
    color: #e0e0e0;
    padding: 10px;
    border: none;
    border-right: 1px solid #3d3d3d;
    border-bottom: 1px solid #3d3d3d;
    font-weight: bold;
}

/* Checkboxes */
QCheckBox {
    spacing: 8px;
    color: #e0e0e0;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border: 2px solid #555555;
    border-radius: 3px;
    background-color: #2d2d2d;
}

QCheckBox::indicator:checked {
    background-color: #0078d4;
    border-color: #0078d4;
}

QCheckBox::indicator:hover {
    border-color: #4fc3f7;
}

/* Progress Bar */
QProgressBar {
    border: 1px solid #3d3d3d;
    border-radius: 4px;
    text-align: center;
    background-color: #2d2d2d;
    color: #e0e0e0;
    height: 25px;
}

QProgressBar::chunk {
    background-color: #0078d4;
    border-radius: 3px;
}

/* Text Edit (Log Panel) */
QTextEdit {
    background-color: #1e1e1e;
    border: 1px solid #3d3d3d;
    border-radius: 4px;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 9pt;
    color: #e0e0e0;
}

/* List Widget */
QListWidget {
    background-color: #252526;
    border: 1px solid #3d3d3d;
    border-radius: 4px;
    color: #e0e0e0;
}

QListWidget::item {
    padding: 8px;
    border-bottom: 1px solid #3d3d3d;
}

QListWidget::item:selected {
    background-color: #0078d4;
    color: #ffffff;
}

QListWidget::item:hover {
    background-color: #2d2d2d;
}

/* Scroll Bars */
QScrollBar:vertical {
    background-color: #1e1e1e;
    width: 12px;
    border-radius: 6px;
}

QScrollBar::handle:vertical {
    background-color: #555555;
    border-radius: 6px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background-color: #777777;
}

QScrollBar:horizontal {
    background-color: #1e1e1e;
    height: 12px;
    border-radius: 6px;
}

QScrollBar::handle:horizontal {
    background-color: #555555;
    border-radius: 6px;
    min-width: 30px;
}

QScrollBar::add-line, QScrollBar::sub-line {
    height: 0;
    width: 0;
}

/* Status Bar */
QStatusBar {
    background-color: #007acc;
    border-top: none;
    color: #ffffff;
}

/* Labels */
QLabel {
    color: #e0e0e0;
    background-color: transparent;
}

QLabel[heading="true"] {
    font-size: 14pt;
    font-weight: bold;
    color: #4fc3f7;
}

QLabel[subheading="true"] {
    font-size: 11pt;
    color: #aaaaaa;
}

QLabel[error="true"] {
    color: #f44747;
    font-weight: bold;
}

QLabel[warning="true"] {
    color: #ffcc00;
    font-weight: bold;
}

QLabel[success="true"] {
    color: #4ec9b0;
    font-weight: bold;
}

/* Message Boxes / Dialogs */
QMessageBox {
    background-color: #252526;
}

QMessageBox QLabel {
    color: #e0e0e0;
}

QDialog {
    background-color: #252526;
}

/* Tool Tips */
QToolTip {
    background-color: #2d2d2d;
    color: #e0e0e0;
    border: 1px solid #555555;
    padding: 5px;
    border-radius: 3px;
}

/* Splitter */
QSplitter::handle {
    background-color: #3d3d3d;
    border-radius: 2px;
}

QSplitter::handle:horizontal {
    width: 8px;
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #1e1e1e, stop:0.3 #3d3d3d, stop:0.5 #555555, stop:0.7 #3d3d3d, stop:1 #1e1e1e);
}

QSplitter::handle:hover {
    background-color: #4fc3f7;
}

QSplitter::handle:horizontal:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #2d3748, stop:0.3 #4fc3f7, stop:0.5 #00acc1, stop:0.7 #4fc3f7, stop:1 #2d3748);
}

/* Menu Bar (if used) */
QMenuBar {
    background-color: #2d2d2d;
    color: #e0e0e0;
}

QMenuBar::item:selected {
    background-color: #3d3d3d;
}

QMenu {
    background-color: #2d2d2d;
    color: #e0e0e0;
    border: 1px solid #3d3d3d;
}

QMenu::item:selected {
    background-color: #0078d4;
}
"""
