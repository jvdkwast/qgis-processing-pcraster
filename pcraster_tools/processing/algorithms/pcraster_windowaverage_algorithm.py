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
    windowaverage,
    setglobaloption
)
from qgis.core import (QgsProcessingParameterRasterDestination,
                       QgsProcessingParameterRasterLayer,
                       QgsProcessingParameterEnum,
                       QgsProcessingParameterNumber)

from pcraster_tools.processing.algorithm import PCRasterAlgorithm


class PCRasterWindowAverageAlgorithm(PCRasterAlgorithm):
    """
    Average of cell values within a specified square neighbourhood
    """

    INPUT_RASTER = 'INPUT'
    INPUT_UNITS = 'INPUT1'
    INPUT_WINDOWLENGTH = 'INPUT2'
    OUTPUT_RASTER = 'OUTPUT'

    def createInstance(self):  # pylint: disable=missing-function-docstring
        return PCRasterWindowAverageAlgorithm()

    def name(self):  # pylint: disable=missing-function-docstring
        return 'windowaverage'

    def displayName(self):  # pylint: disable=missing-function-docstring
        return self.tr('windowaverage')

    def group(self):  # pylint: disable=missing-function-docstring
        return self.tr('PCRaster')

    def groupId(self):  # pylint: disable=missing-function-docstring
        return 'pcraster'

    def shortHelpString(self):  # pylint: disable=missing-function-docstring
        return self.tr(
            """Average of cell values within a specified square neighbourhood
            
            <a href="https://pcraster.geo.uu.nl/pcraster/4.3.1/documentation/pcraster_manual/sphinx/op_windowaverage.html">PCRaster documentation</a>
            
            Parameters:
            
            * <b>Input raster layer</b> (required) - scalar raster layer
            * <b>Units</b> (required) - map units or cells
            * <b>Input window length</b> (required) - window length value in chosen units
            * <b>Output window average layer</b> (required) - Scalar raster with the average value in the window assigned to the cell
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
                self.tr('Window Average Layer')
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
        RasterOutput = windowaverage(RasterInput, input_windowlength)
        outputFilePath = self.parameterAsOutputLayer(parameters, self.OUTPUT_RASTER, context)
        report(RasterOutput, outputFilePath)

        return {self.OUTPUT_RASTER: outputFilePath}
