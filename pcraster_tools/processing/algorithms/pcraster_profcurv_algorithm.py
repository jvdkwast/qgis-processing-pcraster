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
    profcurv
)
from qgis.core import (QgsProcessingParameterRasterDestination,
                       QgsProcessingParameterRasterLayer)

from pcraster_tools.processing.algorithm import PCRasterAlgorithm


class PCRasterProfcurvAlgorithm(PCRasterAlgorithm):
    """
    Profile curvature calculation using a DEM
    """

    INPUT_DEM = 'INPUT'
    OUTPUT_PROFCURV = 'OUTPUT'

    def createInstance(self):  # pylint: disable=missing-function-docstring
        return PCRasterProfcurvAlgorithm()

    def name(self):  # pylint: disable=missing-function-docstring
        return 'profcurv'

    def displayName(self):  # pylint: disable=missing-function-docstring
        return self.tr('profcurv')

    def group(self):  # pylint: disable=missing-function-docstring
        return self.tr('PCRaster')

    def groupId(self):  # pylint: disable=missing-function-docstring
        return 'pcraster'

    def shortHelpString(self):  # pylint: disable=missing-function-docstring
        return self.tr(
            """Profile curvature calculation using a DEM
            
            <a href="https://pcraster.geo.uu.nl/pcraster/4.3.1/documentation/pcraster_manual/sphinx/op_profcurv.html">PCRaster documentation</a>
            
            Parameters:
            
            * <b>Input DEM raster layer</b> (required) - raster layer with scalar data type
            * <b>Output profile curvature layer</b> (required) - scalar raster with the change in slope per distance in horizontal direction, in direction of the slope. It is negative at concave slopes and positive at convex slopes. 
            """
        )

    def initAlgorithm(self, config=None):  # pylint: disable=missing-function-docstring
        # We add the input DEM.
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_DEM,
                self.tr('DEM layer')
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.OUTPUT_PROFCURV,
                self.tr("Output profile curvature layer")
            )
        )

    def processAlgorithm(self, parameters, context, feedback):  # pylint: disable=missing-function-docstring
        input_dem = self.parameterAsRasterLayer(parameters, self.INPUT_DEM, context)

        setclone(input_dem.dataProvider().dataSourceUri())
        DEM = readmap(input_dem.dataProvider().dataSourceUri())
        ProfCurvLayer = profcurv(DEM)
        outputFilePath = self.parameterAsOutputLayer(parameters, self.OUTPUT_PROFCURV, context)

        report(ProfCurvLayer, outputFilePath)

        return {self.OUTPUT_PROFCURV: outputFilePath}
