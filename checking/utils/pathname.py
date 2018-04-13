import os


class Pathname(str):
    """Manipulate path relative to container and host"""

    def __new__(cls, path, prefix='/host'):
        elements = [prefix] if prefix else []

        if isinstance(path, (list, tuple)):
            elements.extend(map(lambda e: e.strip(os.sep), path))
        else:
            elements.append(path.strip(os.sep))
        # now it's "safe" to join all the path elements
        full = os.path.join(*elements)

        obj = super(Pathname, cls).__new__(cls, full)
        obj._path = path
        obj._prefix = prefix
        return obj

    @property
    def relpath(self):
        return self._path

    @property
    def abspath(self):
        return self

    @property
    def prefix(self):
        return self._prefix
