import os


class Pathname(str):
    """Manipulate path relative to container and host"""

    def __new__(cls, path, prefix='/host'):
        if isinstance(path, basestring):
            relpath = path
        else:
            elements = [path[0]]
            elements.extend(map(lambda e: e.strip(os.sep), path[1:]))
            # now it's "safe" to join all the path elements
            relpath = os.path.join(*elements)

        abspath = os.path.join(prefix,
                               relpath.strip(os.sep)) if prefix else relpath

        obj = super(Pathname, cls).__new__(cls, abspath)
        obj._relpath = relpath
        obj._prefix = prefix
        return obj

    @property
    def relpath(self):
        return self._relpath

    @property
    def abspath(self):
        return self

    @property
    def prefix(self):
        return self._prefix
