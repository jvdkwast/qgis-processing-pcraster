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
    slope
)
from qgis.core import (QgsProcessingParameterRasterDestination,
                       QgsProcessingParameterRasterLayer)

from pcraster_tools.processing.algorithm import PCRasterAlgorithm


class PCRasterSlopeAlgorithm(PCRasterAlgorithm):
    """
    Slope of cells using a digital elevation model
    """

    INPUT_DEM = 'INPUT'
    OUTPUT_SLOPE = 'OUTPUT'

    def createInstance(self):  # pylint: disable=missing-function-docstring
        return PCRasterSlopeAlgorithm()

    def name(self):  # pylint: disable=missing-function-docstring
        return 'Slope'

    def displayName(self):  # pylint: disable=missing-function-docstring
        return self.tr('slope')

    def group(self):  # pylint: disable=missing-function-docstring
        return self.tr('PCRaster')

    def groupId(self):  # pylint: disable=missing-function-docstring
        return 'pcraster'

    def shortHelpString(self):  # pylint: disable=missing-function-docstring
        return self.tr(
            """Slope of cells using a digital elevation model

            <a href="https://pcraster.geo.uu.nl/pcraster/4.3.1/documentation/pcraster_manual/sphinx/op_slope.html">PCRaster documentation</a>

            Parameters:

            * <b>Input DEM</b> (required) - scalar raster layer
            * <b>Output slope raster</b> (required) - scalar raster with slope in fraction
            """
        )

    def initAlgorithm(self, config=None):  # pylint: disable=missing-function-docstring,unused-argument
        # We add the input DEM.
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_DEM,
                self.tr('DEM layer')
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.OUTPUT_SLOPE,
                self.tr('Slope layer'),
            )
        )

    def processAlgorithm(self, parameters, context, feedback):  # pylint: disable=missing-function-docstring,unused-argument
        input_dem = self.parameterAsRasterLayer(parameters, self.INPUT_DEM, context)

        setclone(input_dem.dataProvider().dataSourceUri())
        DEM = readmap(input_dem.dataProvider().dataSourceUri())
        slopeMap = slope(DEM)
        outputFilePath = self.parameterAsOutputLayer(parameters, self.OUTPUT_SLOPE, context)

        report(slopeMap, outputFilePath)

        return {self.OUTPUT_SLOPE: outputFilePath}
