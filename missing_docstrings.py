#!/usr/bin/env python
from __future__ import division
import collections
import re
import sys
import os


# Two defaultdicts where the key is the file name and the value is a list of
# lines that contain functions signatures.
documented_functions = collections.defaultdict(list)
undocumented_functions = collections.defaultdict(list)

# A tuple of file names to ignore while scanning.
FILES_TO_IGNORE = (
    'test.py',
    'tests.py',
)

# A tuple of directories to ignore. If a file has any of these directories
# in its path then the file will bep skipped.
DIRS_TO_IGNORE = (
    'migrations',
    'tests',
    '.Trash',
)


FUNCTION_REGEX = re.compile(r'^\s*def\s+.*\(.*\):\s*(#.*)?$', re.DOTALL)
PARTIAL_FUNCTION_REGEX = re.compile(r'^\s*def\s+.*\([^):]*(#.*)?$', re.DOTALL)
FUNCTION_END_REGEX = re.compile(r'^.*\):\s*(#.*)?$', re.DOTALL)
DOCSTRING_REGEX = re.compile(r'^\s*("""|"|\').*$', re.DOTALL)


SCRIPT_USAGE = """Usage:
    python missing_docstrings.py {path_to_project_dir}"""

FUNCTION_SPACING = '    '


def _get_num_of_functions(function_dict):
    return len([item for sub in function_dict.values() for item in sub])


def file_to_process(file_path):
    file_name = os.path.basename(file_path)
    return file_name.endswith('.py')


def file_to_ignore(file_path):
    file_name = os.path.basename(file_path)
    path_parts = set(file_path.split(os.sep))
    # If the file should be ignored or if any of its path is in the
    # DIRS_TO_IGNORE tuple.
    return file_name in FILES_TO_IGNORE or path_parts & set(DIRS_TO_IGNORE)


def is_full_function_definition(line):
    return bool(FUNCTION_REGEX.match(line))


def is_partial_function_definition(line):
    return bool(PARTIAL_FUNCTION_REGEX.match(line))


def is_end_of_function_definition(line):
    return bool(FUNCTION_END_REGEX.match(line))


def has_docstring(line):
    return bool(DOCSTRING_REGEX.match(line))


def add_to_undocumented_functions(file_path, line):
    undocumented_functions[file_path].append(line)


def add_to_documented_functions(file_path, line):
    documented_functions[file_path].append(line)


def process_file(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            process_line(file_path, lines, line, i)


def process_line(file_path, lines, line, current_index):
    if is_full_function_definition(line):
        if len(lines) > (current_index+1) and has_docstring(lines[current_index+1]):
            add_to_documented_functions(file_path, line)
        else:
            add_to_undocumented_functions(file_path, line)
    elif is_partial_function_definition(line):
        function_definition = line
        # Try to find the end of the function definition over the next 20 lines
        for k in range(current_index, current_index + 20):
            current_line = lines[k+1]
            next_line = lines[k+2]
            function_definition += FUNCTION_SPACING + current_line
            if is_end_of_function_definition(current_line):
                if has_docstring(next_line):
                    add_to_documented_functions(file_path, function_definition)
                else:
                    add_to_undocumented_functions(file_path, function_definition)
                break


def _print_detail_lines():
    for file_path, lines in iter(sorted(undocumented_functions.items())):
        print(file_path)
        for line in lines:
            print('{}{}\n'.format(FUNCTION_SPACING, line.strip()))


def _print_summary():
    num_undocumented_functions = _get_num_of_functions(undocumented_functions)
    num_documented_functions = _get_num_of_functions(documented_functions)
    num_functions = num_documented_functions + num_undocumented_functions
    num_files_scanned = len(undocumented_functions.keys())
    try:
        percent_documented = num_documented_functions / num_functions * 100
    except ZeroDivisionError:
        percent_documented = 0
    print('{} files scanned.'.format(num_files_scanned))
    print('{} total functions'.format(num_functions))
    print('{} documented functions, {} undocumented functions.'.format(
        num_documented_functions,
        num_undocumented_functions
    ))
    print('{:.3f}% documented'.format(percent_documented))


def print_results():
    _print_detail_lines()
    _print_summary()


def main():
    if len(sys.argv) == 1:
        sys.exit(SCRIPT_USAGE)

    starting_directory = sys.argv[1]
    full_directory_path = os.path.abspath(starting_directory)

    if not os.path.exists(full_directory_path):
        print("{} is not a valid path".format(full_directory_path))
        sys.exit()

    for path, dirs, files in os.walk(full_directory_path):
        for f in files:
            file_path = os.path.join(path, f)
            if file_to_process(file_path) and not file_to_ignore(file_path):
                process_file(file_path)
    print_results()


if __name__ == '__main__':
    main()
