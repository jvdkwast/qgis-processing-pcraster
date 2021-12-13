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
                       QgsProcessingParameterEnum,
                       QgsProcessingParameterRasterLayer,
                       QgsProcessingException)

from pcraster_tools.processing.algorithm import PCRasterAlgorithm


class PCRasterMapareaAlgorithm(PCRasterAlgorithm):
    """
    Total map area
    """

    INPUT_RASTER = 'INPUT'
    INPUT_UNITS = 'INPUT1'
    OUTPUT_AREA = 'OUTPUT'

    def createInstance(self):  # pylint: disable=missing-function-docstring
        return PCRasterMapareaAlgorithm()

    def name(self):  # pylint: disable=missing-function-docstring
        return 'maparea'

    def displayName(self):  # pylint: disable=missing-function-docstring
        return self.tr('maparea')

    def group(self):  # pylint: disable=missing-function-docstring
        return self.tr('Map operations')

    def groupId(self):  # pylint: disable=missing-function-docstring
        return 'map'

    def shortHelpString(self):  # pylint: disable=missing-function-docstring
        return self.tr(
            """Total map area

            <a href="https://pcraster.geo.uu.nl/pcraster/4.3.2/documentation/pcraster_manual/sphinx/op_maparea.html">PCRaster documentation</a>

            Parameters:

            * <b>Input raster layer</b> (required) - raster layer of any data type
            * <b>Units</b> (required) - map units or cells
            * <b>Output area raster</b> (required) - Scalar raster with true area (map units)
            """
        )

    def initAlgorithm(self, config=None):  # pylint: disable=missing-function-docstring,unused-argument
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_RASTER,
                self.tr('Input raster layer')
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
            QgsProcessingParameterRasterDestination(
                self.OUTPUT_AREA,
                self.tr('Output area layer')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):  # pylint: disable=missing-function-docstring,unused-argument,too-many-locals
        try:
            from pcraster import (   # pylint: disable=import-outside-toplevel
                setclone,
                readmap,
                report,
                setglobaloption,
                maparea
            )
        except ImportError as e:
            raise QgsProcessingException('PCRaster library is not available') from e

        input_raster = self.parameterAsRasterLayer(parameters, self.INPUT_RASTER, context)
        lengthunits = self.parameterAsEnum(parameters, self.INPUT_UNITS, context)
        if lengthunits == 0:
            setglobaloption("unittrue")
        else:
            setglobaloption("unitcell")
        setclone(input_raster.dataProvider().dataSourceUri())
        RasterLayer = readmap(input_raster.dataProvider().dataSourceUri())
        AreaLayer = maparea(RasterLayer)
        outputFilePath = self.parameterAsOutputLayer(parameters, self.OUTPUT_AREA, context)

        report(AreaLayer, outputFilePath)

        self.set_output_crs(output_file=outputFilePath, crs=input_raster.crs(), feedback=feedback, context=context)

        return {self.OUTPUT_AREA: outputFilePath}
