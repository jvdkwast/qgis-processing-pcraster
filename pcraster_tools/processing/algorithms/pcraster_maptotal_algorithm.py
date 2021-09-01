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

from pcraster import (
    setclone,
    readmap,
    report,
    maptotal
)
from qgis.core import (QgsProcessingParameterRasterDestination,
                       QgsProcessingParameterRasterLayer)

from pcraster_tools.processing.algorithm import PCRasterAlgorithm


class PCRasterMaptotalAlgorithm(PCRasterAlgorithm):
    """
    Sum of all cell values
    """

    INPUT_RASTER = 'INPUT1'
    OUTPUT_MAPTOTAL = 'OUTPUT'

    def createInstance(self):  # pylint: disable=missing-function-docstring
        return PCRasterMaptotalAlgorithm()

    def name(self):  # pylint: disable=missing-function-docstring
        return 'maptotal'

    def displayName(self):  # pylint: disable=missing-function-docstring
        return self.tr('maptotal')

    def group(self):  # pylint: disable=missing-function-docstring
        return self.tr('Map operations')

    def groupId(self):  # pylint: disable=missing-function-docstring
        return 'map'

    def shortHelpString(self):  # pylint: disable=missing-function-docstring
        return self.tr(
            """Sum of all cell values

            <a href="https://pcraster.geo.uu.nl/pcraster/4.3.1/documentation/pcraster_manual/sphinx/op_maptotal.html">PCRaster documentation</a>

            Parameters:

            * <b>Input raster layer</b> (required) - Raster layer of scalar data type
            * <b>Output map total raster</b> (required) - scalar raster layer sum of all cell values
            """
        )

    def initAlgorithm(self, config=None):  # pylint: disable=missing-function-docstring,unused-argument
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_RASTER,
                self.tr('Input raster layer')
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.OUTPUT_MAPTOTAL,
                self.tr('Output map total layer')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):  # pylint: disable=missing-function-docstring,unused-argument
        input_raster = self.parameterAsRasterLayer(parameters, self.INPUT_RASTER, context)
        setclone(input_raster.dataProvider().dataSourceUri())
        RasterLayer = readmap(input_raster.dataProvider().dataSourceUri())
        MapTotalLayer = maptotal(RasterLayer)
        outputFilePath = self.parameterAsOutputLayer(parameters, self.OUTPUT_MAPTOTAL, context)

        report(MapTotalLayer, outputFilePath)

        return {self.OUTPUT_MAPTOTAL: outputFilePath}
