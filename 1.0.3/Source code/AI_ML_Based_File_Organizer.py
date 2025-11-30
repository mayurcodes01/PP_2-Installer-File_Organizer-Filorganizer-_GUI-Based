import customtkinter as ctk
import os
import shutil
from tkinter import filedialog, messagebox
import sys
import hashlib
from collections import defaultdict
import datetime
import csv
from pathlib import Path
import webbrowser
from PIL import Image

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

Logo = resource_path(r"C:\Users\mayur\OneDrive\Desktop\MyClgProjects\Final\a\MayurLogo.ico")


ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

folder_selection = None
status_label = None
folder_entry = None
organize_method = None
duplicate_detection_var = None

last_report_data = None


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


def OrganizeFolderByClassification(folder_path, detect_duplicates=True):
    count = 0
    duplicates = 0
    seen_hashes = set()
    category_counts = defaultdict(int)

    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        if os.path.isfile(file_path):
            try:
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
                category_counts[category] += 1
            except Exception as e:
                print(f"Error processing file {file}: {e}")

    return count, duplicates, dict(category_counts)

def OrganizeFolderByExtension(folder_path, detect_duplicates=True):
    count = 0
    duplicates = 0
    seen_hashes = set()
    category_counts = defaultdict(int)

    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        if os.path.isfile(file_path):
            try:
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
                category_counts[category] += 1
            except Exception as e:
                print(f"Error processing file {file}: {e}")

    return count, duplicates, dict(category_counts)


def ExportReportToCSV():
    global last_report_data

    if not last_report_data:
        messagebox.showwarning("No Report", "No organizing operation has been performed yet.")
        return

    documents_folder = Path.home() / "Documents"
    csv_file = documents_folder / "file_organizer_reports.csv"

    timestamp_str = last_report_data["timestamp"].strftime("%Y-%m-%d %H:%M:%S")
    folder_path = last_report_data["folder_path"]
    method = last_report_data["method"]
    organized_count = last_report_data["organized_count"]
    duplicate_count = last_report_data["duplicate_count"]
    category_counts = last_report_data["category_counts"]

    existing_categories = []
    if csv_file.exists():
        with open(csv_file, mode='r', encoding='utf-8', newline='') as f:
            reader = csv.reader(f)
            header = next(reader, None)
            if header:
                existing_categories = header[5:]

    all_categories = set(existing_categories) | set(category_counts.keys())
    all_categories = sorted(all_categories)

    header = ["Timestamp", "Folder Path", "Method", "Files Organized", "Duplicates Skipped"] + all_categories

    row = [
        timestamp_str,
        folder_path,
        method,
        organized_count,
        duplicate_count
    ] + [category_counts.get(cat, 0) for cat in all_categories]

    try:
        if csv_file.exists():
            with open(csv_file, mode='r', encoding='utf-8', newline='') as f:
                reader = list(csv.reader(f))
            if reader and reader[0] != header:
                old_header = reader[0]
                old_rows = reader[1:]
                old_cat_indices = {cat: idx for idx, cat in enumerate(old_header[5:], start=5)}
                new_rows = []
                for old_row in old_rows:
                    new_row = old_row[:5] 
                    for cat in all_categories:
                        if cat in old_cat_indices:
                            new_row.append(old_row[old_cat_indices[cat]])
                        else:
                            new_row.append('0')
                    new_rows.append(new_row)
                new_rows.append(row)
                with open(csv_file, mode='w', encoding='utf-8', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(header)
                    writer.writerows(new_rows)
            else:
                with open(csv_file, mode='a', encoding='utf-8', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(row)
        else:
            with open(csv_file, mode='w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(header)
                writer.writerow(row)

        messagebox.showinfo("Report Saved", f"Report successfully saved to:\n{csv_file}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save report:\n{e}")


def MainWindow():
    global folder_selection, status_label, folder_entry, organize_method, duplicate_detection_var, app

    app = ctk.CTk()
    app.geometry("700x850")
    app.resizable(True,True)
    app.title("AI / ML Based File Organizer Tool - By Mayur Dhole")
    try:
        app.iconbitmap(Logo)
    except Exception:
        pass  # Ignore if icon not found

    # Title bar frame with padding and centered label
    title_bar = ctk.CTkFrame(app, fg_color="#000000", height=0, corner_radius=0)
    title_bar.pack(fill='x')
    title_label = ctk.CTkLabel(title_bar, text="AI / ML Based File Organizer Tool", font=("Consolas", 35, "bold"), text_color="white")
    title_label.pack(pady=50)

    # Instruction label with padding
    instruction_label = ctk.CTkLabel(app,
                 text='\nEnter the path of folder or use "Browse Folder" to select.\nFiles will be organized by classification or extension.\n',
                 font=("Consolas", 18),
                 justify="center"
                 )
    instruction_label.pack(pady=(20, 10))

    # Folder entry and browse button frame for better alignment
    folder_frame = ctk.CTkFrame(app, fg_color="transparent")
    folder_frame.pack(pady=(0, 20))

    folder_selection = ctk.StringVar(value="")
    folder_entry = ctk.CTkEntry(
        folder_frame, width=450, height=45,
        placeholder_text="Enter folder path here...",
        textvariable=folder_selection,
        corner_radius=15,
        font=("Consolas", 14)
    )
    folder_entry.pack(side="left", padx=(0, 10))

    browse_button = ctk.CTkButton(folder_frame, text="Browse Folder", fg_color="black", font=("Consolas", 20), corner_radius=15, width=140, height=45,command=BrowseFolder)
    browse_button.pack(side="left")

    # Organize method selection label
    organize_label = ctk.CTkLabel(app, text="  ● Select Organizing Method:\n", font=("Consolas", 25, "bold"))
    organize_label.pack(pady=(10, 5), anchor="w", padx=10)

    # Organize method radio buttons frame for neat alignment
    radio_frame = ctk.CTkFrame(app, fg_color="transparent")
    radio_frame.pack(pady=(0, 20), anchor="w", padx=70)

    organize_method = ctk.StringVar(value="classification")
    ctk.CTkRadioButton(radio_frame, text="  By Classification (ML-based)", variable=organize_method, value="classification", font=("Consolas", 20,"bold")).pack(anchor="w", pady=10)
    ctk.CTkRadioButton(radio_frame, text="  By File Extension", variable=organize_method, value="extension", font=("Consolas",20,"bold")).pack(anchor="w", pady=10)

    # Duplicate detection checkbox with padding and alignment
    duplicate_detection_var = ctk.BooleanVar(value=True)
    duplicate_checkbox = ctk.CTkCheckBox(app, text=" Enable Duplicate Detection (skip duplicates)", variable=duplicate_detection_var, font=("Consolas",21,"bold"))
    duplicate_checkbox.pack(pady=(0, 30), anchor="w", padx=30)

    # Organize button centered with fixed width
    organize_button = ctk.CTkButton(app, text="Organize Files", fg_color="black", font=("Consolas",26, "bold"), corner_radius=30, width=300,height=55, command=OrganizeFiles)
    organize_button.pack(pady=(0, 20))

    # Save Report button
    save_report_button = ctk.CTkButton(app, text="Save Report", fg_color="black", font=("Consolas",20, "bold"), corner_radius=20, width=200, height=45, command=ExportReportToCSV)
    save_report_button.pack(pady=(0, 20))
       # Hyperlink with GitHub icon
    github_icon_path = resource_path(r"C:\Users\mayur\OneDrive\Desktop\MyClgProjects\Final\a\github.png")
    github_image = ctk.CTkImage(light_image=Image.open(github_icon_path), size=(32, 32))

    def open_github():
        webbrowser.open("https://github.com/mayurcodes01")

    github_frame = ctk.CTkFrame(app, fg_color="transparent")
    github_frame.pack(pady=(10, 10))

    github_icon_label = ctk.CTkLabel(github_frame, image=github_image, text="", cursor="hand2")
    github_icon_label.pack(side="left", padx=10)
    github_icon_label.bind("<Button-1>", lambda e: open_github())

    github_text_label = ctk.CTkLabel(
        github_frame,
        text="mayurcodes01",
        font=("Consolas", 26,"italic"),
        text_color="red",
        cursor="hand2"
    )
    github_text_label.pack(side="left")
    github_text_label.bind("<Button-1>", lambda e: open_github())


    # Status label centered with padding
    status_label = ctk.CTkLabel(app, text="", text_color="green", font=("Consolas", 14))
    status_label.pack(pady=(0, 20))

    return app

def BrowseFolder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        folder_selection.set(folder_path)

def OrganizeFiles():
    global last_report_data

    folder_path = folder_selection.get()
    if not folder_path or not os.path.exists(folder_path):
        messagebox.showerror("Error", "Please select a valid folder")
        return

    detect_duplicates = duplicate_detection_var.get()
    method = organize_method.get()

    status_label.configure(text="Organizing files, please wait...")
    app.update()

    try:
        if method == "classification":
            organized_count, duplicate_count, category_counts = OrganizeFolderByClassification(folder_path, detect_duplicates=detect_duplicates)
        elif method == "extension":
            organized_count, duplicate_count, category_counts = OrganizeFolderByExtension(folder_path, detect_duplicates=detect_duplicates)
        else:
            messagebox.showerror("Error", "Unknown organizing method selected")
            status_label.configure(text="")
            return

        last_report_data = {
            "timestamp": datetime.datetime.now(),
            "folder_path": folder_path,
            "organized_count": organized_count,
            "duplicate_count": duplicate_count,
            "category_counts": category_counts,
            "method": method
        }

        status_label.configure(text=f"\nOrganized {organized_count} files successfully! Skipped {duplicate_count} duplicates.", font=("Consolas", 20, "bold"))
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        status_label.configure(text="")

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()

