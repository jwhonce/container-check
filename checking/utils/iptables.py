"""Model of IPTables rules."""
from __future__ import print_function

import collections
import re
import subprocess

try:
    from functools import lru_cache
except ImportError:
    from backports.functools_lru_cache import lru_cache


class ReMemoize(object):
    """Class to memoize a re.search or re.match."""

    def __init__(self):
        """Construct memoizer."""
        self.last_match = None
        self._patterns = {}

    def match(self, pattern, text):
        """Match pattern against text."""
        cre = self._patterns.get(pattern, re.compile(pattern))
        self.last_match = cre.match(text)

        self._patterns[pattern] = cre
        return self.last_match

    def search(self, pattern, text):
        """Search text for pattern."""
        cre = self._patterns.get(pattern, re.compile(pattern))
        self.last_match = cre.search(text)

        self._patterns[pattern] = cre
        return self.last_match

    def group(self, index):
        """Return matched group index."""
        return self.last_match.group(index)


Chain = collections.namedtuple('Chain', 'name policy references rules')
Rule = collections.namedtuple('Rule', (
    'target',
    'protocol',
    'option',
    'in_',
    'out_',
    'source',
    'destination',
    'state',
))


class IPTables(object):
    """Model for IPTables."""

    def __init__(self):
        """Construct IPTables model."""
        self._output = subprocess.check_output((
            '/sbin/iptables',
            '--verbose',
            '--list',
            '--numeric',
        ))

    @property
    @lru_cache(maxsize=2)
    def table(self):
        """Return all iptables tables."""
        _re = ReMemoize()

        key = None
        table = collections.OrderedDict()
        for line in self._output.split('\n'):
            if not line:
                # skip blank lines
                continue
            elif _re.match(r'\spkts\sbytes\starget', line):
                # skip headers
                continue
            elif _re.match(r'Chain ([^\s]+) \(policy (\w+).*\)', line):
                # Save Chain with policy
                key = _re.group(1)
                table[key] = Chain(key, _re.group(2), None, list())
            elif _re.match(r'Chain ([^\s]+) \((\d+) references\)', line):
                # Save Chain with reference
                key = _re.group(1)
                table[key] = Chain(key, None, _re.group(2), list())
            else:
                # Save rule under last Chain
                fields = line.split(None, 9)[2:]
                fields.extend([None] * (8 - len(fields)))
                table[key].rules.append(Rule(*fields))
        return table
