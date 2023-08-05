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

## publish to pypi

```python
python setup.py bdist_wheel sdist
pip install twine

twine upload dist/*
```

## publish to S3

[source](https://medium.com/november-five/setting-up-a-private-python-package-repository-on-amazon-s3-246290ac6c1e)

