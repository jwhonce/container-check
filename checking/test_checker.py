import copy
import os
import subprocess
import sys
import unittest

from mock import MagicMock, PropertyMock, patch

from checker import Checker

# sys.path.insert(0, os.path.dirname(__file__))
sys.path.append('.')


class TestChecker(unittest.TestCase):
    def setUp(self):
        pass

    def test_constr(self):
        """TODO: patch sys.path to known value"""
        path = copy.deepcopy(sys.path)
        path.append('.')
        path = os.pathsep.join(path)

        checker = Checker(False)
        self.assertEqual({'PYTHONPATH': path}, checker.env)

        checker = Checker(True)
        self.assertEqual({'PYTHONPATH': path, 'DEBUG': 'True'}, checker.env)

    @patch.object(Checker, '_is_exec', return_value=True, auto_spec=True)
    @patch('loggeradapter.LoggerAdapter')
    def test_check_true(self, mock_logger, mock_is_exec):
        mock_popen = self._mock_popen('jokes', '', 0)
        setattr(subprocess, 'Popen', lambda *args, **kwargs: mock_popen)
        mock_logger.return_value = mock_logger

        verify = Checker(False).check('/mock/jester')
        mock_logger.error.assert_not_called()
        mock_logger.info.assert_called_with('jokes')
        mock_is_exec.assert_called_once_with('/mock/jester')
        self.assertTrue(verify)

    @patch.object(Checker, '_is_exec', return_value=True, auto_spec=True)
    @patch('loggeradapter.LoggerAdapter')
    def test_check_false(self, mock_logger, mock_is_exec):
        mock_popen = self._mock_popen('', 'jests', 666)
        setattr(subprocess, 'Popen', lambda *args, **kwargs: mock_popen)
        mock_logger.return_value = mock_logger

        verify = Checker(False).check('/mock/jester')
        mock_logger.error.assert_called_with('jests')
        mock_logger.info.assert_not_called()
        mock_is_exec.assert_called_once_with('/mock/jester')
        self.assertFalse(verify)

    def _mock_popen(self, stdout, stderr, rc):
        class MockPopen(object):
            def __init__(self):
                pass

            def communicate(self, input=None):
                pass

            @property
            def returncode(self):
                pass

        mock = MockPopen()
        mock.communicate = MagicMock(return_value=(stdout, stderr))
        mock_returncode = PropertyMock(return_value=rc)
        type(mock).returncode = mock_returncode
        return mock
