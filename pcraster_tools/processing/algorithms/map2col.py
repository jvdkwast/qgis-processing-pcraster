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

import os

from qgis.core import (QgsProcessing,
                       QgsProcessingParameterMultipleLayers,
                       QgsProcessingParameterFileDestination,
                       )

from pcraster_tools.processing.algorithm import PCRasterAlgorithm


class Map2colAlgorithm(PCRasterAlgorithm):
    """
    Converts from PCRaster map format to column file format.
    """

    INPUT_RASTERS = 'INPUT'
    OUTPUT_CSV = 'OUTPUT'

    def createInstance(self):  # pylint: disable=missing-function-docstring
        return Map2colAlgorithm()

    def name(self):  # pylint: disable=missing-function-docstring
        return 'map2col'

    def displayName(self):  # pylint: disable=missing-function-docstring
        return self.tr('PCRaster maps to column file')

    def group(self):  # pylint: disable=missing-function-docstring
        return self.tr('Data management')

    def groupId(self):  # pylint: disable=missing-function-docstring
        return self.tr('data')

    def shortHelpString(self):  # pylint: disable=missing-function-docstring
        return self.tr(
            """Converts from PCRaster map format to column file format (csv).

            <a href="{}">PCRaster documentation</a>

            Parameters:

            * <b>Input Raster layers</b> (required) - raster layers from any data type. The maps must have the same projection, the other location attributes (use the resample tool if this is not the case) and the data types may be different between the maps.
            * <b>Output text file</b> (required) - text file with comma separated columns
            """
        ).format(PCRasterAlgorithm.documentation_url('app_map2col.html'))

    def initAlgorithm(self, config=None):  # pylint: disable=missing-function-docstring,unused-argument
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.INPUT_RASTERS,
                self.tr('Input Raster Layer(s)'),
                QgsProcessing.TypeRaster
            )
        )

        self.addParameter(
                QgsProcessingParameterFileDestination(
                self.OUTPUT_CSV,
                self.tr('Output textfile with columns'),
                defaultValue=None,
                optional=False
            )
        )

    def processAlgorithm(self, parameters, context, feedback):  # pylint: disable=missing-function-docstring,unused-argument,too-many-locals
        input_rasters = []
        for layer in self.parameterAsLayerList(parameters, self.INPUT_RASTERS, context):
            input_rasters.append(layer.source())

        dst_filename = self.parameterAsFileOutput(parameters, self.OUTPUT_CSV, context)
        rasterstrings = ' '.join(f'"{raster}"' for raster in input_rasters)
        cmd = f'map2col -s , {rasterstrings} "{dst_filename}"'
        feedback.pushInfo(cmd)
        os.system(cmd)

        return {self.OUTPUT_CSV: dst_filename}
