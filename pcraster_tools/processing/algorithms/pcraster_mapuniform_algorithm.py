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


class PCRasterMapuniformAlgorithm(PCRasterAlgorithm):
    """
    Cells get non spatial value taken from an uniform distribution
    """

    INPUT_CLONE = 'INPUT'
    OUTPUT_MAPUNIFORM = 'OUTPUT'

    def createInstance(self):  # pylint: disable=missing-function-docstring
        return PCRasterMapuniformAlgorithm()

    def name(self):  # pylint: disable=missing-function-docstring
        return 'mapuniform'

    def displayName(self):  # pylint: disable=missing-function-docstring
        return self.tr('mapuniform')

    def group(self):  # pylint: disable=missing-function-docstring
        return self.tr('Map operations')

    def groupId(self):  # pylint: disable=missing-function-docstring
        return 'map'

    def shortHelpString(self):  # pylint: disable=missing-function-docstring
        return self.tr(
            """Cells get non spatial value taken from an uniform distribution

            <a href="{}">PCRaster documentation</a>

            Parameters:

            * <b>Input mask raster layer</b> (required) - Raster layer of any data type with the mask for which the values will be calculated
            * <b>Output uniform raster</b> (required) - scalar raster layer with value assigned from a uniform distribution
            """
        ).format(PCRasterAlgorithm.documentation_url('op_mapuniform.html'))

    def initAlgorithm(self, config=None):  # pylint: disable=missing-function-docstring,unused-argument
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_CLONE,
                self.tr('Mask raster layer')
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.OUTPUT_MAPUNIFORM,
                self.tr('Output uniform layer')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):  # pylint: disable=missing-function-docstring,unused-argument,too-many-locals
        try:
            from pcraster import (   # pylint: disable=import-outside-toplevel
                setclone,
                report,
                mapnormal
            )
        except ImportError as e:
            raise QgsProcessingException('PCRaster library is not available') from e

        input_clone = self.parameterAsRasterLayer(parameters, self.INPUT_CLONE, context)

        setclone(input_clone.dataProvider().dataSourceUri())
        MapUniformLayer = mapnormal()
        outputFilePath = self.parameterAsOutputLayer(parameters, self.OUTPUT_MAPUNIFORM, context)

        report(MapUniformLayer, outputFilePath)

        self.set_output_crs(output_file=outputFilePath, crs=input_clone.crs(), feedback=feedback, context=context)

        return {self.OUTPUT_MAPUNIFORM: outputFilePath}
