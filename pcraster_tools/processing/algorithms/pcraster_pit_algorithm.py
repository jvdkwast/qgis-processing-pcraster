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
    pit
)
from qgis.core import (QgsProcessingParameterRasterDestination,
                       QgsProcessingParameterRasterLayer)

from pcraster_tools.processing.algorithm import PCRasterAlgorithm


class PCRasterPitAlgorithm(PCRasterAlgorithm):
    """
    Unique value for each pit cell
    """

    INPUT_LDD = 'INPUT'
    OUTPUT_PIT = 'OUTPUT'

    def createInstance(self):  # pylint: disable=missing-function-docstring
        return PCRasterPitAlgorithm()

    def name(self):  # pylint: disable=missing-function-docstring
        return 'pit'

    def displayName(self):  # pylint: disable=missing-function-docstring
        return self.tr('pit')

    def group(self):  # pylint: disable=missing-function-docstring
        return self.tr('PCRaster')

    def groupId(self):  # pylint: disable=missing-function-docstring
        return 'pcraster'

    def shortHelpString(self):  # pylint: disable=missing-function-docstring
        return self.tr(
            """Unique value for each pit cell

            <a href="https://pcraster.geo.uu.nl/pcraster/4.3.1/documentation/pcraster_manual/sphinx/op_pit.html">PCRaster documentation</a>

            Parameters:

            * <b>Input LDD raster layer</b> (required) - raster layer with LDD data type
            * <b>Output pit raster layer</b> (required) - nominal raster with unique values for pits
            """
        )

    def initAlgorithm(self, config=None):  # pylint: disable=missing-function-docstring
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_LDD,
                self.tr('LDD layer')
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.OUTPUT_PIT,
                self.tr("Output pit raster layer")
            )
        )

    def processAlgorithm(self, parameters, context, feedback):  # pylint: disable=missing-function-docstring
        input_ldd = self.parameterAsRasterLayer(parameters, self.INPUT_LDD, context)

        setclone(input_ldd.dataProvider().dataSourceUri())
        LDD = readmap(input_ldd.dataProvider().dataSourceUri())
        PitLayer = pit(LDD)
        outputFilePath = self.parameterAsOutputLayer(parameters, self.OUTPUT_PIT, context)

        report(PitLayer, outputFilePath)

        return {self.OUTPUT_PIT: outputFilePath}
