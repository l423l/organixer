from datetime import datetime
import tkinter as tk
from tkinter import ttk, filedialog
from categories import CATEGORY_MAP
import os
import shutil

class OrganixerApp:
    def __init__(self, root):
        self.root = root
        root.title("Organixer")
        root.minsize(900, 560)
        self._build_layout()

    def _build_layout(self):
        bot = ttk.Frame(self.root, padding = 10)
        bot.pack(side="bottom", fill="x")
        # Buttons part of the Body,
        self.select_folder_button = tk.Button(bot, text="Select Folder", command=self.select_folder)
        self.select_folder_button.pack(side=tk.LEFT, padx=5)
        self.organize_button = tk.Button(bot, text="Organize", command=self.organize_files)
        self.organize_button.pack(side=tk.LEFT, padx=5)
        self.up_button = tk.Button(bot, text="Up", command=self.one_level_up)
        self.up_button.pack(side=tk.LEFT, padx=5)
        # Label part of the Body,
        self.selected_folder_label = tk.Label(bot, text="No folder selected", background="lightgray")
        self.selected_folder_label.pack(side=tk.LEFT, padx=5)
        #Treeview part of the Body,
        self.treeview()

    def treeview(self):
        self.tree = ttk.Treeview(self.root)
        self.tree.pack(fill="both", expand=True)
        
        self.tree.heading("#0", text="Name", anchor="w")
        self.tree_columns = ["Date Modified", "Type", "Size"]
        self.tree["columns"] = self.tree_columns

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.title(), anchor="w")
            self.tree.column(col, anchor="w")
    
        self.tree.bind("<Double-Button-1>", self.on_two_left_click)

    def show_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for filename in os.listdir(self.target_folder):
            full_path = os.path.join(self.target_folder, filename)
            if os.path.isdir(full_path):
                item_type, size = "File Folder", ""
            else:
                # File type and size formatting
                item_type, size = f"{os.path.splitext(filename)[1][1:].upper()} File", self.size_format(os.path.getsize(full_path))
                # Insert into treeview and tuple the values for date modified, type, and size
            self.tree.insert("", "end", text=filename, values=(self.date_format(os.path.getmtime(full_path)), item_type, size))

    def date_format(self, timestamp):
        return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")

    def size_format(self, size):
        for unit in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0

    def one_level_up(self):
        if self.target_folder == self.root_folder:
            return
        parent_folder = os.path.dirname(self.target_folder)
        if parent_folder and os.path.exists(parent_folder):
            self.target_folder = parent_folder
            self.selected_folder_label.config(text=f"Selected folder: {parent_folder}")
            self.show_tree()
    
    def on_two_left_click(self, event):
        item_id = self.tree.focus()
        if not item_id:
            return
        
        filename = self.tree.item(item_id, "text")
        full_path = os.path.join(self.target_folder, filename)
        if os.path.isdir(full_path):
            self.target_folder = full_path
            self.selected_folder_label.config(text=f"Selected folder: {full_path}")
            self.show_tree()
        
    def select_folder(self):
        folder = filedialog.askdirectory(title="Select folder to organize")
        if not folder:
            return
        self.target_folder = folder
        self.root_folder = folder
        self.selected_folder_label.config(text=f"Selected folder: {folder}")
        self.show_tree()  

    def organize_files(self):
        for filename in os.listdir(self.root_folder):
            full_path = os.path.join(self.root_folder, filename)
            if os.path.isdir(full_path):
                continue
            ext = os.path.splitext(filename)[1]
            category = CATEGORY_MAP.get(ext, "misc")
            category_path = os.path.join(self.root_folder, category)
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