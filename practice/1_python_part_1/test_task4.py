from unittest import TestCase
from task4 import calculate_power_with_difference


class TestTask1(TestCase):
    def test1(self):
        self.expected = [1, 4, 7]
        self.result = calculate_power_with_difference([1, 2, 3])
        self.assertListEqual(self.result, self.expected)
