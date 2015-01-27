import unittest
import missing_docstrings

class TestFunctionDetection(unittest.TestCase):

    def test_valid_line_is_function(self):
        line = 'def test_func(self):'
        self.assertTrue(missing_docstrings.is_function(line))

    def test_valid_line_with_spaces_is_function(self):
        line = '    def test_func(self):'
        self.assertTrue(missing_docstrings.is_function(line))

    def test_valid_line_with_tabs_is_function(self):
        line = '\t\tdef test_func(self):'
        self.assertTrue(missing_docstrings.is_function(line))

    def test_variable_assignment_is_not_function(self):
        line = 'variable = True'
        self.assertFalse(missing_docstrings.is_function(line))

    def test_class_declaration_is_not_function(self):
        line = 'class MyClass:'
        self.assertFalse(missing_docstrings.is_function(line))


class TestDocstringDetection(unittest.TestCase):

    def test_valid_line_has_docstring(self):
        line = '"""test docstring"""'
        self.assertTrue(missing_docstrings.has_docstring(line))

    def test_valid_line_with_spaces_has_docstring(self):
        line = '    """test docstring"""    '
        self.assertTrue(missing_docstrings.has_docstring(line))

    def test_valid_line_with_tabs_has_docstring(self):
        line = '\t\t"""test docstring"""\t\t'
        self.assertTrue(missing_docstrings.has_docstring(line))

    def test_valid_multiline_has_docstrings(self):
        line = '"""\nA multi-line\ndocstring."""'
        self.assertTrue(missing_docstrings.has_docstring(line))

    def test_invalid_line_does_not_have_docstring(self):
        line = 'variable = "test"'
        self.assertFalse(missing_docstrings.has_docstring(line))


if __name__ == '__main__':
    unittest.main()