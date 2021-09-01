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


class PCRasterAreauniformAlgorithm(PCRasterAlgorithm):
    """
    Value assigned to area taken from a uniform distribution
    """

    INPUT_DISCRETE = 'INPUT'
    OUTPUT_AREAUNIFORM = 'OUTPUT'

    def createInstance(self):  # pylint: disable=missing-function-docstring
        return PCRasterAreauniformAlgorithm()

    def name(self):  # pylint: disable=missing-function-docstring
        return 'areauniform'

    def displayName(self):  # pylint: disable=missing-function-docstring
        return self.tr('areauniform')

    def group(self):  # pylint: disable=missing-function-docstring
        return self.tr('Area operations')

    def groupId(self):  # pylint: disable=missing-function-docstring
        return 'area'

    def shortHelpString(self):  # pylint: disable=missing-function-docstring
        return self.tr(
            """Value assigned to area taken from a uniform distribution

            <a href="https://pcraster.geo.uu.nl/pcraster/4.3.1/documentation/pcraster_manual/sphinx/op_areauniform.html">PCRaster documentation</a>

            Parameters:

            * <b>Input class raster layer</b> (required) - boolean, nominal or ordinal raster layer
            * <b>Output area normal raster</b> (required) - scalar raster layer with value assigned to an area taken from a uniform distribution
            """
        )

    def initAlgorithm(self, config=None):  # pylint: disable=missing-function-docstring,unused-argument
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_DISCRETE,
                self.tr('Class raster layer')
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.OUTPUT_AREAUNIFORM,
                self.tr('Output area uniform layer')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):  # pylint: disable=missing-function-docstring,unused-argument,too-many-locals
        try:
            from pcraster import (   # pylint: disable=import-outside-toplevel
                setclone,
                readmap,
                report,
                areauniform
            )
        except ImportError as e:
            raise QgsProcessingException('PCRaster library is not available') from e

        input_discrete = self.parameterAsRasterLayer(parameters, self.INPUT_DISCRETE, context)
        setclone(input_discrete.dataProvider().dataSourceUri())
        ClassLayer = readmap(input_discrete.dataProvider().dataSourceUri())
        AreaUniformLayer = areauniform(ClassLayer)
        outputFilePath = self.parameterAsOutputLayer(parameters, self.OUTPUT_AREAUNIFORM, context)

        report(AreaUniformLayer, outputFilePath)

        return {self.OUTPUT_AREAUNIFORM: outputFilePath}
