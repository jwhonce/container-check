import errno
import subprocess


class RpmError(OSError):
    """Report RPM Error"""

    def __init__(self, errno, strerror, path):
        super(RpmError, self).__init__(errno, strerror, path)


not_found = '{} is not installed/found on host\n'
not_valid = 'Files in package {} failed validation:\n{}'


class Rpm(object):
    """ Helper for rpm commands"""

    @classmethod
    def verify(cls, name, prefix='/host'):
        """Verify files against rpm database, these attributes:
           - Owner
           - Group
           - Mode
           - MD5 Checksum
           - Size
           - Major/Minor Number
           - Symbolic Link String
           - Modification Time
        """
        try:
            subprocess.check_output(
                ['rpm', '--verify', '--root', prefix, name], close_fds=True
            )
            return None, name
        except subprocess.CalledProcessError as e:
            if e.output.find('is not installed') >= 0:
                raise RpmError(errno.ENOENT, not_found.format(name), name)

            msg = ''.join('  ' + line for line in e.output.splitlines(True))
            raise RpmError(errno.EINVAL, not_valid.format(name, msg), name)

    @classmethod
    def name(cls, name, prefix='/host'):
        try:
            output = subprocess.check_output(
                ['rpm', '--query', '--root', prefix, name], close_fds=True
            )
            return None, output.strip()
        except subprocess.CalledProcessError as e:
            if e.output.find('is not installed') >= 0:
                raise RpmError(errno.ENOENT, not_found.format(name), name)

            raise RpmError(
                errno.EINVAL, not_valid.format(name, e.output), name
            )
