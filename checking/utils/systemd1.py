import threading

import dbus


class Systemd1Error(Exception):
    """Raise exception on systemd1 dbus errors"""


class Systemd1(object):
    """Provide wrapper classes and methods for DBus Systemd1 API"""

    def __init__(self, service, prefix='/host'):
        self._lock = threading.Lock()
        self._service = service

        # No duplicate separators allowed in debus path
        path = '/'.join(
            t.strip('/')
            for t in ['unix:path=', prefix, '/var/run/dbus/system_bus_socket']
        )
        bus = dbus.bus.BusConnection(path)

        systemd1 = bus.get_object(
            'org.freedesktop.systemd1', '/org/freedesktop/systemd1'
        )
        manager = dbus.Interface(systemd1, 'org.freedesktop.systemd1.Manager')
        unit = manager.LoadUnit(service)
        proxy = bus.get_object('org.freedesktop.systemd1', str(unit))
        self._interface = dbus.Interface(
            proxy, dbus_interface='org.freedesktop.DBus.Properties'
        )
        self._properties = None

    def isenabled(self):
        return self.get('UnitFileState') == 'enabled'

    def isactive(self):
        return self.get('ActiveState') == 'active'

    def get(self, key):
        return self.__getitem__(key)

    def __getitem__(self, key):
        self._load_properties()
        return str(self._properties[key])

    def __len__(self):
        self._load_properties()
        return len(self._properties)

    def _load_properties(self):
        with self._lock:
            if self._properties:
                return

            self._properties = self._interface.GetAll(
                'org.freedesktop.systemd1.Unit'
            )
