from .version import VERSION, VERSION_SHORT

import sys
from pathlib import Path
from typing import Optional, Union


from .version import VERSION, VERSION_SHORT

import sys
from pathlib import Path
from typing import Optional


def importall(from_folder : Optional[Union[str, Path]] = None, stop_at_parent_folder: Optional[str] = "src"):
    """Crawls upwards from `from_folder` until the `stop_at_parent_folder` folder, then imports all subdirectories recursively.
    If `from_folder` is not provided, it will use the current executing script's folder as the starting point.

    Args:
        from_folder (Optional[str], optional): The folder to start importing modules from. If not provided, it will use the current executing script's folder as the starting point.
        stop_at_parent_folder (Optional[str], optional): The parent directory to stop importing modules from. Defaults to "src".
    """
    if isinstance(from_folder, str):
        from_folder = Path(from_folder)
    
    if not from_folder:
        from_folder = Path(sys.argv[0]).resolve()
        from_folder = Path(from_folder).resolve().parent
        
    root_dir_to_import = None

    # Find the root_dir directory
    for parent in from_folder.parents:
        if parent.name == stop_at_parent_folder:
            root_dir_to_import = parent
            break

    sys.path.append(str(root_dir_to_import))

    if root_dir_to_import and root_dir_to_import not in sys.path:
        # Add all subdirectories of the "src" directory to sys.path
        for subdir in root_dir_to_import.rglob('*'):
            if subdir.is_dir() and not subdir.name.startswith("__"):
                sys.path.append(str(subdir))