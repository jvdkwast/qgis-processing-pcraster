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


class PCRasterAreaminimumAlgorithm(PCRasterAlgorithm):
    """
    Minimum cell value within an area
    """

    INPUT_CLASS = 'INPUT'
    INPUT_RASTER = 'INPUT2'
    OUTPUT_AREAMINIMUM = 'OUTPUT'

    def createInstance(self):  # pylint: disable=missing-function-docstring
        return PCRasterAreaminimumAlgorithm()

    def name(self):  # pylint: disable=missing-function-docstring
        return 'areaminimum'

    def displayName(self):  # pylint: disable=missing-function-docstring
        return self.tr('areaminimum')

    def group(self):  # pylint: disable=missing-function-docstring
        return self.tr('Area operations')

    def groupId(self):  # pylint: disable=missing-function-docstring
        return 'area'

    def shortHelpString(self):  # pylint: disable=missing-function-docstring
        return self.tr(
            """Minimum cell value within an area

            <a href="https://pcraster.geo.uu.nl/pcraster/4.3.1/documentation/pcraster_manual/sphinx/op_areaminimum.html">PCRaster documentation</a>

            Parameters:

            * <b>Input class raster layer</b> (required) - boolean, nominal or ordinal raster layer
            * <b>Input ordinal or scalar raster layer</b> (required) - ordinal or scalar raster layer
            * <b>Output area minimum raster</b> (required) - Raster of same type as input discrete raster layer containing the minimum cell value within an area
            """
        )

    def initAlgorithm(self, config=None):  # pylint: disable=missing-function-docstring,unused-argument
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_CLASS,
                self.tr('Class raster layer')
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_RASTER,
                self.tr('Input ordinal or scalar raster layer')
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.OUTPUT_AREAMINIMUM,
                self.tr('Output area minimum layer')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):  # pylint: disable=missing-function-docstring,unused-argument,too-many-locals
        try:
            from pcraster import (   # pylint: disable=import-outside-toplevel
                setclone,
                readmap,
                areaminimum,
                report
            )
        except ImportError as e:
            raise QgsProcessingException('PCRaster library is not available') from e

        input_class = self.parameterAsRasterLayer(parameters, self.INPUT_CLASS, context)
        input_raster = self.parameterAsRasterLayer(parameters, self.INPUT_RASTER, context)
        setclone(input_raster.dataProvider().dataSourceUri())
        ClassLayer = readmap(input_class.dataProvider().dataSourceUri())
        RasterLayer = readmap(input_raster.dataProvider().dataSourceUri())
        AreaMinimum = areaminimum(RasterLayer, ClassLayer)
        outputFilePath = self.parameterAsOutputLayer(parameters, self.OUTPUT_AREAMINIMUM, context)

        report(AreaMinimum, outputFilePath)

        self.set_output_crs(output_file=outputFilePath, crs=input_raster.crs(), feedback=feedback, context=context)

        return {self.OUTPUT_AREAMINIMUM: outputFilePath}
