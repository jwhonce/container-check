import os


class Pathname(str):
    """Manipulate path relative to container and host"""

    def __new__(cls, path, prefix='/host'):
        elements = [prefix] if prefix else []

        if isinstance(path, (list, tuple)):
            elements.expand(list(path))
        else:
            elements.append(path)
        full = os.sep.join(elements)

        o = super(Pathname, cls).__new__(cls, full)
        o._path = path
        o._prefix = prefix
        return o

    @property
    def relpath(self):
        return self._path

    @property
    def abspath(self):
        return self

    @property
    def prefix(self):
        return self._prefix
