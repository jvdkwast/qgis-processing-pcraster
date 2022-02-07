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
                       QgsProcessingParameterNumber,
                       QgsProcessingException)

from pcraster_tools.processing.algorithm import PCRasterAlgorithm


class PCRasterExtentofviewAlgorithm(PCRasterAlgorithm):
    """
    Total length of the lines in a number of directions from the cell under consideration to the first cell with a different value.
    """

    INPUT_CLASSES = 'INPUT'
    INPUT_DIRECTIONS = 'INPUT2'
    OUTPUT_RASTER = 'OUTPUT'

    def createInstance(self):  # pylint: disable=missing-function-docstring
        return PCRasterExtentofviewAlgorithm()

    def name(self):  # pylint: disable=missing-function-docstring
        return 'extentofview'

    def displayName(self):  # pylint: disable=missing-function-docstring
        return self.tr('extentofview')

    def group(self):  # pylint: disable=missing-function-docstring
        return self.tr('Proximity analysis')

    def groupId(self):  # pylint: disable=missing-function-docstring
        return 'proximity'

    def shortHelpString(self):  # pylint: disable=missing-function-docstring
        return self.tr(
            """Total length of the lines in a number of directions from the cell under consideration to the first cell with a different value.

            <a href="{}">PCRaster documentation</a>

            Parameters:

            * <b>Input class raster layer</b> (required) - boolean, nominal or ordinal raster layer
            * <b>Input number of directions</b> (required) - number of directions
            * <b>Output extent of view raster</b> (required) - Scalar raster with total length of the lines in a number of directions from the cell under consideration to the first cell with a different value.
            """
        ).format(PCRasterAlgorithm.documentation_url('op_extentofview.html'))

    def initAlgorithm(self, config=None):  # pylint: disable=missing-function-docstring,unused-argument
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_CLASSES,
                self.tr('Class raster layer')
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.INPUT_DIRECTIONS,
                self.tr('Number of directions'),
                defaultValue=4
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.OUTPUT_RASTER,
                self.tr('Output extent of view layer')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):  # pylint: disable=missing-function-docstring,unused-argument,too-many-locals
        try:
            from pcraster import (   # pylint: disable=import-outside-toplevel
                setclone,
                readmap,
                report,
                extentofview
            )
        except ImportError as e:
            raise QgsProcessingException('PCRaster library is not available') from e

        input_discrete = self.parameterAsRasterLayer(parameters, self.INPUT_CLASSES, context)
        input_directions = self.parameterAsDouble(parameters, self.INPUT_DIRECTIONS, context)
        setclone(input_discrete.dataProvider().dataSourceUri())
        ClassLayer = readmap(input_discrete.dataProvider().dataSourceUri())
        ResultExtentOfView = extentofview(ClassLayer, input_directions)
        outputFilePath = self.parameterAsOutputLayer(parameters, self.OUTPUT_RASTER, context)

        report(ResultExtentOfView, outputFilePath)

        self.set_output_crs(output_file=outputFilePath, crs=input_discrete.crs(), feedback=feedback, context=context)

        return {self.OUTPUT_RASTER: outputFilePath}
