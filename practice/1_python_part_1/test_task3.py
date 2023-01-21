from unittest import TestCase
from task3 import build_from_unique_words


class TestTask3(TestCase):
    def test1(self):
        self.expected = 'b 2 dog'
        self.result = build_from_unique_words('a b c', '1 1 1 2 3', 'cat dog milk', word_number=1)
        self.assertEqual(self.result, self.expected)

    def test2(self):
        self.expected = 'a cat'
        self.result = build_from_unique_words('a b c', '', 'cat dog milk', word_number=0)
        self.assertEqual(self.result, self.expected)

    def test3(self):
        self.expected = ''
        self.result = build_from_unique_words('1 2', '1 2 3', word_number=10)
        self.assertEqual(self.result, self.expected)

    def test4(self):
        self.expected = ''
        self.result = build_from_unique_words(word_number=10)
        self.assertEqual(self.result, self.expected)
