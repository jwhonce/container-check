import unittest

from systemd import Systemd

from mock import ANY, MagicMock, call, patch


class TestSystemd(unittest.TestCase):
    def setUp(self):
        class Interface(MagicMock):
            def LoadUnit(self, service):
                return 'unit'

            def GetAll(self, unit):
                return {'UnitFileState': 'enabled', 'ActiveState': 'active'}

        patcher = patch(
            'dbus.bus.BusConnection.get_object',
            autospec=True,
            side_effect=['systemd', 'proxy'])
        self.MockBusConnection = patcher.start()
        self.addCleanup(patcher.stop)

        patcher = patch(
            'dbus.Interface', autospec=True, return_value=Interface())
        self.MockInterface = patcher.start()
        self.addCleanup(patcher.stop)
        pass

    def tearDown(self):
        pass

    def test_constr(self):
        systemd = Systemd('/mock')

        calls = [call(ANY, 'org.freedesktop.systemd1', 'unit')]
        self.MockBusConnection.assert_has_calls(calls)

        self.assertTrue(systemd.isenabled)
        self.assertTrue(systemd.isactive)
        self.assertEqual(len(systemd), 2)
        with self.assertRaises(KeyError):
            systemd.get('Mocked')
