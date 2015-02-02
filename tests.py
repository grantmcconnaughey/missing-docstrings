import collections
import unittest
import missing_docstrings


class TestFunctionDetection(unittest.TestCase):

    def test_valid_line_with_tabs_is_function(self):
        line = '\t\tdef test_func(self):'
        self.assertTrue(missing_docstrings.is_full_function_definition(line))

    def test_function_no_arguments(self):
        line = 'def test_function():\n'
        self.assertTrue(missing_docstrings.is_full_function_definition(line))

    def test_function_one_argument(self):
        line = 'def test_function(arg1):\n'
        self.assertTrue(missing_docstrings.is_full_function_definition(line))

    def test_function_two_arguments(self):
        line = 'def test_function(arg1, arg2):\n'
        self.assertTrue(missing_docstrings.is_full_function_definition(line))

    def test_function_with_leading_whitespace(self):
        line = '   def test_function(arg1, arg2):\n'
        self.assertTrue(missing_docstrings.is_full_function_definition(line))

    def test_function_with_trailing_whitespace(self):
        line = 'def test_function(arg1, arg2):    \n'
        self.assertTrue(missing_docstrings.is_full_function_definition(line))

    def test_function_with_comment(self):
        line = 'def test_function(): #  test comment\n'
        self.assertTrue(missing_docstrings.is_full_function_definition(line))

    def test_variable_assignment_is_not_function(self):
        line = 'variable = True'
        self.assertFalse(missing_docstrings.is_full_function_definition(line))

    def test_class_declaration_is_not_function(self):
        line = 'class MyClass:'
        self.assertFalse(missing_docstrings.is_full_function_definition(line))

    def test_function_multi_lines(self):
        line = 'def test_function(arg1,\n'
        self.assertFalse(missing_docstrings.is_full_function_definition(line))

    def test_function_call(self):
        line = 'definition(arg1)'
        self.assertFalse(missing_docstrings.is_full_function_definition(line))

    def test_partial_function(self):
        line = 'def test_func(arg1, arg2,\n'
        self.assertFalse(missing_docstrings.is_full_function_definition(line))


class TestPartialFunctionDetection(unittest.TestCase):

    def test_partial_function(self):
        line = 'def test_func(arg1, arg2,\n'
        self.assertTrue(missing_docstrings.is_partial_function_definition(line))

    def test_partial_function_with_comment(self):
        line = 'def test_func(arg1, arg2,   # Function comment\n'
        self.assertTrue(missing_docstrings.is_partial_function_definition(line))

    def test_full_function(self):
        line = 'def test_func(arg1, arg2, arg3):'
        self.assertFalse(missing_docstrings.is_partial_function_definition(line))


class TestFunctionEndDetection(unittest.TestCase):

    def test_end_of_function_no_whitespace(self):
        line = 'arg3, arg4):\n'
        self.assertTrue(missing_docstrings.is_end_of_function_definition(line))

    def test_end_of_function_leading_whitespace(self):
        line = '    arg3, arg4):\n'
        self.assertTrue(missing_docstrings.is_end_of_function_definition(line))

    def test_end_of_function_trailing_whitespace(self):
        line = 'arg3, arg4):     \n'
        self.assertTrue(missing_docstrings.is_end_of_function_definition(line))

    def test_end_of_function_with_comment(self):
        line = 'arg3, arg4):  # Test comment\n'
        self.assertTrue(missing_docstrings.is_end_of_function_definition(line))

    def test_not_end_of_function(self):
        line = '    arg3, arg4, arg5,\n'
        self.assertFalse(missing_docstrings.is_end_of_function_definition(line))

    def test_no_colon(self):
        line = '    arg3, arg4, arg5)\n'
        self.assertFalse(missing_docstrings.is_end_of_function_definition(line))


class TestDocstringRegex(unittest.TestCase):

    def setUp(self):
        self.regex = missing_docstrings.DOCSTRING_REGEX

    def test_triple_string(self):
        docstring = '    """test"""'
        self.assertTrue(self.regex.match(docstring))

    def test_double_quote(self):
        docstring = '    "test"'
        self.assertTrue(self.regex.match(docstring))

    def test_single_quote(self):
        docstring = "    'test'"
        self.assertTrue(self.regex.match(docstring))

    def test_no_leading_whitespace(self):
        docstring = '"""test"""'
        self.assertTrue(self.regex.match(docstring))

    def test_trailing_newline(self):
        docstring = '    """test"""\n'
        self.assertTrue(self.regex.match(docstring))

    def test_class_declaration(self):
        class_def = '    class Tester:\n'
        self.assertFalse(self.regex.match(class_def))

    def test_function_multi_lines(self):
        function_def = 'def test_function(arg1,\n'
        self.assertFalse(self.regex.match(function_def))

    def test_function_call(self):
        function_call = 'definition(arg1)'
        self.assertFalse(self.regex.match(function_call))


class TestDocstringDetection(unittest.TestCase):

    def test_valid_line_docstring(self):
        line = '"""test docstring"""'
        self.assertTrue(missing_docstrings.has_docstring(line))

    def test_valid_line_with_spaces_docstring(self):
        line = '    """test docstring"""    '
        self.assertTrue(missing_docstrings.has_docstring(line))

    def test_valid_line_with_tabs_docstring(self):
        line = '\t\t"""test docstring"""\t\t'
        self.assertTrue(missing_docstrings.has_docstring(line))

    def test_valid_multiline_docstring(self):
        line = '"""\nA multi-line\ndocstring."""'
        self.assertTrue(missing_docstrings.has_docstring(line))

    def test_valid_single_quoted_docstring(self):
        line = "'This is a docstring'"
        self.assertTrue(missing_docstrings.has_docstring(line))

    def test_valid_double_quoted_docstring(self):
        line = '"This is a docstring"'
        self.assertTrue(missing_docstrings.has_docstring(line))

    def test_variable_assignment_does_not_have_docstring(self):
        line = 'variable = "test"'
        self.assertFalse(missing_docstrings.has_docstring(line))

    def test_class_definition_does_not_have_docstring(self):
        line = 'class Tester:'
        self.assertFalse(missing_docstrings.has_docstring(line))


class TestAddToUndocumentedFunctions(unittest.TestCase):

    def tearDown(self):
        missing_docstrings.undocumented_functions = collections.defaultdict(list)

    def test_add_to_undocumented_functions(self):
        file = '/Users/test/test.py'
        line = 'def this_is_a_test():'

        missing_docstrings.add_to_undocumented_functions(file, line)

        self.assertEqual(len(missing_docstrings.undocumented_functions), 1)

    def test_add_duplicate_to_undocumented_functions(self):
        file = '/Users/test/test.py'
        line = 'def this_is_a_test():'

        # Add multiple lines from the same file
        missing_docstrings.add_to_undocumented_functions(file, line)
        missing_docstrings.add_to_undocumented_functions(file, line)

        # There is still only one entry in undocumented_functions
        self.assertEqual(len(missing_docstrings.undocumented_functions), 1)
        # But there are two entries for that particular file
        self.assertEqual(len(missing_docstrings.undocumented_functions[file]), 2)


if __name__ == '__main__':
    unittest.main()