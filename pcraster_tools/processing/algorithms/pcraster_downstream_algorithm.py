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


class PCRasterDownstreamAlgorithm(PCRasterAlgorithm):
    """
    Cell gets value of the neighbouring downstream cell
    """

    INPUT_LDD = 'INPUT1'
    INPUT_RASTER = 'INPUT2'
    OUTPUT_DOWNSTREAM = 'OUTPUT'

    def createInstance(self):  # pylint: disable=missing-function-docstring
        return PCRasterDownstreamAlgorithm()

    def name(self):  # pylint: disable=missing-function-docstring
        return 'downstream'

    def displayName(self):  # pylint: disable=missing-function-docstring
        return self.tr('downstream')

    def group(self):  # pylint: disable=missing-function-docstring
        return self.tr('Hydrological and material transport operations')

    def groupId(self):  # pylint: disable=missing-function-docstring
        return 'hydrological'

    def shortHelpString(self):  # pylint: disable=missing-function-docstring
        return self.tr(
            """Cell gets value of the neighbouring downstream cell

            <a href="{}">PCRaster documentation</a>

            Parameters:

            * <b>Input flow direction raster</b> (required) - Flow direction raster in PCRaster LDD format (see lddcreate)
            * <b>Input raster layer</b> (required) - Raster layer of any data type
            * <b>Result downstream layer</b> (required) - Raster layer with data type of input raster containing value of neighbouring downstream cell
            """
        ).format(PCRasterAlgorithm.documentation_url('op_downstream.html'))

    def initAlgorithm(self, config=None):  # pylint: disable=missing-function-docstring,unused-argument
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_LDD,
                self.tr('Flow direction layer')
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_RASTER,
                self.tr('Raster layer')
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.OUTPUT_DOWNSTREAM,
                self.tr('Downstream layer')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):  # pylint: disable=missing-function-docstring,unused-argument,too-many-locals
        try:
            from pcraster import (   # pylint: disable=import-outside-toplevel
                setclone,
                readmap,
                report,
                downstream
            )
        except ImportError as e:
            raise QgsProcessingException('PCRaster library is not available') from e

        input_ldd = self.parameterAsRasterLayer(parameters, self.INPUT_LDD, context)
        input_raster = self.parameterAsRasterLayer(parameters, self.INPUT_RASTER, context)
        setclone(input_ldd.dataProvider().dataSourceUri())
        LDD = readmap(input_ldd.dataProvider().dataSourceUri())
        RasterInput = readmap(input_raster.dataProvider().dataSourceUri())
        Downstream = downstream(LDD, RasterInput)
        outputFilePath = self.parameterAsOutputLayer(parameters, self.OUTPUT_DOWNSTREAM, context)
        report(Downstream, outputFilePath)

        self.set_output_crs(output_file=outputFilePath, crs=input_ldd.crs(), feedback=feedback, context=context)

        return {self.OUTPUT_DOWNSTREAM: outputFilePath}
