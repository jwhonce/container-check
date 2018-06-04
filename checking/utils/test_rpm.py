import unittest

from rpm import Rpm


class TestRpm(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_constr(self):
        rpm = Rpm('mt-st')
        self.assertIs(rpm.__enter__(), rpm)

    def test_nvr(self):
        rpm = Rpm('mt-st', prefix=None)
        self.assertTrue(rpm.nvr.startswith('mt-st-1.1'))

    def test_files(self):
        rpm = Rpm('mt-st', prefix=None)
        self.assertIn('/usr/bin/mt', rpm.files)
        self.assertIn('/usr/share/man/man1/mt.1.gz', rpm.files)

    def test_verify(self):
        rpm = Rpm('mt-st', prefix=None)
        self.assertTrue(rpm.verify())
