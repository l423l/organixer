import tkinter as tk
from tkinter import ttk, filedialog
import os
import shutil

CATEGORY_MAP = {
    ".py": "scripts",
    ".js": "scripts",
    ".html": "scripts", ".css": "scripts",
    ".sql": "scripts",
    ".php": "scripts",
    ".pdf": "docs", ".doc": "docs",
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
        bot = ttk.Frame(self.root, padding = 10)
        bot.pack(side="bottom", fill="x")
        # Buttons part of the code,
        self.select_folder_button = tk.Button(bot, text="Select Folder", command=self.select_folder)
        self.select_folder_button.pack(side=tk.LEFT, padx=5)
        self.organize_button = tk.Button(bot, text="Organize", command=self.organize_files)
        self.organize_button.pack(side=tk.LEFT, padx=5)
        # Label part of the code,
        self.selected_folder_label = tk.Label(bot, text="No folder selected", background="lightgray")
        self.selected_folder_label.pack(side=tk.LEFT, padx=5)
        #Treeview part of the code,
        self.treeview()

    def treeview(self):
        self.tree = ttk.Treeview(self.root)
        self.tree.pack(fill="both", expand=True)
        self.tree.heading("#0", text="Files and Folders", anchor="w")
        self.tree_columns = ["Name", "Type", "Size"]
        self.tree["columns"] = self.tree_columns
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.title(), anchor="w")
            self.tree.column(col, anchor="w")

    def show_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for filename in os.listdir(self.target_folder):
            full_path = os.path.join(self.target_folder, filename)
            if os.path.isdir(full_path):
                item_type, size = "Folder", ""
            else:
                item_type, size = "File", f"{os.path.getsize(full_path)} bytes"
            self.tree.insert("", "end", text=filename, values=(filename, item_type, size))


    def select_folder(self):
        folder = filedialog.askdirectory(title="Select folder to organize")
        if not folder:
            return
        self.target_folder = folder
        self.selected_folder_label.config(text=f"Selected folder: {folder}")
        self.show_tree()  

    def organize_files(self):
        for filename in os.listdir(self.select_folder):
            full_path = os.path.join(self.select_folder, filename)
            if os.path.isdir(full_path):
                continue
            ext = os.path.splitext(filename)[1]
            category = CATEGORY_MAP.get(ext, "misc")
            category_path = os.path.join(self.target_folder, category)
            os.makedirs(category_path, exist_ok=True)
            shutil.move(full_path, os.path.join(category_path, filename))
        self.show_tree()

    def on_close(self):
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = OrganixerApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()