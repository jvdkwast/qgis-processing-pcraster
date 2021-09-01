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
    horizontan
)
from qgis.core import (QgsProcessingParameterRasterDestination,
                       QgsProcessingParameterRasterLayer,
                       QgsProcessingParameterNumber)

from pcraster_tools.processing.algorithm import PCRasterAlgorithm


class PCRasterHorizontanAlgorithm(PCRasterAlgorithm):
    """
    Calculates the maximum tangent of the angles of neighbouring cells in the direction of the sun.
    """

    INPUT_DEM = 'INPUT'
    INPUT_ANGLE = 'INPUT2'
    OUTPUT_RASTER = 'OUTPUT'

    def createInstance(self):  # pylint: disable=missing-function-docstring
        return PCRasterHorizontanAlgorithm()

    def name(self):  # pylint: disable=missing-function-docstring
        return 'horizontan'

    def displayName(self):  # pylint: disable=missing-function-docstring
        return self.tr('horizontan')

    def group(self):  # pylint: disable=missing-function-docstring
        return self.tr('Derivatives of digital elevation models')

    def groupId(self):  # pylint: disable=missing-function-docstring
        return 'demderivatives'

    def shortHelpString(self):  # pylint: disable=missing-function-docstring
        return self.tr(
            """Calculates the maximum tangent of the angles of neighbouring cells in the direction of the sun.

            <a href="https://pcraster.geo.uu.nl/pcraster/4.3.1/documentation/pcraster_manual/sphinx/op_horizontan.html">PCRaster documentation</a>

            Parameters:

            * <b>Input digital elevation model</b> (required) - scalar raster layer
            * <b>Input view angle</b> (required) - solar azimuth
            * <b>Output horizontan raster</b> (required) - Scalar raster with the maximum tangent of the angles of neighbouring cells in the direction of the sun.
            """
        )

    def initAlgorithm(self, config=None):  # pylint: disable=missing-function-docstring,unused-argument
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_DEM,
                self.tr('DEM raster layer')
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.INPUT_ANGLE,
                self.tr('Solar azimuth'),
                defaultValue=40
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.OUTPUT_RASTER,
                self.tr('Output horizontan layer')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):  # pylint: disable=missing-function-docstring,unused-argument
        input_dem = self.parameterAsRasterLayer(parameters, self.INPUT_DEM, context)
        input_angle = self.parameterAsDouble(parameters, self.INPUT_ANGLE, context)
        setclone(input_dem.dataProvider().dataSourceUri())
        DEM = readmap(input_dem.dataProvider().dataSourceUri())
        ResultHorizontan = horizontan(DEM, input_angle)
        outputFilePath = self.parameterAsOutputLayer(parameters, self.OUTPUT_RASTER, context)

        report(ResultHorizontan, outputFilePath)

        return {self.OUTPUT_RASTER: outputFilePath}
