# sort_downloads.py
# Tidies your Downloads folder by moving each file into a folder by type.
# It never deletes anything, and never overwrites a file.

from pathlib import Path
import shutil

# 1. Where your Downloads folder is
downloads = Path.home() / "Downloads"

# 2. Which file types go into which folder (you can edit these lists)
categories = {
    "Images":     [".jpg", ".jpeg", ".png", ".gif", ".heic", ".webp", ".bmp", ".svg"],
    "Documents":  [".pdf", ".doc", ".docx", ".txt", ".ppt", ".pptx", ".xls", ".xlsx", ".csv"],
    "Installers": [".exe", ".msi"],
    "Archives":   [".zip", ".rar", ".7z", ".gz"],
    "Videos":     [".mp4", ".mov", ".avi", ".mkv"],
    "Audio":      [".mp3", ".wav", ".m4a"],
}

# Files still downloading - leave them alone
skip = [".crdownload", ".part", ".tmp"]

moved = 0

# 3. Look at every item in Downloads
for item in downloads.iterdir():
    # Skip folders, this script itself, and unfinished downloads
    if item.is_dir() or item.name == Path(__file__).name:
        continue
    extension = item.suffix.lower()
    if extension in skip:
        continue

    # 4. Find the right folder for this file (anything unknown goes to "Other")
    folder_name = "Other"
    for name, extensions in categories.items():
        if extension in extensions:
            folder_name = name
            break

    target_folder = downloads / folder_name
    target_folder.mkdir(exist_ok=True)

    # 5. If a file with the same name is already there, add a number instead of overwriting
    target = target_folder / item.name
    number = 1
    while target.exists():
        target = target_folder / f"{item.stem} ({number}){item.suffix}"
        number += 1

    shutil.move(str(item), str(target))
    print(f"Moved {item.name}  ->  {folder_name}")
    moved += 1

print(f"\nDone! {moved} file(s) sorted.")
