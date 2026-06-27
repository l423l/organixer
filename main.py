import tkinter as tk
from tkinter import ttk, filedialog
import os
import shutil

CATEGORY_MAP = {
    ".py": "scripts",
    ".md": "docs",
    ".txt": "docs",
    ".png": "assets", ".jpg": "assets",
    ".zip": "archives",
}

class OrganixerApp:
    def __init__(self, root):
        self.root = root
        root.title("Organixer")
        root.minsize(900, 560)
        self._build_layout()

    def _build_layout(self):
        top = ttk.Frame(self.root, padding=10)
        top.pack(side="top", fill="x")
        self.select_folder_button = tk.Button(top, text="Select Folder", command=self.select_folder)
        self.select_folder_button.pack(side=tk.LEFT, padx=5)
        self.organize_button = tk.Button(top, text="Organize", command=self.organize_files)
        self.organize_button.pack(side=tk.LEFT, padx=5)

    def select_folder(self):
        folder = filedialog.askdirectory(title="Select folder to organize")
        if not folder:
            return
        self.target_folder = folder
        print(f"Selected: {folder}")

    def organize_files(self):
        for filename in os.listdir(self.target_folder):
            full_path = os.path.join(self.target_folder, filename)
            if os.path.isdir(full_path):
                continue
            ext = os.path.splitext(filename)[1]
            category = CATEGORY_MAP.get(ext, "misc")
            category_path = os.path.join(self.target_folder, category)
            os.makedirs(category_path, exist_ok=True)
            shutil.move(full_path, os.path.join(category_path, filename))

    def on_close(self):
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = OrganixerApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()