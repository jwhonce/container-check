import logging
import unittest
from StringIO import StringIO

from mock import patch

from checked import Checked


class TestChecked(unittest.TestCase):
    def setUp(self):
        logging.basicConfig()
        self.checked = Checked()
        pass

    def tearDown(self):
        pass

    def test_constr(self):
        # verify context manager protocol
        for key in ['__enter__', '__exit__']:
            self.assertTrue(
                hasattr(self.checked, key)
                and callable(getattr(self.checked, key)), (
                    'Expected {}() is not available.'
                    ' Checked failed context manager protocol'
                ).format(key)
            )

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

        self.checked.__exit__(
            Exception, Exception('unittest'),
            [('<stdin>', 1, '<module>', None)]
        )

        self.assertEqual('', mock_out.getvalue())
        self.assertEqual((
            "<type 'exceptions.Exception'>(unittest)\n"
            "[('<stdin>', 1, '<module>', None)]\n"
        ), mock_err.getvalue())
        mock_exit.assert_called_once_with(1)
