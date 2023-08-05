# dummy pypi package

try to make a package to host on pypi

[source](https://www.youtube.com/watch?v=GIF3LaRqgXo)

[chooselicense](https://choosealicense.com/)

## check manifest

```python
pip install check-manifest
check-manifest --create
```

## instalation

```python
pip install helloworld
```

## publish

```python
python setup.py bdist_wheel sdist
pip install twine

twine upload dist/*
```