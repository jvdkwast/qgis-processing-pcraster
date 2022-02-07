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


class PCRasterMapminimumAlgorithm(PCRasterAlgorithm):
    """
    Minimum cell value
    """

    INPUT_RASTER = 'INPUT'
    OUTPUT_MIN = 'OUTPUT'

    def createInstance(self):  # pylint: disable=missing-function-docstring
        return PCRasterMapminimumAlgorithm()

    def name(self):  # pylint: disable=missing-function-docstring
        return 'mapminimum'

    def displayName(self):  # pylint: disable=missing-function-docstring
        return self.tr('mapminimum')

    def group(self):  # pylint: disable=missing-function-docstring
        return self.tr('Map operations')

    def groupId(self):  # pylint: disable=missing-function-docstring
        return 'map'

    def shortHelpString(self):  # pylint: disable=missing-function-docstring
        return self.tr(
            """Minimum cell value

            <a href="{}">PCRaster documentation</a>

            Parameters:

            * <b>Input raster layer</b> (required) - ordinal or scalar raster layer
            * <b>Output maximum value raster</b> (required) - Raster of same type as input containing the minimum cell value
            """
        ).format(PCRasterAlgorithm.documentation_url('op_mapminimum.html'))

    def initAlgorithm(self, config=None):  # pylint: disable=missing-function-docstring,unused-argument
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_RASTER,
                self.tr('Input raster layer')
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.OUTPUT_MIN,
                self.tr('Output minimum value layer')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):  # pylint: disable=missing-function-docstring,unused-argument,too-many-locals
        try:
            from pcraster import (   # pylint: disable=import-outside-toplevel
                setclone,
                readmap,
                report,
                mapminimum,
                cellvalue
            )
        except ImportError as e:
            raise QgsProcessingException('PCRaster library is not available') from e

        input_raster = self.parameterAsRasterLayer(parameters, self.INPUT_RASTER, context)

        setclone(input_raster.dataProvider().dataSourceUri())
        RasterLayer = readmap(input_raster.dataProvider().dataSourceUri())
        MinLayer = mapminimum(RasterLayer)
        print(cellvalue(MinLayer, 1, 1)[0])
        outputFilePath = self.parameterAsOutputLayer(parameters, self.OUTPUT_MIN, context)

        report(MinLayer, outputFilePath)

        self.set_output_crs(output_file=outputFilePath, crs=input_raster.crs(), feedback=feedback, context=context)

        return {self.OUTPUT_MIN: outputFilePath}
