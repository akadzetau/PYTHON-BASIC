"""
Write tests for a read_numbers function.
It should check successful and failed cases
for example:
Test if user inputs: 1, 2, 3, 4
Test if user inputs: 1, 2, Text

Tip: for passing custom values to the input() function
Use unittest.mock patch function
https://docs.python.org/3/library/unittest.mock.html#unittest.mock.patch

TIP: for testing builtin input() function create another function which return input() and mock returned value
"""
from unittest.mock import patch
import io
import importlib
res = importlib.import_module('practice.2_python_part_2.task_input_output')


class TestCompareSysStdin():
    @patch('sys.stdin', io.StringIO("\n".join(["1", "2", "3", "4"])))
    def test_read_numbers_without_text_input(self):
        result = res.read_numbers(4)
        expect = 'Avg: 2.5'
        assert result == expect, "Input 1, 2, 3, 4 should return 'Avg: 2.5'"

    @patch('sys.stdin', io.StringIO("\n".join(["1", "2", "Test"])))
    def test_read_numbers_with_text_input(self):
        result = res.read_numbers(3)
        expect = 'Avg: 1.5'
        assert result == expect, "Input 1, 2, Test should return 'Avg: 1.5'"
