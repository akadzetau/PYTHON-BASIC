from unittest import TestCase
from task2 import set_to_dict


class TestTask1(TestCase):
    def test1(self):
        self.expected = {'a': 1, 'b': 4, 'c': 3}
        self.result = set_to_dict({'a': 1, 'b': 2, 'c': 3}, a=0, b=4)
        self.assertDictEqual(self.result, self.expected)

    def test2(self):
        self.expected = {'a': 0}
        self.result = set_to_dict({}, a=0)
        self.assertDictEqual(self.result, self.expected)

    def test3(self):
        self.expected = {'a': 5}
        self.result = set_to_dict({'a': 5})
        self.assertDictEqual(self.result, self.expected)
