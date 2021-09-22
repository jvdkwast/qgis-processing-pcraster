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


class PCRasterUpstreamAlgorithm(PCRasterAlgorithm):
    """
    Sum of the cell values of its first upstream cell(s)
    """

    INPUT_LDD = 'INPUT1'
    INPUT_RASTER = 'INPUT2'
    OUTPUT_UPSTREAM = 'OUTPUT'

    def createInstance(self):  # pylint: disable=missing-function-docstring
        return PCRasterUpstreamAlgorithm()

    def name(self):  # pylint: disable=missing-function-docstring
        return 'upstream'

    def displayName(self):  # pylint: disable=missing-function-docstring
        return self.tr('upstream')

    def group(self):  # pylint: disable=missing-function-docstring
        return self.tr('Hydrological and material transport operations')

    def groupId(self):  # pylint: disable=missing-function-docstring
        return 'hydrological'

    def shortHelpString(self):  # pylint: disable=missing-function-docstring
        return self.tr(
            """Sum of the cell values of its first upstream cell(s)

            <a href="https://pcraster.geo.uu.nl/pcraster/4.3.1/documentation/pcraster_manual/sphinx/op_upstream.html">PCRaster documentation</a>

            Parameters:

            * <b>Input flow direction raster</b> (required) - Flow direction raster in PCRaster LDD format (see lddcreate)
            * <b>Input material layer</b> (required) - Scalar raster layer with material values
            * <b>Result upstream layer</b> (required) - Scalar raster layer with data type of input raster containing the sum of neighbouring upstream cell(s)
            """
        )

    def initAlgorithm(self, config=None):  # pylint: disable=missing-function-docstring,unused-argument
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_LDD,
                self.tr('LDD layer')
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_RASTER,
                self.tr('Material layer')
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.OUTPUT_UPSTREAM,
                self.tr('Upstream layer')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):  # pylint: disable=missing-function-docstring,unused-argument,too-many-locals
        try:
            from pcraster import (   # pylint: disable=import-outside-toplevel
                setclone,
                readmap,
                report,
                upstream
            )
        except ImportError as e:
            raise QgsProcessingException('PCRaster library is not available') from e

        input_ldd = self.parameterAsRasterLayer(parameters, self.INPUT_LDD, context)
        input_raster = self.parameterAsRasterLayer(parameters, self.INPUT_RASTER, context)
        setclone(input_ldd.dataProvider().dataSourceUri())
        LDD = readmap(input_ldd.dataProvider().dataSourceUri())
        RasterInput = readmap(input_raster.dataProvider().dataSourceUri())
        Upstream = upstream(LDD, RasterInput)
        outputFilePath = self.parameterAsOutputLayer(parameters, self.OUTPUT_UPSTREAM, context)
        report(Upstream, outputFilePath)

        self.set_output_crs(output_file=outputFilePath, crs=input_ldd.crs(), feedback=feedback, context=context)

        return {self.OUTPUT_UPSTREAM: outputFilePath}
