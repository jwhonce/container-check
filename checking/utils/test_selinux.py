import unittest

import mock
from selinux import Selinux


class TestSelinux(unittest.TestCase):
    def setUp(self):
        pass

    def test_constr(self):
        self.assertIsNot(Selinux('/mock'), None)

    def test_isenabled_true(self):
        with mock.patch('__builtin__.open') as mock_open:
            enabled = mock_open.return_value.__enter__.return_value
            enabled.side_effect = '1'
            self.assertTrue(Selinux('/mock').isenabled)
            mock_open.assert_called_once_with(
                '/mock/sys/fs/selinux/enforce', 'r'
            )

    def test_isenabled_false(self):
        with mock.patch('__builtin__.open') as mock_open:
            mock_open.side_effect = IOError()
            self.assertFalse(Selinux('/mock').isenabled)
            mock_open.assert_called_once_with(
                '/mock/sys/fs/selinux/enforce', 'r'
            )

    def test_verify_true(self):
        selinux = Selinux('/mock')
        with mock.patch.object(selinux, '_verify') as mock_verify:
            mock_verify.return_value = True
            file = '/etc/containers/policy.json'
            passed = selinux.verify(file)
            self.assertTrue(passed)
            mock_verify.assert_called_once_with(file)

    def test_verify_false(self):
        selinux = Selinux('/mock')
        with mock.patch.object(selinux, '_verify') as mock_verify:
            mock_verify.return_value = False
            file = '/etc/containers/policy.json'
            passed = selinux.verify(*[file, file])
            self.assertFalse(passed)
            self.assertEqual(mock_verify.call_count, 2)

    @unittest.skip('TODO: design tests for _verify')
    def test__verify(self):
        pass
