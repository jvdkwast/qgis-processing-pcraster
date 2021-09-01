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


class PCRastersuccAlgorithm(PCRasterAlgorithm):
    """
    Ordinal number of the next higher ordinal class
    """

    INPUT_RASTER = 'INPUT'
    OUTPUT_RASTER = 'OUTPUT'

    def createInstance(self):  # pylint: disable=missing-function-docstring
        return PCRastersuccAlgorithm()

    def name(self):  # pylint: disable=missing-function-docstring
        return 'succ'

    def displayName(self):  # pylint: disable=missing-function-docstring
        return self.tr('succ')

    def group(self):  # pylint: disable=missing-function-docstring
        return self.tr('Order')

    def groupId(self):  # pylint: disable=missing-function-docstring
        return 'order'

    def shortHelpString(self):  # pylint: disable=missing-function-docstring
        return self.tr(
            """Ordinal number of the next higher ordinal class

            <a href="https://pcraster.geo.uu.nl/pcraster/4.3.1/documentation/pcraster_manual/sphinx/op_succ.html">PCRaster documentation</a>

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
                self.tr("Output succ layer")
            )
        )

    def processAlgorithm(self, parameters, context, feedback):  # pylint: disable=missing-function-docstring,unused-argument,too-many-locals
        try:
            from pcraster import (   # pylint: disable=import-outside-toplevel
                setclone,
                readmap,
                report,
                succ
            )
        except ImportError as e:
            raise QgsProcessingException('PCRaster library is not available') from e

        input_raster = self.parameterAsRasterLayer(parameters, self.INPUT_RASTER, context)

        setclone(input_raster.dataProvider().dataSourceUri())
        InputRaster = readmap(input_raster.dataProvider().dataSourceUri())
        succLayer = succ(InputRaster)
        outputFilePath = self.parameterAsOutputLayer(parameters, self.OUTPUT_RASTER, context)

        report(succLayer, outputFilePath)

        return {self.OUTPUT_RASTER: outputFilePath}
