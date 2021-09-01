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
                       QgsProcessingParameterRasterLayer,
                       QgsProcessingParameterMultipleLayers,
                       QgsProcessingParameterRasterDestination
                       )

from pcraster_tools.processing.algorithm import PCRasterAlgorithm


class ResampleAlgorithm(PCRasterAlgorithm):
    """
    Cuts one map or joins together several maps by resampling to the cells of the result map.
    """

    INPUT_RASTERS = 'INPUT'
    INPUT_MASK = 'INPUT1'
    OUTPUT_PCRASTER = 'OUTPUT'

    def createInstance(self):  # pylint: disable=missing-function-docstring
        return ResampleAlgorithm()

    def name(self):  # pylint: disable=missing-function-docstring
        return 'resample'

    def displayName(self):  # pylint: disable=missing-function-docstring
        return self.tr('resample')

    def group(self):  # pylint: disable=missing-function-docstring
        return self.tr('Data management')

    def groupId(self):  # pylint: disable=missing-function-docstring
        return self.tr('data')

    def shortHelpString(self):  # pylint: disable=missing-function-docstring
        return self.tr(
            """Cuts one map or joins together several maps by resampling to the cells of the result map.

            <a href="https://pcraster.geo.uu.nl/pcraster/4.3.1/documentation/pcraster_manual/sphinx/app_resample.html">PCRaster documentation</a>

            Parameters:

            * <b>Input Raster layers</b> (required) - raster layers from any data type (all must have the same data type). When one layer is used, it will be resampled to the raster properties of the mask layer. When multiple layers are used, they will also be mosaiced into a raster with the dimensions of the mask layer.
            * <b>Input Mask</b> (required) - clone map that will be used to determine the output raster properties
            * <b>Output raster layer</b> (required) - raster layer with resample result
            """
        )

    def initAlgorithm(self, config=None):  # pylint: disable=missing-function-docstring,unused-argument
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.INPUT_RASTERS,
                self.tr('Input Raster Layer(s)'),
                QgsProcessing.TypeRaster
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_MASK,
                self.tr('Raster mask layer')
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.OUTPUT_PCRASTER,
                self.tr('Output resample raster layer')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):  # pylint: disable=missing-function-docstring,unused-argument
        input_rasters = []
        for layer in self.parameterAsLayerList(parameters, self.INPUT_RASTERS, context):
            input_rasters.append(layer.source())
        input_mask = self.parameterAsRasterLayer(parameters, self.INPUT_MASK, context)
        clone = input_mask.dataProvider().dataSourceUri()

        dst_filename = self.parameterAsOutputLayer(parameters, self.OUTPUT_PCRASTER, context)
        rasterstrings = " ".join(input_rasters)
        cmd = "resample {} {} --clone {}".format(rasterstrings, dst_filename, clone)
        os.system(cmd)

        return {self.OUTPUT_PCRASTER: dst_filename}
