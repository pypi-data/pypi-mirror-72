# coding: utf-8
#/*##########################################################################
# Copyright (C) 2016 European Synchrotron Radiation Facility
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
#############################################################################*/


__authors__ = ["H.Payno"]
__license__ = "MIT"
__date__ = "09/08/2018"


import os


class BlissScan:
    """Simple class to define a Bliss sequence aka as Bliss scan inside tomwer.

    :warning: BlissScan is not compatible with tomwer treatment. This is
    why it does not inherit from TomwerScanBase. This is a utility class.
    """
    def __init__(self, master_file, entry, proposal_file,
                 scan_numbers=None):
        self._master_file = master_file
        self._entry = entry
        self._proposal_file = proposal_file
        self._scan_numbers = scan_numbers or []
        self._tomo_n = None
        self._n_acquired = None
        self._dir_path = os.path.dirname(self.master_file)

    @property
    def tomo_n(self):
        """total number of projections"""
        return self._tomo_n

    @property
    def proposal_file(self):
        return self._proposal_file

    @tomo_n.setter
    def tomo_n(self, n):
        self._tomo_n = n

    @property
    def n_acquired(self):
        """
        number of frame acquired until now. Does not take into account
        dark, flats or alignment"""
        return self._n_acquired

    @n_acquired.setter
    def n_acquired(self, n):
        self._n_acquired = n

    @property
    def master_file(self):
        return self._master_file

    @property
    def entry(self):
        return self._entry

    @property
    def path(self):
        return self._dir_path

    @property
    def scan_numbers(self):
        return self._scan_numbers

    def add_scan_number(self, scan_number):
        self._scan_numbers.append(scan_number)

    def __str__(self):
        return self.get_id_name(master_file=self.master_file, entry=self.entry)

    @staticmethod
    def get_id_name(master_file, entry):
        return '@'.join((str(entry), master_file))

    def _deduce_transfert_scan(self, output_dir):
        new_master_file = os.path.join(output_dir,
                                       os.path.basename(self.master_file))
        return BlissScan(master_file=new_master_file, entry=self.entry)
