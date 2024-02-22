from unittest import TestCase
from unittest import mock
from task_input_output import read_numbers


class Test(TestCase):
    @mock.patch('task_input_output.input', create=True)
    def test1(self, mock_input):
        mock_input.side_effect = ["1", "2", "hello", "2", "world"]
        self.expected = "Avg: 1.67"
        self.result = read_numbers(5)
        self.assertEqual(self.result, self.expected)

    @mock.patch('task_input_output.input', create=True)
    def test2(self, mock_input):
        mock_input.side_effect = ["hello", "world", "foo", "bar", "baz"]
        self.expected = "No numbers entered"
        self.result = read_numbers(5)
        self.assertEqual(self.result, self.expected)