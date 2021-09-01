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
    mapmaximum,
    cellvalue
)
from qgis.core import (QgsProcessingParameterRasterDestination,
                       QgsProcessingParameterRasterLayer)

from pcraster_tools.processing.algorithm import PCRasterAlgorithm


class PCRasterMapmaximumAlgorithm(PCRasterAlgorithm):
    """
    Maximum cell value
    """

    INPUT_RASTER = 'INPUT'
    OUTPUT_MAX = 'OUTPUT'

    def createInstance(self):  # pylint: disable=missing-function-docstring
        return PCRasterMapmaximumAlgorithm()

    def name(self):  # pylint: disable=missing-function-docstring
        return 'mapmaximum'

    def displayName(self):  # pylint: disable=missing-function-docstring
        return self.tr('mapmaximum')

    def group(self):  # pylint: disable=missing-function-docstring
        return self.tr('PCRaster')

    def groupId(self):  # pylint: disable=missing-function-docstring
        return 'pcraster'

    def shortHelpString(self):  # pylint: disable=missing-function-docstring
        return self.tr(
            """Maximum cell value
            
            <a href="https://pcraster.geo.uu.nl/pcraster/4.3.1/documentation/pcraster_manual/sphinx/op_mapmaximum.html">PCRaster documentation</a>
            
            Parameters:
            
            * <b>Input raster layer</b> (required) - ordinal or scalar raster layer
            * <b>Output maximum value raster</b> (required) - Raster of same type as input containing the maximum cell value
            """
        )

    def initAlgorithm(self, config=None):  # pylint: disable=missing-function-docstring
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_RASTER,
                self.tr('Input raster layer')
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.OUTPUT_MAX,
                self.tr('Output maximum value layer')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):  # pylint: disable=missing-function-docstring
        input_raster = self.parameterAsRasterLayer(parameters, self.INPUT_RASTER, context)

        setclone(input_raster.dataProvider().dataSourceUri())
        RasterLayer = readmap(input_raster.dataProvider().dataSourceUri())
        MaxLayer = mapmaximum(RasterLayer)
        print(cellvalue(MaxLayer, 1, 1)[0])
        outputFilePath = self.parameterAsOutputLayer(parameters, self.OUTPUT_MAX, context)

        report(MaxLayer, outputFilePath)

        return {self.OUTPUT_MAX: outputFilePath}
