# AI / ML Based File Organizer Tool

A desktop application built with Python and CustomTkinter that automatically organizes files inside a folder using Machine Learning classification or simple file extension grouping. The app also detects duplicate files and generates CSV reports.

---

## Features

### 1. File Classification (ML-based)
The tool analyzes PDF, DOCX, and TXT documents using TF-IDF and Naive Bayes to predict categories such as:
- Resume
- Education
- Finance
- Others

### 2. Organize by File Extension
Moves files into folders based on their extension (PDF, PNG, JPG, TXT, DOCX, etc.).

### 3. Duplicate File Detection
Uses SHA-256 hashing to safely skip duplicate files during organizing.

### 4. Detailed Reports
A CSV report is generated in your **Documents** folder containing:
- Timestamp  
- Folder path  
- Organizing method  
- Files organized  
- Duplicate count  
- Category breakdown  

### 5. GUI Built with CustomTkinter
A user-friendly interface with:
- Folder selection  
- Method selection  
- Duplicate detection toggle  
- Status messages  
- GitHub link  
- Custom icon support  

---

## Requirements

Install the required libraries:

```bash
pip install customtkinter pillow scikit-learn python-docx PyPDF2
