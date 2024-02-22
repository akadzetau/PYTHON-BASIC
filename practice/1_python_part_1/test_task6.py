from unittest import TestCase
from task6 import get_min_max


class TestTask6(TestCase):
    def test1(self):
        self.expected = (-2, 34)
        self.result = get_min_max("files/1_pyhon_part_1_task6.txt")
        self.assertTupleEqual(self.result, self.expected)