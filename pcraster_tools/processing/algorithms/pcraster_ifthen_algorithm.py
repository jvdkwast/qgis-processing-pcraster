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
                       QgsProcessingException)

from pcraster_tools.processing.algorithm import PCRasterAlgorithm


class PCRasterIfThenAlgorithm(PCRasterAlgorithm):
    """
    Return missing values if condition is not met.
    """

    INPUT_CONDITION = 'INPUT'
    INPUT_TRUE = 'INPUT1'
    OUTPUT = 'OUTPUT'

    def createInstance(self):  # pylint: disable=missing-function-docstring
        return PCRasterIfThenAlgorithm()

    def name(self):  # pylint: disable=missing-function-docstring
        return 'ifthen'

    def displayName(self):  # pylint: disable=missing-function-docstring
        return self.tr('if then')

    def group(self):  # pylint: disable=missing-function-docstring
        return self.tr('Conditional and boolean operators')

    def groupId(self):  # pylint: disable=missing-function-docstring
        return 'conditional'

    def shortHelpString(self):  # pylint: disable=missing-function-docstring
        return self.tr(
            """Return missing values if condition is not met.

            <a href="https://pcraster.geo.uu.nl/pcraster/4.3.1/documentation/pcraster_manual/sphinx/op_ifthen.html#ifthen">PCRaster documentation</a>

            Parameters:

            * <b>Input boolean condition raster layer</b> (required) - boolean raster. True cells will get values of input raster layer. False cells will get nodata
            * <b>Input True Raster</b> (required) - raster layer of any data type with cells that will be assigned to True cells of the boolean input layer
            * <b>Output raster</b> (required) - raster layer of same data type as input raster
            """
        )

    def initAlgorithm(self, config=None):  # pylint: disable=missing-function-docstring,unused-argument
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_CONDITION,
                self.tr('Input Boolean Condition Raster')
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_TRUE,
                self.tr('Input True Raster')
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.OUTPUT,
                self.tr('Output Raster')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):  # pylint: disable=missing-function-docstring,unused-argument,too-many-locals
        try:
            from pcraster import (   # pylint: disable=import-outside-toplevel
                setclone,
                readmap,
                report,
                ifthen
            )
        except ImportError as e:
            raise QgsProcessingException('PCRaster library is not available') from e

        input_condition = self.parameterAsRasterLayer(parameters, self.INPUT_CONDITION, context)
        input_true = self.parameterAsRasterLayer(parameters, self.INPUT_TRUE, context)
        setclone(input_condition.dataProvider().dataSourceUri())
        conditionRaster = readmap(input_condition.dataProvider().dataSourceUri())
        trueRaster = readmap(input_true.dataProvider().dataSourceUri())
        resultRaster = ifthen(conditionRaster, trueRaster)

        outputFilePath = self.parameterAsOutputLayer(parameters, self.OUTPUT, context)

        report(resultRaster, outputFilePath)

        return {self.OUTPUT: outputFilePath}
