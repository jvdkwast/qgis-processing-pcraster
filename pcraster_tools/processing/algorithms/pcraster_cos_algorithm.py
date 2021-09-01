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
    cos
)
from qgis.core import (QgsProcessingParameterRasterDestination,
                       QgsProcessingParameterRasterLayer)

from pcraster_tools.processing.algorithm import PCRasterAlgorithm


class PCRastercosAlgorithm(PCRasterAlgorithm):
    """
    Cosine
    """

    INPUT_RASTER = 'INPUT'
    OUTPUT_RASTER = 'OUTPUT'

    def createInstance(self):  # pylint: disable=missing-function-docstring
        return PCRastercosAlgorithm()

    def name(self):  # pylint: disable=missing-function-docstring
        return 'cos'

    def displayName(self):  # pylint: disable=missing-function-docstring
        return self.tr('cos')

    def group(self):  # pylint: disable=missing-function-docstring
        return self.tr('PCRaster')

    def groupId(self):  # pylint: disable=missing-function-docstring
        return 'pcraster'

    def shortHelpString(self):  # pylint: disable=missing-function-docstring
        return self.tr(
            """Cosine

            <a href="https://pcraster.geo.uu.nl/pcraster/4.3.1/documentation/pcraster_manual/sphinx/op_cos.html">PCRaster documentation</a>

            Parameters:

            * <b>Input raster</b> (required) - directional or scalar raster layer
            * <b>Output raster</b> (required) - cosine result layer with data type of input raster
            """
        )

    def initAlgorithm(self, config=None):  # pylint: disable=missing-function-docstring
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_RASTER,
                self.tr('Directional or Scalar Raster layer')
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.OUTPUT_RASTER,
                self.tr("Output Cosine layer")
            )
        )

    def processAlgorithm(self, parameters, context, feedback):  # pylint: disable=missing-function-docstring
        input_raster = self.parameterAsRasterLayer(parameters, self.INPUT_RASTER, context)
        setclone(input_raster.dataProvider().dataSourceUri())
        InputRaster = readmap(input_raster.dataProvider().dataSourceUri())
        cosLayer = cos(InputRaster)
        outputFilePath = self.parameterAsOutputLayer(parameters, self.OUTPUT_RASTER, context)

        report(cosLayer, outputFilePath)

        return {self.OUTPUT_RASTER: outputFilePath}
