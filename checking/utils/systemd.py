import threading

import dbus


class Systemd(object):
    """Provide wrapper classes and methods for DBus Systemd1 API."""

    def __init__(self, service, prefix='/host'):
        """Construct manager."""
        self._lock = threading.Lock()
        self._service = service
        self._properties = None

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
    def isenabled(self):
        """Service been enabled."""
        return self.get('UnitFileState') == 'enabled'

    @property
    def isactive(self):
        """Service been started."""
        return self.get('ActiveState') == 'active'

    def get(self, key, default=None):
        """Retrieve value for Services' key from Systemd."""
        return self.__getitem__(key, default)

    def __getitem__(self, key, default=None):
        self._load_properties()
        try:
            return self._properties[key]
        except KeyError:
            if default:
                return default
            raise

    def __len__(self):
        self._load_properties()
        return len(self._properties)

    def _load_properties(self):
        with self._lock:
            if self._properties:
                return

            self._properties = self._interface.GetAll(
                'org.freedesktop.systemd1.Unit')
