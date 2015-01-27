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


def file_to_ignore(file_name):
    if file_name in FILES_TO_IGNORE:
        return True
    else:
        return False


def is_function(line):
    clean_line = line.strip()
    return clean_line.startswith('def ')


def has_docstring(line):
    clean_line = line.strip()
    return clean_line.startswith('"""')


def add_to_undocumented_functions(file, line):
    if UNDOCUMENTED_FUNCTIONS.get(file, False):
        UNDOCUMENTED_FUNCTIONS[file].append(line)
    else:
        UNDOCUMENTED_FUNCTIONS[file] = [line]


def process_python_file(file):
    with open(file, 'r') as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if is_function(line):
                if has_docstring(lines[i+1]):
                    DOCUMENTED_FUNCTIONS.append(line)
                else:
                    add_to_undocumented_functions(file, line)


def print_results():
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
    print '{} documented functions, {} undocumented functions.'.format(
        num_documented_functions,
        num_undocumented_functions
    )
    print '{:.3f}% documented'.format(percent_documented)


def main():
    starting_directory = sys.argv[1]
    full_directory_path = os.path.abspath(starting_directory)
    for path, dirs, files in os.walk(full_directory_path):
        for f in files:
            if f.endswith('.py') and not file_to_ignore(f):
                full_file_path = os.path.join(path, f)
                process_python_file(full_file_path)
    print_results()


if __name__ == '__main__':
    main()