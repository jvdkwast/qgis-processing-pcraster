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
    areaorder
)
from qgis.core import (QgsProcessingParameterRasterDestination,
                       QgsProcessingParameterRasterLayer)

from pcraster_tools.processing.algorithm import PCRasterAlgorithm


class PCRasterAreaorderAlgorithm(PCRasterAlgorithm):
    """
    Within each area ordinal numbers to cells in ascending order
    """

    INPUT_DISCRETE = 'INPUT'
    INPUT_RASTER = 'INPUT1'
    OUTPUT_AREAORDER = 'OUTPUT'

    def createInstance(self):  # pylint: disable=missing-function-docstring
        return PCRasterAreaorderAlgorithm()

    def name(self):  # pylint: disable=missing-function-docstring
        return 'areaorder'

    def displayName(self):  # pylint: disable=missing-function-docstring
        return self.tr('areaorder')

    def group(self):  # pylint: disable=missing-function-docstring
        return self.tr('PCRaster')

    def groupId(self):  # pylint: disable=missing-function-docstring
        return 'pcraster'

    def shortHelpString(self):  # pylint: disable=missing-function-docstring
        return self.tr(
            """Within each area ordinal numbers to cells in ascending order

            <a href="https://pcraster.geo.uu.nl/pcraster/4.3.1/documentation/pcraster_manual/sphinx/op_areaorder.html">PCRaster documentation</a>

            Parameters:

            * <b>Input class raster layer</b> (required) - boolean, nominal or ordinal raster layer
            * <b>Input ordinal or scalar raster layer</b> ( required) - ordinal or scalar raster layer
            * <b>Output area normal raster</b> (required) - scalar raster layer order of cells in each class
            """
        )

    def initAlgorithm(self, config=None):  # pylint: disable=missing-function-docstring,unused-argument
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_DISCRETE,
                self.tr('Class raster layer')
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_RASTER,
                self.tr('Input ordinal or scalar raster layer')
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.OUTPUT_AREAORDER,
                self.tr('Output area order layer')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):  # pylint: disable=missing-function-docstring,unused-argument
        input_discrete = self.parameterAsRasterLayer(parameters, self.INPUT_DISCRETE, context)
        input_raster = self.parameterAsRasterLayer(parameters, self.INPUT_RASTER, context)
        setclone(input_discrete.dataProvider().dataSourceUri())
        ClassLayer = readmap(input_discrete.dataProvider().dataSourceUri())
        RasterLayer = readmap(input_raster.dataProvider().dataSourceUri())
        AreaOrderLayer = areaorder(RasterLayer, ClassLayer)
        outputFilePath = self.parameterAsOutputLayer(parameters, self.OUTPUT_AREAORDER, context)

        report(AreaOrderLayer, outputFilePath)

        return {self.OUTPUT_AREAORDER: outputFilePath}
