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
    areatotal,
    report
)
from qgis.core import (QgsProcessingParameterRasterDestination,
                       QgsProcessingParameterRasterLayer)

from pcraster_tools.processing.algorithm import PCRasterAlgorithm


class PCRasterAreatotalAlgorithm(PCRasterAlgorithm):
    """
    Sum of cell values within an area
    """

    INPUT_DISCRETE = 'INPUT'
    INPUT_RASTER = 'INPUT1'
    OUTPUT_AREATOTAL = 'OUTPUT'

    def createInstance(self):  # pylint: disable=missing-function-docstring
        return PCRasterAreatotalAlgorithm()

    def name(self):  # pylint: disable=missing-function-docstring
        return 'areatotal'

    def displayName(self):  # pylint: disable=missing-function-docstring
        return self.tr('areatotal')

    def group(self):  # pylint: disable=missing-function-docstring
        return self.tr('PCRaster')

    def groupId(self):  # pylint: disable=missing-function-docstring
        return 'pcraster'

    def shortHelpString(self):  # pylint: disable=missing-function-docstring
        return self.tr(
            """Sum of cell values within an area
            
            <a href="https://pcraster.geo.uu.nl/pcraster/4.3.1/documentation/pcraster_manual/sphinx/op_areatotal.html">PCRaster documentation</a>
            
            Parameters:
            
            * <b>Input class raster layer</b> (required) - boolean, nominal or ordinal raster layer
            * <b>Input scalar raster layer</b> ( required) - scalar raster layer
            * <b>Output area normal raster</b> (required) - scalar raster layer with sum of cell values within an area
            """
        )

    def initAlgorithm(self, config=None):  # pylint: disable=missing-function-docstring
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_DISCRETE,
                self.tr('Class raster layer')
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_RASTER,
                self.tr('Input scalar raster layer')
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.OUTPUT_AREATOTAL,
                self.tr('Output area total layer')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):  # pylint: disable=missing-function-docstring
        input_discrete = self.parameterAsRasterLayer(parameters, self.INPUT_DISCRETE, context)
        input_raster = self.parameterAsRasterLayer(parameters, self.INPUT_RASTER, context)
        setclone(input_discrete.dataProvider().dataSourceUri())
        ClassLayer = readmap(input_discrete.dataProvider().dataSourceUri())
        RasterLayer = readmap(input_raster.dataProvider().dataSourceUri())
        AreaTotalLayer = areatotal(RasterLayer, ClassLayer)
        outputFilePath = self.parameterAsOutputLayer(parameters, self.OUTPUT_AREATOTAL, context)

        report(AreaTotalLayer, outputFilePath)

        return {self.OUTPUT_AREATOTAL: outputFilePath}
