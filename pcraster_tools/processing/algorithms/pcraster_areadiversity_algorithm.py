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
    areadiversity,
    report
)
from qgis.core import (QgsProcessingParameterRasterDestination,
                       QgsProcessingParameterRasterLayer)

from pcraster_tools.processing.algorithm import PCRasterAlgorithm


class PCRasterAreadiversityAlgorithm(PCRasterAlgorithm):
    """
    Number of unique cell values within an area
    """

    INPUT_CLASS = 'INPUT'
    INPUT_DISCRETE = 'INPUT2'
    OUTPUT_AREADIVERSITY = 'OUTPUT'

    def createInstance(self):  # pylint: disable=missing-function-docstring
        return PCRasterAreadiversityAlgorithm()

    def name(self):  # pylint: disable=missing-function-docstring
        return 'areadiversity'

    def displayName(self):  # pylint: disable=missing-function-docstring
        return self.tr('areadiversity')

    def group(self):  # pylint: disable=missing-function-docstring
        return self.tr('PCRaster')

    def groupId(self):  # pylint: disable=missing-function-docstring
        return 'pcraster'

    def shortHelpString(self):  # pylint: disable=missing-function-docstring
        return self.tr(
            """Number of unique cell values within an area

            <a href="https://pcraster.geo.uu.nl/pcraster/4.3.1/documentation/pcraster_manual/sphinx/op_areadiversity.html">PCRaster documentation</a>

            Parameters:

            * <b>Input class raster layer</b> (required) - boolean, nominal or ordinal raster layer
            * <b>Input discrete raster layer</b> (required) - boolean, nominal or ordinal raster layer
            * <b>Output area raster</b> (required) - Scalar raster with number of unique cell values within an area
            """
        )

    def initAlgorithm(self, config=None):  # pylint: disable=missing-function-docstring
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_CLASS,
                self.tr('Class raster layer')
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_DISCRETE,
                self.tr('Discrete raster layer')
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.OUTPUT_AREADIVERSITY,
                self.tr('Output area diversity layer')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):  # pylint: disable=missing-function-docstring
        input_class = self.parameterAsRasterLayer(parameters, self.INPUT_CLASS, context)
        input_discrete = self.parameterAsRasterLayer(parameters, self.INPUT_DISCRETE, context)
        setclone(input_discrete.dataProvider().dataSourceUri())
        ClassLayer = readmap(input_class.dataProvider().dataSourceUri())
        DiscreteLayer = readmap(input_discrete.dataProvider().dataSourceUri())
        AreaDiversity = areadiversity(DiscreteLayer, ClassLayer)
        outputFilePath = self.parameterAsOutputLayer(parameters, self.OUTPUT_AREADIVERSITY, context)

        report(AreaDiversity, outputFilePath)

        return {self.OUTPUT_AREADIVERSITY: outputFilePath}
