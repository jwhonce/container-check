"""Model for Systemd support."""
import dbus

try:
    from functools import lru_cache
except ImportError:
    from backports.functools_lru_cache import lru_cache


class Systemd(object):
    """Provide wrapper classes and methods for DBus Systemd1 API."""

    def __init__(self, service, prefix='/host'):
        """Construct manager."""
        self._service = service

        # No duplicate separators allowed in dbus path
        path = '/'.join(
            t.strip('/')
            for t in ('unix:path=', prefix, '/var/run/dbus/system_bus_socket'))
        bus = dbus.bus.BusConnection(path)

        systemd = bus.get_object('org.freedesktop.systemd1',
                                 '/org/freedesktop/systemd1')
        manager = dbus.Interface(systemd, 'org.freedesktop.systemd1.Manager')
        unit = manager.LoadUnit(service)
        proxy = bus.get_object('org.freedesktop.systemd1', str(unit))
        self._interface = dbus.Interface(
            proxy, dbus_interface='org.freedesktop.DBus.Properties')

    @property
    @lru_cache(maxsize=1)
    def unit(self):
        """Get unit properties."""
        return self._interface.GetAll('org.freedesktop.systemd1.Unit')

    @property
    @lru_cache(maxsize=1)
    def service(self):
        """Get service propties."""
        return self._interface.GetAll('org.freedesktop.systemd1.Service')

    @property
    def isenabled(self):
        """Service been enabled."""
        return self.unit.get('UnitFileState') == 'enabled'

    @property
    def isactive(self):
        """Service been started."""
        return self.unit.get('ActiveState') == 'active'

    @classmethod
    def map_exec(cls, obj):
        """Map Exec* records to dictionary.

        TODO: Make this happen automatically.
        """
        if not obj:
            return {}

        zipped = zip((
            'binary',
            'args',
            'is_unclean_exit_failure',
            'began_realtime',
            'finished_realtime',
            'began_monotonic',
            'finished_monotonic',
            'pid',
            'returncode',
            'status',
        ), obj[0])
        return dict(zipped)
