from __future__ import absolute_import

import errno
import os
import stat

import selinux


class SelinuxError(OSError):
    """Report Selinux Context Error"""

    def __init__(self, errno, strerror, path):
        super(SelinuxError, self).__init__(errno, strerror, path)


class Selinux(object):
    """Helpers for SeLinux bindings"""

    @classmethod
    def is_enabled(cls, prefix='/host'):
        cooked = os.sep.join([prefix, 'sys/fs/selinux/enforce'])
        with open(cooked, 'r') as fd:
            return True if fd.read().startswith('1') else False

    @classmethod
    def verify(cls, path, prefix='/host'):
        """
        Verify the selinux context on given path is as expected,
        add prefix if provided
        """

        cooked = os.sep.join([prefix, path])
        try:
            mode = os.lstat(cooked)[stat.ST_MODE]
            status, expected = selinux.matchpathcon(path, mode)
        except OSError:
            cooked = os.path.realpath(os.path.expanduser(cooked))
            try:
                mode = os.lstat(cooked)[stat.ST_MODE]
                status, expected = selinux.matchpathcon(path, mode)
            except OSError as e:
                e.filename = path
                raise e

        if status != 0:
            raise SelinuxError(int(status), os.strerror(int(status)), path)

        try:
            _, actual = selinux.lgetfilecon(cooked)
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
