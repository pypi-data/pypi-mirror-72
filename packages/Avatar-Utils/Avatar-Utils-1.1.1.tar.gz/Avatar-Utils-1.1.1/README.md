# Package for common utils of avatar ecosystem

##### Install setuptools and wheel

```
pip install setuptools wheel
```

##### Generate distribution package

```bash
python setup.py sdist bdist_wheel
```

##### Install twine

```bash
pip install twine
```

##### Upload package to index

```bash
python -m twine upload dist/*
```
