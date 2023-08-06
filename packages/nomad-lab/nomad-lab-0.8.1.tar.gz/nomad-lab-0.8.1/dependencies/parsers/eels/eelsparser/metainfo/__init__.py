import sys
from nomad.metainfo import Environment
from nomad.metainfo.legacy import LegacyMetainfoEnvironment
import eelsparser.metainfo.eels
import nomad.datamodel.metainfo.general
import nomad.datamodel.metainfo.general_experimental_method
import nomad.datamodel.metainfo.general_experimental
import nomad.datamodel.metainfo.general_experimental_sample
import nomad.datamodel.metainfo.general_experimental_data

m_env = LegacyMetainfoEnvironment()
m_env.m_add_sub_section(Environment.packages, sys.modules['eelsparser.metainfo.eels'].m_package)  # type: ignore
m_env.m_add_sub_section(Environment.packages, sys.modules['nomad.datamodel.metainfo.general'].m_package)  # type: ignore
m_env.m_add_sub_section(Environment.packages, sys.modules['nomad.datamodel.metainfo.general_experimental_method'].m_package)  # type: ignore
m_env.m_add_sub_section(Environment.packages, sys.modules['nomad.datamodel.metainfo.general_experimental'].m_package)  # type: ignore
m_env.m_add_sub_section(Environment.packages, sys.modules['nomad.datamodel.metainfo.general_experimental_sample'].m_package)  # type: ignore
m_env.m_add_sub_section(Environment.packages, sys.modules['nomad.datamodel.metainfo.general_experimental_data'].m_package)  # type: ignore
