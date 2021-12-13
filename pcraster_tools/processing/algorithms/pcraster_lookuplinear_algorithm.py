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
                       QgsProcessingParameterFile,
                       QgsProcessingException)

from pcraster_tools.processing.algorithm import PCRasterAlgorithm


class PCRasterLookuplinearAlgorithm(PCRasterAlgorithm):
    """
    Assigns table key values with possible interpolation between key values.
    """

    INPUT_RASTER = 'INPUT'
    INPUT_TABLE = 'INPUT1'
    OUTPUT_RASTER = 'OUTPUT'

    def createInstance(self):  # pylint: disable=missing-function-docstring
        return PCRasterLookuplinearAlgorithm()

    def name(self):  # pylint: disable=missing-function-docstring
        return 'lookuplinear'

    def displayName(self):  # pylint: disable=missing-function-docstring
        return self.tr('lookuplinear')

    def group(self):  # pylint: disable=missing-function-docstring
        return self.tr('Relations in tables')

    def groupId(self):  # pylint: disable=missing-function-docstring
        return 'relations'

    def shortHelpString(self):  # pylint: disable=missing-function-docstring
        return self.tr(
            """Assigns table key values with possible interpolation between key values.

            <a href="https://pcraster.geo.uu.nl/pcraster/4.3.2/documentation/pcraster_manual/sphinx/op_lookuplinear.html">PCRaster documentation</a>

            Parameters:

            * <b>Input raster layer</b> (required) - Raster layer of scalar data type
            * <b>Input lookup table</b> (required) - ASCII text table in PCRaster column table format
            * <b>Output raster layer</b> (required) - Output raster layer with scalar data type
            """
        )

    def initAlgorithm(self, config=None):  # pylint: disable=missing-function-docstring,unused-argument
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_RASTER,
                self.tr('Input raster layer')
            )
        )

        self.addParameter(
            QgsProcessingParameterFile(
                self.INPUT_TABLE,
                self.tr('Input lookup table')
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.OUTPUT_RASTER,
                self.tr('Output Raster Layer')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):  # pylint: disable=missing-function-docstring,unused-argument,too-many-locals
        try:
            from pcraster import (   # pylint: disable=import-outside-toplevel
                setclone,
                readmap,
                report,
                lookuplinear
            )
        except ImportError as e:
            raise QgsProcessingException('PCRaster library is not available') from e

        input_raster = self.parameterAsRasterLayer(parameters, self.INPUT_RASTER, context)
        input_lookuptable = self.parameterAsFile(parameters, self.INPUT_TABLE, context)
        setclone(input_raster.dataProvider().dataSourceUri())
        rasterlayer = readmap(input_raster.dataProvider().dataSourceUri())
        outputFilePath = self.parameterAsOutputLayer(parameters, self.OUTPUT_RASTER, context)

        resultlayer = lookuplinear(input_lookuptable, rasterlayer)

        report(resultlayer, outputFilePath)

        self.set_output_crs(output_file=outputFilePath, crs=input_raster.crs(), feedback=feedback, context=context)

        return {self.OUTPUT_RASTER: outputFilePath}
