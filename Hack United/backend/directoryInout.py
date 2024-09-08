import os

def scan_files(directory):
    files_to_rename = []
    for file in os.listdir(directory):
        if file.startswith("untitled") or file.startswith("unnamed"):
            files_to_rename.append(file)
    return files_to_rename
