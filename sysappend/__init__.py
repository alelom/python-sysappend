from .version import VERSION, VERSION_SHORT
import sys, os
from pathlib import Path
from typing import List, Optional, Set, Union
import inspect

ANALYSED_ROOT_DIRS : Set = set()


def __get_importing_filepath() -> str:
    # Get the current frame
    current_frame = inspect.currentframe()
    # Traverse the call stack
    for frame_info in inspect.getouterframes(current_frame):
        # Get the file path of the frame
        filepath = frame_info.filename
        # Check if the file is not part of the package (e.g., not __init__.py)
        if not filepath.endswith('__init__.py'):
            return os.path.abspath(filepath)
    
    return sys.argv[0]


def all(root_dir_name: Optional[str] = None, start_search_from_child_dir : Optional[Union[str, Path]] = None, 
        exceptions: Optional[List[str]] = ["dist", "docs", "tests"],
        skip_symlinks: bool = True,
        skip_dirs_starting_with: List[str] = [".", "__"],
        skip_dirs_invalid_module_name: bool = True):
    """Crawls upwards from `start_search_from_child_dir` until the `root_dir_name` folder, then appends to `sys.path` all subdirectories, recursively.
    If `start_search_from_child_dir` is not provided, it will use the current executing script's folder as the starting point.
    By default, this skips:  
    - symlinks directories (`skip_symlinks` defaults to True); 
    - directories named like strings in the `exceptions` list (defaults: dist, docs, tests);
    - directories starting with the chars in the `skip_dirs_starting_with` (defaults: dot, double underscore).

    Args:
        root_folder_name (Optional[str], optional): The root folder from where all subdirs will be appended to sys.   
        If not provided, it will use [repository root]/src, and [repository root]/source, in this order, if they are found.
        Otherwise, it will use the [repository root] folder.  
        The repository root dir is identified by the presence of a `.git` folder in it.  
        
        start_search_from_child_dir (Optional[str | Path], optional): The child directory from where the upward crawl is initiated.  
        If not provided, it will use the importing script's folder as the starting point.
        
        exceptions (Optional[List[str]], optional): A list of strings that, if found in the path, will be skipped. Defaults to ["dist", "docs", "tests"].
        
        skip_symlinks (bool, optional): If True, skips symlinks. Defaults to True.
        
        skip_dirs_starting_with (List[str], optional): A list of strings that, if found at the start of the directory name, will be skipped. Defaults to [".", "__"].
        
        skip_dirs_invalid_module_name (bool, optional): If True, skips directories that are named with a convention that is not valid for a Python module name. See https://docs.python.org/dev/reference/lexical_analysis.html#identifiers. Defaults to True.
    """
    if isinstance(start_search_from_child_dir, str):
        start_search_from_child_dir = Path(start_search_from_child_dir)
        
    if not start_search_from_child_dir:
        start_search_from_child_dir = Path(__get_importing_filepath()).resolve()
        start_search_from_child_dir = Path(start_search_from_child_dir).resolve().parent
        
    root_dir_to_import = None
    start_dir = start_search_from_child_dir

    # Find the root_dir directory, 
    # crawling upwards from the start_dir until the root_dir_name is found, 
    # or until a .git folder is found.
    for parent in start_dir.parents:
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
        elif parent.name == root_dir_name:
            root_dir_to_import = parent
            break
        
        start_dir = start_dir.parent

    if not root_dir_to_import:
        raise Exception("Root directory not found. Please provide the root directory name.")
    
    root_dir_to_import_str = str(os.path.normpath(root_dir_to_import))
    
    if root_dir_to_import_str in ANALYSED_ROOT_DIRS:
        return
    
    if root_dir_to_import_str not in sys.path:
        sys.path.append(root_dir_to_import_str)
    
    all_paths_to_append = set()

    # Add all subdirectories of the "src" directory to sys.path
    all_subdirs = [x for x in root_dir_to_import.rglob('*') if x.is_dir()]
    for subdir in all_subdirs:
        # Make the subdir path relative to the root_dir_to_import in order to skip only significant directories
        subdir = subdir.relative_to(root_dir_to_import)
        
        if skip_dirs_starting_with and any(part.startswith(prefix) for prefix in skip_dirs_starting_with for part in subdir.parts):
            continue
        
        if exceptions and any(exception in subdir.parts for exception in exceptions):
            continue
        
        if skip_symlinks and subdir.is_symlink():
            continue
        
        if skip_dirs_invalid_module_name and any(not part.isidentifier() for part in subdir.parts):
            continue
        
        if ".egg-info" in str(subdir):
            continue
        
        # Restore the full path and normalize it before adding it to the list.
        subdir = Path.joinpath(root_dir_to_import, subdir)
        path = os.path.normpath(subdir)
        all_paths_to_append.add(path)
    
    all_paths_to_append = sorted(all_paths_to_append)
    
    for path in all_paths_to_append:
        if path not in sys.path:
            sys.path.append(path)
            
    ANALYSED_ROOT_DIRS.add(root_dir_to_import_str)