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


class PCRasterSpreadmaxAlgorithm(PCRasterAlgorithm):
    """
    Total friction of the shortest accumulated friction path over a map with friction values from a source cell to cell under consideration considering maximum spread distance
    """

    INPUT_POINTS = 'INPUT'
    INPUT_UNITS = 'INPUT1'
    INPUT_INITIALFRICTION = 'INPUT2'
    INPUT_FRICTION = 'INPUT3'
    INPUT_MAX = 'INPUT4'
    OUTPUT_SPREAD = 'OUTPUT'

    def createInstance(self):  # pylint: disable=missing-function-docstring
        return PCRasterSpreadmaxAlgorithm()

    def name(self):  # pylint: disable=missing-function-docstring
        return 'spreadmax'

    def displayName(self):  # pylint: disable=missing-function-docstring
        return self.tr('spreadmax')

    def group(self):  # pylint: disable=missing-function-docstring
        return self.tr('Proximity analysis')

    def groupId(self):  # pylint: disable=missing-function-docstring
        return 'proximity'

    def shortHelpString(self):  # pylint: disable=missing-function-docstring
        return self.tr(
            """Total friction of the shortest accumulated friction path over a map with friction values from a source cell to cell under consideration considering maximum spread distance

            <a href="{}">PCRaster documentation</a>

            Parameters:

            * <b>Points raster</b> (required) - boolean, nominal or ordinal raster layer with cells from which the shortest accumulated friction path to every cell centre is calculated
            * <b>Units</b> (required) - map units or cells
            * <b>Initial friction layer</b> (required) - initial friction at start of spreading, scalar data type
            * <b>Friction raster layer</b> (required) - The amount of increase in friction per unit distance, scalar data type
            * <b>Maximum distance</b> (required) - Maximum distance for which the result is calculated. Beyond this distance cell results are given MV
            * <b>Result spread max layer</b> (required) - Scalar raster with total friction of the shortest accumulated friction path over a map with friction values from a source cell to cell under consideration considering maximum spread distance
            """
        ).format(PCRasterAlgorithm.documentation_url('op_spreadmax.html'))

    def initAlgorithm(self, config=None):  # pylint: disable=missing-function-docstring,unused-argument
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_POINTS,
                self.tr('Points raster')
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_INITIALFRICTION,
                self.tr('Initial friction layer'),
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_FRICTION,
                self.tr('Friction layer')
            )
        )

        unitoption = [self.tr('Map units'), self.tr('Cells')]
        self.addParameter(
            QgsProcessingParameterEnum(
                self.INPUT_UNITS,
                self.tr('Distance units'),
                unitoption,
                defaultValue=0
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.INPUT_MAX,
                self.tr('Maximum distance'),
                defaultValue=100
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.OUTPUT_SPREAD,
                self.tr('Output spread max result')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):  # pylint: disable=missing-function-docstring,unused-argument,too-many-locals
        try:
            from pcraster import (   # pylint: disable=import-outside-toplevel
                setclone,
                readmap,
                report,
                spreadmax,
                setglobaloption
            )
        except ImportError as e:
            raise QgsProcessingException('PCRaster library is not available') from e

        input_points = self.parameterAsRasterLayer(parameters, self.INPUT_POINTS, context)
        lengthunits = self.parameterAsEnum(parameters, self.INPUT_UNITS, context)
        if lengthunits == 0:
            setglobaloption("unittrue")
        else:
            setglobaloption("unitcell")
        input_initial = self.parameterAsRasterLayer(parameters, self.INPUT_INITIALFRICTION, context)
        input_friction = self.parameterAsRasterLayer(parameters, self.INPUT_FRICTION, context)
        input_max = self.parameterAsDouble(parameters, self.INPUT_MAX, context)
        setclone(input_points.dataProvider().dataSourceUri())
        PointsLayer = readmap(input_points.dataProvider().dataSourceUri())
        InitialFriction = readmap(input_initial.dataProvider().dataSourceUri())
        Friction = readmap(input_friction.dataProvider().dataSourceUri())
        SpreadLayer = spreadmax(PointsLayer, InitialFriction, Friction, input_max)
        outputFilePath = self.parameterAsOutputLayer(parameters, self.OUTPUT_SPREAD, context)
        report(SpreadLayer, outputFilePath)

        self.set_output_crs(output_file=outputFilePath, crs=input_points.crs(), feedback=feedback, context=context)

        return {self.OUTPUT_SPREAD: outputFilePath}
