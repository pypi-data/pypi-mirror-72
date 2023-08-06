# Copyright 2016-2018 Markus Scheidgen
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


class MPESParserInterface(ParserInterface):
    def get_metainfo_filename(self):
        """
        The parser specific metainfo. To include other metadata definitions, use
        the 'dependencies' key to refer to other local nomadmetainfo.json files or
        to nomadmetainfo.json files that are part of the general nomad-meta-info
        submodule (i.e. ``dependencies/nomad-meta-info``).
         """
        return os.path.join(os.path.dirname(__file__), 'mpes.nomadmetainfo.json')

    def get_parser_info(self):
        """ Basic info about parser used in archive data and logs. """
        return {
            'name': 'mpes-parser',
            'version': '1.0.0'
        }

    def setup_version(self):
        """ Can be used to call :func:`setup_main_parser` differently for different code versions. """
        self.setup_main_parser(None)

    def setup_main_parser(self, _):
        """ Setup the actual parser (behind this interface) """
        self.main_parser = MPESParser(self.parser_context)


class MPESParser(AbstractBaseParser):

    def parse(self, filepath):
        backend = self.parser_context.super_backend

        with open(filepath, 'rt') as f:
            data = json.load(f)
            # print(data)

        root_gid = backend.openSection('section_experiment')
        method_gid = backend.openSection('section_method')

        # Read general experimental parameters
        backend.addValue('experiment_location', ', '.join(reversed(re.findall(r"[\w']+", data.get('experiment_location')))))
        start, end = data.get('experiment_date').split(' ')
        try:
            backend.addValue('experiment_time', int(datetime.strptime(start, '%m.%Y').timestamp()))
        except ValueError:
            pass
        try:
            backend.addValue('experiment_end_time', int(datetime.strptime(end, '%m.%Y').timestamp()))
        except ValueError:
            pass
        backend.addValue('experiment_summary', data.get('experiment_summary'))
        backend.addValue('experiment_facility_institution', data.get('facility_institution'))
        backend.addValue('experiment_facility_name', data.get('facility_name'))

        # Read data parameters
        data_gid = backend.openSection('section_data')
        backend.addValue('data_repository_name', data.get('data_repository_name'))
        backend.addValue('data_repository_url', data.get('data_repository_url'))
        backend.addValue('data_preview_url', 'preview.png')
        backend.closeSection('section_data', data_gid)

        # Read method parameters
        backend.addValue('experiment_method_name', data.get('experiment_method'))
        backend.addValue('experiment_method_abbreviation', data.get('experiment_method_abbrv'))
        backend.addValue('equipment_description', data.get('equipment_description'))
        backend.addValue('probing_method', 'laser pulses')

        backend.addValue('general_beamline', data.get('beamline'))
        backend.addValue('general_source_pump', data.get('source_pump'))
        backend.addValue('general_source_probe', data.get('source_probe'))
        backend.addArrayValues('general_measurement_axis', np.array(re.findall(r"[\w']+", data.get('measurement_axis'))))
        backend.addArrayValues('general_physical_axis', np.array(re.findall(r"[\w']+", data.get('physical_axis'))))

        # Read parameters related to experimental source
        # source_gid = backend.openSection('section_experiment_source_parameters')
        backend.addValue('source_pump_repetition_rate', data.get('pump_rep_rate'))
        backend.addValue('source_pump_pulse_duration', data.get('pump_pulse_duration'))
        backend.addValue('source_pump_wavelength', data.get('pump_wavelength'))
        backend.addArrayValues('source_pump_spectrum', np.array(data.get('pump_spectrum')))
        backend.addValue('source_pump_photon_energy', data.get('pump_photon_energy'))
        backend.addArrayValues('source_pump_size', np.array(data.get('pump_size')))
        backend.addArrayValues('source_pump_fluence', np.array(data.get('pump_fluence')))
        backend.addValue('source_pump_polarization', data.get('pump_polarization'))
        backend.addValue('source_pump_bunch', data.get('pump_bunch'))
        backend.addValue('source_probe_repetition_rate', data.get('probe_rep_rate'))
        backend.addValue('source_probe_pulse_duration', data.get('probe_pulse_duration'))
        backend.addValue('source_probe_wavelength', data.get('probe_wavelength'))
        backend.addArrayValues('source_probe_spectrum', np.array(data.get('probe_spectrum')))
        backend.addValue('source_probe_photon_energy', data.get('probe_photon_energy'))
        backend.addArrayValues('source_probe_size', np.array(data.get('probe_size')))
        backend.addArrayValues('source_probe_fluence', np.array(data.get('probe_fluence')))
        backend.addValue('source_probe_polarization', data.get('probe_polarization'))
        backend.addValue('source_probe_bunch', data.get('probe_bunch'))
        backend.addValue('source_temporal_resolution', data.get('temporal_resolution'))

        # Read parameters related to detector
        # detector_gid = backend.openSection('section_experiment_detector_parameters')
        backend.addValue('detector_extractor_voltage', data.get('extractor_voltage'))
        backend.addValue('detector_work_distance', data.get('work_distance'))
        backend.addArrayValues('detector_lens_names', np.array(re.findall(r"[\w']+", data.get('lens_names'))))
        backend.addArrayValues('detector_lens_voltages', np.array(data.get('lens_voltages')))
        backend.addValue('detector_tof_distance', data.get('tof_distance'))
        backend.addArrayValues('detector_tof_voltages', np.array(data.get('tof_voltages')))
        backend.addValue('detector_sample_bias', data.get('sample_bias'))
        backend.addValue('detector_magnification', data.get('magnification'))
        backend.addArrayValues('detector_voltages', np.array(data.get('detector_voltages')))
        backend.addValue('detector_type', data.get('detector_type'))
        backend.addArrayValues('detector_sensor_size', np.array(data.get('sensor_size')))
        backend.addValue('detector_sensor_count', data.get('sensor_count'))
        backend.addArrayValues('detector_sensor_pixel_size', np.array(data.get('sensor_pixel_size')))
        backend.addArrayValues('detector_calibration_x_to_momentum', np.array(data.get('calibration_x_to_momentum')))
        backend.addArrayValues('detector_calibration_y_to_momentum', np.array(data.get('calibration_y_to_momentum')))
        backend.addArrayValues('detector_calibration_tof_to_energy', np.array(data.get('calibration_tof_to_energy')))
        backend.addArrayValues('detector_calibration_stage_to_delay', np.array(data.get('calibration_stage_to_delay')))
        backend.addArrayValues('detector_calibration_other_converts', np.array(data.get('calibration_other_converts')))
        backend.addArrayValues('detector_momentum_resolution', np.array(data.get('momentum_resolution')))
        backend.addArrayValues('detector_spatial_resolution', np.array(data.get('spatial_resolution')))
        backend.addArrayValues('detector_energy_resolution', np.array(data.get('energy_resolution')))

        backend.closeSection('section_method', method_gid)

        # Read parameters related to sample
        sample_gid = backend.openSection('section_sample')
        backend.addValue('sample_description', data.get('sample_description'))
        backend.addValue('sample_id', data.get('sample_id'))
        backend.addValue('sample_state_of_matter', data.get('sample_state'))
        backend.addValue('sample_purity', data.get('sample_purity'))
        backend.addValue('sample_surface_termination', data.get('sample_surface_termination'))
        backend.addValue('sample_layers', data.get('sample_layers'))
        backend.addValue('sample_stacking_order', data.get('sample_stacking_order'))
        backend.addValue('sample_space_group', data.get('sample_space_group'))
        backend.addValue('sample_chemical_name', data.get('chemical_name'))
        backend.addValue('sample_chemical_formula', data.get('chemical_formula'))
        # backend.addArrayValues('sample_chemical_elements', np.array(re.findall(r"[\w']+", data.get('chemical_elements'))))
        atoms = set(ase.Atoms(data.get('chemical_formula')).get_chemical_symbols())
        backend.addArrayValues('sample_atom_labels', np.array(list(atoms)))
        backend.addValue('sample_chemical_id_cas', data.get('chemical_id_cas'))
        backend.addValue('sample_temperature', data.get('sample_temperature'))
        backend.addValue('sample_pressure', data.get('sample_pressure'))
        backend.addValue('sample_growth_method', data.get('growth_method'))
        backend.addValue('sample_preparation_method', data.get('preparation_method'))
        backend.addValue('sample_vendor', data.get('sample_vendor'))
        backend.addValue('sample_substrate_material', data.get('substrate_material'))
        backend.addValue('sample_substrate_state_of_matter', data.get('substrate_state'))
        backend.addValue('sample_substrate_vendor', data.get('substrate_vendor'))

        # TODO sample classification
        backend.addValue('sample_microstructure', 'bulk sample, polycrystalline')
        backend.addValue('sample_constituents', 'multi phase')

        backend.closeSection('section_sample', sample_gid)

        # Close sections in the reverse order
        # backend.closeSection('section_data', data_gid)
        # backend.closeSection('section_experiment_general_parameters', general_gid)
        # backend.closeSection('section_experiment_source_parameters', source_gid)
        # backend.closeSection('section_experiment_detector_parameters', detector_gid)
        # backend.closeSection('section_experiment_sample_parameters', sample_gid)
        backend.closeSection('section_experiment', root_gid)
