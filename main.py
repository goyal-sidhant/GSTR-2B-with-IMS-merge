"""
GST Processing Tool v5.0 - Entry Point

This is the main entry point for the application.
Run this file to start the GST Processing Tool.

Usage:
    python main.py
"""

import sys
from pathlib import Path

# Add project root to path (for imports)
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def main():
    """Main entry point."""
    try:
        # Import PyQt5
        from PyQt5.QtWidgets import QApplication
        from PyQt5.QtCore import Qt
        
        # Enable high DPI scaling
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
        
        # Create application
        app = QApplication(sys.argv)
        app.setApplicationName("GST Processing Tool")
        app.setApplicationVersion("5.0")
        app.setOrganizationName("Goyal Tax Services")
        
        # Import and create main window
        from ui.main_window import MainWindow
        
        window = MainWindow()
        window.show()
        
        # Run application
        sys.exit(app.exec_())
        
    except ImportError as e:
        print("=" * 50)
        print("ERROR: Missing dependency!")
        print("=" * 50)
        print(f"\n{e}\n")
        print("Please install required packages:")
        print("  pip install -r requirements.txt")
        print("")
        sys.exit(1)
    
    except Exception as e:
        print("=" * 50)
        print("ERROR: Application failed to start!")
        print("=" * 50)
        print(f"\n{e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
