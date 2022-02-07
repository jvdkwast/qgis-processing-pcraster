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


class PCRasterPitAlgorithm(PCRasterAlgorithm):
    """
    Unique value for each pit cell
    """

    INPUT_LDD = 'INPUT'
    OUTPUT_PIT = 'OUTPUT'

    def createInstance(self):  # pylint: disable=missing-function-docstring
        return PCRasterPitAlgorithm()

    def name(self):  # pylint: disable=missing-function-docstring
        return 'pit'

    def displayName(self):  # pylint: disable=missing-function-docstring
        return self.tr('pit')

    def group(self):  # pylint: disable=missing-function-docstring
        return self.tr('Hydrological and material transport operations')

    def groupId(self):  # pylint: disable=missing-function-docstring
        return 'hydrological'

    def shortHelpString(self):  # pylint: disable=missing-function-docstring
        return self.tr(
            """Unique value for each pit cell

            <a href="{}">PCRaster documentation</a>

            Parameters:

            * <b>Input LDD raster layer</b> (required) - raster layer with LDD data type
            * <b>Output pit raster layer</b> (required) - nominal raster with unique values for pits
            """
        ).format(PCRasterAlgorithm.documentation_url('op_pit.html'))

    def initAlgorithm(self, config=None):  # pylint: disable=missing-function-docstring,unused-argument
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_LDD,
                self.tr('LDD layer')
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.OUTPUT_PIT,
                self.tr("Output pit raster layer")
            )
        )

    def processAlgorithm(self, parameters, context, feedback):  # pylint: disable=missing-function-docstring,unused-argument,too-many-locals
        try:
            from pcraster import (   # pylint: disable=import-outside-toplevel
                setclone,
                readmap,
                report,
                pit
            )
        except ImportError as e:
            raise QgsProcessingException('PCRaster library is not available') from e

        input_ldd = self.parameterAsRasterLayer(parameters, self.INPUT_LDD, context)

        setclone(input_ldd.dataProvider().dataSourceUri())
        LDD = readmap(input_ldd.dataProvider().dataSourceUri())
        PitLayer = pit(LDD)
        outputFilePath = self.parameterAsOutputLayer(parameters, self.OUTPUT_PIT, context)

        report(PitLayer, outputFilePath)

        self.set_output_crs(output_file=outputFilePath, crs=input_ldd.crs(), feedback=feedback, context=context)

        return {self.OUTPUT_PIT: outputFilePath}
