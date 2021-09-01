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
    cover
)
from qgis.core import (QgsProcessing,
                       QgsProcessingParameterRasterDestination,
                       QgsProcessingParameterMultipleLayers,
                       QgsProcessingParameterRasterLayer)

from pcraster_tools.processing.algorithm import PCRasterAlgorithm


class PCRasterCoverAlgorithm(PCRasterAlgorithm):
    """
    Missing values substituted for values from other raster(s)
    """

    INPUT_RASTER = 'INPUT'
    INPUT_COVER = 'INPUT2'
    OUTPUT_RASTER = 'OUTPUT'

    def createInstance(self):  # pylint: disable=missing-function-docstring
        return PCRasterCoverAlgorithm()

    def name(self):  # pylint: disable=missing-function-docstring
        return 'cover'

    def displayName(self):  # pylint: disable=missing-function-docstring
        return self.tr('cover')

    def group(self):  # pylint: disable=missing-function-docstring
        return self.tr('PCRaster')

    def groupId(self):  # pylint: disable=missing-function-docstring
        return 'pcraster'

    def shortHelpString(self):  # pylint: disable=missing-function-docstring
        return self.tr(
            """Missing values substituted for values from other raster(s)
            
            <a href="https://pcraster.geo.uu.nl/pcraster/4.3.1/documentation/pcraster_manual/sphinx/op_cover.html">PCRaster documentation</a>
            
            Parameters:
            
            * <b>Input raster</b> (required) - Raster layer of any data type
            * <b>Input cover raster</b> (required) - Raster layer(s) of same data type as input raster
            * <b>Output raster</b> (required) - Raster with result of same data type as input
            """
        )

    def initAlgorithm(self, config=None):  # pylint: disable=missing-function-docstring
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_RASTER,
                self.tr('Input Raster layer')
            )
        )

        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.INPUT_COVER,
                self.tr('Input Cover Layer(s)'),
                QgsProcessing.TypeRaster
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.OUTPUT_RASTER,
                self.tr("Output Raster Layer")
            )
        )

    def processAlgorithm(self, parameters, context, feedback):  # pylint: disable=missing-function-docstring
        input_raster = self.parameterAsRasterLayer(parameters, self.INPUT_RASTER, context)
        input_cover = []
        for layer in self.parameterAsLayerList(parameters, self.INPUT_COVER, context):
            input_cover.append(layer.source())

        # input_cover = self.parameterAsFileList(parameters, self.INPUT_COVER, context)
        setclone(input_raster.dataProvider().dataSourceUri())
        InputRaster = readmap(input_raster.dataProvider().dataSourceUri())
        # coverLayer = readmap(input_cover.dataProvider().dataSourceUri())
        resultLayer = cover(InputRaster, *input_cover)
        outputFilePath = self.parameterAsOutputLayer(parameters, self.OUTPUT_RASTER, context)

        report(resultLayer, outputFilePath)

        return {self.OUTPUT_RASTER: outputFilePath}
