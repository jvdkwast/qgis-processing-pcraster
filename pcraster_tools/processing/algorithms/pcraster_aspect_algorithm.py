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
    aspect
)
from qgis.core import (QgsProcessingParameterRasterDestination,
                       QgsProcessingParameterRasterLayer)

from pcraster_tools.processing.algorithm import PCRasterAlgorithm


class PCRasterAspectAlgorithm(PCRasterAlgorithm):
    """
    Aspects of a map using a digital elevation model
    """

    INPUT_DEM = 'INPUT'
    OUTPUT_ASPECT = 'OUTPUT'

    def createInstance(self):  # pylint: disable=missing-function-docstring
        return PCRasterAspectAlgorithm()

    def name(self):  # pylint: disable=missing-function-docstring
        return 'aspect'

    def displayName(self):  # pylint: disable=missing-function-docstring
        return self.tr('aspect')

    def group(self):  # pylint: disable=missing-function-docstring
        return self.tr('PCRaster')

    def groupId(self):  # pylint: disable=missing-function-docstring
        return 'pcraster'

    def shortHelpString(self):  # pylint: disable=missing-function-docstring

        return self.tr(
            """Aspects of a map using a digital elevation model

            <a href="https://pcraster.geo.uu.nl/pcraster/4.3.1/documentation/pcraster_manual/sphinx/op_aspect.html">PCRaster documentation</a>

            Parameters:

            * <b>Input DEM</b> (required) - scalar raster layer
            * <b>Output aspect raster</b> (required) - directional raster with aspect
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
                self.OUTPUT_ASPECT,
                self.tr("Aspect layer")
            )
        )

    def processAlgorithm(self, parameters, context, feedback):  # pylint: disable=missing-function-docstring,unused-argument
        input_dem = self.parameterAsRasterLayer(parameters, self.INPUT_DEM, context)

        setclone(input_dem.dataProvider().dataSourceUri())
        DEM = readmap(input_dem.dataProvider().dataSourceUri())
        AspectLayer = aspect(DEM)
        outputFilePath = self.parameterAsOutputLayer(parameters, self.OUTPUT_ASPECT, context)

        report(AspectLayer, outputFilePath)

        return {self.OUTPUT_ASPECT: outputFilePath}
