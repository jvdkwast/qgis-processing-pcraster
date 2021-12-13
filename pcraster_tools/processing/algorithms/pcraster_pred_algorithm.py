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


class PCRasterpredAlgorithm(PCRasterAlgorithm):
    """
    Ordinal number of the next lower ordinal class
    """

    INPUT_RASTER = 'INPUT'
    OUTPUT_RASTER = 'OUTPUT'

    def createInstance(self):  # pylint: disable=missing-function-docstring
        return PCRasterpredAlgorithm()

    def name(self):  # pylint: disable=missing-function-docstring
        return 'pred'

    def displayName(self):  # pylint: disable=missing-function-docstring
        return self.tr('pred')

    def group(self):  # pylint: disable=missing-function-docstring
        return self.tr('Order')

    def groupId(self):  # pylint: disable=missing-function-docstring
        return 'order'

    def shortHelpString(self):  # pylint: disable=missing-function-docstring
        return self.tr(
            """Ordinal number of the next lower ordinal class

            <a href="https://pcraster.geo.uu.nl/pcraster/4.3.2/documentation/pcraster_manual/sphinx/op_pred.html">PCRaster documentation</a>

            Parameters:

            * <b>Ordinal raster layer</b> (required)
            * <b>Output raster</b> (required) - Ordinal raster with result
            """
        )

    def initAlgorithm(self, config=None):  # pylint: disable=missing-function-docstring,unused-argument
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_RASTER,
                self.tr('Ordinal Raster layer')
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.OUTPUT_RASTER,
                self.tr("Output pred layer")
            )
        )

    def processAlgorithm(self, parameters, context, feedback):  # pylint: disable=missing-function-docstring,unused-argument,too-many-locals
        try:
            from pcraster import (   # pylint: disable=import-outside-toplevel
                setclone,
                readmap,
                report,
                pred
            )
        except ImportError as e:
            raise QgsProcessingException('PCRaster library is not available') from e

        input_raster = self.parameterAsRasterLayer(parameters, self.INPUT_RASTER, context)

        setclone(input_raster.dataProvider().dataSourceUri())
        InputRaster = readmap(input_raster.dataProvider().dataSourceUri())
        predLayer = pred(InputRaster)
        outputFilePath = self.parameterAsOutputLayer(parameters, self.OUTPUT_RASTER, context)

        report(predLayer, outputFilePath)

        self.set_output_crs(output_file=outputFilePath, crs=input_raster.crs(), feedback=feedback, context=context)

        return {self.OUTPUT_RASTER: outputFilePath}
