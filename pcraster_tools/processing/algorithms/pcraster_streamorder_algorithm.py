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
    streamorder
)
from qgis.core import (QgsProcessingParameterRasterDestination,
                       QgsProcessingParameterRasterLayer)

from pcraster_tools.processing.algorithm import PCRasterAlgorithm


class PCRasterStreamOrderAlgorithm(PCRasterAlgorithm):
    """
    Stream order index of all cells on a local drain direction network
    """

    INPUT_LDD = 'INPUT'
    OUTPUT_STREAMORDER = 'OUTPUT'

    def createInstance(self):  # pylint: disable=missing-function-docstring
        return PCRasterStreamOrderAlgorithm()

    def name(self):  # pylint: disable=missing-function-docstring
        return 'streamorder'

    def displayName(self):  # pylint: disable=missing-function-docstring
        return self.tr('streamorder')

    def group(self):  # pylint: disable=missing-function-docstring
        return self.tr('Hydrological and material transport operations')

    def groupId(self):  # pylint: disable=missing-function-docstring
        return 'hydrological'

    def shortHelpString(self):  # pylint: disable=missing-function-docstring
        return self.tr(
            """Stream order index of all cells on a local drain direction network

            <a href="https://pcraster.geo.uu.nl/pcraster/4.3.1/documentation/pcraster_manual/sphinx/op_streamorder.html">PCRaster documentation</a>

            Parameters:

            * <b>Input Local Drain Direction layer</b> (required) - raster layer with LDD data type
            * <b>Output Stream Order raster</b> (required) - ordinal raster with Strahler orders
            """
        )

    def initAlgorithm(self, config=None):  # pylint: disable=missing-function-docstring,unused-argument
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_LDD,
                self.tr('Local Drain Direction layer')
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.OUTPUT_STREAMORDER,
                self.tr('Stream Order layer')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):  # pylint: disable=missing-function-docstring,unused-argument
        input_ldd = self.parameterAsRasterLayer(parameters, self.INPUT_LDD, context)

        setclone(input_ldd.dataProvider().dataSourceUri())
        LDD = readmap(input_ldd.dataProvider().dataSourceUri())
        strahler = streamorder(LDD)
        outputFilePath = self.parameterAsOutputLayer(parameters, self.OUTPUT_STREAMORDER, context)
        report(strahler, outputFilePath)

        return {self.OUTPUT_STREAMORDER: outputFilePath}
