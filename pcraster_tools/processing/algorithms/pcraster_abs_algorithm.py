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


class PCRasterAbsAlgorithm(PCRasterAlgorithm):
    """
    Absolute value
    """

    INPUT_RASTER = 'INPUT'
    OUTPUT_RASTER = 'OUTPUT'

    def createInstance(self):  # pylint: disable=missing-function-docstring
        return PCRasterAbsAlgorithm()

    def name(self):  # pylint: disable=missing-function-docstring
        return 'abs'

    def displayName(self):  # pylint: disable=missing-function-docstring
        return self.tr('abs')

    def group(self):  # pylint: disable=missing-function-docstring
        return self.tr('Mathematical operators')

    def groupId(self):  # pylint: disable=missing-function-docstring
        return 'operators'

    def shortHelpString(self):  # pylint: disable=missing-function-docstring
        return self.tr(
            """Absolute value

            <a href="https://pcraster.geo.uu.nl/pcraster/4.3.1/documentation/pcraster_manual/sphinx/op_abs.html">PCRaster documentation</a>

            Parameters:

            * <b>Input raster</b> (required) - scalar raster layer
            * <b>Output raster</b> (required) - Scalar raster with result
            """
        )

    def initAlgorithm(self, config=None):  # pylint: disable=missing-function-docstring,unused-argument
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_RASTER,
                self.tr('Raster layer')
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.OUTPUT_RASTER,
                self.tr("Output absolute value layer")
            )
        )

    def processAlgorithm(self, parameters, context, feedback):  # pylint: disable=missing-function-docstring,unused-argument,too-many-locals
        try:
            from pcraster import (   # pylint: disable=import-outside-toplevel, redefined-builtin
                setclone,
                readmap,
                report,
                abs
            )
        except ImportError as e:
            raise QgsProcessingException('PCRaster library is not available') from e

        input_raster = self.parameterAsRasterLayer(parameters, self.INPUT_RASTER, context)

        setclone(input_raster.dataProvider().dataSourceUri())
        input_raster = readmap(input_raster.dataProvider().dataSourceUri())
        abs_layer = abs(input_raster)
        output_file_path = self.parameterAsOutputLayer(parameters, self.OUTPUT_RASTER, context)

        report(abs_layer, output_file_path)

        return {self.OUTPUT_RASTER: output_file_path}
