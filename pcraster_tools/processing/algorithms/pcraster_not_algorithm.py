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


class PCRasterNotAlgorithm(PCRasterAlgorithm):
    """
    Absolute value
    """

    INPUT_RASTER = 'INPUT'
    OUTPUT_RASTER = 'OUTPUT'

    def createInstance(self):  # pylint: disable=missing-function-docstring
        return PCRasterNotAlgorithm()

    def name(self):  # pylint: disable=missing-function-docstring
        return 'not'

    def displayName(self):  # pylint: disable=missing-function-docstring
        return self.tr('not')

    def group(self):  # pylint: disable=missing-function-docstring
        return self.tr('Conditional and boolean operators')

    def groupId(self):  # pylint: disable=missing-function-docstring
        return 'conditional'

    def shortHelpString(self):  # pylint: disable=missing-function-docstring
        return self.tr(
            """Boolean-not operation

            <a href="{}">PCRaster documentation</a>

            Parameters:

            * <b>Input raster</b> (required) - boolean raster layer
            * <b>Output raster</b> (required) - boolean raster with result
            """
        ).format(PCRasterAlgorithm.documentation_url('op_not.html'))

    def initAlgorithm(self, config=None):  # pylint: disable=missing-function-docstring,unused-argument
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_RASTER,
                self.tr('Boolean raster layer')
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.OUTPUT_RASTER,
                self.tr("Output boolean raster layer")
            )
        )

    def processAlgorithm(self, parameters, context, feedback):  # pylint: disable=missing-function-docstring,unused-argument,too-many-locals
        try:
            from pcraster import (   # pylint: disable=import-outside-toplevel, redefined-builtin
                setclone,
                readmap,
                report,
                pcrnot
            )
        except ImportError as e:
            raise QgsProcessingException('PCRaster library is not available') from e

        input_raster = self.parameterAsRasterLayer(parameters, self.INPUT_RASTER, context)

        setclone(input_raster.dataProvider().dataSourceUri())
        input_raster = readmap(input_raster.dataProvider().dataSourceUri())
        not_layer = pcrnot(input_raster)
        output_file_path = self.parameterAsOutputLayer(parameters, self.OUTPUT_RASTER, context)

        report(not_layer, output_file_path)

        self.set_output_crs(output_file=output_file_path, crs=input_raster.crs(), feedback=feedback, context=context)

        return {self.OUTPUT_RASTER: output_file_path}
