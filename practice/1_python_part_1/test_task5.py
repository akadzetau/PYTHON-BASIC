from unittest import TestCase
from task5 import remove_duplicated_words


class TestTask1(TestCase):
    def test1(self):
        self.expected = 'cat dog 1 2'
        self.result = remove_duplicated_words('cat cat dog 1 dog 2')
        self.assertEqual(self.result, self.expected)

    def test2(self):
        self.expected = 'cat'
        self.result = remove_duplicated_words('cat cat cat')
        self.assertEqual(self.result, self.expected)

    def test3(self):
        self.expected = '1 2 3'
        self.result = remove_duplicated_words('1 2 3')
        self.assertEqual(self.result, self.expected)

    def test4(self):
        self.expected = ''
        self.result = remove_duplicated_words('')
        self.assertEqual(self.result, self.expected)
