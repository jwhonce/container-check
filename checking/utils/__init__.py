"""Helper Classes for python checks."""

import os
import re
import subprocess
import sys

from .audit import Audit
from .checked import Checked
from .kmod import Kmod
from .pathname import Pathname
from .rpm import Rpm
from .selinux import Selinux
from .systemd import Systemd

__all__ = [
    'Audit',
    'Checked',
    'Kmod'
    'Pathname',
    'Rpm',
    'Selinux',
    'Systemd',
]


def resolve_config(path):
    """Return options from shell formatted configuration file."""
    try:
        cmd = 'set -o allexport; . {} >&/dev/null; env'.format(path)
        out = subprocess.check_output(cmd, close_fds=True, shell=True, env={})
    except subprocess.CalledProcessError:
        env = {}
    else:
        env = {
            k: v
            for k, v in (x.split('=', 1) for x in out.splitlines() if '=' in x)
        }
        for k in ('SHLVL', 'PWD', '_'):
            env.pop(k, None)
    finally:
        return env


def strip_config(path):
    """Return lines stripped of comments from configuration file."""
    try:
        with open(path, 'r') as f:
            for line in f.readline():
                cooked = re.sub(r'#.*$', '', line.strip())
                if len(cooked) > 0:
                    yield cooked
    except IOError as e:
        sys.stderr.write(e.message + '\n')


def grep(pattern, path):
    """Search file for pattern."""
    _re = pattern if hasattr(pattern, 'search') else re.compile(pattern)
    for line in strip_config(path):
        if _re.search(line):
            yield line


def find_files(*args):
    for entry in args:
        if os.path.isfile(entry):
            yield entry
        else:
            for d, _, files in os.walk(entry):
                for f in files:
                    yield os.path.join(d, f)


def log_error(msg):  # pragma: no cover
    """Log error text."""
    sys.stderr.write(str(msg) + '\n')
    sys.stderr.flush()


def log_info(msg):  # pragma: no cover
    """Log informational text."""
    sys.stdout.write(str(msg) + '\n')
