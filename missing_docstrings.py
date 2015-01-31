#!/usr/bin/env python
from __future__ import division
import re
import sys
import os


# A list of lines that contain documented functions
DOCUMENTED_FUNCTIONS = {}

# A dict where the key is the file name and the value is a list of
# lines that contain undocumented functions.
UNDOCUMENTED_FUNCTIONS = {}

# A tuple of file names to ignore while scanning.
FILES_TO_IGNORE = (
    'test.py',
    'tests.py',
)

# A tuple of directories to ignore. If a file has any of these directories
# in its path then the file will be skipped.
DIRS_TO_IGNORE = (
    'migrations',
    'tests',
)


FUNCTION_REGEX = re.compile(r'^\s*def\s+.*\(.*\):\s*')


def _get_num_of_functions(function_dict):
    return len([item for sublist in function_dict.values() for item in sublist])


def file_to_process(file_path):
    """
    Determines if a file should be processed by the script.

    Args:
        file_path (str): The path to the file.

    Returns:
        bool: True if the file should be processed by the script.
    """
    file_name = os.path.basename(file_path)
    return file_name.endswith('.py')


def file_to_ignore(file_path):
    """
    Determines if a file should be ignored by the script.

    Args:
        file_path (str): The path to the file.

    Returns:
        bool: True if the file should be ignored by the script.
    """
    file_name = os.path.basename(file_path)
    path_parts = set(file_path.split(os.sep))
    # If the file should be ignored or if any of its path is in the
    # DIRS_TO_IGNORE tuple.
    if file_name in FILES_TO_IGNORE or path_parts & set(DIRS_TO_IGNORE):
        return True
    else:
        return False


def is_full_function_definition(line):
    """
    Determines if a line in a file is a full one-line function declaration.

    Args:
        line (str): The line to check for a function declaration.

    Returns:
        bool: True if the line is a function declaration.
    """
    return FUNCTION_REGEX.match(line)


def has_docstring(line):
    """
    Determines if a line in a file is a docstring.

    Args:
        line (str): The line to check for a docstring.

    Returns:
        bool: True if the line is a docstring.
    """
    clean_line = line.strip()
    return (clean_line.startswith('"""')
            or clean_line.startswith("'")
            or clean_line.startswith('"'))


def _add_to_function_dict(function_dict, file_path, line):
    """
    Adds a documented function to a function dict
    (DOCUMENTED_FUNCTIONS or UNDOCUMENTED_FUNCTIONS).

    Args:
        function_dict (dict): A function dict data structure
            (either DOCUMENTED_FUNCTIONS or UNDOCUMENTED_FUNCTIONS)
        file_path (str): The path to the file with the documented function.
        line (str): The line that contains the documented function.
    """
    if function_dict.get(file_path, False):
        function_dict[file_path].append(line)
    else:
        function_dict[file_path] = [line]


def add_to_undocumented_functions(file_path, line):
    _add_to_function_dict(UNDOCUMENTED_FUNCTIONS, file_path, line)


def add_to_documented_functions(file_path, line):
    _add_to_function_dict(DOCUMENTED_FUNCTIONS, file_path, line)


def process_file(file_path):
    """
    Scans a file line by line and finds each function that
    does not have an associated docstring.

    Args:
        file_path (str): The path to the file.
    """
    with open(file_path, 'r') as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            process_line(file_path, lines, line, i)


def process_line(file_path, lines, line, i):
    if is_full_function_definition(line):
        if has_docstring(lines[i+1]):
            add_to_documented_functions(file_path, line)
        else:
            add_to_undocumented_functions(file_path, line)


def _print_detail_lines():
    for file, lines in UNDOCUMENTED_FUNCTIONS.items():
        print(file)
        for line in lines:
            print('\t' + line.strip())
            print('')


def _print_summary():
    num_undocumented_functions = _get_num_of_functions(UNDOCUMENTED_FUNCTIONS)
    num_documented_functions = _get_num_of_functions(DOCUMENTED_FUNCTIONS)
    num_functions = num_documented_functions + num_undocumented_functions
    num_files_scanned = len(UNDOCUMENTED_FUNCTIONS.keys())
    percent_documented = num_documented_functions / num_functions * 100
    print('{} files scanned.'.format(num_files_scanned))
    print('{} total functions'.format(num_functions))
    print('{} documented functions, {} undocumented functions.'.format(
        num_documented_functions,
        num_undocumented_functions
    ))
    print('{:.3f}% documented'.format(percent_documented))


def print_results():
    """Prints the results of the script's run."""
    _print_detail_lines()
    _print_summary()


def main():
    """Runs the script."""
    starting_directory = sys.argv[1]
    full_directory_path = os.path.abspath(starting_directory)
    for path, dirs, files in os.walk(full_directory_path):
        for f in files:
            file_path = os.path.join(path, f)
            if file_to_process(file_path) and not file_to_ignore(file_path):
                process_file(file_path)
    print_results()


if __name__ == '__main__':
    main()