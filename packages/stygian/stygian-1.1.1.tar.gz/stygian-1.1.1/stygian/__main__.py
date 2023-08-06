#!/usr/bin/env python3
import logging.handlers
import multiprocessing
import os
import signal
import sys
import time

from PySide2 import QtCore

import asphodel
import hyperborea.proxy
import stygian.dispatcher

logger = logging.getLogger(__name__)


def main_is_frozen():
    """Return True if the script is frozen, False otherwise."""
    return getattr(sys, 'frozen', False)


def get_main_dir():
    """Return the path of the main script's directory, even when frozen."""
    if main_is_frozen():
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(sys.argv[0]))


def setup_logging():
    """Configure logging for the whole program."""

    def my_excepthook(exctype, value, traceback):
        """Log the caught exception using the logging module."""
        exc_info = (exctype, value, traceback)
        logger.error("Uncaught Exception", exc_info=exc_info)
        QtCore.QCoreApplication.quit()

    sys.excepthook = my_excepthook

    # get an appropriate location for the log file
    logdir = QtCore.QStandardPaths.writableLocation(
        QtCore.QStandardPaths.DataLocation)
    logfile = os.path.join(logdir, "main.log")

    # make sure the directory exists
    os.makedirs(logdir, exist_ok=True)

    # filter for creating %(optdevice) format option
    optdevice_filter = hyperborea.proxy.OptionalDeviceStringFilter("[%s] ", "")

    # create a log file handler
    file_log_handler = logging.handlers.RotatingFileHandler(logfile,
                                                            maxBytes=10e6,
                                                            backupCount=9)
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(optdevice)s%(message)s")
    file_formatter.default_time_format = '%Y-%m-%dT%H:%M:%S'
    file_formatter.default_msec_format = '%s,%03dZ'
    file_formatter.converter = time.gmtime
    file_log_handler.addFilter(optdevice_filter)
    file_log_handler.setFormatter(file_formatter)
    file_log_handler.setLevel(logging.DEBUG)

    console_formatter = logging.Formatter("%(optdevice)s%(message)s")
    console_formatter.default_time_format = '%Y-%m-%dT%H:%M:%S'
    console_formatter.default_msec_format = '%s,%03dZ'
    console_formatter.converter = time.gmtime
    console_handler = logging.StreamHandler()
    console_handler.addFilter(optdevice_filter)
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(logging.INFO)

    root_logger = logging.getLogger()
    root_logger.addHandler(file_log_handler)
    root_logger.addHandler(console_handler)
    root_logger.setLevel(logging.DEBUG)

    # remove pyusb's logging info
    pyusb_logger = logging.getLogger("usb")
    pyusb_logger.propagate = False

    # suppress boto3 (aws) debug messages
    logging.getLogger('boto3').setLevel(logging.INFO)
    logging.getLogger('botocore').setLevel(logging.INFO)
    logging.getLogger('s3transfer').setLevel(logging.INFO)
    logging.getLogger('urllib3').setLevel(logging.INFO)


def force_exit():
    # based on pyqtgraph.exit, with fix for macos

    # # invoke atexit callbacks
    import atexit
    atexit._run_exitfuncs()

    # # close file handles
    if sys.platform == 'darwin':
        # trying to close 7 produces an illegal instruction on the Mac
        os.closerange(3, 7)
        os.closerange(8, 4096)
    else:
        os.closerange(3, 4096)  # just guessing on the maximum descriptor count

    os._exit(0)


def shutdown_signal(*args):
    QtCore.QCoreApplication.quit()


def main():
    """Run the program."""

    # freeze_support() MUST be first. Anything before this will cease to exist
    multiprocessing.freeze_support()

    # spawn is only option on windows, linux needs spawn or forkserver to work
    multiprocessing.set_start_method("spawn")

    # work around for botocore data
    if main_is_frozen():
        cacert = os.path.join(os.path.dirname(sys.executable), 'botodata',
                              'cacert.pem')
        os.environ["AWS_CA_BUNDLE"] = cacert
        botodata = os.path.join(os.path.dirname(sys.executable), 'botodata')
        os.environ["AWS_DATA_PATH"] = botodata

    if not sys.stdout or not sys.stderr:
        sys.stdout = open(os.devnull)
        sys.stderr = open(os.devnull)

    app = QtCore.QCoreApplication([])
    app.setApplicationName("Stygian")
    app.setOrganizationDomain("suprocktech.com")
    app.setOrganizationName("Suprock Tech")

    # force the settings to use an INI file instead of the registry
    QtCore.QSettings.setDefaultFormat(QtCore.QSettings.IniFormat)

    app.setApplicationVersion(stygian.__version__)

    setup_logging()

    logger.info("Stygian started (Version {})".format(stygian.__version__))

    try:
        missing_funcs = asphodel.nativelib.missing_funcs
    except AttributeError:
        missing_funcs = []  # to bypass the next warning
        message = "Asphodel python mismatch!"
        logging.warning(message)

    if missing_funcs:
        missing_str = ", ".join(sorted(missing_funcs))
        logging.warning("Missing Asphodel functions: {}".format(missing_str))

    settings = QtCore.QSettings()
    settings_file = settings.fileName()
    logger.info("Settings: {}".format(os.path.abspath(settings_file)))

    proxy_manager = hyperborea.proxy.DeviceProxyManager()

    # create and start the dispacher
    dispatcher = stygian.dispatcher.Dispatcher(proxy_manager)

    # allow program to be closed gracefully
    signal.signal(signal.SIGINT, shutdown_signal)  # ctrl+c
    signal.signal(signal.SIGTERM, shutdown_signal)

    # periodically go into the python interpreter from Qt for SIGINT handling
    timer = QtCore.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    # run until QCoreApplication.exit() or .quit()
    app.exec_()

    logger.info("Stygian exiting")

    proxy_manager.stop()
    if dispatcher.upload_manager:
        dispatcher.upload_manager.stop()
        dispatcher.upload_manager.join()

    logger.info("Stygian finished")

    force_exit()

if __name__ == '__main__':
    main()
