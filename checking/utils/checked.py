import sys
import traceback


class Checked(object):
    """Context Manager for running checks."""

    def __init__(self):
        """Construct context manager for processing checked value."""
        self._error = False

    @property
    def error(self):
        """Error has occurred."""
        return self._error

    @error.setter
    def error(self, value):
        if not isinstance(value, bool):
            raise ValueError()
        self._error = value

    def confirm(self, boolean, message, *args, **kwargs):
        """Set errors and write out message."""
        if not boolean:
            self.error = True
            sys.stderr.write(str(message) + '\n')
            sys.stderr.flush()

    def __enter__(self):
        """Enter context manager and provide handlers."""
        return (self.confirm, lambda v: setattr(self, 'error', v))

    def __exit__(self, ex_type, ex_value, ex_traceback):
        """Log any exceptions."""
        if ex_type:
            sys.stderr.write(''.join(
                traceback.format_exception(ex_type, ex_value, ex_traceback)))

        # Clean up before exiting
        sys.stderr.flush()
        sys.stdout.flush()
        sys.exit(1 if self._error else 0)
