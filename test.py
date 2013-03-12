from unittest import TestCase
import os
import makedb
from collections import Counter
import unittest


TEST_DATA_PATH = os.path.join(os.path.dirname(__file__), 'test_data')


class CueDBTestCase(TestCase):
    def test_read_directory_words(self):
        result = makedb.read_directory_words(os.path.join(TEST_DATA_PATH, 'read_directory'))
        self.assertEqual(Counter(result), Counter({('elvis', 'test_data/read_directory/a.txt'): 3,
                                                   ('is', 'test_data/read_directory/b/c/file.txt'): 1,
                                                   ('dead', 'test_data/read_directory/b/c/file.txt'): 1,
                                                   ('lincoln', 'test_data/read_directory/b/c/file.txt'): 1,
                                                   ('whatever', 'test_data/read_directory/b.txt'): 1,
                                                   ('elvis', 'test_data/read_directory/b/file.txt'): 1,
                                                   ('lives!', 'test_data/read_directory/b/file.txt'): 1}))

    # def test_maketrie(self):
    #     result = makedb.maketrie([('ala', 'a.txt'), ('bt', 'b.txt'), ('bt', 'a.txt'), ('alu', 'b.txt')])
    #     self.assertEqual(result, {'a': {'l': {'a': {'$': ['a.txt']},
    #                                           'u': {'$': ['b.txt']}}},
    #                               'b': {'t': {'$': ['b.txt', 'a.txt']}}})


if __name__ == '__main__':
    unittest.main()
