# Missing Docstrings

A command line utility to search a Python project for functions with missing docstrings.

## Usage

Search an entire directory structure for functions/methods with missing docstrings:

```
python missing-docstrings.py /Users/grant/Dev/django/superlists/
```

Example output:

```
/Users/grant/Dev/django/superlists/lists/views.py
    def home_page(request):

    def view_list(request, list_id):

/Users/grant/Dev/django/superlists/lists/forms.py
    def __init__(self, for_list, *args, **kwargs):

    def save(self):

/Users/grant/Dev/django/superlists/lists/tests/test_models.py
    def test_get_absolute_url(self):

    def test_duplicate_items_are_invalid(self):

/Users/grant/Dev/django/superlists/functional_tests/test_layout_and_styling.py
    def test_layout_and_styling(self):

9 files scanned.
53 total functions
6 documented functions, 47 undocumented functions.
11.321% documented
```

## Known Issues

* Only works if function definitions are on one line. For instance, this docstring will be detected:

```python
def my_function(arg1, arg2, arg3):
    """My function docstring"""
```

While this will be falsely reported as a function without a docstring:

```python
def my_function(arg1, arg2,
                arg3, arg4):
    """My function docstring"""
```
