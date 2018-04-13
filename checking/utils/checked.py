import sys


class Checked(object):
    def __init__(self):
        self._error = False

    @property
    def error(self):
        return self._error

    @error.setter
    def error(self, value):
        if not isinstance(value, bool):
            raise ValueError()
        self._error = value

    def confirm(self, boolean, message):
        if not boolean:
            self.error = True
            sys.stderr.write(str(message) + '\n')
            sys.stderr.flush()

    def __enter__(self):
        return (
            self.confirm, lambda v: setattr(self, 'error', v)
        )

    def __exit__(self, exc_type, value, traceback):
        if traceback:
            sys.stderr.write(
                'Type {}({})\n{}'.format(exc_type, value, traceback)
            )

        sys.stderr.flush()
        sys.stdout.flush()
        sys.exit(1 if self._error else 0)
