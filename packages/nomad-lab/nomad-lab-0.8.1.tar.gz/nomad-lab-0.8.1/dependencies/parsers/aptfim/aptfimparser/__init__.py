# Copyright 2016-2019 Markus Scheidgen, Markus Kühbach
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import sys
import os.path
import json
import ase
import re
import numpy as np
from datetime import datetime

from nomadcore.simple_parser import SimpleMatcher
from nomadcore.baseclasses import ParserInterface, AbstractBaseParser


class APTFIMParserInterface(ParserInterface):
    def get_metainfo_filename(self):
        """
        The parser specific metainfo. To include other metadata definitions, use
        the 'dependencies' key to refer to other local nomadmetainfo.json files or
        to nomadmetainfo.json files that are part of the general nomad-meta-info
        submodule (i.e. ``dependencies/nomad-meta-info``).
         """
        return os.path.join(os.path.dirname(__file__), 'aptfim.nomadmetainfo.json')

    def get_parser_info(self):
        """ Basic info about parser used in archive data and logs. """
        return {
            'name': 'aptfimparser',
            'version': '0.1.0'
        }

    def setup_version(self):
        """ Can be used to call :func:`setup_main_parser` differently for different code versions. """
        self.setup_main_parser(None)

    def setup_main_parser(self, _):
        """ Setup the actual parser (behind this interface) """
        self.main_parser = APTFIMParser(self.parser_context)


class APTFIMParser(AbstractBaseParser):

    def parse(self, filepath):
        backend = self.parser_context.super_backend

        with open(filepath, 'rt') as f:
            data = json.load(f)

        root_gid = backend.openSection('section_experiment')

        # Read general tool environment details
        backend.addValue('experiment_location', data.get('experiment_location'))
        backend.addValue('experiment_facility_institution', data.get('experiment_facility_institution'))
        backend.addValue('experiment_summary', '%s of %s.' % (data.get('experiment_method').capitalize(), data.get('specimen_description')))
        try:
            backend.addValue('experiment_time', int(datetime.strptime(data.get('experiment_date_global_start'), '%d.%m.%Y %M:%H:%S').timestamp()))
        except ValueError:
            pass
        try:
            backend.addValue('experiment_end_time', int(datetime.strptime(data.get('experiment_date_global_end'), '%d.%m.%Y %M:%H:%S').timestamp()))
        except ValueError:
            pass

        # Read data parameters
        data_gid = backend.openSection('section_data')
        backend.addValue('data_repository_name', data.get('data_repository_name'))
        backend.addValue('data_repository_url', data.get('data_repository_url'))
        preview_url = data.get('data_preview_url')
        # TODO: This a little hack to correct the preview url and should be removed
        # after urls are corrected
        preview_url = '%s/files/%s' % tuple(preview_url.rsplit('/', 1))
        backend.addValue('data_preview_url', preview_url)
        backend.closeSection('section_data', data_gid)

        # Read parameters related to method
        method_gid = backend.openSection('section_method')
        backend.addValue('experiment_method_name', data.get('experiment_method'))
        backend.addValue('experiment_method_abbreviation', 'APT/FIM')
        backend.addValue('probing_method', 'electric pulsing')
        # backend.addValue('experiment_tool_info', data.get('instrument_info')) ###test here the case that input.json keyword is different to output.json
        # measured_pulse_voltage for instance should be a conditional read
        # backend.addValue('measured_number_ions_evaporated', data.get('measured_number_ions_evaporated'))
        # backend.addValue('measured_detector_hit_pos', data.get('measured_detector_hit_pos'))
        # backend.addValue('measured_detector_hit_mult', data.get('measured_detector_hit_mult'))
        # backend.addValue('measured_detector_dead_pulses', data.get('measured_detector_dead_pulses'))
        # backend.addValue('measured_time_of_flight', data.get('measured_time_of_flight'))
        # backend.addValue('measured_standing_voltage', data.get('measured_standing_voltage'))
        # backend.addValue('measured_pulse_voltage', data.get('measured_pulse_voltage'))
        # backend.addValue('experiment_operation_method', data.get('experiment_operation_method'))
        # backend.addValue('experiment_imaging_method', data.get('experiment_imaging_method'))
        backend.closeSection('section_method', method_gid)

        # Read parameters related to sample
        sample_gid = backend.openSection('section_sample')
        backend.addValue('sample_description', data.get('specimen_description'))
        backend.addValue('sample_microstructure', data.get('specimen_microstructure'))
        backend.addValue('sample_constituents', data.get('specimen_constitution'))
        atom_labels = data.get('specimen_chemistry')
        formula = ase.Atoms(atom_labels).get_chemical_formula()
        backend.addArrayValues('sample_atom_labels', np.array(atom_labels))
        backend.addValue('sample_chemical_formula', formula)
        backend.closeSection('section_sample', sample_gid)

        # Close sections in the reverse order
        backend.closeSection('section_experiment', root_gid)
