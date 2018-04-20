import unittest

from pathname import Pathname


class TestPathname(unittest.TestCase):
    def setUp(self):
        pass

    def test_default(self):
        self.assertEqual(Pathname('/a/b'), '/host/a/b')
        self.assertEqual(Pathname(('a', 'b')), '/host/a/b')
        self.assertEqual(Pathname(['a', 'b']), '/host/a/b')
        self.assertEqual(Pathname('a/b', prefix=None), 'a/b')

    def test_path(self):
        self.assertEqual(Pathname(('/a', 'b')).relpath, '/a/b')
        self.assertEqual(Pathname(['/a', 'b']).abspath, '/host/a/b')

    def test_prefix(self):
        self.assertEqual(Pathname(['a', 'b'], '/var'), '/var/a/b')
        self.assertEqual(Pathname(['a', 'b'], '/var').prefix, '/var')
        self.assertEqual(Pathname(['a', 'b']).prefix, '/host')
