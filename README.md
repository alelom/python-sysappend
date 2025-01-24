# sysappend

This appends every folder in your repository to the `sys.path` variable, so Python is able to import any folder. 

If you use this package, you don't need to pollute your project with `__init__.py` files, and you will unlock **relative imports** (both parent and child folders) from anywhere, without all the fuss. You will get correctly working debug, test and deploy features without going mad. At the same time, you get correct type-hinting, syntax highlighting, and module highlights.

This package does require you to add a short one-liner to the top of all your Python files (it doesn't need to be all files -- but it's convenient and can be enforced with CI/CD, GitHub actions or simply added via a quick copy-paste).

In my opinion, this solves the super-nasty import and relative package management in an developer-friendly way which basic Python fails to deliver.

### How to use it

1. `pip install sysappend`
2. Add an `if True: import sysappend; sysappend.all()` statement at the top of every python file in your repo. (It doesn't need to be every file, but it's just easier for convenience, and the function caches results avoiding redundant computation, so it doesn't slow the code down).

### Recommended folder referencing when importing

You should always try to reference the folders in the same way.  
For example, use one (or few) agreed-upon **_primary source code folder_** from which to reference the sub-directories and stick to that convention.

E.g., if your directory looks like the below, you could pick `src` to be the primary source code folder:

```
sample_project/
    src/
        sub_folder_1/
            utils.py
        sub_folder_2/
            models.py
    app.py

```

So, when you write imports, they should start from the primary `src` folder. 

E.g., in your `app.py` file, you should do:

```python
from src.sub_folder_1.utils import somefunction
```

and you should do the same thing in `models.py`:
```python
from src.sub_folder_1.utils import somefunction
```

Do not use a `sub_folder` as a starting name for an import, i.e., do **not** do `from sub_folder_1.utils import somefunction`.
Although it will may still work in most cases, it may fail when you do type comparisons or deserialization, as Python looks at the import path to compare/deserialize types. 


### Quality of life setting for editors like VSCode
If you're using an editor like VSCode, you may want to add the main **_primary source code folder(s)_** to your `settings.json` file, like:

```
    "python.autoComplete.extraPaths": [
        "./src",
    ]
```

This will help the autocomplete to reference the folders always starting from `src`, in the same way as explained above -- i.e., you won't get automatic completion that attempt to do imports from sub folders.


## Installation

`pip install sysappend`

## Example usage

Place this line at the top of every Python file: 

```python
if True: import sysappend; sysappend.all()
```

Note: the `if True:` is optional, but it's useful to avoid linters/automated procedures to move this line from the top position.



