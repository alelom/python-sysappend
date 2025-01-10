# Release Process

1. Update the version in `sysappend/version.py`.

2. Run `python3 -m build`

3. Delete any previous releases from the `dist` folder

4. Upload to PyPiTest: `python3 -m twine upload --repository testpypi dist/*`
   
5. Upload to PyPi: `python3 -m twine upload dist/*` 

