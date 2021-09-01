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


class PCRasterComparisonOperatorsAlgorithm(PCRasterAlgorithm):
    """
    Boolean operators
    """

    INPUT1 = 'INPUT'
    INPUT_OPERATOR = 'INPUT1'
    INPUT2 = 'INPUT2'
    OUTPUT = 'OUTPUT'

    def createInstance(self):  # pylint: disable=missing-function-docstring
        return PCRasterComparisonOperatorsAlgorithm()

    def name(self):  # pylint: disable=missing-function-docstring
        return 'comparisonoperators'

    def displayName(self):  # pylint: disable=missing-function-docstring
        return self.tr('comparison operators')

    def group(self):  # pylint: disable=missing-function-docstring
        return self.tr('Conditional and boolean operators')

    def groupId(self):  # pylint: disable=missing-function-docstring
        return 'conditional'

    def shortHelpString(self):  # pylint: disable=missing-function-docstring
        return self.tr(
            """Boolean operators

            <a href="https://pcraster.geo.uu.nl/pcraster/4.3.1/documentation/pcraster_manual/sphinx/secfunclist.html#comparison-operators">PCRaster documentation</a>

            Parameters:

            * <b>Input raster layer</b> (required) - raster layer of any data type
            * <b>Comparison operator</b> (required) - ==,>,>=,<,<=,!=
            * <b>Input raster layer</b> (required) - raster layer of same data type as first input raster layer
            * <b>Output raster</b> (required) - boolean raster layer
            """
        )

    def initAlgorithm(self, config=None):  # pylint: disable=missing-function-docstring,unused-argument
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT1,
                self.tr('Input raster')
            )
        )

        unitoption = [self.tr('=='), self.tr('>='), self.tr('>'), self.tr('<='), self.tr('<'), self.tr('!=')]
        self.addParameter(
            QgsProcessingParameterEnum(
                self.INPUT_OPERATOR,
                self.tr('Comparison operator'),
                unitoption,
                defaultValue=0
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT2,
                self.tr('Input raster')
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.OUTPUT,
                self.tr('Output Boolean raster')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):  # pylint: disable=missing-function-docstring,unused-argument,too-many-locals
        try:
            from pcraster import (   # pylint: disable=import-outside-toplevel
                setclone,
                readmap,
                report,
            )
        except ImportError as e:
            raise QgsProcessingException('PCRaster library is not available') from e

        input1 = self.parameterAsRasterLayer(parameters, self.INPUT1, context)
        input2 = self.parameterAsRasterLayer(parameters, self.INPUT2, context)
        comparisonoperator = self.parameterAsEnum(parameters, self.INPUT_OPERATOR, context)
        setclone(input1.dataProvider().dataSourceUri())
        Expression1 = readmap(input1.dataProvider().dataSourceUri())
        Expression2 = readmap(input2.dataProvider().dataSourceUri())
        if comparisonoperator == 0:
            ResultComparison = Expression1 == Expression2
        elif comparisonoperator == 1:
            ResultComparison = Expression1 >= Expression2
        elif comparisonoperator == 2:
            ResultComparison = Expression1 > Expression2
        elif comparisonoperator == 3:
            ResultComparison = Expression1 <= Expression2
        elif comparisonoperator == 4:
            ResultComparison = Expression1 < Expression2
        else:
            ResultComparison = Expression1 != Expression2

        outputFilePath = self.parameterAsOutputLayer(parameters, self.OUTPUT, context)

        report(ResultComparison, outputFilePath)

        return {self.OUTPUT: outputFilePath}
