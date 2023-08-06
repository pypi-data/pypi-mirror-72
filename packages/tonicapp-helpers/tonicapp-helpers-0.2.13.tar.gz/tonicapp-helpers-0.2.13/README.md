# Helpers

## Requirements
* Python
* Django
* Django Rest Framework
* DRF spectacular ("https://pypi.org/project/drf-spectacular/")


## Installation

```
$ pip install tonicapp-helpers
```

Add the application to your project's `INSTALLED_APPS` in `settings.py`.

```
INSTALLED_APPS = [
    ...
    'helpers',
]
```


## Source

```
https://pypi.org/project/tonicapp-helpers/
```


## Update Library

```
python setup.py sdist
```

```
python -m twine upload dist/*
```