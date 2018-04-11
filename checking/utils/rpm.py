import copy
import errno
import subprocess


class RpmError(OSError):
    """Report RPM Error"""
    pass


class Rpm(object):
    """ Helper for rpm commands"""
    not_found = 'Package "{}" is not installed/found on host'
    not_valid = 'Files in package "{}" failed validation:\n{}'

    def __init__(self, name, prefix='/host'):
        self._name = name
        self._prefix = prefix

    def _query(self, command):
        try:
            return subprocess.check_output(command, close_fds=True).strip()
        except subprocess.CalledProcessError as e:
            if e.output.find('is not installed') >= 0:
                raise RpmError(
                    errno.ENOENT, Rpm.not_found.format(self._name), self._name
                )
            raise RpmError(
                errno.EINVAL,
                Rpm.not_valid.format(self._name, e.output.strip()), self._name
            )

    def _build_command(self, command):
        c = copy.deepcopy(command)
        if self._prefix:
            c.extend(['--root', self._prefix])
        c.append(self._name)
        return c

    def verify(self):
        """Verify files against rpm database, See rpm manpage."""
        c = self._build_command(['rpm', '--verify'])
        self._query(c)
        return True

    @property
    def files(self):
        """Obtain files  for package"""
        c = self._build_command(['rpm', '--query', '--list'])
        o = self._query(c)
        return o.strip().splitlines()

    @property
    def nvr(self):
        """Obtain (name, version, release) for package"""
        c = self._build_command(['rpm', '--query'])
        return self._query(c)
