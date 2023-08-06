import numpy as np            # pylint: disable=unused-import
import typing                 # pylint: disable=unused-import
from nomad.metainfo import (  # pylint: disable=unused-import
    MSection, MCategory, Category, Package, Quantity, Section, SubSection, SectionProxy,
    Reference
)
from nomad.metainfo.legacy import LegacyDefinition

from nomad.datamodel.metainfo import general_experimental
from nomad.datamodel.metainfo import general_experimental_sample

m_package = Package(
    name='eels_nomadmetainfo_json',
    description='None',
    a_legacy=LegacyDefinition(name='eels.nomadmetainfo.json'))


class section_user(MSection):
    '''
    Information about the user.
    '''

    m_def = Section(validate=False, a_legacy=LegacyDefinition(name='section_user'))

    username = Quantity(
        type=str,
        shape=[],
        a_legacy=LegacyDefinition(name='username'))

    email = Quantity(
        type=str,
        shape=[],
        a_legacy=LegacyDefinition(name='email'))

    profile_api_url = Quantity(
        type=str,
        shape=[],
        a_legacy=LegacyDefinition(name='profile_api_url'))

    profile_url = Quantity(
        type=str,
        shape=[],
        description='''
        Link to a website of the user
        ''',
        a_legacy=LegacyDefinition(name='profile_url'))

    role = Quantity(
        type=str,
        shape=[],
        a_legacy=LegacyDefinition(name='role'))

    telephone_number = Quantity(
        type=str,
        shape=[],
        a_legacy=LegacyDefinition(name='telephone_number'))


class section_em(MSection):
    '''
    Information about the instrument.
    '''

    m_def = Section(validate=False, a_legacy=LegacyDefinition(name='section_em'))

    name_em = Quantity(
        type=str,
        shape=[],
        description='''
        Name of the microscope
        ''',
        a_legacy=LegacyDefinition(name='name_em'))

    gun_type = Quantity(
        type=str,
        shape=[],
        a_legacy=LegacyDefinition(name='gun_type'))

    energy_filter_active = Quantity(
        type=bool,
        shape=[],
        a_legacy=LegacyDefinition(name='energy_filter_active'))

    instrument_attachments = Quantity(
        type=str,
        shape=[],
        description='''
        List of the possible instruments
        ''',
        a_legacy=LegacyDefinition(name='instrument_attachments'))

    instrument_attachments_active = Quantity(
        type=str,
        shape=[],
        description='''
        List of the activated instruments
        ''',
        a_legacy=LegacyDefinition(name='instrument_attachments_active'))

    instrument_base = Quantity(
        type=str,
        shape=[],
        a_legacy=LegacyDefinition(name='instrument_base'))

    instrument_location = Quantity(
        type=str,
        shape=[],
        a_legacy=LegacyDefinition(name='instrument_location'))

    instrument_manufacturer = Quantity(
        type=str,
        shape=[],
        a_legacy=LegacyDefinition(name='instrument_manufacturer'))

    monochromator_active = Quantity(
        type=bool,
        shape=[],
        a_legacy=LegacyDefinition(name='monochromator_active'))

    precession_active = Quantity(
        type=bool,
        shape=[],
        a_legacy=LegacyDefinition(name='precession_active'))

    calibration = Quantity(
        type=str,
        shape=[],
        description='''
        Description of the made calibration
        ''',
        a_legacy=LegacyDefinition(name='calibration'))

    projector_setting = Quantity(
        type=str,
        shape=[],
        a_legacy=LegacyDefinition(name='projector_setting'))

    short_name = Quantity(
        type=str,
        shape=[],
        a_legacy=LegacyDefinition(name='short_name'))

    detector = Quantity(
        type=str,
        shape=[],
        a_legacy=LegacyDefinition(name='detector'))

    readouts = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        description='''
        number of readouts
        ''',
        a_legacy=LegacyDefinition(name='readouts'))

    intergration_time = Quantity(
        type=str,
        shape=[],
        a_legacy=LegacyDefinition(name='intergration_time'))

    number_of_readouts = Quantity(
        type=str,
        shape=[],
        a_legacy=LegacyDefinition(name='number_of_readouts'))

    dark_current_correction = Quantity(
        type=bool,
        shape=[],
        a_legacy=LegacyDefinition(name='dark_current_correction'))

    gain_variation_spectrum = Quantity(
        type=bool,
        shape=[],
        a_legacy=LegacyDefinition(name='gain_variation_spectrum'))

    convergence_semi_angle = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='milliradian',
        a_legacy=LegacyDefinition(name='convergence_semi_angle'))

    convergence_angle = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='milliradian',
        a_legacy=LegacyDefinition(name='convergence_angle'))

    relative_thickness = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        in t/lambda
        ''',
        a_legacy=LegacyDefinition(name='relative_thickness'))

    collection_semi_angle = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='milliradian',
        a_legacy=LegacyDefinition(name='collection_semi_angle'))

    integration_time = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='second',
        a_legacy=LegacyDefinition(name='integration_time'))

    acquisition_mode = Quantity(
        type=str,
        shape=[],
        a_legacy=LegacyDefinition(name='acquisition_mode'))

    specimen_holder = Quantity(
        type=str,
        shape=[],
        a_legacy=LegacyDefinition(name='specimen_holder'))

    specimin_holder_manufacturer = Quantity(
        type=str,
        shape=[],
        a_legacy=LegacyDefinition(name='specimin_holder_manufacturer'))

    camera_length = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        a_legacy=LegacyDefinition(name='camera_length'))

    camera_pixel_size_axis1 = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        a_legacy=LegacyDefinition(name='camera_pixel_size_axis1'))

    camera_pixel_size_axis2 = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        a_legacy=LegacyDefinition(name='camera_pixel_size_axis2'))

    pixel_size_axis1 = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='milliradian',
        a_legacy=LegacyDefinition(name='pixel_size_axis1'))

    pixel_size_axis2 = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='milliradian',
        a_legacy=LegacyDefinition(name='pixel_size_axis2'))

    conversion_factor = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        in counts per electron
        ''',
        a_legacy=LegacyDefinition(name='conversion_factor'))

    section_ap1 = SubSection(
        sub_section=SectionProxy('section_ap1'),
        repeats=True,
        a_legacy=LegacyDefinition(name='section_ap1'))

    section_ap2 = SubSection(
        sub_section=SectionProxy('section_ap2'),
        repeats=True,
        a_legacy=LegacyDefinition(name='section_ap2'))

    section_ap3 = SubSection(
        sub_section=SectionProxy('section_ap3'),
        repeats=True,
        a_legacy=LegacyDefinition(name='section_ap3'))

    section_ap4 = SubSection(
        sub_section=SectionProxy('section_ap4'),
        repeats=True,
        a_legacy=LegacyDefinition(name='section_ap4'))

    section_ap5 = SubSection(
        sub_section=SectionProxy('section_ap5'),
        repeats=True,
        a_legacy=LegacyDefinition(name='section_ap5'))

    section_ap6 = SubSection(
        sub_section=SectionProxy('section_ap6'),
        repeats=True,
        a_legacy=LegacyDefinition(name='section_ap6'))

    section_camera = SubSection(
        sub_section=SectionProxy('section_camera'),
        repeats=True,
        a_legacy=LegacyDefinition(name='section_camera'))

    section_source1 = SubSection(
        sub_section=SectionProxy('section_source1'),
        repeats=True,
        a_legacy=LegacyDefinition(name='section_source1'))


class section_ap1(MSection):
    '''
    Information about the first aperture.
    '''

    m_def = Section(validate=False, a_legacy=LegacyDefinition(name='section_ap1'))

    name_ap1 = Quantity(
        type=str,
        shape=[],
        a_legacy=LegacyDefinition(name='name_ap1'))

    position_ap1 = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        a_legacy=LegacyDefinition(name='position_ap1'))

    position_x_ap1 = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        a_legacy=LegacyDefinition(name='position_x_ap1'))

    position_y_ap1 = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        a_legacy=LegacyDefinition(name='position_y_ap1'))


class section_ap2(MSection):
    '''
    Information about the second aperture.
    '''

    m_def = Section(validate=False, a_legacy=LegacyDefinition(name='section_ap2'))

    name_ap2 = Quantity(
        type=str,
        shape=[],
        a_legacy=LegacyDefinition(name='name_ap2'))

    position_ap2 = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        a_legacy=LegacyDefinition(name='position_ap2'))

    position_x_ap2 = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        a_legacy=LegacyDefinition(name='position_x_ap2'))

    position_y_ap2 = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        a_legacy=LegacyDefinition(name='position_y_ap2'))


class section_ap3(MSection):
    '''
    Information about the third aperture.
    '''

    m_def = Section(validate=False, a_legacy=LegacyDefinition(name='section_ap3'))

    name_ap3 = Quantity(
        type=str,
        shape=[],
        a_legacy=LegacyDefinition(name='name_ap3'))

    position_ap3 = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        a_legacy=LegacyDefinition(name='position_ap3'))

    position_x_ap3 = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        a_legacy=LegacyDefinition(name='position_x_ap3'))

    position_y_ap3 = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        a_legacy=LegacyDefinition(name='position_y_ap3'))


class section_ap4(MSection):
    '''
    Information about the fourth aperture.
    '''

    m_def = Section(validate=False, a_legacy=LegacyDefinition(name='section_ap4'))

    name_ap4 = Quantity(
        type=str,
        shape=[],
        a_legacy=LegacyDefinition(name='name_ap4'))

    position_ap4 = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        a_legacy=LegacyDefinition(name='position_ap4'))

    position_x_ap4 = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        a_legacy=LegacyDefinition(name='position_x_ap4'))

    position_y_ap4 = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        a_legacy=LegacyDefinition(name='position_y_ap4'))


class section_ap5(MSection):
    '''
    Information about the fifth aperture.
    '''

    m_def = Section(validate=False, a_legacy=LegacyDefinition(name='section_ap5'))

    name_ap5 = Quantity(
        type=str,
        shape=[],
        a_legacy=LegacyDefinition(name='name_ap5'))

    position_ap5 = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        a_legacy=LegacyDefinition(name='position_ap5'))

    position_x_ap5 = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        a_legacy=LegacyDefinition(name='position_x_ap5'))

    position_y_ap5 = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        a_legacy=LegacyDefinition(name='position_y_ap5'))


class section_ap6(MSection):
    '''
    Information about the sixth aperture.
    '''

    m_def = Section(validate=False, a_legacy=LegacyDefinition(name='section_ap6'))

    name_ap6 = Quantity(
        type=str,
        shape=[],
        a_legacy=LegacyDefinition(name='name_ap6'))

    position_ap6 = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        a_legacy=LegacyDefinition(name='position_ap6'))

    position_x_ap6 = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        a_legacy=LegacyDefinition(name='position_x_ap6'))

    position_y_ap6 = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        a_legacy=LegacyDefinition(name='position_y_ap6'))


class section_camera(MSection):
    '''
    Information about the camera (detector).
    '''

    m_def = Section(validate=False, a_legacy=LegacyDefinition(name='section_camera'))

    bit_depth_readout = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        a_legacy=LegacyDefinition(name='bit_depth_readout'))

    cartesian_scan_dimensions = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        a_legacy=LegacyDefinition(name='cartesian_scan_dimensions'))

    cartesian_scan_dimension1_count = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        a_legacy=LegacyDefinition(name='cartesian_scan_dimension1_count'))

    cartesian_scan_dimension2_count = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        a_legacy=LegacyDefinition(name='cartesian_scan_dimension2_count'))

    cartesian_scan_dimension3_count = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        a_legacy=LegacyDefinition(name='cartesian_scan_dimension3_count'))

    darkfield_applied = Quantity(
        type=bool,
        shape=[],
        a_legacy=LegacyDefinition(name='darkfield_applied'))

    flatfield_applied = Quantity(
        type=bool,
        shape=[],
        a_legacy=LegacyDefinition(name='flatfield_applied'))

    camera_name = Quantity(
        type=str,
        shape=[],
        a_legacy=LegacyDefinition(name='camera_name'))

    number_of_cycles = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        a_legacy=LegacyDefinition(name='number_of_cycles'))

    sensor_material = Quantity(
        type=str,
        shape=[],
        a_legacy=LegacyDefinition(name='sensor_material'))

    series_param_pt1 = Quantity(
        type=str,
        shape=[],
        description='''
        name of the parameters
        ''',
        a_legacy=LegacyDefinition(name='series_param_pt1'))

    series_param_pt2 = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        description='''
        Number of parameters
        ''',
        a_legacy=LegacyDefinition(name='series_param_pt2'))

    camera_type = Quantity(
        type=str,
        shape=[],
        a_legacy=LegacyDefinition(name='camera_type'))

    exposure_time = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='millisecond',
        a_legacy=LegacyDefinition(name='exposure_time'))

    series_param1 = Quantity(
        type=str,
        shape=[],
        unit='dimensionless',
        a_legacy=LegacyDefinition(name='series_param1'))

    series_param2 = Quantity(
        type=str,
        shape=[],
        unit='nanometer',
        a_legacy=LegacyDefinition(name='series_param2'))

    series_param3 = Quantity(
        type=str,
        shape=[],
        unit='nanometer',
        a_legacy=LegacyDefinition(name='series_param3'))

    section_scan_properties = SubSection(
        sub_section=SectionProxy('section_scan_properties'),
        repeats=True,
        a_legacy=LegacyDefinition(name='section_scan_properties'))


class section_scan_properties(MSection):
    '''
    Information about the scan properties.
    '''

    m_def = Section(validate=False, a_legacy=LegacyDefinition(name='section_scan_properties'))

    scan_system = Quantity(
        type=str,
        shape=[],
        a_legacy=LegacyDefinition(name='scan_system'))

    scan_area_axis1 = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='nanometer',
        a_legacy=LegacyDefinition(name='scan_area_axis1'))

    scan_area_axis2 = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='nanometer',
        a_legacy=LegacyDefinition(name='scan_area_axis2'))


class section_source1(MSection):
    '''
    Information about the source.
    '''

    m_def = Section(validate=False, a_legacy=LegacyDefinition(name='section_source1'))

    probe = Quantity(
        type=str,
        shape=[],
        a_legacy=LegacyDefinition(name='probe'))

    incident_energy = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='kilovolt',
        description='''
        Incident Beam Energy, high tension
        ''',
        a_legacy=LegacyDefinition(name='incident_energy'))

    resolution = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='electron_volt',
        a_legacy=LegacyDefinition(name='resolution'))

    dispersion = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='electron_volt',
        description='''
        In eV per pixel.
        ''',
        a_legacy=LegacyDefinition(name='dispersion'))

    wavelength = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='picometer',
        a_legacy=LegacyDefinition(name='wavelength'))

    monochromated = Quantity(
        type=bool,
        shape=[],
        description='''
        boolean wheter the source is monochromated or not
        ''',
        a_legacy=LegacyDefinition(name='monochromated'))


class section_reference(MSection):
    '''
    Information about the Theory and a link to the paper.
    '''

    m_def = Section(validate=False, a_legacy=LegacyDefinition(name='section_reference'))

    authors = Quantity(
        type=str,
        shape=[],
        a_legacy=LegacyDefinition(name='authors'))

    doi = Quantity(
        type=str,
        shape=[],
        description='''
        digital object identifier
        ''',
        a_legacy=LegacyDefinition(name='doi'))

    issue = Quantity(
        type=str,
        shape=[],
        a_legacy=LegacyDefinition(name='issue'))

    journal = Quantity(
        type=str,
        shape=[],
        a_legacy=LegacyDefinition(name='journal'))

    page = Quantity(
        type=str,
        shape=[],
        a_legacy=LegacyDefinition(name='page'))

    title_ref = Quantity(
        type=str,
        shape=[],
        a_legacy=LegacyDefinition(name='title_ref'))

    url = Quantity(
        type=str,
        shape=[],
        description='''
        a link to the publication
        ''',
        a_legacy=LegacyDefinition(name='url'))

    volume = Quantity(
        type=str,
        shape=[],
        a_legacy=LegacyDefinition(name='volume'))

    year = Quantity(
        type=str,
        shape=[],
        description='''
        year of publication
        ''',
        a_legacy=LegacyDefinition(name='year'))

    freetext = Quantity(
        type=str,
        shape=[],
        description='''
        additional information not fitting somewhere els
        ''',
        a_legacy=LegacyDefinition(name='freetext'))


class section_experiment(general_experimental.section_experiment):

    m_def = Section(validate=False, extends_base_section=True, a_legacy=LegacyDefinition(name='section_experiment'))

    definition = Quantity(
        type=str,
        shape=[],
        a_legacy=LegacyDefinition(name='definition'))

    spectrum_type = Quantity(
        type=str,
        shape=[],
        a_legacy=LegacyDefinition(name='spectrum_type'))

    elemental_edges = Quantity(
        type=str,
        shape=[],
        description='''
        Names of the shown elemental edges in the plot
        ''',
        a_legacy=LegacyDefinition(name='elemental_edges'))

    source_and_purity = Quantity(
        type=str,
        shape=[],
        a_legacy=LegacyDefinition(name='source_and_purity'))

    title = Quantity(
        type=str,
        shape=[],
        a_legacy=LegacyDefinition(name='title'))

    start_time = Quantity(
        type=str,
        shape=[],
        a_legacy=LegacyDefinition(name='start_time'))

    end_time = Quantity(
        type=str,
        shape=[],
        a_legacy=LegacyDefinition(name='end_time'))

    section_user = SubSection(
        sub_section=SectionProxy('section_user'),
        repeats=True,
        a_legacy=LegacyDefinition(name='section_user'))

    section_em = SubSection(
        sub_section=SectionProxy('section_em'),
        repeats=True,
        a_legacy=LegacyDefinition(name='section_em'))


class section_sample(general_experimental_sample.section_sample):

    m_def = Section(validate=False, extends_base_section=True, a_legacy=LegacyDefinition(name='section_sample'))

    probe_size = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='nanometer ** 2',
        a_legacy=LegacyDefinition(name='probe_size'))

    source_purity = Quantity(
        type=str,
        shape=[],
        description='''
        description of the probe and probe preparation
        ''',
        a_legacy=LegacyDefinition(name='source_purity'))

    specimen = Quantity(
        type=str,
        shape=[],
        description='''
        Description of the used specimen
        ''',
        a_legacy=LegacyDefinition(name='specimen'))


class section_data(general_experimental.section_data):

    m_def = Section(validate=False, extends_base_section=True, a_legacy=LegacyDefinition(name='section_data'))

    data_range = Quantity(
        type=str,
        shape=[],
        description='''
        the plot range of the energy
        ''',
        a_legacy=LegacyDefinition(name='data_range'))

    min_energy = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='electron_volt',
        description='''
        the plot range of the energy - minimum
        ''',
        a_legacy=LegacyDefinition(name='min_energy'))

    max_energy = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='electron_volt',
        description='''
        the plot range of the energy - maximum
        ''',
        a_legacy=LegacyDefinition(name='max_energy'))

    api_permalink = Quantity(
        type=str,
        shape=[],
        description='''
        link to the metadata
        ''',
        a_legacy=LegacyDefinition(name='api_permalink'))

    other_links = Quantity(
        type=str,
        shape=[],
        description='''
        other links to the data
        ''',
        a_legacy=LegacyDefinition(name='other_links'))

    permalink = Quantity(
        type=str,
        shape=[],
        description='''
        perma link to the data
        ''',
        a_legacy=LegacyDefinition(name='permalink'))

    published = Quantity(
        type=str,
        shape=[],
        description='''
        date of publishing
        ''',
        a_legacy=LegacyDefinition(name='published'))

    comment_count = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        description='''
        number of comments to the data set
        ''',
        a_legacy=LegacyDefinition(name='comment_count'))

    edges = Quantity(
        type=str,
        shape=[],
        description='''
        name of the seen element edges in the plot
        ''',
        a_legacy=LegacyDefinition(name='edges'))

    associated_spectra = Quantity(
        type=str,
        shape=[],
        description='''
        name of an associated spectra
        ''',
        a_legacy=LegacyDefinition(name='associated_spectra'))

    id = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        description='''
        identification number of the data
        ''',
        a_legacy=LegacyDefinition(name='id'))

    reference = Quantity(
        type=str,
        shape=[],
        description='''
        more references
        ''',
        a_legacy=LegacyDefinition(name='reference'))

    description = Quantity(
        type=str,
        shape=[],
        description='''
        further information about the data and the processing
        ''',
        a_legacy=LegacyDefinition(name='description'))

    section_reference = SubSection(
        sub_section=SectionProxy('section_reference'),
        repeats=True,
        a_legacy=LegacyDefinition(name='section_reference'))


m_package.__init_metainfo__()
