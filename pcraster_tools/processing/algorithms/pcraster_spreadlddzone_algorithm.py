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
    spreadlddzone,
    setglobaloption
)
from qgis.core import (QgsProcessingParameterRasterDestination,
                       QgsProcessingParameterRasterLayer,
                       QgsProcessingParameterEnum)

from pcraster_tools.processing.algorithm import PCRasterAlgorithm


class PCRasterSpreadlddzoneAlgorithm(PCRasterAlgorithm):
    """
    Shortest friction-distance path over map with friction from a source cell to cell under consideration, only paths in downstream direction from the source cell are considered
    """

    INPUT_LDD = 'INPUT'
    INPUT_POINTS = 'INPUT1'
    INPUT_UNITS = 'INPUT4'
    INPUT_INITIALFRICTION = 'INPUT2'
    INPUT_FRICTION = 'INPUT3'
    OUTPUT_SPREAD = 'OUTPUT'

    def createInstance(self):  # pylint: disable=missing-function-docstring
        return PCRasterSpreadlddzoneAlgorithm()

    def name(self):  # pylint: disable=missing-function-docstring
        return 'spreadlddzone'

    def displayName(self):  # pylint: disable=missing-function-docstring
        return self.tr('spreadlddzone')

    def group(self):  # pylint: disable=missing-function-docstring
        return self.tr('PCRaster')

    def groupId(self):  # pylint: disable=missing-function-docstring
        return 'pcraster'

    def shortHelpString(self):  # pylint: disable=missing-function-docstring
        return self.tr(
            """Shortest friction-distance path over map with friction from a source cell to cell under consideration, only paths in downstream direction from the source cell are considered

            <a href="https://pcraster.geo.uu.nl/pcraster/4.3.1/documentation/pcraster_manual/sphinx/op_spreadlddzone.html">PCRaster documentation</a>

            Parameters:

            * <b>LDD raster</b> (required) - Raster with local drain direction with LDD data type
            * <b>Points raster</b> (required) - boolean, nominal or ordinal raster layer with cells from which the shortest accumulated friction path to every cell centre is calculated
            * <b>Units</b> (required) - map units or cells
            * <b>Initial friction layer</b> (required) - initial friction at start of spreading, scalar data type
            * <b>Friction raster layer</b> (required) - The amount of increase in friction per unit distance, scalar data type
            * <b>Result spread ldd zone layer</b> (required) - each cell is assigned the points cell value of the cell where the shortest path to the cell begins, data type same as points raster
            """
        )

    def initAlgorithm(self, config=None):  # pylint: disable=missing-function-docstring,unused-argument
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_LDD,
                self.tr('Local drain direction raster')
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_POINTS,
                self.tr('Points raster')
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

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.OUTPUT_SPREAD,
                self.tr('Output spread ldd zone result')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):  # pylint: disable=missing-function-docstring,unused-argument
        input_ldd = self.parameterAsRasterLayer(parameters, self.INPUT_LDD, context)
        input_points = self.parameterAsRasterLayer(parameters, self.INPUT_POINTS, context)
        lengthunits = self.parameterAsEnum(parameters, self.INPUT_UNITS, context)
        if lengthunits == 0:
            setglobaloption("unittrue")
        else:
            setglobaloption("unitcell")
        input_initial = self.parameterAsRasterLayer(parameters, self.INPUT_INITIALFRICTION, context)
        input_friction = self.parameterAsRasterLayer(parameters, self.INPUT_FRICTION, context)
        setclone(input_ldd.dataProvider().dataSourceUri())
        LDD = readmap(input_ldd.dataProvider().dataSourceUri())
        PointsLayer = readmap(input_points.dataProvider().dataSourceUri())
        InitialFriction = readmap(input_initial.dataProvider().dataSourceUri())
        Friction = readmap(input_friction.dataProvider().dataSourceUri())
        SpreadLayer = spreadlddzone(LDD, PointsLayer, InitialFriction, Friction)
        outputFilePath = self.parameterAsOutputLayer(parameters, self.OUTPUT_SPREAD, context)
        report(SpreadLayer, outputFilePath)

        return {self.OUTPUT_SPREAD: outputFilePath}
