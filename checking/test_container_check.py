import shutil
import imp
import os
import tempfile
import unittest

from mock import MagicMock, call, patch


class TestContainerCheck(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = 'container_check'
        with open(path, 'r') as src:
            module = imp.load_module(
                'ContainerCheck', src, path, ('', 'r', imp.PY_SOURCE)
            )
        cls.main_cls = module.Main

    def setUp(self):
        def mkdirs(path):
            os.makedirs(path)
            return path

        def mkfile(prefix, dirname, mode, content=''):
            dir = mkdirs(os.path.join(prefix, dirname))
            (fd, file) = tempfile.mkstemp(suffix='py', prefix='check', dir=dir)
            try:
                os.write(fd, content)
                os.fchmod(fd, mode)
            finally:
                os.close(fd)
            return dir, file

        self.home = tempfile.mkdtemp()

        self.no_dir = os.path.join(self.home, 'no_directory')

        self.empty_dir = mkdirs(os.path.join(self.home, 'empty_dir'))

        # create no executable directory
        self.lost_dir, self.lost_file = mkfile(
            self.home, 'lost_dir', 0444,
            '#!/usr/bin/env python\nprint "hello, world"'
        )

        # create no executable directory
        self.checks_dir, self.check_file = mkfile(
            self.home, 'checks', 0555, '#!/usr/bin/env python\nexit(0)'
        )

    def tearDown(self):
        shutil.rmtree(self.home)

    @patch('checking.Checker.check', return_value=False)
    def test_bad_dir(self, mock_checker):
        mock_log = MagicMock()
        parser = self.main_cls.get_parser()

        bad_path = os.pathsep.join([
            self.no_dir, self.empty_dir, self.lost_dir
        ])
        args = parser.parse_args(['--checks', bad_path])
        setattr(args, 'log', mock_log)

        rc = self.main_cls.apply(args)
        calls = [call('"{}" is not an existing directory'.format(self.no_dir))]
        mock_log.error.assert_has_calls(calls)
        mock_log.info.assert_not_called()
        mock_checker.assert_called_once()
        self.assertEqual(rc, 2)

    @patch('checking.Checker.check', return_value=False)
    def test_no_checks(self, mock_checker):
        mock_log = MagicMock()
        parser = self.main_cls.get_parser()

        bad_path = self.empty_dir
        args = parser.parse_args(['--checks', bad_path])
        setattr(args, 'log', mock_log)

        rc = self.main_cls.apply(args)
        calls = [call('"{}" contain no checks'.format(self.empty_dir))]
        mock_log.error.assert_has_calls(calls)
        mock_log.info.assert_not_called()
        mock_checker.assert_called_once()
        self.assertEqual(rc, 1)

    @patch('checking.Checker.check', return_value=True)
    def test_appy(self, mock_checker):
        mock_log = MagicMock()
        parser = self.main_cls.get_parser()

        args = parser.parse_args(['--checks', self.checks_dir])
        setattr(args, 'log', mock_log)

        rc = self.main_cls.apply(args)
        mock_log.error.assert_not_called()
        mock_log.info.assert_not_called()
        mock_checker.assert_called_once()
        self.assertEqual(rc, 0)
