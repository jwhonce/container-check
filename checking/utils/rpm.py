import errno
import subprocess


class RpmError(OSError):
    """Report RPM Error"""

    def __init__(self, errno, strerror, path):
        super(RpmError, self).__init__(errno, strerror, path)


not_found = 'Package "{}" is not installed/found on host\n'
not_valid = 'Files in package "{}" failed validation:\n{}'


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
            cmd = ['rpm', '--verify']
            if prefix:
                cmd += ['--root', prefix]
            cmd.append(name)

            subprocess.check_output(cmd, close_fds=True)
            return name
        except subprocess.CalledProcessError as e:
            if e.output.find('is not installed') >= 0:
                raise RpmError(errno.ENOENT, not_found.format(name), name)
            raise RpmError(
                errno.EINVAL, not_valid.format(name, e.output), name
            )

    @classmethod
    def nvr(cls, name, prefix='/host'):
        try:
            cmd = ['rpm', '--query']
            if prefix:
                cmd += ['--root', prefix]
            cmd.append(name)

            return subprocess.check_output(cmd, close_fds=True).strip()
        except subprocess.CalledProcessError as e:
            if e.output.find('is not installed') >= 0:
                raise RpmError(errno.ENOENT, not_found.format(name), name)

            raise RpmError(
                errno.EINVAL, not_valid.format(name, e.output), name
            )
