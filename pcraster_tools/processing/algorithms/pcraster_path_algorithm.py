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
        return self.tr('Hydrological and material transport operations')

    def groupId(self):  # pylint: disable=missing-function-docstring
        return 'hydrological'

    def shortHelpString(self):  # pylint: disable=missing-function-docstring
        return self.tr(
            """Path over the local drain direction network downstream to its pit

            <a href="{}">PCRaster documentation</a>

            Parameters:

            * <b>Input Local Drain Direction raster</b> (required) - LDD raster
            * <b>Points raster layer</b> (required) - Boolean raster layer with cells from which path to pit is calculated
            * <b>Result path layer</b> (required) - Boolean raster with path from points to downstream pit
            """
        ).format(PCRasterAlgorithm.documentation_url('op_path.html'))

    def initAlgorithm(self, config=None):  # pylint: disable=missing-function-docstring,unused-argument
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

    def processAlgorithm(self, parameters, context, feedback):  # pylint: disable=missing-function-docstring,unused-argument,too-many-locals
        try:
            from pcraster import (   # pylint: disable=import-outside-toplevel
                setclone,
                readmap,
                report,
                path
            )
        except ImportError as e:
            raise QgsProcessingException('PCRaster library is not available') from e

        input_ldd = self.parameterAsRasterLayer(parameters, self.INPUT_LDD, context)
        input_points = self.parameterAsRasterLayer(parameters, self.INPUT_POINTS, context)
        setclone(input_ldd.dataProvider().dataSourceUri())
        LDD = readmap(input_ldd.dataProvider().dataSourceUri())
        Points = readmap(input_points.dataProvider().dataSourceUri())
        PathLayer = path(LDD, Points)
        outputFilePath = self.parameterAsOutputLayer(parameters, self.OUTPUT_PATH, context)
        report(PathLayer, outputFilePath)

        self.set_output_crs(output_file=outputFilePath, crs=input_ldd.crs(), feedback=feedback, context=context)

        return {self.OUTPUT_PATH: outputFilePath}
