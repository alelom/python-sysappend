# sysappend

Append every folder in your repository to the `sys.path` variable, so Python is able to import any folder.

## Installation

`pip install sysappend`

## Example usage

Place this line at the top of every Python file: 

```python
if True: import sysappend; sysappend.all()
```

Note: the `if True:` is optional, but it's useful to avoid linters/automated procedures to move this line from the top position.



