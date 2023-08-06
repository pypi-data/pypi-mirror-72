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
import numpy as np
from datetime import datetime
import time
import ast
import logging

from nomadcore.simple_parser import SimpleMatcher
from nomadcore.baseclasses import ParserInterface, AbstractBaseParser

from .hyper2json import transform as read_hyper


logger = logging.getLogger(__name__)


class EelsParserInterface(ParserInterface):

    def get_metainfo_filename(self):
        """
        The parser specific metainfo. To include other metadata definitions, use
        the 'dependencies' key to refer to other local nomadmetainfo.json files or
        to nomadmetainfo.json files that are part of the general nomad-meta-info
        submodule (i.e. ``dependencies/nomad-meta-info``).
         """
        return os.path.join(os.path.dirname(__file__), 'eels.nomadmetainfo.json')

    def get_parser_info(self):
        """ Basic info about parser used in archive data and logs. """
        return {
            'name': 'eels parser',
            'version': '1.0.0'
        }

    def setup_version(self):
        """ Can be used to call :func:`setup_main_parser` differently for different code versions. """
        self.setup_main_parser(None)

    def setup_main_parser(self, _):
        """ Setup the actual parser (behind this interface) """
        self.main_parser = EelsParser(self.parser_context)


class EelsParser(AbstractBaseParser):
    def parse(self, filepath):
        backend = self.parser_context.super_backend

        try:
            data = read_hyper(filepath)
        except Exception as e:
            logger.error('could not read mainfile', exc_info=e)
            raise e

        a_gid = backend.openSection('section_experiment')
        backend.addValue('experiment_summary', 'EELS-Spectra')
        backend.addValue('experiment_location', 'Earth')

        try:
            dt_string = data.get('published')
            dt_object = datetime.strptime(dt_string, "%Y-%m-%d %H:%M:%S")
            backend.addValue('experiment_time', int(time.mktime(dt_object.timetuple())))
        except ValueError as e:
            logger.warn('Wrong time format in start time!', exc_info=e)
            dt_string = data.get('published')
            backend.addValue('start_time', dt_string)
        except Exception as e:
            logger.warn('Some error occured transforming the time.', exc_info=e)
            dt_string = data.get('published')
            backend.addValue('start_time', dt_string)

        backend.addValue('spectrum_type', data.get('type'))
        backend.addValue('title', data.get('title'))

        af_gid = backend.openSection('section_user')
        backend.addValue('username', data.get('author').get('name'))
        backend.addValue('profile_api_url', data.get('author').get('profile_api_url'))
        backend.addValue('profile_url', data.get('author').get('profile_url'))
        backend.closeSection('section_user', af_gid)

        ag_gid = backend.openSection('section_method')
        backend.addValue('experiment_method_name', 'Electron Energy Loss Spectroscopy')
        backend.addValue('probing_method', 'electrons')
        backend.closeSection('section_method', ag_gid)

        ad_gid = backend.openSection('section_sample')
        backend.addArrayValues('sample_atom_labels', np.asarray(ast.literal_eval(data.get('elements'))))
        backend.addValue('sample_chemical_formula', data.get('formula'))
        temp = data.get('probesize')
        #unfortunately necessary because not every dataset contains this information
        if temp is not None:
            split = temp.find(' ')
            temp1 = temp[:split]
            backend.addValue('probe_size', float(temp1))
        #test = data.get('source_purity')
        #print(type(test))
        backend.addValue('source_purity', data.get('source_purity'))
        backend.closeSection('section_sample', ad_gid)

        ab_gid = backend.openSection('section_em')
        backend.addValue('name_em', data.get('microscope'))
        backend.addValue('gun_type', data.get('guntype'))
        backend.addValue('acquisition_mode', data.get('acquisition_mode'))
        temp = data.get('convergence')
        if temp is not None:
            split = temp.find(' ')
            temp1 = temp[:split]
            backend.addValue('convergence_semi_angle', float(temp1))
        temp = data.get('collection')
        if temp is not None:
            split = temp.find(' ')
            temp1 = temp[:split]
            backend.addValue('collection_semi_angle', float(temp1))
        backend.addValue('detector', data.get('detector'))
        temp = data.get('integratetime')
        if temp is not None:
            split = temp.find(' ')
            temp1 = temp[:split]
            backend.addValue('integration_time', float(temp1))
        temp = data.get('readouts')
        if temp is not None:
            backend.addValue('readouts', int(temp))
        temp = data.get('darkcurrent')
        temp1 = False
        if temp is not None:
            if(temp == 'Yes'):
                temp1 = True
        backend.addValue('dark_current_correction', temp1)
        temp = data.get('gainvariation')
        temp1 = False
        if temp is not None:
            if(temp == 'Yes'):
                temp1 = True
        backend.addValue('gain_variation_spectrum', temp1)
        temp = data.get('thickness')
        if temp is not None:
            split = temp.find(' ')
            temp1 = temp[:split]
            backend.addValue('relative_thickness', float(temp1))

        ae_gid = backend.openSection('section_source1')
        temp = data.get('beamenergy')
        if temp is not None:
            split = temp.find(' ')
            temp1 = temp[:split]
            backend.addValue('incident_energy', float(temp1))
        temp = data.get('resolution')
        if temp is not None:
            split = temp.find(' ')
            temp1 = temp[:split]
            backend.addValue('resolution', float(temp1))
        temp = data.get('stepSize')
        if temp is not None:
            split = temp.find(' ')
            temp1 = temp[:split]
            backend.addValue('dispersion', float(temp1))
        temp = data.get('monochromated')
        temp1 = False
        if temp is not None:
            if(temp == 'Yes'):
                temp1 = True
        backend.addValue('monochromated', temp1)
        backend.closeSection('section_source1', ae_gid)
        backend.closeSection('section_em', ab_gid)

        ac_gid = backend.openSection('section_data')
        backend.addValue('id', int(data.get('id')))
        backend.addValue('edges', data.get('edges'))
        temp = data.get('min_energy')
        if temp is not None:
            split = temp.find(' ')
            temp1 = temp[:split]
            backend.addValue('min_energy', float(temp1))
        temp = data.get('max_energy')
        if temp is not None:
            split = temp.find(' ')
            temp1 = temp[:split]
            backend.addValue('max_energy', float(temp1))
        temp1 = data.get('description')
        for i in range(3):
            j=i+1
            temp0 = 'additionalInformation' + str(j)
            temp = data.get(temp0)
            if temp is not None:
                temp1 = temp1 + ', ' + temp
        temp = data.get('keywords')
        if temp is not None:
            temp1 = temp1 + ', ' + temp
        backend.addValue('description', temp1)
        backend.addValue('data_repository_name', 'EELS-DB')
        backend.addValue('data_repository_url', data.get('download_link'))
        backend.addValue('data_preview_url', data.get('download_link'))
        backend.addValue('entry_repository_url', data.get('permalink'))
        backend.addValue('published', data.get('published'))
        backend.addValue('permalink', data.get('permalink'))
        backend.addValue('api_permalink', data.get('api_permalink'))
        backend.addValue('other_links', data.get('other_links'))
        if data.get('comment_count') is not None:
            backend.addValue('comment_count', int(data.get('comment_count')))
        backend.addValue('associated_spectra', data.get('associated_spectra'))
        tempref = data.get('reference')
        if tempref is not None:
            ag_gid = backend.openSection('section_reference')
            backend.addValue('authors', tempref.get('authors'))
            backend.addValue('doi', tempref.get('doi'))
            backend.addValue('issue', tempref.get('issue'))
            backend.addValue('journal', tempref.get('journal'))
            backend.addValue('page', tempref.get('page'))
            backend.addValue('title_ref', tempref.get('title'))
            backend.addValue('url', tempref.get('url'))
            backend.addValue('volume', tempref.get('volume'))
            backend.addValue('year', tempref.get('year'))
            temp1 = tempref.get('freetext')
            for i in range(2):
                j=i+4
                temp0 = 'additionalInformation' + str(j)
                temp = tempref.get(temp0)
                if temp is not None:
                    temp1 = temp1 + ', ' + temp
            backend.addValue('freetext', temp1)
            backend.closeSection('section_reference', af_gid)
        backend.closeSection('section_data', ac_gid)

        backend.closeSection('section_experiment', a_gid)
