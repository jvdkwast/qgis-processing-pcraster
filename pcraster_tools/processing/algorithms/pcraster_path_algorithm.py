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
    path
)
from qgis.core import (QgsProcessingParameterRasterDestination,
                       QgsProcessingParameterRasterLayer)

from pcraster_tools.processing.algorithm import PCRasterAlgorithm


class PCRasterPathAlgorithm(PCRasterAlgorithm):
    """
    Path over the local drain direction network downstream to its pit
    """

    INPUT_LDD = 'INPUT'
    INPUT_POINTS = 'INPUT2'
    OUTPUT_PATH = 'OUTPUT'

    def createInstance(self):  # pylint: disable=missing-function-docstring
        return PCRasterPathAlgorithm()

    def name(self):  # pylint: disable=missing-function-docstring
        return 'path'

    def displayName(self):  # pylint: disable=missing-function-docstring
        return self.tr('path')

    def group(self):  # pylint: disable=missing-function-docstring
        return self.tr('PCRaster')

    def groupId(self):  # pylint: disable=missing-function-docstring
        return 'pcraster'

    def shortHelpString(self):  # pylint: disable=missing-function-docstring
        return self.tr(
            """Path over the local drain direction network downstream to its pit
            
            <a href="https://pcraster.geo.uu.nl/pcraster/4.3.1/documentation/pcraster_manual/sphinx/op_path.html">PCRaster documentation</a>
            
            Parameters:
            
            * <b>Input Local Drain Direction raster</b> (required) - LDD raster
            * <b>Points raster layer</b> (required) - Boolean raster layer with cells from which path to pit is calculated
            * <b>Result path layer</b> (required) - Boolean raster with path from points to downstream pit
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
            QgsProcessingParameterRasterLayer(
                self.INPUT_POINTS,
                self.tr('Points raster layer')
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.OUTPUT_PATH,
                self.tr('Result path layer')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):  # pylint: disable=missing-function-docstring
        input_ldd = self.parameterAsRasterLayer(parameters, self.INPUT_LDD, context)
        input_points = self.parameterAsRasterLayer(parameters, self.INPUT_POINTS, context)
        setclone(input_ldd.dataProvider().dataSourceUri())
        LDD = readmap(input_ldd.dataProvider().dataSourceUri())
        Points = readmap(input_points.dataProvider().dataSourceUri())
        PathLayer = path(LDD, Points)
        outputFilePath = self.parameterAsOutputLayer(parameters, self.OUTPUT_PATH, context)
        report(PathLayer, outputFilePath)

        return {self.OUTPUT_PATH: outputFilePath}
