"""Model for kernel modules API."""
from backports.functools_lru_cache import lru_cache

from .pathname import Pathname


class Kmod(object):
    """Manager for kernel modules."""

    def __init__(self, name, prefix='/host'):
        """Construct manager for kernel modules."""
        self.modules_path = Pathname('/proc/modules', prefix=prefix)
        self.name = name

    @property
    @lru_cache(maxsize=2)
    def ispresent(self):
        """Check if module is present."""
        with open(self.modules_path) as modules:
            module_name = self.name.replace('-', '_') + ' '
            for line in modules.readline():
                if line.startswith(module_name):
                    return True
            else:
                return False
