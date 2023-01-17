from unittest import TestCase
from task1 import delete_from_list


class TestTask1(TestCase):
    def test1(self):
        self.expected = [1, 2, 4]
        self.result = delete_from_list([1, 2, 3, 4, 3], 3)
        self.assertListEqual(self.result, self.expected)

    def test2(self):
        self.expected = ['a', 'c', 'd']
        self.result = delete_from_list(['a', 'b', 'c', 'b', 'd'], 'b')
        self.assertListEqual(self.result, self.expected)

    def test3(self):
        self.expected = [1, 2, 3]
        self.result = delete_from_list([1, 2, 3], 'b')
        self.assertListEqual(self.result, self.expected)

    def test4(self):
        self.expected = []
        self.result = delete_from_list([], 'b')
        self.assertListEqual(self.result, self.expected)
