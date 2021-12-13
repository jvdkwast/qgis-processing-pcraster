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


class PCRasterAreanormalAlgorithm(PCRasterAlgorithm):
    """
    Value assigned to an area taken from a normal distribution
    """

    INPUT_DISCRETE = 'INPUT'
    OUTPUT_AREANORMAL = 'OUTPUT'

    def createInstance(self):  # pylint: disable=missing-function-docstring
        return PCRasterAreanormalAlgorithm()

    def name(self):  # pylint: disable=missing-function-docstring
        return 'areanormal'

    def displayName(self):  # pylint: disable=missing-function-docstring
        return self.tr('areanormal')

    def group(self):  # pylint: disable=missing-function-docstring
        return self.tr('Area operations')

    def groupId(self):  # pylint: disable=missing-function-docstring
        return 'area'

    def shortHelpString(self):  # pylint: disable=missing-function-docstring
        return self.tr(
            """Value assigned to an area taken from a normal distribution

            <a href="https://pcraster.geo.uu.nl/pcraster/4.3.2/documentation/pcraster_manual/sphinx/op_areanormal.html">PCRaster documentation</a>

            Parameters:

            * <b>Input class raster layer</b> (required) - boolean, nominal or ordinal raster layer
            * <b>Output area normal raster</b> (required) - scalar raster layer with value assigned to an area taken from a normal distribution
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
                self.OUTPUT_AREANORMAL,
                self.tr('Output area normal layer')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):  # pylint: disable=missing-function-docstring,unused-argument,too-many-locals
        try:
            from pcraster import (   # pylint: disable=import-outside-toplevel
                setclone,
                readmap,
                report,
                areanormal
            )
        except ImportError as e:
            raise QgsProcessingException('PCRaster library is not available') from e

        input_discrete = self.parameterAsRasterLayer(parameters, self.INPUT_DISCRETE, context)
        setclone(input_discrete.dataProvider().dataSourceUri())
        ClassLayer = readmap(input_discrete.dataProvider().dataSourceUri())
        AreaNormalLayer = areanormal(ClassLayer)
        outputFilePath = self.parameterAsOutputLayer(parameters, self.OUTPUT_AREANORMAL, context)

        report(AreaNormalLayer, outputFilePath)

        self.set_output_crs(output_file=outputFilePath, crs=input_discrete.crs(), feedback=feedback, context=context)

        return {self.OUTPUT_AREANORMAL: outputFilePath}
