# Copyright 2016-2018 R. Patrick Xian
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

from nomadcore.simple_parser import SimpleMatcher
from nomadcore.baseclasses import ParserInterface, AbstractBaseParser

from nomad.parsing import LocalBackend


class PhotoemissionParserInterface(ParserInterface):

    def get_metainfo_filename(self):
        """ The parser specific metainfo. This file must be part of the nomad-meta-info. """
        return os.path.join(os.path.dirname(__file__), 'photoemission.nomadmetainfo.json')

    def get_parser_info(self):
        """ Basic info about parser used in archive data and logs. """
        return {
            'name': 'vaspoutcar_parser',
            'version': '1.0.0'
        }

    def setup_version(self):
        """ Can be used to call :func:`setup_main_parser` differently for different code versions. """
        self.setup_main_parser(None)

    def setup_main_parser(self, _):
        """ Setup the actual parser (behind this interface) """
        self.main_parser = PhotoemissionParser(self.parser_context)


class PhotoemissionParser(AbstractBaseParser):
    def parse(self, filepath):
        backend = self.parser_context.super_backend

        root_gid = backend.openSection('section_experiment')
        backend.addValue('experiment_location', 'here...')
        backend.closeSection('section_experiment', root_gid)
