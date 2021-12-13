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
                       QgsProcessingParameterEnum,
                       QgsProcessingParameterRasterLayer,
                       QgsProcessingException)

from pcraster_tools.processing.algorithm import PCRasterAlgorithm


class PCRastercellareaAlgorithm(PCRasterAlgorithm):
    """
    Area of one cell
    """

    INPUT_RASTER = 'INPUT'
    INPUT_UNITS = 'INPUT1'
    OUTPUT_RASTER = 'OUTPUT'

    def createInstance(self):  # pylint: disable=missing-function-docstring
        return PCRastercellareaAlgorithm()

    def name(self):  # pylint: disable=missing-function-docstring
        return 'cellarea'

    def displayName(self):  # pylint: disable=missing-function-docstring
        return self.tr('cellarea')

    def group(self):  # pylint: disable=missing-function-docstring
        return self.tr('Data management')

    def groupId(self):  # pylint: disable=missing-function-docstring
        return self.tr('data')

    def shortHelpString(self):  # pylint: disable=missing-function-docstring
        return self.tr(
            """Area of one cell

                <a href="https://pcraster.geo.uu.nl/pcraster/4.3.2/documentation/pcraster_manual/sphinx/op_cellarea.html">PCRaster documentation</a>

                Parameters:

                 * <b>Input raster layer</b> (required) - raster layer for which the cell area will be calculated
                 * <b>Units</b> (required) - map units or cells
                 * <b>Output cell area layer</b> (required) - where the results will be saved.

                Results:

                 * OUTPUT_RASTER
            """
        )

    def helpUrl(self):  # pylint: disable=missing-function-docstring
        return "https://pcraster.geo.uu.nl/pcraster/4.3.1/documentation/pcraster_manual/sphinx/op_cellarea.html"

    def initAlgorithm(self, config=None):  # pylint: disable=missing-function-docstring,unused-argument
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_RASTER,
                self.tr('Raster layer')
            )
        )

        unitoption = [self.tr('Map units'), self.tr('Cells')]
        self.addParameter(
            QgsProcessingParameterEnum(
                self.INPUT_UNITS,
                self.tr('Units'),
                unitoption,
                defaultValue=0
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.OUTPUT_RASTER,
                self.tr("Output cellarea layer")
            )
        )

    def processAlgorithm(self, parameters, context, feedback):  # pylint: disable=missing-function-docstring,unused-argument,too-many-locals
        try:
            from pcraster import (   # pylint: disable=import-outside-toplevel
                setclone,
                report,
                setglobaloption,
                cellarea
            )
        except ImportError as e:
            raise QgsProcessingException('PCRaster library is not available') from e

        input_raster = self.parameterAsRasterLayer(parameters, self.INPUT_RASTER, context)
        lengthunits = self.parameterAsEnum(parameters, self.INPUT_UNITS, context)
        if lengthunits == 0:
            setglobaloption("unittrue")
        else:
            setglobaloption("unitcell")
        setclone(input_raster.dataProvider().dataSourceUri())
        cellareaLayer = cellarea()
        outputFilePath = self.parameterAsOutputLayer(parameters, self.OUTPUT_RASTER, context)

        report(cellareaLayer, outputFilePath)

        self.set_output_crs(output_file=outputFilePath, crs=input_raster.crs(), feedback=feedback, context=context)

        return {self.OUTPUT_RASTER: outputFilePath}
