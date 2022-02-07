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


class PCRasterDefinedAlgorithm(PCRasterAlgorithm):
    """
    Boolean TRUE for non missing values and FALSE for missing values
    """

    INPUT_RASTER = 'INPUT'
    OUTPUT_BOOLEAN = 'OUTPUT'

    def createInstance(self):  # pylint: disable=missing-function-docstring
        return PCRasterDefinedAlgorithm()

    def name(self):  # pylint: disable=missing-function-docstring
        return 'defined'

    def displayName(self):  # pylint: disable=missing-function-docstring
        return self.tr('defined')

    def group(self):  # pylint: disable=missing-function-docstring
        return self.tr('Missing value creation, detection, alteration')

    def groupId(self):  # pylint: disable=missing-function-docstring
        return 'missingvalues'

    def shortHelpString(self):  # pylint: disable=missing-function-docstring
        return self.tr(
            """Boolean TRUE for non missing values and FALSE for missing values

            <a href="{}">PCRaster documentation</a>

            Parameters:

            * <b>Input raster</b> (required) - input raster layer of any data type
            * <b>Output raster</b> (required) - boolean output raster with TRUE for non missing values and FALSE for missing values
            """
        ).format(PCRasterAlgorithm.documentation_url('op_defined.html'))

    def initAlgorithm(self, config=None):  # pylint: disable=missing-function-docstring,unused-argument
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_RASTER,
                self.tr('Raster layer')
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.OUTPUT_BOOLEAN,
                self.tr("Output boolean layer")
            )
        )

    def processAlgorithm(self, parameters, context, feedback):  # pylint: disable=missing-function-docstring,unused-argument,too-many-locals
        try:
            from pcraster import (   # pylint: disable=import-outside-toplevel
                setclone,
                readmap,
                report,
                defined
            )
        except ImportError as e:
            raise QgsProcessingException('PCRaster library is not available') from e

        input_raster = self.parameterAsRasterLayer(parameters, self.INPUT_RASTER, context)

        setclone(input_raster.dataProvider().dataSourceUri())
        InputRaster = readmap(input_raster.dataProvider().dataSourceUri())
        DefinedLayer = defined(InputRaster)
        outputFilePath = self.parameterAsOutputLayer(parameters, self.OUTPUT_BOOLEAN, context)

        report(DefinedLayer, outputFilePath)

        self.set_output_crs(output_file=outputFilePath, crs=input_raster.crs(), feedback=feedback, context=context)

        return {self.OUTPUT_BOOLEAN: outputFilePath}
