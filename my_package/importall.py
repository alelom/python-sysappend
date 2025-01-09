import sys
from pathlib import Path


def from_folder(root_dir_name: str):
    # Append all the parent directories and subdirectories to the parent directories to the sys.path, up until "src".
    # Include also all the child directories to the directories so found, recursing for every child of the parent directory.
    current_dir = Path(__file__).resolve().parent
    root_dir_to_import = None

    # Find the root_dir directory
    for parent in current_dir.parents:
        if parent.name == root_dir_name:
            root_dir_to_import = parent
            break

    sys.path.append(str(root_dir_to_import))

    if root_dir_to_import and root_dir_to_import not in sys.path:
        # Add all subdirectories of the "src" directory to sys.path
        for subdir in root_dir_to_import.rglob('*'):
            if subdir.is_dir():
                sys.path.append(str(subdir))