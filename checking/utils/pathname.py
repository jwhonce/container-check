import os


class Pathname(str):
    """Manipulate path relative to container and host."""

    MOUNT_PREFIX = '/host'

    def __new__(cls, path, **kwargs):
        """Allocate new Pathname object."""
        default = os.environ.get('MOUNT_PREFIX', Pathname.MOUNT_PREFIX)
        prefix = kwargs.get('prefix', default)

        relpath = Pathname.join(path) if hasattr(path, '__iter__') else path
        abspath = Pathname.join((prefix, relpath)) if prefix else relpath

        obj = super(Pathname, cls).__new__(cls, abspath)
        obj._relpath = relpath
        obj._prefix = prefix
        return obj

    @property
    def relpath(self):
        """Pathname relative to container."""
        return self._relpath

    @property
    def abspath(self):
        """Pathname relative to the host."""
        return self

    @property
    def prefix(self):
        """Prefix of host mount points."""
        return self._prefix

    @classmethod
    def join(cls, arg):
        """Join path elements and normalize path."""
        return os.path.normpath(os.sep.join(arg))
