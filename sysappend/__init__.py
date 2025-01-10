from .version import VERSION, VERSION_SHORT

import sys
from pathlib import Path
from typing import List, Optional, Union


from .version import VERSION, VERSION_SHORT

import sys
from pathlib import Path
from typing import Optional


def all(root_dir_name: Optional[str] = None, start_search_from_child_dir : Optional[Union[str, Path]] = None, exceptions: Optional[List[str]] = ["dist", "docs", "tests"]):
    """Crawls upwards from `from_folder` until the `stop_at_parent_folder` folder, then appends to `sys.path` all subdirectories, recursively.
    If `from_folder` is not provided, it will use the current executing script's folder as the starting point.

    Args:
        root_folder_name (Optional[str], optional): The root folder from where all subdirs will be appended to sys.   
        If not provided, it will use [repository root]/src.  
        If src folder is not found, it will use the [repository root] folder.  
        The repository root is identified crawling upward from the `start_search_from_child_dir` by the presence of a `.git` folder in it.  
        
        start_search_from_child_dir (Optional[str | Path], optional): The child directory from where the upward crawl is initiated.  
        If not provided, it will use the current executing script's folder as the starting point.
    """
    if isinstance(start_search_from_child_dir, str):
        start_search_from_child_dir = Path(start_search_from_child_dir)
        
    if not start_search_from_child_dir:
        start_search_from_child_dir = Path(sys.argv[0]).resolve()
        start_search_from_child_dir = Path(start_search_from_child_dir).resolve().parent
        
    root_dir_to_import = None

    # Find the root_dir directory
    for parent in start_search_from_child_dir.parents:
        if not root_dir_name:
            gitdir = Path.joinpath(parent, ".git")
            if (gitdir).exists():
                if (Path.joinpath(parent, "src")).exists():
                    root_dir_to_import = Path.joinpath(parent, "src")
                    break
                
                if (Path.joinpath(parent, "source")).exists():
                    root_dir_to_import = Path.joinpath(parent, "source")
                    break
                
                root_dir_to_import = gitdir.parent
                break
                
            root_dir_to_import = parent
            break
        elif parent.name == root_dir_name:
            root_dir_to_import = parent
            break

    sys.path.append(str(root_dir_to_import))

    if root_dir_to_import and root_dir_to_import not in sys.path:
        # Add all subdirectories of the "src" directory to sys.path
        all_subdirs = [x for x in root_dir_to_import.rglob('*') if x.is_dir() and not x.name.startswith('.') and not x.name.startswith('__')]
        all_subdirs = [d for d in all_subdirs if not any(part.startswith('.') or part.startswith('__') for part in d.parts)]
        for subdir in all_subdirs:
            if ".egg-info" in str(subdir):
                continue
            
            if exceptions and any(subdir.parts[-1] == exception for exception in exceptions):
                continue
            
            sys.path.append(str(subdir))