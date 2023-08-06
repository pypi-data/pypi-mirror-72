import functools
import logging
import os
import threading

from PySide2 import QtCore

import asphodel
from hyperborea.preferences import read_bool_setting
import hyperborea.upload

from .device_recorder import DeviceRecorder

logger = logging.getLogger(__name__)


def find_and_open_tcp_device(location_string):
    devices = asphodel.find_tcp_devices()
    for device in devices:
        device_location_string = device.get_location_string()
        if device_location_string == location_string:
            device.open()
            return device


def find_and_open_usb_device(location_string):
    devices = asphodel.find_usb_devices()
    for device in devices:
        device_location_string = device.get_location_string()
        if device_location_string == location_string:
            device.open()
            return device


class Dispatcher(QtCore.QObject):
    device_check_finished = QtCore.Signal(object)

    def __init__(self, proxy_manager):
        super().__init__()

        self.settings = QtCore.QSettings()

        self.upload_manager = None  # will be created later, if necessary

        self.load_base_dir()

        self.proxy_manager = proxy_manager
        self.proxy_lock = threading.Lock()  # locks access to self.proxies
        self.proxies = {}  # location string key, proxy value
        self.device_recorders = {}  # serial number key, recorder value
        self.disconnected_recorders = set()

        self.find_all_devices = False  # set in initial_device_connect
        self.finished = threading.Event()
        self.should_scan = threading.Event()

        self.setup_callbacks()

        self.create_upload_manager()

        # schedule the initial connect for the beginning of the main loop
        QtCore.QTimer.singleShot(0, self.initial_device_connect)

    def load_base_dir(self):
        self.base_dir = self.settings.value("BasePath")
        if not self.base_dir:
            documents_path = QtCore.QStandardPaths.writableLocation(
                QtCore.QStandardPaths.DocumentsLocation)
            app_name = QtCore.QCoreApplication.applicationName()
            self.base_dir = os.path.join(documents_path, app_name + " Data")
        logger.info("Output: {}".format(os.path.abspath(self.base_dir)))

    def create_upload_manager(self):
        if self.upload_manager is not None:
            # remove the old one
            self.upload_manager.stop()
            self.upload_manager = None

        self.settings.beginGroup("Upload")
        upload_enabled = read_bool_setting(self.settings, "Enabled", False)
        delete_original = read_bool_setting(self.settings, "DeleteOriginal",
                                            False)
        upload_options = {
            'delete_after_upload': delete_original,
            's3_bucket': self.settings.value("S3Bucket"),
            'key_prefix': self.settings.value("Directory"),
            'access_key_id': self.settings.value("AccessKeyID"),
            'secret_access_key': self.settings.value("SecretAccessKey"),
            'aws_region': self.settings.value("AWSRegion")}
        self.settings.endGroup()

        if upload_enabled:
            try:
                self.upload_manager = hyperborea.upload.UploadManager(
                    self.base_dir, **upload_options)
            except:
                msg = "Error starting uploader. Check upload configuration."
                logger.exception(msg)
                return

    def setup_callbacks(self):
        self.device_check_thread = threading.Thread(
            target=self.device_check_thread_run)
        self.device_check_thread.start()
        self.device_check_finished.connect(self.device_check_finished_cb)

        self.destroyed.connect(self.destroyed_cb)

    def destroyed_cb(self, junk=None):
        self.finished.set()
        if self.upload_manager:
            self.upload_manager.stop()

    def create_proxy(self, find_and_open_func, location_string, serial_number):
        proxy = self.proxy_manager.new_proxy(serial_number,
                                             find_and_open_func,
                                             location_string)
        connected = functools.partial(self.proxy_connected, proxy,
                                      location_string, serial_number)
        proxy.connected.connect(connected)
        disconnected = functools.partial(self.proxy_disconnected, proxy,
                                         location_string, serial_number)
        proxy.disconnected.connect(disconnected)
        proxy.open_connection()
        with self.proxy_lock:
            self.proxies[location_string] = proxy

    def collect_new_usb_device_keys(self):
        with self.proxy_lock:
            location_strings = self.proxies.copy().keys()
        keys = []
        for device in asphodel.find_usb_devices():
            location_str = device.get_location_string()
            if location_str not in location_strings:
                # found one we don't already have
                try:
                    device.open()
                    serial_number = device.get_serial_number()
                except asphodel.AsphodelError:
                    continue
                finally:
                    device.close()

                # SN first in the tuple for sorting reasons
                keys.append((serial_number, location_str))
        return keys

    def initial_device_connect(self):
        find_method = self.settings.value("Devices/FindMethod")
        if find_method is None:
            find_method = 'initial'

        find_method_lower = find_method.lower()

        if find_method_lower == "all":
            exit_with_none = False
            find_initial_devices = True
            self.find_all_devices = True
            self.should_scan.set()
            logger.info("Will stream from new devices as they are connected")
        elif find_method_lower == "initial":
            exit_with_none = True
            find_initial_devices = True
            self.find_all_devices = False
            logger.info("Will stream from currently connected devices")
        elif find_method_lower == "list":
            exit_with_none = False
            find_initial_devices = False
            self.find_all_devices = False
            serial_numbers = []
            size = self.settings.beginReadArray("Devices/FindList")
            if size is None or size <= 0:
                logger.error("Nothing set for FindList/size")
                QtCore.QCoreApplication.quit()
                return
            for i in range(size):
                self.settings.setArrayIndex(i)
                sn = self.settings.value("serial")
                if sn is None:
                    s = "Invalid setting for FindList/{}/serial".format(i + 1)
                    logger.error(s)
                    QtCore.QCoreApplication.quit()
                    return
                serial_numbers.append(sn)
            self.settings.endArray()
            serials_str = ", ".join(serial_numbers)
            logger.info("Connecting to serials: {}".format(serials_str))

            for sn in serial_numbers:
                recorder = DeviceRecorder(sn, self.base_dir, self,
                                          self.upload_manager)
                self.device_recorders[sn] = recorder
                self.disconnected_recorders.add(recorder)
        else:
            msg = "Unknown option for FindMethod: {}".format(find_method)
            logger.error(msg)
            QtCore.QCoreApplication.quit()
            return

        created_proxy_serials = set()

        if asphodel.nativelib.usb_devices_supported:
            usb_keys = self.collect_new_usb_device_keys()
            for sn, location_str in sorted(usb_keys):
                if find_initial_devices:
                    recorder = DeviceRecorder(sn, self.base_dir, self,
                                              self.upload_manager)
                    self.device_recorders[sn] = recorder
                    self.disconnected_recorders.add(recorder)

                if sn in self.device_recorders:
                    created_proxy_serials.add(sn)
                    self.create_proxy(find_and_open_usb_device, location_str,
                                      sn)

        if asphodel.nativelib.tcp_devices_supported:
            devices = asphodel.find_tcp_devices()
            tcp_keys = self.get_tcp_device_keys(devices)

            for sn, location_str in sorted(tcp_keys):
                if find_initial_devices:
                    recorder = DeviceRecorder(sn, self.base_dir, self,
                                              self.upload_manager)
                    self.device_recorders[sn] = recorder
                    self.disconnected_recorders.add(recorder)

                if sn in self.device_recorders:
                    created_proxy_serials.add(sn)
                    self.create_proxy(find_and_open_tcp_device, location_str,
                                      sn)

        if not (asphodel.nativelib.usb_devices_supported or
                asphodel.nativelib.tcp_devices_supported):
            # no TCP or USB supported by DLL
            msg = "Asphodel library does not support USB or TCP devices"
            logger.warning(msg)

        if len(created_proxy_serials) == 0:
            logger.warning("No devices found")

            if exit_with_none:
                QtCore.QCoreApplication.quit()
                return

        desired_serials = set(self.device_recorders.keys())
        missing_serials = desired_serials.difference(created_proxy_serials)
        if missing_serials:
            self.should_scan.set()
            missing_str = ", ".join(sorted(missing_serials))
            logger.warning("Missing devices: {}".format(missing_str))

    def get_tcp_device_keys(self, devices):
        keys = []
        for device in devices:
            location_str = device.get_location_string()
            adv = device.tcp_get_advertisement()
            serial_number = adv.serial_number
            # SN first in the tuple for sorting reasons
            keys.append((serial_number, location_str))
        return keys

    def device_check_finished_cb(self, results):
        for (sn, location_str), func in results:
            if self.find_all_devices or sn in self.device_recorders:
                # found one to reconnect
                self.create_proxy(func, location_str, sn)

    def device_check_thread_run(self):
        while True:
            if self.finished.wait(timeout=1.5):
                return  # done

            if not self.should_scan.is_set():
                continue

            results = []

            # look for USB devices
            if asphodel.nativelib.usb_devices_supported:
                usb_keys = self.collect_new_usb_device_keys()
                func = find_and_open_usb_device
                results.extend((k, func) for k in usb_keys)

            # look for TCP devices
            if asphodel.nativelib.tcp_devices_supported:
                tcp_devices = asphodel.find_tcp_devices()
                tcp_keys = self.get_tcp_device_keys(tcp_devices)

                with self.proxy_lock:
                    location_strings = self.proxies.copy().keys()

                for serial_number, location_str in tcp_keys:
                    if location_str not in location_strings:
                        results.append(((serial_number, location_str),
                                        find_and_open_tcp_device))

            if results:
                self.device_check_finished.emit(results)

    def proxy_connected(self, proxy, location_string, serial_number):
        if serial_number in self.device_recorders:
            recorder = self.device_recorders[serial_number]
            self.disconnected_recorders.discard(recorder)
            if not self.disconnected_recorders:
                if not self.find_all_devices:
                    self.should_scan.clear()
        else:
            # create a new device recorder
            recorder = DeviceRecorder(serial_number, self.base_dir, self,
                                      self.upload_manager)
            self.device_recorders[serial_number] = recorder
        recorder.set_proxy(proxy)

    def proxy_disconnected(self, proxy, location_string, serial_number):
        # recorder handles its own disconnect

        # remove the proxy from the proxies list
        with self.proxy_lock:
            if self.proxies.get(location_string) == proxy:
                del self.proxies[location_string]
        recorder = self.device_recorders.get(serial_number, None)
        if recorder:
            self.disconnected_recorders.add(recorder)
            self.should_scan.set()

    def create_recorder(self, proxy, sn):  # called from a radio panel
        # create a new device recorder
        recorder = DeviceRecorder(sn, self.base_dir, self, self.upload_manager)
        recorder.set_proxy(proxy)
        return recorder
