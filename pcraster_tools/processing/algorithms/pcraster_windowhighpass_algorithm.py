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
                       QgsProcessingParameterEnum,
                       QgsProcessingParameterNumber,
                       QgsProcessingException)

from pcraster_tools.processing.algorithm import PCRasterAlgorithm


class PCRasterWindowHighPassAlgorithm(PCRasterAlgorithm):
    """
    Increases spatial frequency within a specified square neighbourhood
    """

    INPUT_RASTER = 'INPUT'
    INPUT_UNITS = 'INPUT1'
    INPUT_WINDOWLENGTH = 'INPUT2'
    OUTPUT_RASTER = 'OUTPUT'

    def createInstance(self):  # pylint: disable=missing-function-docstring
        return PCRasterWindowHighPassAlgorithm()

    def name(self):  # pylint: disable=missing-function-docstring
        return 'windowhighpass'

    def displayName(self):  # pylint: disable=missing-function-docstring
        return self.tr('windowhighpass')

    def group(self):  # pylint: disable=missing-function-docstring
        return self.tr('Window operations')

    def groupId(self):  # pylint: disable=missing-function-docstring
        return 'window'

    def shortHelpString(self):  # pylint: disable=missing-function-docstring
        return self.tr(
            """Increases spatial frequency within a specified square neighbourhood

            <a href="https://pcraster.geo.uu.nl/pcraster/4.3.1/documentation/pcraster_manual/sphinx/op_windowhighpass.html">PCRaster documentation</a>

            Parameters:

            * <b>Input raster layer</b> (required) - scalar raster layer
            * <b>Units</b> (required) - map units or cells
            * <b>Input window length</b> (required) - window length value in chosen units
            * <b>Output window high pass layer</b> (required) - Scalar raster with high pass values
            """
        )

    def initAlgorithm(self, config=None):  # pylint: disable=missing-function-docstring,unused-argument
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_RASTER,
                self.tr('Scalar Raster layer')
            )
        )

        unitoption = [self.tr('Map units'), self.tr('Cells')]
        self.addParameter(
            QgsProcessingParameterEnum(
                self.INPUT_UNITS,
                self.tr('Unit of Window Length'),
                unitoption,
                defaultValue=0
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.INPUT_WINDOWLENGTH,
                self.tr('Window length'),
                defaultValue=100
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.OUTPUT_RASTER,
                self.tr('Window High Pass Layer')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):  # pylint: disable=missing-function-docstring,unused-argument,too-many-locals
        try:
            from pcraster import (   # pylint: disable=import-outside-toplevel
                setclone,
                readmap,
                report,
                windowhighpass,
                setglobaloption
            )
        except ImportError as e:
            raise QgsProcessingException('PCRaster library is not available') from e

        input_raster = self.parameterAsRasterLayer(parameters, self.INPUT_RASTER, context)
        lengthunits = self.parameterAsEnum(parameters, self.INPUT_UNITS, context)
        if lengthunits == 0:
            setglobaloption("unittrue")
        else:
            setglobaloption("unitcell")
        input_windowlength = self.parameterAsDouble(parameters, self.INPUT_WINDOWLENGTH, context)
        setclone(input_raster.dataProvider().dataSourceUri())
        RasterInput = readmap(input_raster.dataProvider().dataSourceUri())
        RasterOutput = windowhighpass(RasterInput, input_windowlength)
        outputFilePath = self.parameterAsOutputLayer(parameters, self.OUTPUT_RASTER, context)
        report(RasterOutput, outputFilePath)

        self.set_output_crs(output_file=outputFilePath, crs=input_raster.crs(), feedback=feedback, context=context)

        return {self.OUTPUT_RASTER: outputFilePath}