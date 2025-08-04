# PP_2-Installer-File_Organizer-Filorganizer-_GUI-Based
Personal Project 2 :A simple GUI-based file organizer built using Python and [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter). This tool allows users to organize files in a selected folder into subfolders based on their file extensions.
#  File Organizer Tool

A simple GUI-based file organizer built using Python and [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter). This tool allows users to organize files in a selected folder into subfolders based on their file extensions.

---

##  Features

- Modern and clean CustomTkinter GUI
- Organizes files into subfolders by file type (e.g., `.pdf`, `.jpg`, `.txt`, etc.)
- Browse folders using a built-in dialog
- Status feedback on operation success
- Works with PyInstaller for creating standalone executables
- Icon customization support

---

##  Getting Started

### Prerequisites

Make sure you have Python 3.7+ installed.

Install required Python libraries:
```bash
pip install customtkinter



##  Important: Handling Resource Paths with PyInstaller



When packaging your Python project as a standalone executable using **PyInstaller**, file paths to bundled data (e.g., images, icons, config files) may not behave as expected. This is because PyInstaller extracts files to a **temporary directory** at runtime.

Use the following helper function to correctly resolve paths to bundled resources:



```python

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

