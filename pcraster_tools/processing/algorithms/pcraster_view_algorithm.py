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


class PCRasterViewAlgorithm(PCRasterAlgorithm):
    """
    TRUE or FALSE value for visibility from viewpoint(s) defined by a digital elevation model
    """

    INPUT_DEM = 'INPUT'
    INPUT_POINTS = 'INPUT2'
    OUTPUT_VIEW = 'OUTPUT'

    def createInstance(self):  # pylint: disable=missing-function-docstring
        return PCRasterViewAlgorithm()

    def name(self):  # pylint: disable=missing-function-docstring
        return 'view'

    def displayName(self):  # pylint: disable=missing-function-docstring
        return self.tr('view')

    def group(self):  # pylint: disable=missing-function-docstring
        return self.tr('Derivatives of digital elevation models')

    def groupId(self):  # pylint: disable=missing-function-docstring
        return 'demderivatives'

    def shortHelpString(self):  # pylint: disable=missing-function-docstring
        return self.tr(
            """TRUE or FALSE value for visibility from viewpoint(s) defined by a digital elevation model

            <a href="https://pcraster.geo.uu.nl/pcraster/4.3.1/documentation/pcraster_manual/sphinx/op_view.html">PCRaster documentation</a>

            Parameters:

            * <b>Input DEM layer</b> (required) - Scalar raster with elevations
            * <b>Viewpoints layer</b> (required) - Boolean raster layer. All cells with value TRUE are used as viewpoints
            * <b>Result viewshed layer</b> (required) - Boolean raster layer with TRUE for each cell which is visible from viewpoints and FALSE for cells that are not visible.
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
            QgsProcessingParameterRasterLayer(
                self.INPUT_POINTS,
                self.tr('Viewpoints layer')
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.OUTPUT_VIEW,
                self.tr('Viewshed layer')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):  # pylint: disable=missing-function-docstring,unused-argument,too-many-locals
        try:
            from pcraster import (   # pylint: disable=import-outside-toplevel
                setclone,
                readmap,
                report,
                view
            )
        except ImportError as e:
            raise QgsProcessingException('PCRaster library is not available') from e

        input_dem = self.parameterAsRasterLayer(parameters, self.INPUT_DEM, context)
        input_points = self.parameterAsRasterLayer(parameters, self.INPUT_POINTS, context)
        setclone(input_dem.dataProvider().dataSourceUri())
        DEM = readmap(input_dem.dataProvider().dataSourceUri())
        Points = readmap(input_points.dataProvider().dataSourceUri())
        Viewshed = view(DEM, Points)
        outputFilePath = self.parameterAsOutputLayer(parameters, self.OUTPUT_VIEW, context)
        report(Viewshed, outputFilePath)

        self.set_output_crs(output_file=outputFilePath, crs=input_dem.crs(), feedback=feedback, context=context)

        return {self.OUTPUT_VIEW: outputFilePath}
