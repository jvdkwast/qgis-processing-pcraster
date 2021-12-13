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


class PCRasterUniformAlgorithm(PCRasterAlgorithm):
    """
    Boolean TRUE cell gets value from an uniform distribution
    """

    INPUT_BOOLEAN = 'INPUT'
    OUTPUT_UNIFORM = 'OUTPUT'

    def createInstance(self):  # pylint: disable=missing-function-docstring
        return PCRasterUniformAlgorithm()

    def name(self):  # pylint: disable=missing-function-docstring
        return 'uniform'

    def displayName(self):  # pylint: disable=missing-function-docstring
        return self.tr('uniform')

    def group(self):  # pylint: disable=missing-function-docstring
        return self.tr('Mathematical operators')

    def groupId(self):  # pylint: disable=missing-function-docstring
        return 'operators'

    def shortHelpString(self):  # pylint: disable=missing-function-docstring
        return self.tr(
            """Boolean TRUE cell gets value from an uniform distribution

            <a href="https://pcraster.geo.uu.nl/pcraster/4.3.2/documentation/pcraster_manual/sphinx/op_uniform.html">PCRaster documentation</a>

            Parameters:

            * <b>Input boolean raster</b> (required) - Raster layer with boolean data type
            * <b>Output raster</b> (required) - Scalar raster with values taken from a uniform distribution
            """
        )

    def initAlgorithm(self, config=None):  # pylint: disable=missing-function-docstring,unused-argument
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_BOOLEAN,
                self.tr('Input boolean layer')
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.OUTPUT_UNIFORM,
                self.tr("Uniform layer")
            )
        )

    def processAlgorithm(self, parameters, context, feedback):  # pylint: disable=missing-function-docstring,unused-argument,too-many-locals
        try:
            from pcraster import (   # pylint: disable=import-outside-toplevel
                setclone,
                readmap,
                report,
                uniform
            )
        except ImportError as e:
            raise QgsProcessingException('PCRaster library is not available') from e

        input_boolean = self.parameterAsRasterLayer(parameters, self.INPUT_BOOLEAN, context)

        setclone(input_boolean.dataProvider().dataSourceUri())
        InputBoolean = readmap(input_boolean.dataProvider().dataSourceUri())
        UniformLayer = uniform(InputBoolean)
        outputFilePath = self.parameterAsOutputLayer(parameters, self.OUTPUT_UNIFORM, context)

        report(UniformLayer, outputFilePath)

        self.set_output_crs(output_file=outputFilePath, crs=input_boolean.crs(), feedback=feedback, context=context)

        return {self.OUTPUT_UNIFORM: outputFilePath}
