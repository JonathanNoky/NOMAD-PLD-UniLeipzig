from typing import (
    TYPE_CHECKING,
)

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import (
        EntryArchive,
    )
    from structlog.stdlib import (
        BoundLogger,
    )

import numpy as np
import plotly.graph_objects as go
from nomad.config import config
from nomad.datamodel.data import (
    ArchiveSection,
    EntryData,
)
from nomad.datamodel.metainfo.annotations import (
    BrowserAnnotation,
    ELNAnnotation,
    SectionProperties,
)
from nomad.datamodel.metainfo.basesections.v1 import (
    CompositeSystem,
)
from nomad.datamodel.metainfo.plot import PlotlyFigure, PlotSection
from nomad.metainfo import Quantity, SchemaPackage, Section, SubSection
from nomad.units import ureg
from nomad_material_processing.vapor_deposition.pvd.pld import (
    PLDStep,
    PulsedLaserDeposition,
)

configuration = config.get_plugin_entry_point(
    'nomad_pld_unileipzig.schema_packages:uni_leipzig_pld_schema'
)

m_package = SchemaPackage()

# The following sections are BaseSections with expanded properties as
# neccessary for the PLD Experiment from the Uni Leipzig. They can be expanded
# as neccessary.


class UniLeipzigPLDStep(PLDStep):
    m_def = Section(
        a_eln=ELNAnnotation(
            properties=SectionProperties(
                order=['name', 'datetime', 'jpg_file', 'steps'],
            ),
            lane_width='600px',
        ),
    )

    stepnumber = Quantity(type=int, description='Step number it belongs to')

    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:
        super().normalize(archive, logger)


class UniLeipzigPLDSample(CompositeSystem, EntryData):
    elabftw_identifier = Quantity(type=str, description='Identifier from ELABFTW')

    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:
        super().normalize(archive, logger)


class UniLeipzigChamber(EntryData, ArchiveSection):
    name = Quantity(type=str, description='DESCRIPTION')

    chamber_images = Quantity(
        type=str,
        description="""The .pdf file.""",
        a_browser=BrowserAnnotation(adaptor='RawFileAdaptor'),
        a_eln=ELNAnnotation(component='FileEditQuantity'),
    )

    elabftw_identifier = Quantity(type=str, description='Identifier from ELABFTW')

    laser = Quantity(type=str, description='DESCRIPTION')

    heaterDevice = Quantity(type=str, description='DESCRIPTION')

    vacuumController = Quantity(type=str, description='DESCRIPTION')

    laserSpotCalibrationFunction = Quantity(type=str, description='DESCRIPTION')

    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:
        super().normalize(archive, logger)


class UniLeipzigPulsedLaserDeposition(PulsedLaserDeposition, PlotSection, EntryData):
    # The main PLD schema. Also contains functions to postprocess the data.
    m_def = Section(
        a_eln=ELNAnnotation(
            properties=SectionProperties(
                order=['name', 'datetime', 'jpg_file', 'steps'],
            ),
            lane_width='600px',
        ),
    )

    protocol_file = Quantity(
        type=str,
        description="""The .ptk file.""",
        a_browser=BrowserAnnotation(adaptor='RawFileAdaptor'),
        a_eln=ELNAnnotation(component='FileEditQuantity'),
    )

    abs_file = Quantity(
        type=str,
        description="""The .abs file.""",
        a_browser=BrowserAnnotation(adaptor='RawFileAdaptor'),
        a_eln=ELNAnnotation(component='FileEditQuantity'),
    )

    jpg_file = Quantity(
        type=str,
        description="""The .jpg file.""",
        a_browser=BrowserAnnotation(adaptor='RawFileAdaptor'),
        a_eln=ELNAnnotation(component='FileEditQuantity'),
    )

    pdf_file = Quantity(
        type=str,
        description="""The .pdf file.""",
        a_browser=BrowserAnnotation(adaptor='RawFileAdaptor'),
        a_eln=ELNAnnotation(component='FileEditQuantity'),
    )

    steps = SubSection(section_def=UniLeipzigPLDStep, repeats=True)
    layer = SubSection(section_def=UniLeipzigPLDStep, repeats=True)

    chamber = Quantity(
        type=UniLeipzigChamber,
        a_eln=ELNAnnotation(
            component='ReferenceEditQuantity',
        ),
    )

    def plot(self) -> None:
        """
        Method for plotting the section.
        """
        fig = go.Figure()
        x0 = None
        y0 = None
        y20 = None
        y30 = None
        shapes = []
        for step in self.steps:
            if (
                not np.any(step.environment.pressure.time)
                or not np.any(step.environment.pressure.value)
                or not np.any(step.sources[0].vapor_source.power.value)
            ):
                continue
            x = step.environment.pressure.time.to('second').magnitude
            y = step.environment.pressure.value.to('mbar').magnitude
            y2 = step.sources[0].vapor_source.power.value.to('watt').magnitude
            y3 = (
                step.sample_parameters[0]
                .substrate_temperature.value.to('celsius')
                .magnitude
            )
            if x0 is not None:
                x = np.insert(x, 0, x0)
                y = np.insert(y, 0, y0)
                y2 = np.insert(y2, 0, y20)
                y3 = np.insert(y3, 0, y30)
            fig.add_trace(
                go.Scatter(
                    x=x,
                    y=y,
                    name=step.name,
                    line=dict(color='#2A4CDF', width=2),
                    yaxis='y',
                ),
            )
            fig.add_trace(
                go.Scatter(
                    x=x,
                    y=y3,
                    name=step.name,
                    line=dict(color='#008A68', width=2),
                    yaxis='y3',
                ),
            )
            fig.add_trace(
                go.Scatter(
                    x=x,
                    y=y2,
                    name=step.name,
                    line=dict(color='#192E87', width=2),
                    yaxis='y2',
                ),
            )
            fig.add_annotation(
                text=step.name,
                yref='paper',
                x=(x[0] + (x[-1] - x[0]) / 2),
                y=0.85,
                showarrow=False,
                textangle=-90,
            )
            x0 = x[-1]
            y0 = y[-1]
            y20 = y2[-1]
            y30 = y3[-1]
            shapes.append(
                dict(
                    type='line',
                    x0=x[-1],
                    x1=x[-1],
                    y0=0,
                    y1=1,
                    xref='x',
                    yref='paper',
                    line=dict(
                        color='grey',
                        width=1,
                    ),
                )
            )
        fig.update_layout(shapes=shapes)
        fig.update_layout(
            template='plotly_white',
            hovermode='closest',
            dragmode='zoom',
            xaxis=dict(
                fixedrange=False,
                autorange=True,
                rangeslider=dict(
                    autorange=True,
                    borderwidth=1,
                ),
                title='Process time / s',
                mirror='all',
                showline=True,
                gridcolor='#EAEDFC',
            ),
            yaxis=dict(
                fixedrange=False,
                type='log',
                anchor='x',
                title='Chamber pressure / mbar',
                domain=[0, 0.48],
                titlefont=dict(color='#2A4CDF'),
                tickfont=dict(color='#2A4CDF'),
                gridcolor='#EAEDFC',
            ),
            yaxis2=dict(
                fixedrange=False,
                anchor='x',
                title='Source power / W',
                domain=[0.52, 1],
                titlefont=dict(color='#192E87'),
                tickfont=dict(color='#192E87'),
                gridcolor='#EAEDFC',
            ),
            yaxis3=dict(
                fixedrange=False,
                anchor='x',
                title='Substrate Temperature / °C',
                side='right',
                overlaying='y',
                titlefont=dict(color='#008A68'),
                tickfont=dict(color='#008A68'),
                ticks='outside',
                gridcolor='#CCE8E1',
            ),
        )
        plot_json = fig.to_plotly_json()
        plot_json['config'] = dict(
            scrollZoom=False,
        )
        self.figures.append(
            PlotlyFigure(
                label='Power, pressure, and temperature',
                figure=plot_json,
            )
        )

    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:
        if self.protocol_file:
            with archive.m_context.raw_file(self.protocol_file, 'r') as file:
                cleaned_data = [line[2:] for line in file.readlines()]
                data = np.genfromtxt(cleaned_data, skip_header=3)

            # Read in the data from the protocol file into the NOMAD metadata sections.

            for i in set(data[:, 0]):
                stepdata = data[data[:, 0] == i]
                for j in range(len(self.steps)):
                    if self.steps[j].stepnumber == i:
                        self.steps[j].environment.pressure.value = stepdata[
                            :, 1
                        ] * ureg('mbar')
                        self.steps[j].environment.pressure.time = stepdata[:, 12]
                        self.steps[j].sample_parameters[
                            0
                        ].substrate_temperature.value = stepdata[:, 5] * ureg('K')
                        self.steps[j].sample_parameters[
                            0
                        ].substrate_temperature.time = stepdata[:, 12]
                        self.steps[j].sources[0].vapor_source.power.value = stepdata[
                            :, 3
                        ] * ureg('W')
                        self.steps[j].sources[0].vapor_source.power.time = stepdata[
                            :, 12
                        ]
                        self.steps[j].duration = stepdata[:, 11][-1]
                for j in range(len(self.layer)):
                    if self.layer[j].stepnumber == i:
                        self.layer[j].environment.pressure.value = stepdata[
                            :, 1
                        ] * ureg('mbar')
                        self.layer[j].environment.pressure.time = stepdata[:, 12]
                        self.layer[j].sample_parameters[
                            0
                        ].substrate_temperature.value = stepdata[:, 5] * ureg('K')
                        self.layer[j].sample_parameters[
                            0
                        ].substrate_temperature.time = stepdata[:, 12]
                        self.layer[j].sources[0].vapor_source.power.value = stepdata[
                            :, 3
                        ] * ureg('W')
                        self.layer[j].sources[0].vapor_source.power.time = stepdata[
                            :, 12
                        ]
                        self.layer[j].duration = stepdata[:, 11][-1]

            # Build the unified PLD plot.

            self.plot()

        super().normalize(archive, logger)


m_package.__init_metainfo__()
