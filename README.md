# Missing Docstrings

A command line utility to search a Python project for functions with missing docstrings.

## Usage

```
usage: missing_docstrings.py [-h] [--skipinit] [--skipinitpy] path

positional arguments:
  path          The path to your Python project

optional arguments:
  -h, --help    show this help message and exit
  --skipinit    Flag that indicates if __init__() methods should be skipped.
  --skipinitpy  Flag that indicates if __init__.py files should be skipped.
```

## Examples

Search an entire directory structure for functions/methods with missing docstrings:

```
python missing_docstrings.py ~/Dev/django/superlists/
```

Example output:

```
/Users/grant/Dev/django/superlists/lists/views.py
    def home_page(request):

    def view_list(request, list_id):

/Users/grant/Dev/django/superlists/lists/forms.py
    def __init__(self, for_list, *args, **kwargs):

    def save(self):

/Users/grant/Dev/django/superlists/functional_tests/test_layout_and_styling.py
    def test_layout_and_styling(self):

9 files scanned.
53 total functions
6 documented functions, 47 undocumented functions.
11.321% documented
```

## Skipped files/directories

Files with the following names will be skipped:

* test.py
* tests.py

If a file has one of the following directories in its path then it will also be skipped:

* migrations
* tests
* .Trash
