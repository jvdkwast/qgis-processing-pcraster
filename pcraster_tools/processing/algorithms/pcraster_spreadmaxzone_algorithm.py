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
    spreadmaxzone,
    setglobaloption
)
from qgis.core import (QgsProcessingParameterRasterDestination,
                       QgsProcessingParameterRasterLayer,
                       QgsProcessingParameterEnum,
                       QgsProcessingParameterNumber)

from pcraster_tools.processing.algorithm import PCRasterAlgorithm


class PCRasterSpreadmaxzoneAlgorithm(PCRasterAlgorithm):
    """
    Shortest friction-distance path over a map with friction from an identified source cell or cells to the cell under consideration
    """

    INPUT_POINTS = 'INPUT'
    INPUT_UNITS = 'INPUT1'
    INPUT_INITIALFRICTION = 'INPUT2'
    INPUT_FRICTION = 'INPUT3'
    INPUT_MAX = 'INPUT4'
    OUTPUT_SPREAD = 'OUTPUT'

    def createInstance(self):  # pylint: disable=missing-function-docstring
        return PCRasterSpreadmaxzoneAlgorithm()

    def name(self):  # pylint: disable=missing-function-docstring
        return 'spreadmaxzone'

    def displayName(self):  # pylint: disable=missing-function-docstring
        return self.tr('spreadmaxzone')

    def group(self):  # pylint: disable=missing-function-docstring
        return self.tr('PCRaster')

    def groupId(self):  # pylint: disable=missing-function-docstring
        return 'pcraster'

    def shortHelpString(self):  # pylint: disable=missing-function-docstring
        return self.tr(
            """Shortest friction-distance path over a map with friction from an identified source cell or cells to the cell under consideration

            <a href="https://pcraster.geo.uu.nl/pcraster/4.3.1/documentation/pcraster_manual/sphinx/op_spreadmaxzone.html">PCRaster documentation</a>

            Parameters:

            * <b>Points raster</b> (required) - boolean, nominal or ordinal raster layer with cells from which the shortest accumulated friction path to every cell centre is calculated
            * <b>Units</b> (required) - map units or cells
            * <b>Initial friction layer</b> (required) - initial friction at start of spreading, scalar data type
            * <b>Friction raster layer</b> (required) - The amount of increase in friction per unit distance, scalar data type
            * <b>Maximum distance</b> (required) - Maximum distance for which the result is calculated. Beyond this distance cell results are given MV
            * <b>Result spread max zone layer</b> (required) - Raster with value of points within the maximum spread distance
            """
        )

    def initAlgorithm(self, config=None):  # pylint: disable=missing-function-docstring
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
                self.tr('Output spread max zone result')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):  # pylint: disable=missing-function-docstring
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
        SpreadLayer = spreadmaxzone(PointsLayer, InitialFriction, Friction, input_max)
        outputFilePath = self.parameterAsOutputLayer(parameters, self.OUTPUT_SPREAD, context)
        report(SpreadLayer, outputFilePath)

        return {self.OUTPUT_SPREAD: outputFilePath}
