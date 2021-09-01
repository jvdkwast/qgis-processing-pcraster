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
    areaaverage,
    report
)
from qgis.core import (QgsProcessingParameterRasterDestination,
                       QgsProcessingParameterRasterLayer)

from pcraster_tools.processing.algorithm import PCRasterAlgorithm


class PCRasterAreaaverageAlgorithm(PCRasterAlgorithm):
    """
    The area of the area to which a cell belongs
    """

    INPUT_DISCRETE = 'INPUT'
    INPUT_SCALAR = 'INPUT2'
    OUTPUT_AREAAVERAGE = 'OUTPUT'

    def createInstance(self):  # pylint: disable=missing-function-docstring
        return PCRasterAreaaverageAlgorithm()

    def name(self):  # pylint: disable=missing-function-docstring
        return 'areaaverage'

    def displayName(self):  # pylint: disable=missing-function-docstring
        return self.tr('areaaverage')

    def group(self):  # pylint: disable=missing-function-docstring
        return self.tr('Area operations')

    def groupId(self):  # pylint: disable=missing-function-docstring
        return 'area'

    def shortHelpString(self):  # pylint: disable=missing-function-docstring
        return self.tr(
            """The area of the area to which a cell belongs

            <a href="https://pcraster.geo.uu.nl/pcraster/4.3.1/documentation/pcraster_manual/sphinx/op_areaaverage.html">PCRaster documentation</a>

            Parameters:

            * <b>Input class raster layer</b> (required) - boolean, nominal or ordinal raster layer
            * <b>Input scalar raster layer</b> (required) - scalar raster layer
            * <b>Output area average raster</b> (required) - Scalar raster with average cell value of each class
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
                self.INPUT_SCALAR,
                self.tr('Scalar raster layer')
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.OUTPUT_AREAAVERAGE,
                self.tr('Output area average layer')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):  # pylint: disable=missing-function-docstring,unused-argument
        input_discrete = self.parameterAsRasterLayer(parameters, self.INPUT_DISCRETE, context)
        input_scalar = self.parameterAsRasterLayer(parameters, self.INPUT_SCALAR, context)
        setclone(input_discrete.dataProvider().dataSourceUri())
        ClassLayer = readmap(input_discrete.dataProvider().dataSourceUri())
        ScalarLayer = readmap(input_scalar.dataProvider().dataSourceUri())
        AreaAverage = areaaverage(ScalarLayer, ClassLayer)
        outputFilePath = self.parameterAsOutputLayer(parameters, self.OUTPUT_AREAAVERAGE, context)

        report(AreaAverage, outputFilePath)

        return {self.OUTPUT_AREAAVERAGE: outputFilePath}
