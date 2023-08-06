import numpy as np            # pylint: disable=unused-import
import typing                 # pylint: disable=unused-import
from nomad.metainfo import (  # pylint: disable=unused-import
    MSection, MCategory, Category, Package, Quantity, Section, SubSection, SectionProxy,
    Reference
)
from nomad.metainfo.legacy import LegacyDefinition

from nomad.datamodel.metainfo import general_experimental
from nomad.datamodel.metainfo import general_experimental_method
from nomad.datamodel.metainfo import general_experimental_sample

m_package = Package(
    name='mpes_nomadmetainfo_json',
    description='None',
    a_legacy=LegacyDefinition(name='mpes.nomadmetainfo.json'))


class section_experiment(general_experimental.section_experiment):

    m_def = Section(validate=False, extends_base_section=True, a_legacy=LegacyDefinition(name='section_experiment'))

    none_shape = Quantity(
        type=int,
        shape=[],
        description='''
        Shape of the None/Null object
        ''',
        a_legacy=LegacyDefinition(name='none_shape'))

    number_of_location_names = Quantity(
        type=int,
        shape=[],
        description='''
        Number of name segments in the experiment location
        ''',
        a_legacy=LegacyDefinition(name='number_of_location_names'))


class section_method(general_experimental_method.section_method):

    m_def = Section(validate=False, extends_base_section=True, a_legacy=LegacyDefinition(name='section_method'))

    general_beamline = Quantity(
        type=str,
        shape=[],
        unit='dimensionless',
        description='''
        Name of the beamline the experiment took place.
        ''',
        a_legacy=LegacyDefinition(name='general_beamline'))

    general_source_pump = Quantity(
        type=str,
        shape=[],
        unit='dimensionless',
        description='''
        Name or model of the pump light source.
        ''',
        a_legacy=LegacyDefinition(name='general_source_pump'))

    general_source_probe = Quantity(
        type=str,
        shape=[],
        unit='dimensionless',
        description='''
        Name or model of the probe light source.
        ''',
        a_legacy=LegacyDefinition(name='general_source_probe'))

    number_of_axes = Quantity(
        type=int,
        shape=[],
        description='''
        Number of axes in the measurement hardware.
        ''',
        a_legacy=LegacyDefinition(name='number_of_axes'))

    general_measurement_axis = Quantity(
        type=str,
        shape=['number_of_axes'],
        unit='dimensionless',
        description='''
        Names of the axes in the measurement hardware.
        ''',
        a_legacy=LegacyDefinition(name='general_measurement_axis'))

    general_physical_axis = Quantity(
        type=str,
        shape=['number_of_axes'],
        unit='dimensionless',
        description='''
        Names of the axes in physical terms.
        ''',
        a_legacy=LegacyDefinition(name='general_physical_axis'))

    source_pump_repetition_rate = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='hertz',
        description='''
        Repetition rate of the pump source.
        ''',
        a_legacy=LegacyDefinition(name='source_pump_repetition_rate'))

    source_pump_pulse_duration = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='femtosecond',
        description='''
        Pulse duration of the pump source.
        ''',
        a_legacy=LegacyDefinition(name='source_pump_pulse_duration'))

    source_pump_wavelength = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='nanometer',
        description='''
        Center wavelength of the pump source.
        ''',
        a_legacy=LegacyDefinition(name='source_pump_wavelength'))

    source_pump_spectrum = Quantity(
        type=np.dtype(np.float64),
        shape=['length_of_spectrum'],
        unit='dimensionless',
        description='''
        Spectrum of the pump source.
        ''',
        a_legacy=LegacyDefinition(name='source_pump_spectrum'))

    source_pump_photon_energy = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='electron_volt',
        description='''
        Photon energy of the pump source.
        ''',
        a_legacy=LegacyDefinition(name='source_pump_photon_energy'))

    source_pump_size = Quantity(
        type=np.dtype(np.float64),
        shape=['none_shape'],
        unit='millimeter ** 2',
        description='''
        Full-width at half-maximum (FWHM) of the pump source size at or closest to the
        sample position.
        ''',
        a_legacy=LegacyDefinition(name='source_pump_size'))

    source_pump_fluence = Quantity(
        type=np.dtype(np.float64),
        shape=['none_shape'],
        unit='millijoule / millimeter ** 2',
        description='''
        Fluence of the pump source at or closest to the sample position.
        ''',
        a_legacy=LegacyDefinition(name='source_pump_fluence'))

    source_pump_polarization = Quantity(
        type=str,
        shape=[],
        unit='dimensionless',
        description='''
        Polarization of the pump source.
        ''',
        a_legacy=LegacyDefinition(name='source_pump_polarization'))

    source_pump_bunch = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        unit='dimensionless',
        description='''
        Total bunch number of the pump source.
        ''',
        a_legacy=LegacyDefinition(name='source_pump_bunch'))

    source_probe_repetition_rate = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='hertz',
        description='''
        Repetition rate of the probe source.
        ''',
        a_legacy=LegacyDefinition(name='source_probe_repetition_rate'))

    source_probe_pulse_duration = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='femtosecond',
        description='''
        Pulse duration of the probe source.
        ''',
        a_legacy=LegacyDefinition(name='source_probe_pulse_duration'))

    source_probe_wavelength = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='nanometer',
        description='''
        Center wavelength of the probe source.
        ''',
        a_legacy=LegacyDefinition(name='source_probe_wavelength'))

    length_of_spectrum = Quantity(
        type=int,
        shape=[],
        description='''
        Number of pixel elements in the spectrum.
        ''',
        a_legacy=LegacyDefinition(name='length_of_spectrum'))

    source_probe_spectrum = Quantity(
        type=np.dtype(np.float64),
        shape=['length_of_spectrum'],
        unit='dimensionless',
        description='''
        Spectrum of the probe source.
        ''',
        a_legacy=LegacyDefinition(name='source_probe_spectrum'))

    source_probe_photon_energy = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='electron_volt',
        description='''
        Photon energy of the probe source.
        ''',
        a_legacy=LegacyDefinition(name='source_probe_photon_energy'))

    source_probe_size = Quantity(
        type=np.dtype(np.float64),
        shape=['none_shape'],
        unit='millimeter ** 2',
        description='''
        Full-width at half-maximum (FWHM) of the probe source size at or closest to the
        sample position.
        ''',
        a_legacy=LegacyDefinition(name='source_probe_size'))

    source_probe_fluence = Quantity(
        type=np.dtype(np.float64),
        shape=['none_shape'],
        unit='millijoule / millimeter ** 2',
        description='''
        Fluence of the probe source at or closest to the sample position.
        ''',
        a_legacy=LegacyDefinition(name='source_probe_fluence'))

    source_probe_polarization = Quantity(
        type=str,
        shape=[],
        unit='dimensionless',
        description='''
        Polarization of the probe source.
        ''',
        a_legacy=LegacyDefinition(name='source_probe_polarization'))

    source_probe_bunch = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        unit='dimensionless',
        description='''
        Total bunch number of the probe source.
        ''',
        a_legacy=LegacyDefinition(name='source_probe_bunch'))

    source_temporal_resolution = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='femtosecond',
        description='''
        Full-width at half-maximum (FWHM) of the pump-probe cross-correlation function.
        ''',
        a_legacy=LegacyDefinition(name='source_temporal_resolution'))

    detector_extractor_voltage = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='volt',
        description='''
        Voltage between the extractor and the sample.
        ''',
        a_legacy=LegacyDefinition(name='detector_extractor_voltage'))

    detector_work_distance = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='millimeter',
        description='''
        Distance between the sample and the detector entrance.
        ''',
        a_legacy=LegacyDefinition(name='detector_work_distance'))

    number_of_lenses = Quantity(
        type=int,
        shape=[],
        description='''
        Number of electron lenses in the electron detector.
        ''',
        a_legacy=LegacyDefinition(name='number_of_lenses'))

    detector_lens_names = Quantity(
        type=str,
        shape=['number_of_lenses'],
        unit='dimensionless',
        description='''
        Set of names for the electron-optic lenses.
        ''',
        a_legacy=LegacyDefinition(name='detector_lens_names'))

    detector_lens_voltages = Quantity(
        type=np.dtype(np.float64),
        shape=['number_of_lenses'],
        unit='volt',
        description='''
        Set of electron-optic lens voltages.
        ''',
        a_legacy=LegacyDefinition(name='detector_lens_voltages'))

    detector_tof_distance = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='meter',
        description='''
        Drift distance of the time-of-flight tube.
        ''',
        a_legacy=LegacyDefinition(name='detector_tof_distance'))

    number_of_tof_voltages = Quantity(
        type=int,
        shape=[],
        description='''
        Number of time-of-flight (TOF) drift tube voltage values in the electron detector.
        ''',
        a_legacy=LegacyDefinition(name='number_of_tof_voltages'))

    detector_tof_voltages = Quantity(
        type=np.dtype(np.float64),
        shape=['number_of_tof_voltages'],
        unit='volt',
        description='''
        Voltage applied to the time-of-flight tube.
        ''',
        a_legacy=LegacyDefinition(name='detector_tof_voltages'))

    detector_sample_bias = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='volt',
        description='''
        Voltage bias applied to sample.
        ''',
        a_legacy=LegacyDefinition(name='detector_sample_bias'))

    detector_magnification = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='dimensionless',
        description='''
        Detector magnification.
        ''',
        a_legacy=LegacyDefinition(name='detector_magnification'))

    number_of_detector_voltages = Quantity(
        type=int,
        shape=[],
        description='''
        Number of detector voltage settings in the electron detector.
        ''',
        a_legacy=LegacyDefinition(name='number_of_detector_voltages'))

    detector_voltages = Quantity(
        type=np.dtype(np.float64),
        shape=['number_of_detector_voltages'],
        unit='volt',
        description='''
        Voltage applied to detector.
        ''',
        a_legacy=LegacyDefinition(name='detector_voltages'))

    detector_type = Quantity(
        type=str,
        shape=[],
        unit='dimensionless',
        description='''
        Description of the detector type (e.g. ‘MCP’, ‘CCD’, ‘CMOS’, etc.).
        ''',
        a_legacy=LegacyDefinition(name='detector_type'))

    number_of_sensor_sizes = Quantity(
        type=int,
        shape=[],
        description='''
        Number of detector sensor size dimensions (depending on the number of sensors).
        ''',
        a_legacy=LegacyDefinition(name='number_of_sensor_sizes'))

    detector_sensor_size = Quantity(
        type=np.dtype(np.float64),
        shape=['number_of_sensor_sizes'],
        unit='millimeter',
        description='''
        Size of each of the imaging sensor chip on the detector.
        ''',
        a_legacy=LegacyDefinition(name='detector_sensor_size'))

    detector_sensor_count = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        unit='dimensionless',
        description='''
        Number of imaging sensor chips on the detector.
        ''',
        a_legacy=LegacyDefinition(name='detector_sensor_count'))

    detector_sensor_pixel_size = Quantity(
        type=np.dtype(np.float64),
        shape=['none_shape'],
        unit='micrometer',
        description='''
        Pixel size of the imaging sensor chip on the detector.
        ''',
        a_legacy=LegacyDefinition(name='detector_sensor_pixel_size'))

    number_of_momentum_calibration_coefficients = Quantity(
        type=int,
        shape=[],
        description='''
        Number of the momentum calibration parameters for the detector.
        ''',
        a_legacy=LegacyDefinition(name='number_of_momentum_calibration_coefficients'))

    detector_calibration_x_to_momentum = Quantity(
        type=np.dtype(np.float64),
        shape=['number_of_momentum_calibration_coefficients'],
        unit='1 / angstrom',
        description='''
        Pixel x axis to kx momentum calibration.
        ''',
        a_legacy=LegacyDefinition(name='detector_calibration_x_to_momentum'))

    detector_calibration_y_to_momentum = Quantity(
        type=np.dtype(np.float64),
        shape=['number_of_momentum_calibration_coefficients'],
        unit='1 / angstrom',
        description='''
        Pixel y axis to ky momentum calibration.
        ''',
        a_legacy=LegacyDefinition(name='detector_calibration_y_to_momentum'))

    number_of_energy_calibration_coefficients = Quantity(
        type=int,
        shape=[],
        description='''
        Number of the energy calibration parameters for the detector.
        ''',
        a_legacy=LegacyDefinition(name='number_of_energy_calibration_coefficients'))

    detector_calibration_tof_to_energy = Quantity(
        type=np.dtype(np.float64),
        shape=['number_of_energy_calibration_coefficients'],
        unit='electron_volt',
        description='''
        Time-of-flight to energy calibration.
        ''',
        a_legacy=LegacyDefinition(name='detector_calibration_tof_to_energy'))

    detector_calibration_stage_to_delay = Quantity(
        type=np.dtype(np.float64),
        shape=['number_of_delay_calibration_coefficients'],
        unit='femtosecond',
        description='''
        Translation stage position to pump-probe delay calibration.
        ''',
        a_legacy=LegacyDefinition(name='detector_calibration_stage_to_delay'))

    number_of_other_calibration_coefficients = Quantity(
        type=int,
        shape=[],
        description='''
        Number of the other calibration parameters for the detector.
        ''',
        a_legacy=LegacyDefinition(name='number_of_other_calibration_coefficients'))

    detector_calibration_other_converts = Quantity(
        type=np.dtype(np.float64),
        shape=['number_of_other_calibration_coefficients'],
        unit='dimensionless',
        description='''
        Conversion factor between other measured and physical axes.
        ''',
        a_legacy=LegacyDefinition(name='detector_calibration_other_converts'))

    detector_momentum_resolution = Quantity(
        type=np.dtype(np.float64),
        shape=['none_shape'],
        unit='1 / angstrom',
        description='''
        Momentum resolution of the detector.
        ''',
        a_legacy=LegacyDefinition(name='detector_momentum_resolution'))

    detector_spatial_resolution = Quantity(
        type=np.dtype(np.float64),
        shape=['none_shape'],
        unit='micrometer',
        description='''
        Spatial resolution of the source.
        ''',
        a_legacy=LegacyDefinition(name='detector_spatial_resolution'))

    detector_energy_resolution = Quantity(
        type=np.dtype(np.float64),
        shape=['none_shape'],
        unit='electron_volt',
        description='''
        Energy resolution of the detector.
        ''',
        a_legacy=LegacyDefinition(name='detector_energy_resolution'))


class section_sample(general_experimental_sample.section_sample):

    m_def = Section(validate=False, extends_base_section=True, a_legacy=LegacyDefinition(name='section_sample'))

    sample_state_of_matter = Quantity(
        type=str,
        shape=[],
        unit='dimensionless',
        description='''
        Physical state of the sample.
        ''',
        a_legacy=LegacyDefinition(name='sample_state_of_matter'))

    sample_purity = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='dimensionless',
        description='''
        Chemical purity of the sample.
        ''',
        a_legacy=LegacyDefinition(name='sample_purity'))

    sample_surface_termination = Quantity(
        type=str,
        shape=[],
        unit='dimensionless',
        description='''
        Surface termination of the sample (if crystalline).
        ''',
        a_legacy=LegacyDefinition(name='sample_surface_termination'))

    sample_layers = Quantity(
        type=str,
        shape=[],
        unit='dimensionless',
        description='''
        Sample layer or bulk structure.
        ''',
        a_legacy=LegacyDefinition(name='sample_layers'))

    sample_stacking_order = Quantity(
        type=str,
        shape=[],
        unit='dimensionless',
        description='''
        Stacking order of the solid surface (if crystalline).
        ''',
        a_legacy=LegacyDefinition(name='sample_stacking_order'))

    sample_chemical_id_cas = Quantity(
        type=str,
        shape=[],
        unit='dimensionless',
        description='''
        CAS registry number of the sample’s chemical content.
        ''',
        a_legacy=LegacyDefinition(name='sample_chemical_id_cas'))

    sample_pressure = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='pascal',
        description='''
        Pressure surrounding the sample at the time of measurement.
        ''',
        a_legacy=LegacyDefinition(name='sample_pressure'))

    sample_growth_method = Quantity(
        type=str,
        shape=[],
        unit='dimensionless',
        description='''
        Sample growth method.
        ''',
        a_legacy=LegacyDefinition(name='sample_growth_method'))

    sample_preparation_method = Quantity(
        type=str,
        shape=[],
        unit='dimensionless',
        description='''
        Sample preparation method.
        ''',
        a_legacy=LegacyDefinition(name='sample_preparation_method'))

    sample_vendor = Quantity(
        type=str,
        shape=[],
        unit='dimensionless',
        description='''
        Name of the sample vendor.
        ''',
        a_legacy=LegacyDefinition(name='sample_vendor'))

    sample_substrate_material = Quantity(
        type=str,
        shape=[],
        unit='dimensionless',
        description='''
        Material of the substrate the sample has immediate contact with.
        ''',
        a_legacy=LegacyDefinition(name='sample_substrate_material'))

    sample_substrate_state_of_matter = Quantity(
        type=str,
        shape=[],
        unit='dimensionless',
        description='''
        State of matter of the substrate material.
        ''',
        a_legacy=LegacyDefinition(name='sample_substrate_state_of_matter'))

    sample_substrate_vendor = Quantity(
        type=str,
        shape=[],
        unit='dimensionless',
        description='''
        Name of the substrate vendor.
        ''',
        a_legacy=LegacyDefinition(name='sample_substrate_vendor'))


m_package.__init_metainfo__()
