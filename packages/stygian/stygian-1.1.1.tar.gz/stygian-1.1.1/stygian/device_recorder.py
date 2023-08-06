import logging
import multiprocessing
import threading

from PySide2 import QtCore

import asphodel
import hyperborea.device_info
from hyperborea.preferences import read_bool_setting
import hyperborea.proxy
import hyperborea.stream

from .radio_manager import RadioManager

logger = logging.getLogger(__name__)


class DeviceRecorder(QtCore.QObject):
    status_received = QtCore.Signal(object)

    def __init__(self, serial_number, base_dir, dispatcher,
                 upload_manager=None):
        super().__init__()

        self.stream_list = True  # NOTE: True means activate all streams

        self.settings = QtCore.QSettings()
        self.auto_rgb = read_bool_setting(self.settings, "AutoRGB", True)

        self.proxy = None
        self.device_info = None
        self.dispatcher = dispatcher
        self.serial_number = serial_number
        self.base_dir = base_dir

        self.radio_manager = None

        self.upload_manager = upload_manager

        self.streaming = False
        self.streaming_stopped = threading.Event()
        self.status_thread = None

        self.setup_logging()
        self.setup_callbacks()
        self.setup_usb_operations()

    def setup_logging(self):
        self.logger = hyperborea.proxy.DeviceLoggerAdapter(logger,
                                                           self.serial_number)

    def setup_callbacks(self):
        self.status_received.connect(self.status_callback)

        app = QtCore.QCoreApplication.instance()
        app.aboutToQuit.connect(self.stop_and_close)

    def setup_usb_operations(self):
        self.get_initial_info_op = hyperborea.proxy.DeviceOperation(
            hyperborea.device_info.get_initial_info)
        self.get_initial_info_op.completed.connect(self.initial_info_cb)
        self.get_reconnect_info_op = hyperborea.proxy.DeviceOperation(
            hyperborea.device_info.get_reconnect_info)
        self.get_reconnect_info_op.completed.connect(self.reconnect_info_cb)
        self.set_rgb_op = hyperborea.proxy.SimpleDeviceOperation(
            "set_rgb_values")

        self.start_streaming_op = hyperborea.proxy.DeviceOperation(
            hyperborea.stream.start_streaming)
        self.stop_streaming_op = hyperborea.proxy.DeviceOperation(
            hyperborea.stream.stop_streaming)
        self.stop_streaming_op.completed.connect(self.stop_streaming_cb)
        self.stop_streaming_op.error.connect(self.stop_streaming_cb)
        self.close_device_op = hyperborea.proxy.SimpleDeviceOperation("close")

    def start_usb_operation(self, operation, *args, **kwargs):
        if not self.proxy:
            self.logger.error("called start_usb_operation with no proxy")
            return
        self.proxy.send_job(operation, *args, **kwargs)

    def proxy_disconnect_cb(self):
        self.logger.info("Disconnected")
        self.proxy = None

        if self.radio_manager:
            self.radio_manager.disconnected()

        self.streaming = False
        self.streaming_stopped.set()

    def set_proxy(self, proxy):
        self.proxy = proxy
        self.proxy.disconnected.connect(self.proxy_disconnect_cb)

        self.logger.info("Connecting...")

        self.connect_stopped = False
        if not self.device_info:
            self.start_usb_operation(self.get_initial_info_op)
        else:
            self.start_usb_operation(self.get_reconnect_info_op)

    def initial_info_cb(self, info):
        if not info:
            # error while getting initial info
            if self.proxy:
                self.proxy.close_connection()
            return

        self.device_info = info

        if info['user_tag_1']:
            self.display_name = info['user_tag_1']
        else:
            # fall back to serial number
            self.display_name = self.serial_number

        if info['supports_radio']:
            self.radio_manager = RadioManager(self.start_usb_operation, self,
                                              self.dispatcher)

        self.rgb_connected()

        self.logger.info("Starting streaming...")

        self.start_streaming(info['streams'])

    def reconnect_info_cb(self, info):
        if not info:
            # error while getting reconnect info
            if self.proxy:
                self.proxy.close_connection()
            return

        self.device_info.update(info)

        self.rgb_connected()

        self.logger.debug("Starting streaming...")

        self.start_streaming(self.device_info['streams'])

    def stop_and_close(self):
        self.rgb_disconnected()

        self.stop_streaming()

        if self.radio_manager:
            self.radio_manager.stop()

        self.start_usb_operation(self.close_device_op)

        if self.proxy:
            self.proxy.close_connection()

    def status_callback(self, status):
        if (status.startswith("error")):
            self.logger.error("Error in status: {}".format(status))
            self.stop_and_close()
            if self.radio_manager:
                self.radio_manager.disconnected()
        elif (status == "connected"):
            self.logger.info("Connected")
            self.rgb_streaming()
            if self.radio_manager:
                self.radio_manager.connected(self.device_info)
        else:
            self.logger.info("Status: {}".format(status))

    def status_thread_run(self):
        pipe = self.status_rx_pipe
        try:
            while True:
                # check if should exit
                if self.streaming_stopped.is_set():
                    break

                if pipe.poll(0.1):  # 100 ms
                    try:
                        data = pipe.recv()
                    except EOFError:
                        break

                    # send the data to status_callback()
                    self.status_received.emit(data)
        finally:
            self.status_rx_pipe.close()
            self.status_tx_pipe.close()

    def start_streaming(self, streams):
        if self.streaming:
            raise AssertionError("Already Streaming")

        compression_level = self.settings.value("CompressionLevel")
        if compression_level is not None:
            try:
                compression_level = int(compression_level)
            except:
                compression_level = None  # default

        if self.stream_list is True:
            indexes = list(range(len(streams)))
        else:
            indexes = [i for i in self.stream_list if i < len(streams)]

        if len(indexes) == 0:
            # No streams: can't start streaming
            self.logger.info("Connected")
            self.rgb_streaming()
            if self.radio_manager:
                self.radio_manager.connected(self.device_info)
            return

        warm_up_time = 0.0
        for stream in streams:
            if stream.warm_up_delay > warm_up_time:
                warm_up_time = stream.warm_up_delay

        active_streams = [s for i, s in enumerate(streams) if i in indexes]

        stream_counts = asphodel.nativelib.get_streaming_counts(
            active_streams, response_time=0.05, buffer_time=0.5, timeout=1000)

        header_dict = self.device_info.copy()
        header_dict['stream_counts'] = stream_counts
        header_dict['streams_to_activate'] = indexes
        header_dict['warm_up_time'] = warm_up_time

        self.streaming = True
        self.streaming_stopped.clear()

        rx, tx = multiprocessing.Pipe(False)
        self.status_rx_pipe = rx
        self.status_tx_pipe = tx
        self.status_thread = threading.Thread(target=self.status_thread_run)
        self.status_thread.start()

        if self.upload_manager is not None:
            rx, tx = multiprocessing.Pipe(False)
            self.upload_rx_pipe = rx
            self.upload_tx_pipe = tx
            self.upload_manager.register_upload_pipe(self.upload_rx_pipe)
        else:
            self.upload_tx_pipe = None

        self.start_usb_operation(
            self.start_streaming_op, indexes, warm_up_time, stream_counts,
            header_dict, None, self.status_tx_pipe, self.display_name,
            self.base_dir, False, compression_level, self.upload_tx_pipe)

    def stop_streaming(self):
        if self.streaming:
            self.start_usb_operation(self.stop_streaming_op)
            self.streaming = False

    def stop_streaming_cb(self):
        # can't stop the threads until the stop_streaming_op has finished
        self.streaming_stopped.set()
        if self.status_thread:
            self.status_thread.join()

    def rgb_set(self, color):
        if self.device_info is not None and self.auto_rgb:
            if len(self.device_info['rgb_settings']) > 0:
                self.start_usb_operation(self.set_rgb_op, 0, color)

    def rgb_connected(self):
        if self.device_info is not None:
            if self.device_info['supports_radio']:
                self.rgb_set((0, 255, 255))  # cyan
            else:
                self.rgb_set((0, 0, 255))  # blue

    def rgb_disconnected(self):
        self.rgb_set((255, 0, 0))  # red

    def rgb_streaming(self):
        if self.device_info is not None:
            if self.device_info['supports_radio']:
                pass
            else:
                self.rgb_set((0, 255, 0))  # green

    def rgb_remote_connected(self):
        self.rgb_set((0, 0, 255))  # blue

    def rgb_remote_disconnected(self):
        self.rgb_set((0, 255, 255))  # cyan

    def rgb_remote_streaming(self):
        self.rgb_set((0, 255, 0))  # green
