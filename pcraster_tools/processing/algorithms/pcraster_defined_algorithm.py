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
    defined
)
from qgis.core import (QgsProcessingParameterRasterDestination,
                       QgsProcessingParameterRasterLayer)

from pcraster_tools.processing.algorithm import PCRasterAlgorithm


class PCRasterDefinedAlgorithm(PCRasterAlgorithm):
    """
    Boolean TRUE for non missing values and FALSE for missing values
    """

    INPUT_RASTER = 'INPUT'
    OUTPUT_BOOLEAN = 'OUTPUT'

    def createInstance(self):  # pylint: disable=missing-function-docstring
        return PCRasterDefinedAlgorithm()

    def name(self):  # pylint: disable=missing-function-docstring
        return 'defined'

    def displayName(self):  # pylint: disable=missing-function-docstring
        return self.tr('defined')

    def group(self):  # pylint: disable=missing-function-docstring
        return self.tr('PCRaster')

    def groupId(self):  # pylint: disable=missing-function-docstring
        return 'pcraster'

    def shortHelpString(self):  # pylint: disable=missing-function-docstring
        return self.tr(
            """Boolean TRUE for non missing values and FALSE for missing values
            
            <a href="https://pcraster.geo.uu.nl/pcraster/4.3.1/documentation/pcraster_manual/sphinx/op_defined.html">PCRaster documentation</a>
            
            Parameters:
            
            * <b>Input raster</b> (required) - input raster layer of any data type
            * <b>Output raster</b> (required) - boolean output raster with TRUE for non missing values and FALSE for missing values
            """
        )

    def initAlgorithm(self, config=None):  # pylint: disable=missing-function-docstring
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_RASTER,
                self.tr('Raster layer')
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.OUTPUT_BOOLEAN,
                self.tr("Output boolean layer")
            )
        )

    def processAlgorithm(self, parameters, context, feedback):  # pylint: disable=missing-function-docstring
        input_raster = self.parameterAsRasterLayer(parameters, self.INPUT_RASTER, context)

        setclone(input_raster.dataProvider().dataSourceUri())
        InputRaster = readmap(input_raster.dataProvider().dataSourceUri())
        DefinedLayer = defined(InputRaster)
        outputFilePath = self.parameterAsOutputLayer(parameters, self.OUTPUT_BOOLEAN, context)

        report(DefinedLayer, outputFilePath)

        return {self.OUTPUT_BOOLEAN: outputFilePath}
