# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2016-2020 European Synchrotron Radiation Facility
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
# ###########################################################################*/

__authors__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "04/03/2019"


import os
import copy
try:
    from contextlib import AbstractContextManager
except ImportError:
    from tomwer.third_party.contextlib import AbstractContextManager
import datetime
from silx.utils.enum import Enum as _Enum
import tomwer.version
from tomwer.core.log import TomwerLogger
from tomwer.core.scan.scanbase import _TomwerBaseDock
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.core.scan.edfscan import EDFTomoScan
from tomwer.core.scan.hdf5scan import HDF5TomoScan
from tomwer.core.process.baseprocess import (SingleProcess, _input_desc,
                                             _output_desc)
from nabu.resources.processconfig import ProcessConfig
from nabu.resources.dataset_analyzer import EDFDatasetAnalyzer, HDF5DatasetAnalyzer
from nabu.resources.dataset_analyzer import DatasetAnalyzer
from multiprocessing import Process
from nabu.io.config import generate_nabu_configfile
from nabu import version as nabu_version
from silx.io.dictdump import h5todict
import h5py
import sys

_logger = TomwerLogger(__name__)


NABU_FILE_PER_GROUP = 100

NABU_CONFIG_FILE_EXTENSION = '.cfg'


def run_reconstruction(scan: TomwerScanBase, config: dict,
                       dry_run: bool = False, local: bool = True) -> None:
    """
    call nabu for a reconstruction on scan with the given configuration

    :param TomwerScanBase scan: scan to reconstruct
    :param dict config: configuration to run the reconstruction
    :param bool dry_run: do we want to run dry
    :param bool local: do we want to run a local reconstruction
    """
    _logger.info('start reconstruction of %s' % scan.path)
    # if scan contains some center of position copy it to nabu
    if scan.axis_params is not None and scan.axis_params.value is not None:
        if 'reconstruction' in config:
            # move the cor value to the nabu reference
            cor_nabu_ref = scan.axis_params.value + scan.dim_1 // 2
            config['reconstruction']['rotation_axis_position'] = str(cor_nabu_ref)

    nabu_configurations = _interpret_tomwer_configuration(config, scan=scan)
    for nabu_configuration in nabu_configurations:
        config, slice_index = nabu_configuration
        _run_single_reconstruction(config=config, scan=scan, local=local,
                                   slice_index=slice_index, dry_run=dry_run)


class Nabu(SingleProcess):
    """Definition of the nabu reconstruction Single process"""
    inputs = [
        _input_desc(name="change recons params", type=_TomwerBaseDock,
                    handler='updateReconsParam',
                    doc='input with scan + reconstruction parameters'),
        _input_desc(name='data', type=TomwerScanBase, handler='pathReceived',
                    doc='scan path'),
    ]
    # Note : scanReady don't intend to find an 'octave_FT_params.h5' file at
    # the folder level.
    # But updateReconsParam should always have a .h5 file defined
    outputs = [_output_desc(name='data', type=TomwerScanBase, doc='scan path'), ]

    def __init__(self, *arg, **kwargs):
        SingleProcess.__init__(self, *arg, **kwargs)
        self._dry_run = False

    def process(self, scan=None):
        if scan is None:
            return None
        else:
            run_reconstruction(scan=scan, config=self.get_configuration(),
                               dry_run=self.dry_run)
            # register result
            entry = 'entry'
            if isinstance(scan, HDF5TomoScan):
                entry = scan.entry
            with scan.acquire_process_file_lock():
                self.register_process(process_file=scan.process_file,
                                      entry=entry,
                                      configuration=self.get_configuration(),
                                      results={},
                                      process_index=scan.pop_process_index(),
                                      overwrite=True)

    @staticmethod
    def program_name():
        return 'nabu'

    @staticmethod
    def program_version():
        return nabu_version

    def set_dry_run(self, dry_run):
        self._dry_run = dry_run

    @property
    def dry_run(self):
        return self._dry_run

    @staticmethod
    def get_process_frm_process_file(process_file, entry):
        """
        Read informations regarding the nabu process save in the
        tomwer_process.h5 file

        :param process_file:
        :param entry:
        :return: dictionnary with the contain of the nabu process
        :rtype:dict
        """
        if entry is None:
            with h5py.File(process_file, 'r', swmr=True) as h5f:
                entries = Nabu._get_process_nodes(root_node=h5f,
                                                  process=Nabu)
                if len(entries) == 0:
                    _logger.info(
                        'unable to find a Axis process in %s' % process_file)
                    return None
                elif len(entries) > 1:
                    raise ValueError('several entry found, entry should be '
                                     'specify')
                else:
                    entry = list(entries.keys())[0]
                    _logger.info('take %s as default entry' % entry)

        configuration_path = None
        res = {}

        with h5py.File(process_file, 'r', swmr=True) as h5f:
            nabu_nodes = Nabu._get_process_nodes(root_node=h5f[entry],
                                                 process=Nabu)
            index_to_path = {}
            for key, value in nabu_nodes.items():
                index_to_path[key] = key

            if len(nabu_nodes) == 0:
                return None
            # take the last processed dark ref
            last_process_index = sorted(list(nabu_nodes.keys()))[-1]
            last_process_dark = index_to_path[last_process_index]
            if (len(index_to_path)) > 1:
                _logger.debug('several processing found for dark-ref,'
                             'take the last one: %s' % last_process_dark)

            for key_name in ('class_instance', 'date', 'program',
                             'sequence_index', 'version'):
                if key_name in h5f[last_process_dark]:
                    res[key_name] = h5f[last_process_dark][key_name][()]
            if 'configuration' in h5f[last_process_dark]:
                configuration_path = '/'.join((h5f[last_process_dark].name,
                                               'configuration'))

        if configuration_path is not None:
            res['configuration'] = h5todict(h5file=process_file,
                                            path=configuration_path)
        return res


def _interpret_tomwer_configuration(config: dict, scan: TomwerScanBase) -> tuple:
    """
    tomwer can 'mock' the nabu reconstruction to request more feature.
    Typical use case is that we can ask for reconstruction of several
    slices and not only the volume

    :param dict config: tomwer configuration for nabu
    :return: tuple of tuples (nabu configuration, is slice)
    """
    def get_nabu_config(config):
        nabu_config = copy.deepcopy(config)
        if 'tomwer_slices' in nabu_config:
            del nabu_config['tomwer_slices']
        return nabu_config

    if 'tomwer_slices' in config:
        slices = list(NabuSliceMode.getSlices(config['tomwer_slices'], scan))
    else:
        slices = []

    if 'phase' in config and 'delta_beta' in config['phase']:
        pag_dbs = _retrieve_lst_of_value_from_str(config['phase']['delta_beta'])
        if len(pag_dbs) == 0:
            pag_dbs = (None,)
    else:
        pag_dbs = (None,)

    # by default add the slice 'None' which is the slice for the volume
    slices.append(None)
    nabu_config = get_nabu_config(config=config)
    res = []
    for slice in slices:
        for pag_db in pag_dbs:
            local_config = copy.deepcopy(nabu_config)
            if slice is not None:
                local_config['reconstruction']['start_z'] = slice
                local_config['reconstruction']['end_z'] = slice + 1
            if pag_db is not None:
                local_config['phase']['delta_beta'] = str(pag_db)
            res.append((local_config, slice))
    return tuple(res)


def _get_file_basename_reconstruction(scan, slice_index, pag, db):
    """

    :param TomwerScanBase scan: scan reconstructed
    :param Union[None, int] slice_index: index of the slice reconstructed.
                                         if None, we want to reconstruct the
                                         entire volume
    :param bool pag: is it a paganin reconstruction
    :param int db: delta / beta parameter
    :return: basename of the file reconstructed (without any extension)
    """
    assert type(db) in (int, type(None))
    if slice_index is None:
        if pag:
            return '_'.join((os.path.basename(scan.path) + 'pag', 'db' + str(db).zfill(4)))
        else:
            return os.path.basename(scan.path)
    else:
        if pag:
            return '_'.join((os.path.basename(scan.path) + 'slice_pag',
                             str(slice_index).zfill(4),
                             'db' + str(db).zfill(4)))
        else:
            return '_'.join((os.path.basename(scan.path) + 'slice',
                             str(slice_index).zfill(4)))


def _launch_reconstruction(config_file, slice_index):
    from nabu.resources.processconfig import ProcessConfig
    proc = ProcessConfig(config_file)
    
    from nabu.app.fullfield_cuda import CudaFullFieldPipeline
    worker_process = CudaFullFieldPipeline(
        proc,
        sub_region=(None, None, slice_index, slice_index + 1),
    )
    worker_process.process_chunk()


def _run_single_reconstruction(scan, config, dry_run, slice_index, local,
                               use_cuda=True):
    """

    :param scan:
    :param config:
    :param dry_run:
    :param Union[None,int] slice_index: slice index to reconstruct
    :param local:
    :param use_cuda:
    :return:
    """
    dataset_analyzer = get_nabu_dataset_analyzer(scan=scan)
    config['dataset'] = get_nabu_dataset_desc(scan=scan)
    if local is True:
        resources_method = 'local'
    else:
        resources_method = 'slurm'
    config['resources'] = get_nabu_resources_desc(scan=scan, workers=1,
                                                  method=resources_method)
    config['about'] = get_nabu_about_desc(overwrite=True)

    def treateOutputConfig(_config):
        """
        - add or overwrite some parameters of the dictionary
        - create the output directory if does not exist
        """
        pag = False
        db = None
        if 'phase' in _config:
            if 'method' in _config['phase'] and _config['phase']['method'] != '':
                pag = True
                if 'delta_beta' in _config['phase']:
                    db = round(float(_config['phase']['delta_beta']))
        file_name = _get_file_basename_reconstruction(scan=scan,
                                                      slice_index=slice_index,
                                                      pag=pag,
                                                      db=db)
        if 'output' in config:
            _config['output']['file_prefix'] = os.path.basename(scan.path)
            _config['output']['file_prefix'] = file_name
            if _config['output']['location'] not in ('', None):
                # if user specify the location
                if not os.path.isdir(_config['output']['location']):
                    os.makedirs(_config['output']['location'])
            else:
                # otherwise default location will be the data root level
                _config['output']['location'] = scan.path
        return _config

    config = treateOutputConfig(config)
    # the policy is to save nabu .cfg file at the same location as the
    # reconstructed scan
    process_config = ProcessConfig(conf_dict=config,
                                   dataset_infos=dataset_analyzer)
    # write the .conf file
    conf_file = os.path.join(config['output']['location'],
                            config['output']['file_prefix'] + NABU_CONFIG_FILE_EXTENSION)
    _logger.info('create %s' % conf_file)

    # add some tomwer metadata and save the configuration
    # note: for now the section is ignored by nabu but shouldn't stay that way
    with _TomwerInfo(config) as config_to_dump:
        generate_nabu_configfile(fname=conf_file, config=config_to_dump,
                                 options_level='advanced')
        
    if slice_index is not None and dry_run is False and local:
        _logger.info('run nabu reconstruction for %s with %s'
                     '' % (scan.path, config))
        # need to be excuted in his own context
        process = Process(target=_launch_reconstruction, args=(conf_file, slice_index))
        process.start()
        process.join()


def get_nabu_dataset_analyzer(scan: TomwerScanBase) -> DatasetAnalyzer:
    """

    :param scan:
    :return:
    """
    if isinstance(scan, EDFTomoScan):
        return EDFDatasetAnalyzer(location=scan.path)
    elif isinstance(scan, HDF5TomoScan):
        assert os.path.exists(scan.master_file)
        assert os.path.isfile(scan.master_file)
        return HDF5DatasetAnalyzer(location=scan.master_file)
    else:
        raise TypeError('given scan type %s is not managed' % type(scan))


def get_nabu_dataset_desc(scan: TomwerScanBase) -> dict:
    """
    Create the descriptor for the outputs of scan for nabu

    :param TomwerScanBase scan:
    :return: nabu's description for the output
    """
    assert isinstance(scan, TomwerScanBase)
    if isinstance(scan, EDFTomoScan):
        return {
            'location': scan.path,
            'binning': 1,
            'binning_z': 1,
            'projections_subsampling': 1,
        }
    elif isinstance(scan, HDF5TomoScan):
        return {
            'location': scan.master_file,
            'binning': 1,
            'binning_z': 1,
            'projections_subsampling': 1,
        }
    else:
        raise ValueError('TomoBase type not recognized: ' + str(type(scan)))


def get_nabu_resources_desc(scan: TomwerScanBase, method, workers=1) -> dict:
    """
    Create the descriptor of nabu's resources

    :param TomwerScanBase scan:
    :param str method:
    :return: nabu's description of resources to be used
    """
    assert isinstance(scan, TomwerScanBase)
    res = {
        'method': method,
        'cpu_workers': workers,
        'queue': 'gpu',
        'memory_per_node': '90%',
        'threads_per_node': '100%',
        'walltime': '01:00:00',
    }
    return res


def get_nabu_about_desc(overwrite) -> dict:
    """
    Create the description for nabu's about

    :param self:
    :return:
    """
    return {
        'overwrite_results': str(bool(overwrite)),
    }


class _NabuMode(_Enum):
    FULL_FIELD = 'full field imaging'
    HALF_ACQ = 'half acquisition'


class _NabuStages(_Enum):
    INI = 'initialization'
    PRE = 'pre-processing'
    PHASE = 'phase'
    PROC = 'processing'
    POST = 'post-processing'

    @staticmethod
    def getStagesOrder():
        return (_NabuStages.INI, _NabuStages.PRE, _NabuStages.PHASE,
                _NabuStages.PROC, _NabuStages.POST)

    @staticmethod
    def getProcessEnum(stage):
        """Return the process Enum associated to the stage"""
        stage = _NabuStages.from_value(stage)
        if stage is _NabuStages.INI:
            raise NotImplementedError()
        elif stage is _NabuStages.PRE:
            return _NabuPreprocessing
        elif stage is _NabuStages.PHASE:
            return _NabuPhase
        elif stage is _NabuStages.PROC:
            return _NabuProcessing
        elif stage is _NabuStages.POST:
            return _NabuPostProcessing
        raise NotImplementedError()


class _NabuPreprocessing(_Enum):
    """Define all the preprocessing action possible and the order they
    are applied on"""
    FLAT_FIELD_NORMALIZATION = 'flat field normalization'
    CCD_FILTER = 'hot spot correction'

    @staticmethod
    def getPreProcessOrder():
        return (_NabuPreprocessing.FLAT_FIELD_NORMALIZATION,
                _NabuPreprocessing.CCD_FILTER)


class _NabuPhase(_Enum):
    """Define all the phase action possible and the order they
    are applied on"""
    PHASE = 'phase retrieval'
    UNSHARP_MASK = 'unsharp mask'
    LOGARITHM = 'logarithm'

    @staticmethod
    def getPreProcessOrder():
        return (_NabuPhase.PHASE, _NabuPhase.UNSHARP_MASK,
                _NabuPhase.LOGARITHM)


class _NabuProcessing(_Enum):
    """Define all the processing action possible"""
    RECONSTRUCTION = 'reconstruction'

    @staticmethod
    def getProcessOrder():
        return (_NabuProcessing.RECONSTRUCTION, )


class _ConfigurationLevel(_Enum):
    REQUIRED = 'required'
    OPTIONAL = 'optional'
    ADVANCED = 'advanced'

    def _get_num_value(self) -> int:
        if self is self.REQUIRED:
            return 0
        elif self is self.OPTIONAL:
            return 1
        elif self is self.ADVANCED:
            return 2

    def __le__(self, other):
        assert isinstance(other, _ConfigurationLevel)
        return self._get_num_value() <= other._get_num_value()


class _NabuPostProcessing(_Enum):
    """Define all the post processing action available"""
    SAVE_DATA = 'save'

    @staticmethod
    def getProcessOrder():
        return (_NabuPostProcessing.SAVE_DATA, )


class _NabuReconstructionMethods(_Enum):
    FBP = 'FBP'


class _NabuPhaseMethod(_Enum):
    """
    Nabu phase method
    """
    PAGANIN = 'Paganin'


class _NabuFBPFilterType(_Enum):
    RAMLAK = 'ramlak'


class _NabuPaddingType(_Enum):
    ZEROS = 'zeros'
    EDGES = 'edges'


def _retrieve_lst_of_value_from_str(my_string: str) -> tuple:
    """
    Return a list of value from a string like '12,23' or '(12, 23)',
    '[12;23]', '12;23' or with the pattern from:to:step like '0:10:1'
    :param str mystring:
    :return: list of single value
    """
    assert type(my_string) is str, 'work on string only'
    res = []
    my_string = my_string.replace('(', '')
    my_string = my_string.replace(')', '')
    my_string = my_string.replace('[', '')
    my_string = my_string.replace(']', '')
    if my_string.count(':') == 2:
        _from, _to, _step = my_string.split(':')
        _from, _to, _step = int(_from), int(_to), int(_step)
        if (_from > _to):
            tmp = _to
            _to = _from
            _from = tmp
        while _from <= _to:
            res.append(_from)
            _from += _step
        return tuple(res)
    else:
        vals = my_string.replace(' ', '')
        vals = vals.replace('_', '')
        vals = vals.replace(';', ',').split(',')
        for val in vals:
            try:
                res.append(int(val))
            except Exception:
                pass
        return tuple(res)


class NabuSliceMode(_Enum):
    MIDDLE = 'middle'
    OTHER = 'other'

    @staticmethod
    def getSlices(slices, scan) -> tuple:
        res = []
        try:
            mode = NabuSliceMode.from_value(slices)
        except ValueError:
            try:
                res = _retrieve_lst_of_value_from_str(slices)
            except Exception:
                pass
        else:
            if mode == mode.MIDDLE:
                n_slice = scan.dim_2 or 2048
                res.append(n_slice // 2)
            else:
                raise ValueError('there should be only two ways of defining '
                                 'slices: middle one or other, by giving '
                                 'an unique value or a list or a tuple')
        return tuple(res)


class _TomwerInfo(AbstractContextManager):
    """Simple context manager to add tomwer metadata to a dict before
    writing it"""
    def __init__(self, config_dict):
        self.config = config_dict

    def __enter__(self):
        self.config['other'] = {
            'tomwer_version': tomwer.version.version,
            'date': datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        }
        return self.config

    def __exit__(self, exc_type, exc_val, exc_tb):
        del self.config['other']['tomwer_version']
        del self.config['other']['date']
