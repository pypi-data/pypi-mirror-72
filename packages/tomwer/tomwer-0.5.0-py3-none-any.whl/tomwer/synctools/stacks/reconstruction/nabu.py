# coding: utf-8
###########################################################################
# Copyright (C) 2016-2019 European Synchrotron Radiation Facility
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
#############################################################################

__authors__ = ["H.Payno"]
__license__ = "MIT"
__date__ = "21/02/2020"


from silx.gui import qt
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.core.scan.edfscan import EDFTomoScan
from tomwer.core.process.reconstruction import nabu
from tomwer.core.settings import get_lbsram_path, isOnLbsram
from tomwer.core.utils import isLowOnMemory
from ..processingstack import FIFO, ProcessingThread
import logging
import h5py

_logger = logging.getLogger(__name__)


class NabuProcessStack(FIFO, qt.QObject):
    """Implementation of the `.AxisProcess` but having a stack for treating
    scans and making computation in threads"""
    def __init__(self, parent=None):
        qt.QObject.__init__(self, parent=parent)
        FIFO.__init__(self)
        self._dry_run = False

    def _create_processing_thread(self):
        return _ProcessingThread()

    def _process(self, scan, configuration, callback=None):
        self._scan_currently_computed = scan
        assert isinstance(scan, TomwerScanBase)
        if isOnLbsram() and isLowOnMemory(get_lbsram_path()) is True:
            # if computer is running into low memory on lbsram skip it
            mess = 'low memory, skip nabu reconstruction for', scan.path
            _logger.processSkipped(mess)
            self._end_threaded_computation()
        else:
            self._computationThread.init(scan=scan,
                                         configuration=configuration)
            self._computationThread.setDryRun(self._dry_run)
            # need to manage connect before starting it because
            self._computationThread.finished.connect(self._end_threaded_computation)
            self._computationThread.start()

    def _create_processing_thread(self) -> qt.QThread:
        return _ProcessingThread()

    def setDryRun(self, dry_run):
        self._dry_run = dry_run


class _ProcessingThread(ProcessingThread):
    """
    Thread use to execute the processing of nabu reconstruction
    """
    def __init__(self):
        ProcessingThread.__init__(self)
        self._scan = None
        self._configuration = None
        self._dry_run = False

    def setDryRun(self, dry_run):
        self._dry_run = dry_run

    def init(self, scan, configuration):
        self._scan = scan
        self._configuration = configuration

    def run(self):
        self.sigComputationStarted.emit()
        # nabu can access some data from the process file.
        nabu.run_reconstruction(config=self._configuration, scan=self._scan,
                                dry_run=self._dry_run)
        index = self._scan.pop_process_index()
        if isinstance(self._scan, EDFTomoScan):
            entry = None
        else:
            entry = self._scan.entry
        nabu.run_reconstruction(config=self._configuration, scan=self._scan,
                                dry_run=self._dry_run)

        index = self._scan.pop_process_index()
        if isinstance(self._scan, EDFTomoScan):
            entry = None
        else:
            entry = self._scan.entry
        nabu.Nabu._register_process(process_file=self._scan.process_file,
                                    entry=entry,
                                    configuration=self._configuration,
                                    results={},
                                    process=nabu.Nabu,
                                    process_index=index,
                                    overwrite=True)
