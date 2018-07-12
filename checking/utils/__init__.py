"""Helper Classes for python checks."""
from __future__ import print_function

import fileinput
import os
import re
import subprocess
import sys
from contextlib import closing

from .audit import Audit
from .checked import Checked
from .iptables import IPTables
from .kmod import Kmod
from .net import Net
from .pathname import Pathname
from .rpm import Rpm
from .selinux import Selinux
from .systemd import Systemd

try:
    basestring
except NameError:
    basestring = str

__all__ = [
    'Audit',
    'Checked',
    'IPTables',
    'Kmod'
    'Net',
    'Pathname',
    'Rpm',
    'Selinux',
    'Systemd',
]


def resolve_config(path):
    """Return options from shell formatted configuration file."""
    # TODO: Can augeas Shellvar lens do this instead?
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
        re_comment = re.compile(r'\s*#.*$')
        with open(path, 'r') as f:
            for line in f:
                cooked = line.rstrip()
                cooked = re_comment('', line)
                if len(cooked):
                    yield cooked
    except IOError as e:
        sys.stderr.write(e.message + '\n')


def grep(pattern, path):
    """Search file(s) for pattern."""
    paths = path if not isinstance(path, basestring) else [path]

    re_comment = re.compile(r'\s*#.*$')
    _re = pattern if hasattr(pattern, 'search') else re.compile(pattern)
    with closing(fileinput.input(paths)) as fd:
        for line in fd:
            cooked = line.rstrip()
            cooked = re_comment.sub('', cooked)
            if _re.search(cooked):
                yield cooked


def find_files(*args):
    """Build list of files from args.

    Silently ignore missing filesystem path(s).
    """
    for entry in args:
        if os.path.isfile(entry):
            yield entry
        elif os.path.isdir(entry):
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
