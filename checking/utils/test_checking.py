import os
import shutil
import tempfile
import unittest

from checking.utils import resolve_config, strip_config


class TestChecking(unittest.TestCase):
    def setUp(self):
        self.home = tempfile.mkdtemp()

        self.no_file = os.path.join(self.home, 'no_file_here')

        self.script_storage = os.path.join(self.home, 'script_storage')
        with open(self.script_storage, 'w') as config:
            config.write('# comment 1\nSTORAGE=holographic')

        self.script_empty = os.path.join(self.home, 'empty')
        with open(self.script_empty, 'w') as config:
            pass

        self.script_error = os.path.join(self.home, 'error')
        with open(self.script_error, 'w') as config:
            config.write('#!/bin/bash\n()=Bozo')

        self.script_all_comments = os.path.join(self.home, 'all_comments')
        with open(self.script_all_comments, 'w') as config:
            config.write('#!/bin/bash\n# line 1\n # line 2\n')

        self.script_comments = os.path.join(self.home, 'comments')
        with open(self.script_comments, 'w') as config:
            config.write('#!/bin/bash\nline 1\nline 2\n')

    def tearDown(self):
        shutil.rmtree(self.home)

    def test_resolve_storage(self):
        config = resolve_config(self.script_storage)
        self.assertEqual(config['STORAGE'], 'holographic')

    def test_resolve_no_file(self):
        config = resolve_config(self.no_file)
        self.assertDictEqual(config, {})

    def test_resolve_empty(self):
        config = resolve_config(self.script_empty)
        self.assertDictEqual(config, {})

    def test_resolve_error(self):
        config = resolve_config(self.script_error)
        self.assertDictEqual(config, {})

    def test_strip_storage(self):
        config = strip_config(self.script_storage)
        self.assertListEqual(config, ['STORAGE=holographic'])

    def test_strip_no_file(self):
        config = strip_config(self.no_file)
        self.assertListEqual(config, [])

    def test_strip_empty(self):
        config = strip_config(self.script_empty)
        self.assertListEqual(config, [])

    def test_strip_error(self):
        config = strip_config(self.script_error)
        self.assertListEqual(config, ['()=Bozo'])
