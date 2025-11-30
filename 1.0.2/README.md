
</think># File Organizer Tool

A Python-based GUI application that organizes files in a selected folder using either file extension or machine learning-based classification. The tool uses CustomTkinter for the interface and scikit-learn for text classification on supported document types (PDF, DOCX, TXT).

## Features

- **Graphical User Interface**: Built with CustomTkinter for a modern, cross-platform look.
- **Organizing Methods**:
  - **By File Extension**: Groups files into folders based on their file extensions (e.g., PDF, TXT, DOCX).
  - **By Classification**: Uses a trained Naive Bayes model to classify text-based files into categories like "Resume", "Finance", "Education", or "OTHERS".
- **File Size Limit**: Skip files larger than a specified size (default: 100 MB) to avoid processing large files.
- **Duplicate Detection**: Optionally detect and skip duplicate files based on SHA256 hash.
- **Supported File Types**: Extracts text from PDF, DOCX, and TXT files for classification.
- **Error Handling**: Gracefully handles errors during file processing and text extraction.

## Requirements

- Python 3.7+
- Libraries:
  - `customtkinter`
  - `scikit-learn`
  - `PyPDF2`
  - `python-docx`
  - `tkinter` (usually included with Python)
  - `hashlib` (standard library)
  - `shutil` (standard library)
  - `os` (standard library)
  - `sys` (standard library)

Install the required libraries using pip:

```bash
pip install customtkinter scikit-learn PyPDF2 python-docx
```

## Installation

1. Clone or download the repository.
2. Ensure all dependencies are installed (see Requirements).
3. Run the script:

```bash
python your_script_name.py
```

Note: The application uses PyInstaller-compatible resource paths for icons. If using PyInstaller to create an executable, ensure the icon file is bundled correctly.

## Usage

1. Launch the application.
2. Enter or browse to select the folder containing files to organize.
3. Choose the organizing method:
   - **By Classification**: Uses ML to categorize text files.
   - **By File Extension**: Groups by file type.
4. Set the maximum file size (in MB) to process.
5. Enable or disable duplicate detection.
6. Click "Organize Files" to start the process.
7. View the status message for results (e.g., number of files organized and duplicates skipped).

The tool will create subfolders in the selected directory and move files accordingly. Files are moved, not copied, so ensure you have backups if needed.

## How It Works

- **Text Extraction**: For classification, the tool extracts text from PDF, DOCX, and TXT files using libraries like PyPDF2 and python-docx.
- **ML Classification**: A pre-trained TfidfVectorizer and MultinomialNB model classifies text into categories based on sample training data (e.g., resumes, invoices).
- **File Handling**: Checks file size and duplicates (if enabled), then moves files to category-based subfolders.
- **Fallback**: Non-text files or unclassifiable files are grouped by extension or labeled as "OTHERS".

The ML model is trained on a small dataset included in the code. For better accuracy, expand the training data.

## Screenshots

*(Add screenshots here if available)*

Example GUI layout:
- Title bar with app name.
- Folder path entry and browse button.
- Radio buttons for organizing method.
- Entry for max file size.
- Checkbox for duplicate detection.
- Organize button and status label.

## Limitations

- ML classification is limited to text-based files and relies on the provided training data.
- Large files are skipped based on size limit.
- Duplicate detection uses file hashing, which may be slow for very large folders.
- Icon path is hardcoded; modify `resource_path` for custom builds.

## Contributing

Feel free to fork the repository and submit pull requests. Suggestions for improving the ML model or adding more file types are welcome.

## License

This project is open-source. Use at your own risk. No warranties provided.

## Author

Mayur Dhole
mayursdwin11@gmail.com
