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
    window4total
)
from qgis.core import (QgsProcessingParameterRasterDestination,
                       QgsProcessingParameterRasterLayer)

from pcraster_tools.processing.algorithm import PCRasterAlgorithm


class PCRasterwindow4totalAlgorithm(PCRasterAlgorithm):
    """
    Sum the values of the four surrounding cells.
    """

    INPUT_RASTER = 'INPUT'
    OUTPUT_RASTER = 'OUTPUT'

    def createInstance(self):  # pylint: disable=missing-function-docstring
        return PCRasterwindow4totalAlgorithm()

    def name(self):  # pylint: disable=missing-function-docstring
        return 'window4total'

    def displayName(self):  # pylint: disable=missing-function-docstring
        return self.tr('window4total')

    def group(self):  # pylint: disable=missing-function-docstring
        return self.tr('PCRaster')

    def groupId(self):  # pylint: disable=missing-function-docstring
        return 'pcraster'

    def shortHelpString(self):  # pylint: disable=missing-function-docstring
        return self.tr(
            """Sum the values of the four surrounding cells.
            <a href="https://pcraster.geo.uu.nl/pcraster/4.3.1/documentation/pcraster_manual/sphinx/op_window4total.html">PCRaster documentation</a>

            Parameters:

            * <b>Input raster</b> (required) - scalar raster layer
            * <b>Output roundup raster</b> (required) - Scalar raster with result
            """
        )

    def initAlgorithm(self, config=None):  # pylint: disable=missing-function-docstring
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_RASTER,
                self.tr('Scalar Raster layer')
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.OUTPUT_RASTER,
                self.tr("Output window4total layer")
            )
        )

    def processAlgorithm(self, parameters, context, feedback):  # pylint: disable=missing-function-docstring
        input_raster = self.parameterAsRasterLayer(parameters, self.INPUT_RASTER, context)

        output_raster = self.parameterAsRasterLayer(parameters, self.OUTPUT_RASTER, context)
        setclone(input_raster.dataProvider().dataSourceUri())
        InputRaster = readmap(input_raster.dataProvider().dataSourceUri())
        window4totalLayer = window4total(InputRaster)
        outputFilePath = self.parameterAsOutputLayer(parameters, self.OUTPUT_RASTER, context)

        report(window4totalLayer, outputFilePath)

        return {self.OUTPUT_RASTER: output_raster}
