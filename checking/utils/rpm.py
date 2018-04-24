import copy
import os
import subprocess
import sys


class Rpm(object):
    """ Helper for rpm commands"""
    not_found = 'Package "{}" is not installed/found on host\n'
    not_valid = 'Files in package "{}" failed validation:\n{}\n'

    def __init__(self, name, prefix='/host'):
        self._name = name
        self._prefix = prefix

    def __enter__(self):
        """context manager protocol"""
        return self

    def __exit__(self, *args):
        """context manager protocol"""
        pass

    def _query(self, command):
        if os.environ.get('DEBUG', False):
            sys.stdout.write('DEBUG: rpm query: {}\n'.format(command))
            sys.stdout.flush()

        try:
            return subprocess.check_output(
                command, close_fds=True
            ).strip(), None
        except subprocess.CalledProcessError as e:
            if e.output.find('is not installed') >= 0:
                sys.stderr.write(Rpm.not_found.format(self._name))
            else:
                sys.stderr.write(
                    Rpm.not_valid.format(self._name, e.output.strip())
                )
            return None, e

    def _build_command(self, command):
        c = copy.deepcopy(command)
        if self._prefix:
            c.extend(['--root', self._prefix])
        c.append(self._name)
        return c

    def verify(self):
        """Verify files against rpm database, See rpm manpage."""
        c = self._build_command(['rpm', '--verify'])
        _, e = self._query(c)
        return True if e is None else False

    @property
    def files(self):
        """Obtain files for package"""
        c = self._build_command(['rpm', '--query', '--list'])
        o, e = self._query(c)
        return o.splitlines() if e is None else []

    @property
    def nvr(self):
        """Obtain (name, version, release) for package"""
        c = self._build_command(['rpm', '--query'])
        o, e = self._query(c)
        return o if e is None else None
