import customtkinter as ctk
import os
import shutil
from tkinter import filedialog, messagebox
import sys
import hashlib

#ML imports
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import PyPDF2
from docx import Document

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

Logo = resource_path("D:\\My_Softwares\\2\\Installer\\myicons.ico")

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

folder_selection = None
status_label = None
folder_entry = None
organize_method = None
max_file_size_var = None
duplicate_detection_var = None

# ML model setup---

texts = [
    "Resume for software engineer job",
    "Bank statement",
    "College assignment",
    "Invoice for payment",
    "Project report",
    "Job application resume",
    "Financial report",
    "Homework assignment"
]
labels = [
    "Resume",
    "Finance",
    "Education",
    "Finance",
    "Education",
    "Resume",
    "Finance",
    "Education"
]

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts)
model = MultinomialNB()
model.fit(X, labels)

# Utility functions---

def extract_text_from_pdf(file_path):
    try:
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            text = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
            return text
    except Exception as e:
        print(f"PDF extraction error: {e}")
        return ""

def extract_text_from_docx(file_path):
    try:
        doc = Document(file_path)
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        return '\n'.join(full_text)
    except Exception as e:
        print(f"DOCX extraction error: {e}")
        return ""

def extract_text_from_txt(file_path):
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except Exception as e:
        print(f"TXT extraction error: {e}")
        return ""

def extract_text_from_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext == ".docx":
        return extract_text_from_docx(file_path)
    elif ext == ".txt":
        return extract_text_from_txt(file_path)
    else:
        return ""

def classify_text_file(file_path):
    text = extract_text_from_file(file_path)
    if text.strip():
        X_new = vectorizer.transform([text])
        predicted = model.predict(X_new)
        return predicted[0]
    return "OTHERS"

def file_hash(file_path):
    """Compute SHA256 hash of a file for duplicate detection."""
    hash_sha256 = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()
    except Exception as e:
        print(f"Error hashing file {file_path}: {e}")
        return None

# Organizing functions

def OrganizeFolderByClassification(folder_path, max_file_size_mb=100, detect_duplicates=True):
    count = 0
    duplicates = 0
    seen_hashes = set()

    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        if os.path.isfile(file_path):
            try:
                size_mb = os.path.getsize(file_path) / (1024 * 1024)
                if size_mb > max_file_size_mb:
                    print(f"Skipping large file: {file} ({size_mb:.2f} MB)")
                    continue

                if detect_duplicates:
                    h = file_hash(file_path)
                    if h is None:
                        continue
                    if h in seen_hashes:
                        print(f"Duplicate detected, skipping: {file}")
                        duplicates += 1
                        continue
                    seen_hashes.add(h)

                ext = os.path.splitext(file)[1].lower()
                if ext in [".txt", ".pdf", ".docx"]:
                    category = classify_text_file(file_path)
                else:
                    category = ext[1:].upper() if ext else "OTHERS"

                dest_folder = os.path.join(folder_path, category)
                os.makedirs(dest_folder, exist_ok=True)

                shutil.move(file_path, os.path.join(dest_folder, file))
                count += 1
            except Exception as e:
                print(f"Error processing file {file}: {e}")

    return count, duplicates

def OrganizeFolderByExtension(folder_path, max_file_size_mb=100, detect_duplicates=True):
    count = 0
    duplicates = 0
    seen_hashes = set()

    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        if os.path.isfile(file_path):
            try:
                size_mb = os.path.getsize(file_path) / (1024 * 1024)
                if size_mb > max_file_size_mb:
                    print(f"Skipping large file: {file} ({size_mb:.2f} MB)")
                    continue

                if detect_duplicates:
                    h = file_hash(file_path)
                    if h is None:
                        continue
                    if h in seen_hashes:
                        print(f"Duplicate detected, skipping: {file}")
                        duplicates += 1
                        continue
                    seen_hashes.add(h)

                ext = os.path.splitext(file)[1].lower()
                category = ext[1:].upper() if ext else "OTHERS"

                dest_folder = os.path.join(folder_path, category)
                os.makedirs(dest_folder, exist_ok=True)

                shutil.move(file_path, os.path.join(dest_folder, file))
                count += 1
            except Exception as e:
                print(f"Error processing file {file}: {e}")

    return count, duplicates

def MainWindow():
    global folder_selection, status_label, folder_entry, organize_method, max_file_size_var, duplicate_detection_var

    app = ctk.CTk()
    app.geometry("650x650")
    app.resizable(False, False)
    app.title("File Organizer Tool")
    try:
        app.iconbitmap(Logo)
    except Exception:
        pass  # Ignore if icon not found

    title_bar = ctk.CTkFrame(app, fg_color="#000000", height=40, corner_radius=0)
    title_bar.pack(fill='x')
    title_label = ctk.CTkLabel(title_bar, text="\nFile Organizer Tool\n", font=("Consolas", 30, "bold"), text_color="white")
    title_label.pack(pady=5)

    folder_selection = ctk.StringVar(value="")
    ctk.CTkLabel(app,
                 text='\nEnter the path of folder or "Browse Folder" to organize files.',
                 font=("Consolas", 17)
                 ).pack(pady=0)

    folder_entry = ctk.CTkEntry(
        app, width=500, height=40,
        placeholder_text="Enter folder path here...",
        textvariable=folder_selection,
        corner_radius=20
    )
    folder_entry.pack(pady=10)

    ctk.CTkButton(app, text="Browse Folder", fg_color="black", font=("Consolas", 18), corner_radius=20, command=BrowseFolder).pack(pady=5)

    # Organize method selection
    ctk.CTkLabel(app, text="\nSelect Organizing Method:", font=("Consolas", 16, "bold")).pack(pady=(20, 5))

    organize_method = ctk.StringVar(value="classification")
    ctk.CTkRadioButton(app, text="By Classification (ML-based)", variable=organize_method, value="classification").pack(anchor="w", padx=50)
    ctk.CTkRadioButton(app, text="By File Extension", variable=organize_method, value="extension").pack(anchor="w", padx=50)

    # Max file size option
    ctk.CTkLabel(app, text="\nMax File Size to Process (MB):", font=("Consolas", 16, "bold")).pack(pady=(20, 5))
    max_file_size_var = ctk.IntVar(value=100)
    max_file_size_entry = ctk.CTkEntry(app, width=100, height=30, textvariable=max_file_size_var, corner_radius=10)
    max_file_size_entry.pack()

    # Duplicate detection option
    duplicate_detection_var = ctk.BooleanVar(value=True)
    ctk.CTkCheckBox(app, text="Enable Duplicate Detection (skip duplicates)", variable=duplicate_detection_var).pack(pady=20)

    ctk.CTkButton(app, text="Organize Files", fg_color="black", font=("Consolas", 18), corner_radius=20, command=OrganizeFiles).pack(pady=10)

    status_label = ctk.CTkLabel(app, text="", text_color="green", font=("Consolas", 14))
    status_label.pack(pady=10)

    return app

def BrowseFolder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        folder_selection.set(folder_path)

def OrganizeFiles():
    folder_path = folder_selection.get()
    if not folder_path or not os.path.exists(folder_path):
        messagebox.showerror("Error", "Please select a valid folder")
        return

    try:
        max_size = max_file_size_var.get()
    except Exception:
        max_size = 100

    detect_duplicates = duplicate_detection_var.get()
    method = organize_method.get()

    status_label.configure(text="Organizing files, please wait...")
    app.update()

    try:
        if method == "classification":
            organized_count, duplicate_count = OrganizeFolderByClassification(folder_path, max_file_size_mb=max_size, detect_duplicates=detect_duplicates)
        elif method == "extension":
            organized_count, duplicate_count = OrganizeFolderByExtension(folder_path, max_file_size_mb=max_size, detect_duplicates=detect_duplicates)
        else:
            messagebox.showerror("Error", "Unknown organizing method selected")
            status_label.configure(text="")
            return

        status_label.configure(text=f"Organized {organized_count} files successfully! Skipped {duplicate_count} duplicates.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        status_label.configure(text="")

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
