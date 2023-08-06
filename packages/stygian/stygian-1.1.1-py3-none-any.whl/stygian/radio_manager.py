import enum
import functools
import logging

from PySide2 import QtCore

import hyperborea.proxy

logger = logging.getLogger(__name__)


def create_remote(device):
    remote = device.get_remote_device()
    remote.open()
    return remote


@enum.unique
class RadioState(enum.Enum):
        UNINITIALIZED = 0
        DISCONNECTED = 1
        CONNECTING = 2
        CONNECTED = 3
        SCANNING = 4  # not used


class RadioManager(QtCore.QObject):
    def __init__(self, start_usb_operation, device_recorder, dispatcher):
        super().__init__(device_recorder)

        self.start_usb_operation = start_usb_operation
        self.device_recorder = device_recorder
        self.dispatcher = dispatcher

        self.state = RadioState.UNINITIALIZED

        self.default_serial = None

        self.remote_recorder = None

        self.setup_callbacks()
        self.setup_usb_operations()

    def setup_callbacks(self):
        self.connect_check_timer = QtCore.QTimer(self)
        self.connect_check_timer.timeout.connect(self.connect_check_timer_cb)

    def setup_usb_operations(self):
        self.stop_op = hyperborea.proxy.SimpleDeviceOperation("stop_radio")

        self.connect_radio_op = hyperborea.proxy.SimpleDeviceOperation(
            "connect_radio")
        self.connect_radio_op.completed.connect(self.connect_radio_cb)
        self.get_status_op = hyperborea.proxy.SimpleDeviceOperation(
            "get_radio_status")
        self.get_status_op.completed.connect(self.get_status_cb)

    def go_to_disconnected_state(self):
        # no device is connected; not scanning; may have scan results
        self.state = RadioState.DISCONNECTED

        self.device_recorder.rgb_remote_disconnected()

    def go_to_connecting_state(self):
        # trying to connect to a device
        self.state = RadioState.CONNECTING

        self.device_recorder.rgb_remote_disconnected()

    def go_to_connected_state(self):
        # device is connected
        self.state = RadioState.CONNECTED

        self.device_recorder.rgb_remote_connected()

    def connected(self, device_info):
        # the device has been reconnected
        self.go_to_disconnected_state()
        self.default_serial = device_info['radio_default_serial'] & 0xFFFFFFFF

        if self.default_serial:
            self.start_usb_operation(self.connect_radio_op,
                                     self.default_serial)
            self.go_to_connecting_state()

    def disconnected(self):
        # the device has been disconnected (e.g. unplugged)
        self.state = RadioState.UNINITIALIZED

        self.connect_check_timer.stop()

        if self.remote_recorder:
            self.remote_recorder.stop_and_close()
            self.remote_recorder = None

    def stop(self):
        if self.remote_recorder:
            self.remote_recorder.stop_and_close()
            self.remote_recorder = None
        self.default_serial = None
        self.start_usb_operation(self.stop_op)

    def connect_radio_cb(self):
        # immediately check the connected status
        self.connect_check_timer_cb()

    def connect_check_timer_cb(self):
        self.connect_check_timer.stop()  # will be restarted if necessary
        if self.state in (RadioState.CONNECTED, RadioState.CONNECTING):
            self.start_usb_operation(self.get_status_op)

    def get_status_cb(self, status):
        connected = status[0]
        if connected:
            self.device_recorder.rgb_remote_connected()

            subproxy = self.device_recorder.proxy.create_subproxy(
                create_remote)
            cb = functools.partial(self.subproxy_connected_cb, subproxy)
            subproxy.connected.connect(cb)
            subproxy.disconnected.connect(self.reconnect)
            subproxy.open_connection()
        elif status[1] == 0:
            # disconnected immediately; go straight to reconnect
            if self.state in (RadioState.CONNECTED, RadioState.CONNECTING):
                self.reconnect()
        else:
            self.connect_check_timer.start(250)  # 0.25 seconds

    def subproxy_connected_cb(self, subproxy):
        if self.state in (RadioState.CONNECTED, RadioState.CONNECTING):
            get_sn_op = hyperborea.proxy.SimpleDeviceOperation(
                "get_serial_number")
            cb = functools.partial(self.get_sn_cb, subproxy)
            get_sn_op.completed.connect(cb)
            subproxy.send_job(get_sn_op)
        else:
            subproxy.disconnected.disconnect(self.reconnect)
            subproxy.close_connection()

    def get_sn_cb(self, subproxy, serial):
        if self.state not in (RadioState.CONNECTED, RadioState.CONNECTING):
            subproxy.close_connection()
            return

        if self.remote_recorder:
            self.remote_recorder.set_proxy(subproxy)
            self.go_to_connected_state()
        else:
            self.remote_recorder = self.dispatcher.create_recorder(
                subproxy, serial)

            self.go_to_connected_state()

    def reconnect(self):
        if self.default_serial:
            if self.state in (RadioState.CONNECTED, RadioState.CONNECTING):
                self.start_usb_operation(self.connect_radio_op,
                                         self.default_serial)
                self.go_to_connecting_state()
