# Release Process

1. Update the version in `sysappend/version.py`.

2. Run `rm dist/*.* | python3 -m build` to delete any previous releases from the `dist` folder and then build

3. Upload to PyPiTest: `python3 -m twine upload --repository testpypi dist/*`
   
4. Upload to PyPi: `python3 -m twine upload dist/*` 

