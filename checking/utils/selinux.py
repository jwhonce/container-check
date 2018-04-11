from __future__ import absolute_import

import errno
import os
import stat

import selinux

from .pathname import Pathname


class SelinuxError(OSError):
    """Report Selinux Context Error"""
    pass


class Selinux(object):
    """Helpers for SeLinux bindings"""

    def __init__(self, prefix='/host'):
        self._prefix = '/host'

    @property
    def isenabled(self):
        path = Pathname('/sys/fs/selinux/enforce', self._prefix)
        with open(path, 'r') as fd:
            return True if fd.read().startswith('1') else False

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
                e.filename = path
                raise e

        if status != 0:
            raise SelinuxError(int(status), os.strerror(int(status)), path)

        try:
            _, actual = selinux.lgetfilecon(fn)
        except OSError as e:
            if e.errno != errno.ENODATA:
                raise SelinuxError(e.errno, os.strerror(int(e.errno)), path)
            actual = None

        if expected != actual:
            raise SelinuxError(
                errno.EINVAL,
                "Incorrect context: actual({}) expected({})".format(
                    actual, expected
                ), path
            )
