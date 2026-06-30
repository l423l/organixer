# Organixer

A desktop GUI tool that organizes a folder's files into category subfolders (scripts, docs, images, archives, media) based on file extension — built to clean up messy project/code directories.

## Features

- Pick any folder and browse its contents in a live, file-explorer-style table (name, date modified, type, size)
- One-click organize: sorts loose files into category subfolders automatically
- Double-click into subfolders to browse, with an "Up" button to navigate back
- Organize always targets the folder you originally selected, even while browsing into subfolders
- Easily customizable sorting rules via a separate `categories.py` file

## Installation

Clone the repository from [GitHub](https://github.com/l423l/organixer.git), then run:

\```bash
git clone https://github.com/l423l/organixer.git
cd organixer
python main.py
\```

No external dependencies — built entirely with Python's standard library (`tkinter`, `os`, `shutil`, `datetime`).

## Usage

1. Click **Select Folder** to choose the folder you want to organize.
2. Browse its contents in the table. Double-click a folder to view what's inside, click **Up** to go back.
3. Click **Organize** to sort all loose files in the selected folder into category subfolders.

## Built With

- Python
- tkinter