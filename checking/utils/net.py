"""Model for /proc/net/tcp? interface."""
from __future__ import absolute_import

import collections
import fileinput
import socket
import struct
from contextlib import closing

from .pathname import Pathname


class Net(object):
    """Class for TCP statistics."""

    STATE_ESTABLISHED = '01'
    STATE_SYNC_SENT = '02'
    STATE_SYNC_RECV = '03'
    STATE_FIN_WAIT1 = '04'
    STATE_FIN_WAIT2 = '05'
    STATE_TIME_WAIT = '06'
    STATE_CLOSE = '07'
    STATE_CLOSE_WAIT = '08'
    STATE_LAST_ACK = '09'
    STATE_LISTEN = '0A'
    STATE_CLOSING = '0B'

    # See https://www.kernel.org/doc/Documentation/networking/proc_net_tcp.txt
    Connection = collections.namedtuple('Connection', [
        'slot',
        'local_address',
        'remote_address',
        'state',
        'tx_queue',
        'rx_queue',
        'timer_active',
        'tm_when',
        'rto_timeouts',
        'uid',
        'probe_timeouts',
        'inode',
        'reference_count',
        'socket_location',
        'retrans_timeouts',
        'tick',
        'pingpong',
        'tx_congestion',
        'slowstart_threshold',
    ])

    class EndPoint(collections.namedtuple('EndPoint', 'address port family')):
        """Class to hold address, port and socket family."""

        def __repr__(self):
            """Format EndPoint as expected."""
            if self.family == socket.AF_INET:
                return '{}:{}'.format(self.address, self.port)
            elif self.family == socket.AF_INET6:
                return '[{}]:{}'.format(self.address, self.port)
            else:
                return super().__repr__()

    def __init__(self, prefix='/host'):
        """Construct net model."""
        self.tcp4 = Pathname('/proc/net/tcp', prefix=prefix)
        self.tcp6 = Pathname('/proc/net/tcp6', prefix=prefix)

    def _fmt_ip(self, end_point):
        addr, port = end_point.split(':')
        if len(addr) > 8:
            addr = addr.decode('hex')
            addr = struct.unpack('>IIII', addr)
            addr = struct.pack('@IIII', *addr)
            addr = socket.inet_ntop(socket.AF_INET6, addr)
            return Net.EndPoint(addr, int(port, base=16), socket.AF_INET6)
        else:
            return Net.EndPoint(
                socket.inet_ntop(socket.AF_INET,
                                 struct.pack('<I', int(addr, base=16))),
                int(port, base=16), socket.AF_INET)

    def match_state(self, state):
        """Filter network connections for given state."""
        lines = []
        with closing(fileinput.input([self.tcp4, self.tcp6])) as fd:
            for line in fd:
                if fd.isfirstline():
                    continue
                lines.append(line)

        for line in lines:
            raw = line.split()
            if raw[3] == state:
                # See Conntection definition above for fields.
                cooked = list(raw[0][:-1])
                cooked.append(self._fmt_ip(raw[1]))
                cooked.append(self._fmt_ip(raw[2]))
                cooked.append(raw[3])
                cooked.extend(raw[4].split(':'))
                cooked.extend(raw[5].split(':'))
                cooked.extend(raw[6:17])
                yield Net.Connection(*cooked)
            else:
                continue
