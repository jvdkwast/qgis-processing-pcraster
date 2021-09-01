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
    pcrand,
    pcrnot,
    pcrxor,
    pcror
)
from qgis.core import (QgsProcessingParameterRasterDestination,
                       QgsProcessingParameterEnum,
                       QgsProcessingParameterRasterLayer)

from pcraster_tools.processing.algorithm import PCRasterAlgorithm


class PCRasterBooleanOperatorsAlgorithm(PCRasterAlgorithm):
    """
    Boolean operators
    """

    INPUT_BOOLEAN1 = 'INPUT'
    INPUT_OPERATOR = 'INPUT1'
    INPUT_BOOLEAN2 = 'INPUT2'
    OUTPUT = 'OUTPUT'

    def createInstance(self):  # pylint: disable=missing-function-docstring
        return PCRasterBooleanOperatorsAlgorithm()

    def name(self):  # pylint: disable=missing-function-docstring
        return 'booleanoperators'

    def displayName(self):  # pylint: disable=missing-function-docstring
        return self.tr('boolean operators')

    def group(self):  # pylint: disable=missing-function-docstring
        return self.tr('PCRaster')

    def groupId(self):  # pylint: disable=missing-function-docstring
        return 'pcraster'

    def shortHelpString(self):  # pylint: disable=missing-function-docstring
        return self.tr(
            """Boolean operators
            
            <a href="https://pcraster.geo.uu.nl/pcraster/4.3.1/documentation/pcraster_manual/sphinx/secfunclist.html#boolean-operators">PCRaster documentation</a>
            
            Parameters:
            
            * <b>Input boolean raster layer</b> (required) - boolean raster layer
            * <b>Boolean operator</b> (required) - AND, OR, XOR, NOT
            * <b>Input boolean raster layer</b> (required) - boolean raster layer
            * <b>Output raster</b> (required) - boolean raster layer
            """
        )

    def initAlgorithm(self, config=None):  # pylint: disable=missing-function-docstring
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_BOOLEAN1,
                self.tr('Input Boolean raster')
            )
        )

        unitoption = [self.tr('AND'), self.tr('NOT'), self.tr('OR'), self.tr('XOR')]
        self.addParameter(
            QgsProcessingParameterEnum(
                self.INPUT_OPERATOR,
                self.tr('Boolean operator'),
                unitoption,
                defaultValue=0
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_BOOLEAN2,
                self.tr('Input Boolean raster')
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.OUTPUT,
                self.tr('Output Boolean raster')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):  # pylint: disable=missing-function-docstring
        input_boolean1 = self.parameterAsRasterLayer(parameters, self.INPUT_BOOLEAN1, context)
        input_boolean2 = self.parameterAsRasterLayer(parameters, self.INPUT_BOOLEAN2, context)
        booleanoperator = self.parameterAsEnum(parameters, self.INPUT_OPERATOR, context)
        setclone(input_boolean1.dataProvider().dataSourceUri())
        Expression1 = readmap(input_boolean1.dataProvider().dataSourceUri())
        Expression2 = readmap(input_boolean2.dataProvider().dataSourceUri())
        if booleanoperator == 0:
            ResultBoolean = pcrand(Expression1, Expression2)
        elif booleanoperator == 1:
            ResultBoolean = pcrnot(Expression1, Expression2)
        elif booleanoperator == 2:
            ResultBoolean = pcror(Expression1, Expression2)
        else:
            ResultBoolean = pcrxor(Expression1, Expression2)

        outputFilePath = self.parameterAsOutputLayer(parameters, self.OUTPUT, context)

        report(ResultBoolean, outputFilePath)

        return {self.OUTPUT: outputFilePath}
