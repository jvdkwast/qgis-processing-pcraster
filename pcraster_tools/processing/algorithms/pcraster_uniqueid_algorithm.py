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


class PCRasterUniqueidAlgorithm(PCRasterAlgorithm):
    """
    Unique whole value for each Boolean TRUE cell
    """

    INPUT_BOOLEAN = 'INPUT'
    OUTPUT_SCALAR = 'OUTPUT'

    def createInstance(self):  # pylint: disable=missing-function-docstring
        return PCRasterUniqueidAlgorithm()

    def name(self):  # pylint: disable=missing-function-docstring
        return 'uniqueid'

    def displayName(self):  # pylint: disable=missing-function-docstring
        return self.tr('uniqueid')

    def group(self):  # pylint: disable=missing-function-docstring
        return self.tr('Missing value creation, detection, alteration')

    def groupId(self):  # pylint: disable=missing-function-docstring
        return 'missingvalues'

    def shortHelpString(self):  # pylint: disable=missing-function-docstring
        return self.tr(
            """Unique whole value for each Boolean TRUE cell

            <a href="{}">PCRaster documentation</a>

            Parameters:

            * <b>Input boolean raster layer</b> (required) - Raster layer with boolean data type
            * <b>Output unique id raster</b> (required) - Scalar raster with unique id's for TRUE cells in the input boolean raster
            """
        ).format(PCRasterAlgorithm.documentation_url('op_uniqueid.html'))

    def initAlgorithm(self, config=None):  # pylint: disable=missing-function-docstring,unused-argument
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_BOOLEAN,
                self.tr('Input boolean layer')
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.OUTPUT_SCALAR,
                self.tr("Output unique id raster")
            )
        )

    def processAlgorithm(self, parameters, context, feedback):  # pylint: disable=missing-function-docstring,unused-argument,too-many-locals
        try:
            from pcraster import (   # pylint: disable=import-outside-toplevel
                setclone,
                readmap,
                report,
                uniqueid
            )
        except ImportError as e:
            raise QgsProcessingException('PCRaster library is not available') from e

        input_boolean = self.parameterAsRasterLayer(parameters, self.INPUT_BOOLEAN, context)

        setclone(input_boolean.dataProvider().dataSourceUri())
        InputLayer = readmap(input_boolean.dataProvider().dataSourceUri())
        ID = uniqueid(InputLayer)
        outputFilePath = self.parameterAsOutputLayer(parameters, self.OUTPUT_SCALAR, context)

        report(ID, outputFilePath)

        self.set_output_crs(output_file=outputFilePath, crs=input_boolean.crs(), feedback=feedback, context=context)

        return {self.OUTPUT_SCALAR: outputFilePath}
