#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import sys
from silx.gui import qt
import argparse
from tomwer.gui import icons
from tomwer.gui.utils.splashscreen import getMainSplashScreen
from tomwer.gui.reconstruction.nabu.nabu import NabuDialog
from tomwer.core.scan.scanfactory import ScanFactory
from tomwer.core.scan.hdf5scan import HDF5TomoScan
from tomwer.core.process.reconstruction.nabu import run_reconstruction
import signal

logging.basicConfig()
_logger = logging.getLogger(__name__)


def getinputinfo():
    return "tomwer nabu [scan_path]"


def sigintHandler(*args):
    """Handler for the SIGINT signal."""
    qt.QApplication.quit()


class NabuProcessingThread(qt.QThread):
    def init(self, scan, config, dry_run=False):
        self._scan = scan
        self._config = config
        self._dry_run = dry_run

    def run(self):
        run_reconstruction(scan=self._scan, config=self._config,
                           dry_run=self._dry_run)


class NabuWindow(NabuDialog):
    def __init__(self, parent=None):
        NabuDialog.__init__(self, parent)
        self.__scan = None
        self.__processingThread = NabuProcessingThread()
        self._dry_run = False

        # connect signal / slot
        self._computePB.released.connect(self._requireComputation)

    def setScan(self, scan):
        self.__scan = scan

    def getScan(self):
        return self.__scan

    def _requireComputation(self, *arg, **kwargs):
        self.setEnabled(False)
        qt.QApplication.setOverrideCursor(qt.Qt.WaitCursor)
        scan = self.getScan()
        if scan is not None:
            self._launchComputation(scan=scan, config=self.getConfiguration())

    def _computationEnded(self):
        self.setEnabled(True)
        qt.QApplication.restoreOverrideCursor()

    def getProcessingThread(self):
        return self.__processingThread

    def _launchComputation(self, scan, config):
        # update the processing thread
        thread = self.getProcessingThread()
        thread.init(scan=scan, config=config, dry_run=self._dry_run)
        thread.finished.connect(self._computationEnded)

        # start processing
        thread.start(priority=qt.QThread.LowPriority)

    def set_dry_run(self, dry_run):
        self._dry_run = dry_run


def main(argv):
    import os
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        'scan_path',
        help='Data file to show (h5 file, edf files, spec files)')
    parser.add_argument(
        '--entry',
        default=None,
        help='An entry should be specify for hdf5 files')
    parser.add_argument(
        '--output-dir',
        help='output directory of the reconstruction(s)')
    parser.add_argument(
        '--debug',
        dest="debug",
        action="store_true",
        default=False,
        help='Set logging system in debug mode')
    parser.add_argument(
        '--dry-run',
        dest="dry_run",
        action="store_true",
        default=False,
        help='Only create the .nabu file and print the configuration used')
    options = parser.parse_args(argv[1:])

    global app  # QApplication must be global to avoid seg fault on quit
    app = qt.QApplication.instance() or qt.QApplication([])

    qt.QLocale.setDefault(qt.QLocale(qt.QLocale.English))
    qt.QLocale.setDefault(qt.QLocale.c())
    signal.signal(signal.SIGINT, sigintHandler)
    sys.excepthook = qt.exceptionHandler
    timer = qt.QTimer()
    timer.start(500)
    # Application have to wake up Python interpreter, else SIGINT is not
    # catch
    timer.timeout.connect(lambda: None)

    splash = getMainSplashScreen()
    options.scan_path = options.scan_path.rstrip(os.path.sep)
    if options.entry is None:
        scan = ScanFactory.create_scan_object(options.scan_path)
    else:
        scan = HDF5TomoScan(scan=options.scan_path, entry=options.entry)
    if scan is None:
        raise ValueError('Given scan path is not recognized as a path'
                         'containing a scan')
    widget = NabuWindow(parent=None)
    widget.setScan(scan)
    if options.output_dir is not None:
        widget.setOutputDir(options.output_dir)
    # for the application we run for the reconstruction to be finished
    # to give back hand to the user
    widget.set_dry_run(options.dry_run)
    widget.setWindowTitle('Nabu reconstruction')
    widget.setWindowIcon(icons.getQIcon('tomwer'))
    splash.finish(widget)
    widget.show()
    app.exec_()


if __name__ == '__main__':
    main(sys.argv)
