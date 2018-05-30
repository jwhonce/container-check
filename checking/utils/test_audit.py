import errno
import os
import unittest

from audit import Audit

from mock import patch


class TestAudit(unittest.TestCase):
    """Audit() methods are helpers for auparse, not much to test"""

    @patch('auparse.AuParser')
    def test_constr_IOError(self, mock_parser):
        mock_parser.side_effect = IOError(errno.ENOENT,
                                          os.strerror(errno.ENOENT),
                                          '/mock/jester')

        with self.assertRaises(IOError) as cm:
            Audit('/jester', '/mock')
        self.assertEqual('/jester', cm.exception.filename)
