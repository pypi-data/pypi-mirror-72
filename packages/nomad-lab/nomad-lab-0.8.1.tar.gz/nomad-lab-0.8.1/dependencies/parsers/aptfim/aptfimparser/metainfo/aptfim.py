import numpy as np            # pylint: disable=unused-import
import typing                 # pylint: disable=unused-import
from nomad.metainfo import (  # pylint: disable=unused-import
    MSection, MCategory, Category, Package, Quantity, Section, SubSection, SectionProxy,
    Reference
)
from nomad.metainfo.legacy import LegacyDefinition

from nomad.datamodel.metainfo import general_experimental

m_package = Package(
    name='aptfim_nomadmetainfo_json',
    description='None',
    a_legacy=LegacyDefinition(name='aptfim.nomadmetainfo.json'))


class section_experiment(general_experimental.section_experiment):

    m_def = Section(validate=False, extends_base_section=True, a_legacy=LegacyDefinition(name='section_experiment'))

    none_shape = Quantity(
        type=int,
        shape=[],
        description='''
        Shape of the None/Null object
        ''',
        a_legacy=LegacyDefinition(name='none_shape'))

    experiment_tool_info = Quantity(
        type=str,
        shape=[],
        unit='dimensionless',
        description='''
        Name of the equipment, instrument with which the experiment was performed e.g.
        LEAP5000XS
        ''',
        a_legacy=LegacyDefinition(name='experiment_tool_info'))

    experiment_operation_method = Quantity(
        type=str,
        shape=[],
        unit='dimensionless',
        description='''
        Operation mode of the instrument (APT, FIM or combination)
        ''',
        a_legacy=LegacyDefinition(name='experiment_operation_method'))

    experiment_imaging_method = Quantity(
        type=str,
        shape=[],
        unit='dimensionless',
        description='''
        Pulsing method to enforce a controlled ion evaporation sequence
        ''',
        a_legacy=LegacyDefinition(name='experiment_imaging_method'))

    specimen_description = Quantity(
        type=str,
        shape=[],
        unit='dimensionless',
        description='''
        Sample description e.g. pure W wire samples trial 2
        ''',
        a_legacy=LegacyDefinition(name='specimen_description'))

    number_of_disjoint_elements = Quantity(
        type=int,
        shape=[],
        unit='dimensionless',
        description='''
        Number of elements (disjoint element names) expected
        ''',
        a_legacy=LegacyDefinition(name='number_of_disjoint_elements'))

    specimen_chemistry = Quantity(
        type=str,
        shape=['number_of_elements'],
        unit='dimensionless',
        description='''
        List of periodic table names expected contained in dataset
        ''',
        a_legacy=LegacyDefinition(name='specimen_chemistry'))

    specimen_microstructure = Quantity(
        type=str,
        shape=[],
        unit='dimensionless',
        description='''
        Qualitative type of specimen and microstructure analyzed (e.g. thin films, nano
        objects, single crystal, polycrystal)
        ''',
        a_legacy=LegacyDefinition(name='specimen_microstructure'))

    specimen_constitution = Quantity(
        type=str,
        shape=[],
        unit='dimensionless',
        description='''
        Qualitative information how many phases in the specimen
        ''',
        a_legacy=LegacyDefinition(name='specimen_constitution'))

    measured_number_ions_evaporated = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        unit='dimensionless',
        description='''
        Number of ions successfully evaporated
        ''',
        a_legacy=LegacyDefinition(name='measured_number_ions_evaporated'))

    measured_detector_hit_pos = Quantity(
        type=str,
        shape=[],
        unit='millimeter ** 2',
        description='''
        Detector hit positions x and y
        ''',
        a_legacy=LegacyDefinition(name='measured_detector_hit_pos'))

    measured_detector_hit_mult = Quantity(
        type=str,
        shape=[],
        unit='dimensionless',
        description='''
        Detector hit multiplicity
        ''',
        a_legacy=LegacyDefinition(name='measured_detector_hit_mult'))

    measured_detector_dead_pulses = Quantity(
        type=str,
        shape=[],
        unit='dimensionless',
        description='''
        Detector number of dead pulses
        ''',
        a_legacy=LegacyDefinition(name='measured_detector_dead_pulses'))

    measured_time_of_flight = Quantity(
        type=str,
        shape=[],
        unit='nanosecond',
        description='''
        Raw ion time of flight
        ''',
        a_legacy=LegacyDefinition(name='measured_time_of_flight'))

    measured_standing_voltage = Quantity(
        type=str,
        shape=[],
        unit='volt',
        description='''
        Standing voltage
        ''',
        a_legacy=LegacyDefinition(name='measured_standing_voltage'))

    measured_pulse_voltage = Quantity(
        type=str,
        shape=[],
        unit='volt',
        description='''
        Pulse voltage
        ''',
        a_legacy=LegacyDefinition(name='measured_pulse_voltage'))


m_package.__init_metainfo__()
