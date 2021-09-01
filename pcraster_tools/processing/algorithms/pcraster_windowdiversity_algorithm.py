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

from pcraster import (
    setclone,
    readmap,
    report,
    windowdiversity,
    setglobaloption
)
from qgis.core import (QgsProcessingParameterRasterDestination,
                       QgsProcessingParameterRasterLayer,
                       QgsProcessingParameterEnum,
                       QgsProcessingParameterNumber)

from pcraster_tools.processing.algorithm import PCRasterAlgorithm


class PCRasterWindowDiversityAlgorithm(PCRasterAlgorithm):
    """
    Number of unique values within a specified square neighbourhood
    """

    INPUT_RASTER = 'INPUT'
    INPUT_UNITS = 'INPUT1'
    INPUT_WINDOWLENGTH = 'INPUT2'
    OUTPUT_RASTER = 'OUTPUT'

    def createInstance(self):  # pylint: disable=missing-function-docstring
        return PCRasterWindowDiversityAlgorithm()

    def name(self):  # pylint: disable=missing-function-docstring
        return 'windowdiversity'

    def displayName(self):  # pylint: disable=missing-function-docstring
        return self.tr('windowdiversity')

    def group(self):  # pylint: disable=missing-function-docstring
        return self.tr('PCRaster')

    def groupId(self):  # pylint: disable=missing-function-docstring
        return 'pcraster'

    def shortHelpString(self):  # pylint: disable=missing-function-docstring
        return self.tr(
            """Number of unique values within a specified square neighbourhood
            
            <a href="https://pcraster.geo.uu.nl/pcraster/4.3.1/documentation/pcraster_manual/sphinx/op_windowdiversity.html">PCRaster documentation</a>
            
            Parameters:
            
            * <b>Input raster layer</b> (required) - boolean, nominal or ordinal raster layer
            * <b>Units</b> (required) - map units or cells
            * <b>Input window length</b> (required) - window length value in chosen units
            * <b>Output window diversity layer</b> (required) - Scalar raster with the number of unique values in the window assigned to the cell
            """
        )

    def initAlgorithm(self, config=None):  # pylint: disable=missing-function-docstring
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_RASTER,
                self.tr('Input raster layer')
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
                self.tr('Window Diversity Layer')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):  # pylint: disable=missing-function-docstring
        input_raster = self.parameterAsRasterLayer(parameters, self.INPUT_RASTER, context)
        lengthunits = self.parameterAsEnum(parameters, self.INPUT_UNITS, context)
        if lengthunits == 0:
            setglobaloption("unittrue")
        else:
            setglobaloption("unitcell")
        input_windowlength = self.parameterAsDouble(parameters, self.INPUT_WINDOWLENGTH, context)
        setclone(input_raster.dataProvider().dataSourceUri())
        RasterInput = readmap(input_raster.dataProvider().dataSourceUri())
        RasterOutput = windowdiversity(RasterInput, input_windowlength)
        outputFilePath = self.parameterAsOutputLayer(parameters, self.OUTPUT_RASTER, context)
        report(RasterOutput, outputFilePath)

        return {self.OUTPUT_RASTER: outputFilePath}
