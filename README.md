# GST Processing Tool v5.0

A desktop application for automating GSTR-2B and IMS Reco file processing for GST compliance in India.

## 🎯 What This Tool Does

This tool helps tax professionals process monthly GST files by:

1. **Merging Files** - Combines GSTR-2B files with their corresponding IMS Reco files
2. **Creating Files** - Generates new GSTR-2B files from IMS Reco when GSTR-2B is missing
3. **Organizing Output** - Creates organized folders for processed and created files
4. **Generating Reports** - Creates detailed Excel reports with processing status for all clients

## ✨ Features

- **Client Selection** - Choose which clients to process with checkboxes
- **Auto-Detection** - Automatically detects month, year, and client count from files
- **Folder Rescan** - Refresh folder contents without restarting the app
- **Preview Before Processing** - See breakdown of what will happen before you start
- **Extra Files Warning** - Identifies files that won't be processed
- **Comparison Reports** - Add previous month reports for trend analysis
- **Dark/Light Mode** - Toggle between themes for comfortable viewing
- **Live Progress Log** - See real-time processing status
- **Detailed Logging** - All actions logged to file for troubleshooting

## 🖥️ Requirements

- Python 3.8 or higher
- Windows / macOS / Linux

## 📦 Installation

1. Clone or download this repository:
   ```
   git clone https://github.com/yourusername/gst-tool-v5.git
   cd gst-tool-v5
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python main.py
   ```

## 📁 Expected File Structure

Place your files in a folder with this naming convention:

```
Input Folder/
├── GSTR2B-ClientName-StateCode-MMM YYYY.xlsx
├── GSTR2B-ABC Corp-27-May 2025.xlsx
├── GSTR2B-XYZ Ltd-29-May 2025.xlsx
├── ImsReco-ClientName-StateCode-....xlsx
├── ImsReco-ABC Corp-27-May 2025.xlsx
└── ImsReco-XYZ Ltd-29-May 2025.xlsx
```

## 🚀 How to Use

1. **Select Folder** - Click Browse to select your input folder
2. **Verify Detection** - Check that month, year, and client count are correct
3. **Select Clients** - Check/uncheck clients you want to process
4. **Review Preview** - See how many files will be merged/created/copied
5. **Add Comparison Reports** (Optional) - Add previous month reports for analysis
6. **Start Processing** - Click the process button and confirm
7. **View Results** - Check the output folder and generated report

## 📊 Output Structure

```
GSTR-2B with IMS May 2025_14062025_103045/
├── Processed Files/          # Merged GSTR-2B + IMS files
├── Created GSTR-2B Files/    # New GSTR-2B files created from IMS
└── GSTR-2B Processing Report May 2025_14062025_103045.xlsx
```

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+O` | Browse for folder |
| `Ctrl+R` | Rescan folder |
| `Ctrl+Enter` | Start processing |
| `F5` | Refresh |
| `Ctrl+A` | Select all clients |
| `Ctrl+D` | Deselect all clients |
| `Ctrl+T` | Toggle theme |
| `Ctrl+Q` | Quit |

## 📝 Log File

Processing logs are saved to `logs/gst_tool.log` in the application folder.
Each run appends to this file for complete history.

## 🛠️ Project Structure

```
gst_tool_v5/
├── main.py              # Application entry point
├── core/                # Business logic
│   ├── models.py        # Data structures
│   ├── validators.py    # File validation
│   ├── excel_handler.py # Excel operations
│   ├── file_processor.py# Main processing
│   └── report_generator.py
├── ui/                  # User interface
│   ├── main_window.py   # Main application window
│   ├── widgets/         # UI components
│   └── styles/          # Theme stylesheets
├── utils/               # Helper utilities
│   ├── constants.py
│   ├── file_utils.py
│   ├── date_utils.py
│   └── logger.py
└── logs/                # Log files
```

## 📄 License

This project is for personal/professional use.

## 👨‍💻 Author

Built with assistance from Claude AI.

---

*GST Processing Tool v5.0 - Making tax compliance easier!*
