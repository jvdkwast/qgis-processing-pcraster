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


class PCRasterNormalAlgorithm(PCRasterAlgorithm):
    """
    Boolean TRUE cell gets value taken from a normal distribution
    """

    INPUT_BOOLEAN = 'INPUT'
    OUTPUT = 'OUTPUT'

    def createInstance(self):  # pylint: disable=missing-function-docstring
        return PCRasterNormalAlgorithm()

    def name(self):  # pylint: disable=missing-function-docstring
        return 'normal'

    def displayName(self):  # pylint: disable=missing-function-docstring
        return self.tr('normal')

    def group(self):  # pylint: disable=missing-function-docstring
        return self.tr('Mathematical operators')

    def groupId(self):  # pylint: disable=missing-function-docstring
        return 'operators'

    def shortHelpString(self):  # pylint: disable=missing-function-docstring
        return self.tr(
            """Boolean TRUE cell gets value taken from a normal distribution

            <a href="{}">PCRaster documentation</a>

            Parameters:

            * <b>Input boolean raster</b> (required) - Raster layer with boolean data type
            * <b>Output raster</b> (required) - Scalar raster with values taken from a normal distribution
            """
        ).format(PCRasterAlgorithm.documentation_url('op_normal.html'))

    def initAlgorithm(self, config=None):  # pylint: disable=missing-function-docstring,unused-argument
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_BOOLEAN,
                self.tr('Input boolean layer')
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.OUTPUT,
                self.tr("Normal output layer")
            )
        )

    def processAlgorithm(self, parameters, context, feedback):  # pylint: disable=missing-function-docstring,unused-argument,too-many-locals
        try:
            from pcraster import (   # pylint: disable=import-outside-toplevel
                setclone,
                readmap,
                report,
                normal
            )
        except ImportError as e:
            raise QgsProcessingException('PCRaster library is not available') from e

        input_boolean = self.parameterAsRasterLayer(parameters, self.INPUT_BOOLEAN, context)

        setclone(input_boolean.dataProvider().dataSourceUri())
        InputBoolean = readmap(input_boolean.dataProvider().dataSourceUri())
        NormalLayer = normal(InputBoolean)
        outputFilePath = self.parameterAsOutputLayer(parameters, self.OUTPUT, context)

        report(NormalLayer, outputFilePath)

        self.set_output_crs(output_file=outputFilePath, crs=input_boolean.crs(), feedback=feedback, context=context)

        return {self.OUTPUT: outputFilePath}
