from unittest import TestCase
from unittest import mock
from task_exceptions import division, DivisionByOneException


class Test(TestCase):
    @mock.patch('task_exceptions.print')
    def test1(self, mock_print):
        self.result = division(1, 0)
        self.assertIsNone(self.result)
        self.assertListEqual(mock_print.mock_calls[0:2], [mock.call('Division by 0'), mock.call('Division finished')])

    @mock.patch('task_exceptions.print')
    def test2(self, mock_print):
        self.assertRaises(DivisionByOneException, division, 1, 1)
        self.assertListEqual(mock_print.mock_calls[0:1], [mock.call('Division finished')])

    @mock.patch('task_exceptions.print')
    def test3(self, mock_print):
        self.expected = 1
        self.result = division(2, 2)
        self.assertEqual(self.result, self.expected)
        self.assertListEqual(mock_print.mock_calls[0:2], [mock.call(1), mock.call('Division finished')])
