from __future__ import absolute_import

import errno
import os
import stat
import sys

import selinux

from .pathname import Pathname


class Selinux(object):
    """Helpers for SeLinux bindings"""

    def __init__(self, prefix='/host'):
        self._prefix = prefix

    @property
    def isenabled(self):
        path = Pathname('/sys/fs/selinux/enforce', self._prefix)
        try:
            with open(path, 'r') as fd:
                return True if fd.read().startswith('1') else False
        except (OSError, IOError):
            return False

    def verify(self, path):
        """Verify the selinux context on given path is as expected"""
        fn = Pathname(path, self._prefix)
        try:
            mode = os.lstat(fn)[stat.ST_MODE]
            status, expected = selinux.matchpathcon(path, mode)
        except OSError:
            fn = Pathname(os.path.realpath(os.path.expanduser(fn)), None)
            try:
                mode = os.lstat(fn)[stat.ST_MODE]
                status, expected = selinux.matchpathcon(path, mode)
            except OSError as e:
                sys.stderr.write(
                    'Verifying "{}" failed with {}\n'.format(
                        path, os.strerror(int(e.errno))
                    )
                )
                return False

        if status != 0:
            sys.stderr.write(
                'Verifying "{}" failed with {}\n'.format(
                    path, os.strerror(int(status))
                )
            )
            return False

        try:
            _, actual = selinux.lgetfilecon(fn)
        except OSError as e:
            if e.errno != errno.ENODATA:
                sys.stderr.write(
                    'Verifying "{}" failed with {}\n'.format(
                        path, os.strerror(int(e.errno))
                    )
                )
                return False
            actual = None

        if expected != actual:
            sys.stderr.write(
                "{} incorrect context: actual({}) expected({})\n".format(
                    path, actual, expected
                )
            )
            return False
        return True
