import customtkinter as ctk
import os
import shutil
from tkinter import filedialog,messagebox
import sys
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
folder_selection=None
status_label=None
folder_entry=None

def MainWIndow():
    global folder_selection,status_label,folder_entry
    app=ctk.CTk()
    app.geometry("550x400")
    app.resizable(False,False)
    title_bar=ctk.CTkFrame(app,fg_color="#000000",height=40,corner_radius=0)
    title_bar.pack(fill='x')
    title_label=ctk.CTkLabel(title_bar,text="\nFile Organizer Tool\n",font=("Consolas",30,"bold"),text_color="white")
    title_label.pack(pady=5)
    folder_selection=ctk.StringVar(value="")
    ctk.CTkLabel(app,
                 text='\nEnter the path of folder or "Browse Folder" to Organize \nfiles into sub_folders according to files type. ',
                 font=("Consolas",17)
                 ).pack(pady=0)
    folder_entry=ctk.CTkEntry(
        app,width=350,height=40,
        placeholder_text="Enter files path here...",
        textvariable=folder_selection,
        corner_radius=20
    )
    folder_entry.pack(pady=20)
    ctk.CTkButton(app,text="Browse Folder",fg_color="black",font=("Consolas",18),corner_radius=20,command=BrowseFolder).pack(pady=5)
    ctk.CTkButton(app,text="Organize Files",fg_color="black",font=("Consolas",18),corner_radius=20,command=OrganizeFiles).pack(pady=20)
    status_label=ctk.CTkLabel(app,text="",text_color="green")
    status_label.pack(pady=10)
    return app
def BrowseFolder():
    folder_path=filedialog.askdirectory()
    if folder_path:
        folder_selection.set(folder_path)
def OrganizeFiles():
    folder_path =folder_selection.get()
    if not folder_path or not os.path.exists(folder_path):
        messagebox.showerror("Error","Please select a valid folder")
        return
    organized_count=OrganizeFolderByExtension(folder_path)
    status_label.configure(text=f"Organized {organized_count} files successfully!")
def OrganizeFolderByExtension(folder_path):
    count=0
    for file in os.listdir(folder_path):
        file_path=os.path.join(folder_path,file)
        if os.path.isfile(file_path):
            ext=os.path.splitext(file)[1][1:] or "others"
            dest_folder=os.path.join(folder_path,ext.upper())
            os.makedirs(dest_folder,exist_ok=True)
            shutil.move(file_path,os.path.join(dest_folder,file))
            count+=1
    return count 
app=MainWIndow()
app.mainloop()       
