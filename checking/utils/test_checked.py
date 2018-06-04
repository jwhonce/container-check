import collections
import logging
import sys
import traceback
import unittest
from StringIO import StringIO

from checked import Checked
from mock import patch


class FakeCode(object):
    def __init__(self, co_filename, co_name):
        self.co_filename = co_filename
        self.co_name = co_name


class FakeFrame(object):
    def __init__(self, f_code, f_globals):
        self.f_code = f_code
        self.f_globals = f_globals


class FakeTraceback(object):
    def __init__(self, frames, line_nums):
        if len(frames) != len(line_nums):
            raise ValueError("Ya messed up!")
        self._frames = frames
        self._line_nums = line_nums
        self.tb_frame = frames[0]
        self.tb_lineno = line_nums[0]

    @property
    def tb_next(self):
        if len(self._frames) > 1:
            return FakeTraceback(self._frames[1:], self._line_nums[1:])


class FakeException(Exception):
    def __init__(self, *args, **kwargs):
        self._tb = None
        super(FakeException, self).__init__(*args, **kwargs)

    @property
    def __traceback__(self):
        return self._tb

    @__traceback__.setter
    def __traceback__(self, value):
        self._tb = value

    def with_traceback(self, value):
        self._tb = value
        return self


class TestChecked(unittest.TestCase):
    def setUp(self):
        logging.basicConfig()
        self.checked = Checked()
        pass

    def tearDown(self):
        pass

    def test_constr(self):
        # verify context manager protocol
        for key in ('__enter__', '__exit__'):
            self.assertTrue(
                hasattr(self.checked, key)
                and callable(getattr(self.checked, key)),
                ('Expected {}() is not available.'
                 ' Checked failed context manager protocol').format(key))

    @patch('sys.stderr', new_callable=StringIO)
    @patch('sys.stdout', new_callable=StringIO)
    def test_enter(self, mock_out, mock_err):
        confirm, error = self.checked.__enter__()
        error(True)
        self.assertTrue(self.checked.error)

        confirm(False, 'unittest')
        self.assertEqual('', mock_out.getvalue())
        self.assertEqual('unittest\n', mock_err.getvalue())

    @patch('sys.exit')
    @patch('sys.stderr', new_callable=StringIO)
    @patch('sys.stdout', new_callable=StringIO)
    def test_exit(self, mock_out, mock_err, mock_exit):
        mock_exit.return_value = True
        confirm, error = self.checked.__enter__()
        error(True)

        code1 = FakeCode('fake1.py', 'mock_fn1')
        code2 = FakeCode('fake2.py', 'mock_fn2')
        frame1 = FakeFrame(code1, {})
        frame2 = FakeFrame(code2, {})
        tback = FakeTraceback([frame1, frame2], [1, 3])
        exc = FakeException('unittest').with_traceback(tback)

        self.checked.__exit__(Exception, exc, tback)

        self.assertEqual('', mock_out.getvalue())
        self.assertEqual(
            ('Traceback (most recent call last):\n'
             '  File "fake1.py", line 1, in mock_fn1\n'
             '  File "fake2.py", line 3, in mock_fn2\nException: unittest\n'),
            mock_err.getvalue())
        mock_exit.assert_called_once_with(1)
