# -*- coding: utf-8 -*-

"""
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

from qgis.core import (QgsProcessingParameterRasterDestination,
                       QgsProcessingParameterRasterLayer,
                       QgsProcessingParameterEnum,
                       QgsProcessingParameterNumber,
                       QgsProcessingException)

from pcraster_tools.processing.algorithm import PCRasterAlgorithm


class PCRasterLDDCreateDEMAlgorithm(PCRasterAlgorithm):
    """
    Modified digital elevation model
    """

    INPUT_DEM = 'INPUT'
    INPUT_UNITS = 'INPUT1'
    INPUT_EDGE = 'INPUT0'
    INPUT_ELEVATION = 'INPUT6'
    INPUT_OUTFLOWDEPTH = 'INPUT2'
    INPUT_COREVOLUME = 'INPUT3'
    INPUT_COREAREA = 'INPUT4'
    INPUT_PRECIPITATION = 'INPUT5'
    OUTPUT_DEMFILLED = 'OUTPUT'

    def createInstance(self):  # pylint: disable=missing-function-docstring
        return PCRasterLDDCreateDEMAlgorithm()

    def name(self):  # pylint: disable=missing-function-docstring
        return 'lddcreatedem'

    def displayName(self):  # pylint: disable=missing-function-docstring
        return self.tr('lddcreatedem')

    def group(self):  # pylint: disable=missing-function-docstring
        return self.tr('Hydrological and material transport operations')

    def groupId(self):  # pylint: disable=missing-function-docstring
        return 'hydrological'

    def shortHelpString(self):  # pylint: disable=missing-function-docstring
        return self.tr(
            """Modified digital elevation model

            <a href="{}">PCRaster documentation</a>

            Parameters:

            * <b>Input DEM layer</b> (required) - scalar raster layer
            * <b>Remove pits at edge</b> (required) - no/yes
            * <b>Assignment of elevation in pits</b> (required) - fill or cut
            * <b>Units</b> (required) - map units or cells
            * <b>Outflow depth value</b> (required) - outflow depth
            * <b>Core volume value</b> (required) - core volume
            * <b>Core area value</b> (required) - core area
            * <b>Catchment precipitation</b> (required) - catchment precipitation
            * <b>Local drain direction layer output</b> (required) - raster with local drain direction (ldd data type)
            """
        ).format(PCRasterAlgorithm.documentation_url('op_lddcreatedem.html'))

    def initAlgorithm(self, config=None):  # pylint: disable=missing-function-docstring,unused-argument
        # We add the input DEM.
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_DEM,
                self.tr('DEM layer')
            )
        )

        unitoption = [self.tr('No'), self.tr('Yes')]
        self.addParameter(
            QgsProcessingParameterEnum(
                self.INPUT_EDGE,
                self.tr('Remove pits at edge?'),
                unitoption,
                defaultValue=0
            )
        )

        unitoption = [self.tr('Fill'), self.tr('Cut')]
        self.addParameter(
            QgsProcessingParameterEnum(
                self.INPUT_ELEVATION,
                self.tr('Assignment of elevation in pits'),
                unitoption,
                defaultValue=0
            )
        )

        unitoption = [self.tr('Map units'), self.tr('Cells')]
        self.addParameter(
            QgsProcessingParameterEnum(
                self.INPUT_UNITS,
                self.tr('Units'),
                unitoption,
                defaultValue=0
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.INPUT_OUTFLOWDEPTH,
                self.tr('Outflow depth (map units)'),
                defaultValue=9999999,
                type=QgsProcessingParameterNumber.Double
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.INPUT_COREAREA,
                self.tr('Core area (map units)'),
                defaultValue=9999999,
                type=QgsProcessingParameterNumber.Double
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.INPUT_COREVOLUME,
                self.tr('Core volume (map units)'),
                defaultValue=9999999,
                type=QgsProcessingParameterNumber.Double
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.INPUT_PRECIPITATION,
                self.tr('Catchment precipitation (map units)'),
                defaultValue=9999999,
                type=QgsProcessingParameterNumber.Double
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.OUTPUT_DEMFILLED,
                self.tr('Filled DEM')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):  # pylint: disable=missing-function-docstring,unused-argument,too-many-locals
        try:
            from pcraster import (   # pylint: disable=import-outside-toplevel
                setclone,
                readmap,
                report,
                setglobaloption,
                lddcreatedem
            )
        except ImportError as e:
            raise QgsProcessingException('PCRaster library is not available') from e

        input_dem = self.parameterAsRasterLayer(parameters, self.INPUT_DEM, context)
        elevationsetting = self.parameterAsEnum(parameters, self.INPUT_ELEVATION, context)
        if elevationsetting == 0:
            setglobaloption("lddfill")
        else:
            setglobaloption("lddcut")
        edgesetting = self.parameterAsEnum(parameters, self.INPUT_EDGE, context)
        if edgesetting == 0:
            setglobaloption("lddout")
        else:
            setglobaloption("lddin")
        lengthunits = self.parameterAsEnum(parameters, self.INPUT_UNITS, context)
        if lengthunits == 0:
            setglobaloption("unittrue")
        else:
            setglobaloption("unitcell")
        input_outflowdepth = self.parameterAsDouble(parameters, self.INPUT_OUTFLOWDEPTH, context)
        input_corearea = self.parameterAsDouble(parameters, self.INPUT_COREAREA, context)
        input_corevolume = self.parameterAsDouble(parameters, self.INPUT_COREVOLUME, context)
        input_precipitation = self.parameterAsDouble(parameters, self.INPUT_PRECIPITATION, context)
        setclone(input_dem.dataProvider().dataSourceUri())
        DEM = readmap(input_dem.dataProvider().dataSourceUri())
        DEMFilled = lddcreatedem(DEM, input_outflowdepth, input_corearea, input_corevolume, input_precipitation)
        outputFilePath = self.parameterAsOutputLayer(parameters, self.OUTPUT_DEMFILLED, context)
        report(DEMFilled, outputFilePath)

        self.set_output_crs(output_file=outputFilePath, crs=input_dem.crs(), feedback=feedback, context=context)

        return {self.OUTPUT_DEMFILLED: outputFilePath}
