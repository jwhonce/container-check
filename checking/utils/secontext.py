import errno
import os
import stat

import selinux


class SeContextError(OSError):
    """Report Selinux Context Error"""

    def __init__(self, errno, strerror, path):
        super(SeContextError, self).__init__(errno, strerror, path)


class SeContext(object):
    """Helpers for SeLinux bindings"""

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
            raise SeContextError(int(status), os.strerror(int(status)), path)

        try:
            _, actual = selinux.lgetfilecon(cooked)
        except OSError as e:
            if e.errno != errno.ENODATA:
                raise SeContextError(e.errno, os.strerror(int(e.errno)), path)
            actual = None

        if expected != actual:
            raise SeContextError(
                errno.EINVAL,
                "Incorrect context: actual({}) expected({})".format(
                    actual, expected
                ), path
            )
