"""Helper Classes for python checks"""

import re
import subprocess
import sys

from .audit import Audit
from .checked import Checked
from .pathname import Pathname
from .rpm import Rpm
from .selinux import Selinux
from .systemd import Systemd

__all__ = [
    'Audit',
    'Checked',
    'Pathname',
    'Rpm',
    'Selinux',
    'Systemd',
]


def resolve_config(path):
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


def strip_config(path):
    """Return lines stripped of comments from configuration file"""
    lines = []
    try:
        with open(path, 'r') as f:
            data = f.readlines()
    except IOError as e:
        sys.stderr.write(e.message + '\n')

    for line in data:
        lo = re.sub('^ *#.*', '', line.strip())
        if len(lo) > 0:
            lines.append(lo)
    return lines


def log_error(msg):
    """Helper to log error text"""
    sys.stderr.write(str(msg) + '\n')
    sys.stderr.flush()


def log_info(msg):
    """Helper to log informational text"""
    sys.stdout.write(str(msg) + '\n')
