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


class PCRasterClumpAlgorithm(PCRasterAlgorithm):
    """
    Contiguous groups of cells with the same value (‘clumps’)
    """

    INPUT_RASTER = 'INPUT'
    INPUT_DIRECTIONS = 'INPUT1'
    OUTPUT_CLUMP = 'OUTPUT'

    def createInstance(self):  # pylint: disable=missing-function-docstring
        return PCRasterClumpAlgorithm()

    def name(self):  # pylint: disable=missing-function-docstring
        return 'clump'

    def displayName(self):  # pylint: disable=missing-function-docstring
        return self.tr('clump')

    def group(self):  # pylint: disable=missing-function-docstring
        return self.tr('Area operations')

    def groupId(self):  # pylint: disable=missing-function-docstring
        return 'area'

    def shortHelpString(self):  # pylint: disable=missing-function-docstring
        return self.tr(
            """Contiguous groups of cells with the same value (‘clumps’)

                <a href="https://pcraster.geo.uu.nl/pcraster/4.3.1/documentation/pcraster_manual/sphinx/op_clump.html">PCRaster documentation</a>

                Parameters:

                 * <b>Input raster layer</b> (required) - Boolean, nominal or ordinal raster layer
                 * <b>Input directions</b> (required) - diagonal (D8) or non-diagonal (D4)
                 * <b>Output clump raster layer</b> (required) - nominal raster layer with clumps
            """
        )

    def initAlgorithm(self, config=None):  # pylint: disable=missing-function-docstring,unused-argument
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_RASTER,
                self.tr('Input raster layer')
            )
        )

        directionoption = [self.tr('Diagonal (8 cell)'), self.tr('Non-diagonal (4 cell)')]
        self.addParameter(
            QgsProcessingParameterEnum(
                self.INPUT_DIRECTIONS,
                self.tr('Clump direction'),
                directionoption,
                defaultValue=0
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.OUTPUT_CLUMP,
                self.tr('Clump layer')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):  # pylint: disable=missing-function-docstring,unused-argument,too-many-locals
        try:
            from pcraster import (   # pylint: disable=import-outside-toplevel
                setclone,
                readmap,
                report,
                setglobaloption,
                clump
            )
        except ImportError as e:
            raise QgsProcessingException('PCRaster library is not available') from e

        input_raster = self.parameterAsRasterLayer(parameters, self.INPUT_RASTER, context)
        direction_options = self.parameterAsEnum(parameters, self.INPUT_DIRECTIONS, context)
        if direction_options == 0:
            setglobaloption("diagonal")
        else:
            setglobaloption("nondiagonal")
        setclone(input_raster.dataProvider().dataSourceUri())
        ClassLayer = readmap(input_raster.dataProvider().dataSourceUri())
        ClumpResult = clump(ClassLayer)
        outputFilePath = self.parameterAsOutputLayer(parameters, self.OUTPUT_CLUMP, context)

        report(ClumpResult, outputFilePath)

        return {self.OUTPUT_CLUMP: outputFilePath}
