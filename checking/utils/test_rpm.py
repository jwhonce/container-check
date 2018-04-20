import unittest

import mock
from rpm import Rpm


class TestRpm(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_constr(self):
        rpm = Rpm('mock-me')
        self.assertIs(rpm.__enter__(), rpm)

    def test_nvr(self):
        expected = 'mock-me-0.0.0-0.gitdeadbeef.fc100.x86_4096'
        rpm = Rpm('mock-me', prefix='/mock')
        with mock.patch.object(rpm, '_query') as query:
            query.return_value = (expected, None)
            self.assertEqual(expected, rpm.nvr)
            query.assert_called_once_with([
                'rpm', '--query', '--root', '/mock', 'mock-me'
            ])

    def test_files(self):
        expected = ['Pocket', 'Wamba', 'Rigoletto']
        rpm = Rpm('mock-me', prefix='/mock')
        with mock.patch.object(rpm, '_query') as query:
            query.return_value = ('\n'.join(expected), None)
            self.assertEqual(expected, rpm.files)
            query.assert_called_once_with([
                'rpm', '--query', '--list', '--root', '/mock', 'mock-me'
            ])

    def test_verify(self):
        rpm = Rpm('mock-me', prefix='/mock')
        with mock.patch.object(rpm, '_query') as query:
            query.return_value = (None, None)
            self.assertTrue(rpm.verify())
            query.assert_called_once_with([
                'rpm', '--verify', '--root', '/mock', 'mock-me'
            ])
