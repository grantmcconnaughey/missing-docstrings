#!/usr/bin/env python
from __future__ import division
import re
import sys
import os


# A list of lines that contain documented functions
DOCUMENTED_FUNCTIONS = []

# A dict where the key is the file name and the value is a list of
# lines that contain undocumented functions.
UNDOCUMENTED_FUNCTIONS = {}

# A tuple of file names to ignore while scanning.
FILES_TO_IGNORE = (
    'test.py',
)


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
    if file_name in FILES_TO_IGNORE:
        return True
    else:
        return False


def is_function(line):
    """
    Determines if a line in a file is a function declaration.

    Args:
        line (str): The line to check for a function declaration.

    Returns:
        bool: True if the line is a function declaration.
    """
    return line.strip().startswith('def ')


def has_docstring(line):
    """
    Determines if a line in a file is a docstring.

    Args:
        line (str): The line to check for a docstring.

    Returns:
        bool: True if the line is a docstring.
    """
    return line.strip().startswith('"""')


def add_to_undocumented_functions(file_path, line):
    """
    Adds an undocumented function to the UNDOCUMENTED_FUNCTIONS constant.

    Args:
        file_path (str): The path to the file with the undocumented function.
        line (str): The line that contains the undocumented function.
    """
    if UNDOCUMENTED_FUNCTIONS.get(file_path, False):
        UNDOCUMENTED_FUNCTIONS[file_path].append(line)
    else:
        UNDOCUMENTED_FUNCTIONS[file_path] = [line]


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
            if is_function(line):
                if has_docstring(lines[i+1]):
                    DOCUMENTED_FUNCTIONS.append(line)
                else:
                    add_to_undocumented_functions(file_path, line)


def print_results():
    """Prints the results of the script's run."""
    num_undocumented_functions = 0
    # Print detail lines
    for file, lines in UNDOCUMENTED_FUNCTIONS.items():
        print file
        for line in lines:
            num_undocumented_functions += 1
            print '\t' + line.strip()
            print ''

    # Print summary
    num_documented_functions = len(DOCUMENTED_FUNCTIONS)
    num_functions = num_documented_functions + num_undocumented_functions
    percent_documented = num_documented_functions / num_functions * 100
    print '{} files scanned.'.format(len(UNDOCUMENTED_FUNCTIONS.keys()))
    print '{} total functions'.format(num_functions)
    print '{} documented functions, {} undocumented functions.'.format(
        num_documented_functions,
        num_undocumented_functions
    )
    print '{:.3f}% documented'.format(percent_documented)


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