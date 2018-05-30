import os

from .pathname import Pathname


class Kmod(object):
    """Manager for kernel modules."""

    def __init__(self, prefix='/host'):
        """Construct manager for kernel modules."""
        self._modules_path = Pathname('/proc/modules', prefix=prefix)

    def is_present(self, name):
        """Check if module is present."""
        with open(self._modules_path) as modules:
            module_name = name.replace('-', '_') + ' '
            for line in modules:
                if line.startswith(module_name):
                    return True
            else:
                return False
