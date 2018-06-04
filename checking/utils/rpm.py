from __future__ import absolute_import

import subprocess
import sys
from backports.functools_lru_cache import lru_cache
import rpm as _rpm

from .pathname import Pathname


class Rpm(object):
    """Model for RPM database."""

    def __init__(self, name, prefix='/host'):
        """Construct rpm manager."""
        self.name = name
        self._prefix = prefix

        _rpm.addMacro('_dbpath', Pathname('/var/lib/rpm/'))
        t = _rpm.TransactionSet()
        m = t.dbMatch('name', name)
        for hdr in m:
            self.package = hdr
            break
        else:
            self.package = None

    def __enter__(self):
        """Context manager protocol."""
        return self

    def __exit__(self, *args):
        """Context manager protocol."""
        pass

    @property
    def isinstalled(self):
        """Return True if package is installed."""
        return False if self.package is None else True

    @property
    def nvr(self):
        """Return Name-Version-Release for package."""
        if self.package:
            return self.package.sprintf("%{NAME}-%{VERSION}-%{RELEASE}")
        return None

    @property
    @lru_cache(maxsize=1)
    def files(self):
        """Return list of files in package."""
        if self.package:
            return [f[0] for f in self.package.fiFromHeader()]
        return []

    def verify(self):
        """Return True if no errors are found.

        Use rpm command to take care of verify.
        """
        cmd = ['rpm', '--verify']
        if self._prefix:
            cmd.extend(['--root', self._prefix])
        cmd.append(self.name)

        try:
            subprocess.check_output(cmd, close_fds=True)
            return True
        except subprocess.CalledProcessError as e:
            if e.output.find('is not installed') >= 0:
                sys.stderr.write(
                    'Package "{}" is not installed/found on host.\n'.format(
                        self.name))
            else:
                sys.stderr.write(
                    'Files in package "{}" failed validation:\n{}\n'.format(
                        self.name, e.output.strip()))
