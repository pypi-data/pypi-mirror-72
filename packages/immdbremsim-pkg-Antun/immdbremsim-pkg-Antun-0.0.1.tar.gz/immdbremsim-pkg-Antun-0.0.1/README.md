

# Preparing release for pypi
python3 setup.py sdist bdist_wheel
python3 -m twine upload --repository testpypi dist/*


# Installing newly uploaded package
python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps example-pkg-YOUR-USERNAME-HERE


