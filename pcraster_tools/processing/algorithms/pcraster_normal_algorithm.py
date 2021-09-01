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
    normal
)
from qgis.core import (QgsProcessingParameterRasterDestination,
                       QgsProcessingParameterRasterLayer)

from pcraster_tools.processing.algorithm import PCRasterAlgorithm


class PCRasterNormalAlgorithm(PCRasterAlgorithm):
    """
    Boolean TRUE cell gets value taken from a normal distribution
    """

    INPUT_BOOLEAN = 'INPUT'
    OUTPUT = 'OUTPUT'

    def createInstance(self):  # pylint: disable=missing-function-docstring
        return PCRasterNormalAlgorithm()

    def name(self):  # pylint: disable=missing-function-docstring
        return 'normal'

    def displayName(self):  # pylint: disable=missing-function-docstring
        return self.tr('normal')

    def group(self):  # pylint: disable=missing-function-docstring
        return self.tr('Mathematical operators')

    def groupId(self):  # pylint: disable=missing-function-docstring
        return 'operators'

    def shortHelpString(self):  # pylint: disable=missing-function-docstring
        return self.tr(
            """Boolean TRUE cell gets value taken from a normal distribution

            <a href="https://pcraster.geo.uu.nl/pcraster/4.3.1/documentation/pcraster_manual/sphinx/op_normal.html">PCRaster documentation</a>

            Parameters:

            * <b>Input boolean raster</b> (required) - Raster layer with boolean data type
            * <b>Output raster</b> (required) - Scalar raster with values taken from a normal distribution
            """
        )

    def initAlgorithm(self, config=None):  # pylint: disable=missing-function-docstring,unused-argument
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_BOOLEAN,
                self.tr('Input boolean layer')
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.OUTPUT,
                self.tr("Normal output layer")
            )
        )

    def processAlgorithm(self, parameters, context, feedback):  # pylint: disable=missing-function-docstring,unused-argument
        input_boolean = self.parameterAsRasterLayer(parameters, self.INPUT_BOOLEAN, context)

        setclone(input_boolean.dataProvider().dataSourceUri())
        InputBoolean = readmap(input_boolean.dataProvider().dataSourceUri())
        NormalLayer = normal(InputBoolean)
        outputFilePath = self.parameterAsOutputLayer(parameters, self.OUTPUT, context)

        report(NormalLayer, outputFilePath)

        return {self.OUTPUT: outputFilePath}
