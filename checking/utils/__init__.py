"""Helper Classes for python checks"""

import subprocess
import sys

from .audit import Audit
from .pathname import Pathname
from .rpm import Rpm, RpmError
from .selinux import Selinux, SelinuxError
from .systemd import Systemd

__all__ = [
    'Audit',
    'Pathname',
    'Rpm',
    'RpmError',
    'Selinux',
    'SelinuxError',
    'Systemd',
]


def read_config(path):
    """Return options from shell formatted configuration file"""
    try:
        cmd = 'set -o allexport; . {}; env'.format(path)
        out = subprocess.check_output(cmd, shell=True)
    except (subprocess.CalledProcessError, OSError) as e:
        sys.stderr.write(e.message + '\n')
        return {}
    else:
        return {
            k: v
            for k, v in
            (x.split('=', 1) for x in out.splitlines() if '=' in x)
        }


def log_error(msg):
    """Helper to log error text"""
    sys.stderr.write(str(msg) + '\n')
    sys.stderr.flush()


def log_info(msg):
    """Helper to log informational text"""
    sys.stdout.write(str(msg) + '\n')
