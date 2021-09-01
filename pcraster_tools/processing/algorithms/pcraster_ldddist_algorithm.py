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
    ldddist,
    setglobaloption
)
from qgis.core import (QgsProcessingParameterRasterDestination,
                       QgsProcessingParameterEnum,
                       QgsProcessingParameterRasterLayer)

from pcraster_tools.processing.algorithm import PCRasterAlgorithm


class PCRasterLDDDistAlgorithm(PCRasterAlgorithm):
    """
    Friction-distance from the cell under consideration to downstream nearest TRUE cell
    """

    INPUT_LDD = 'INPUT'
    INPUT_UNITS = 'INPUT1'
    INPUT_POINTS = 'INPUT2'
    INPUT_FRICTION = 'INPUT3'
    OUTPUT_LDDDIST = 'OUTPUT'

    def createInstance(self):  # pylint: disable=missing-function-docstring
        return PCRasterLDDDistAlgorithm()

    def name(self):  # pylint: disable=missing-function-docstring
        return 'ldddist'

    def displayName(self):  # pylint: disable=missing-function-docstring
        return self.tr('ldddist')

    def group(self):  # pylint: disable=missing-function-docstring
        return self.tr('Hydrological and material transport operations')

    def groupId(self):  # pylint: disable=missing-function-docstring
        return 'hydrological'

    def shortHelpString(self):  # pylint: disable=missing-function-docstring
        return self.tr(
            """Friction-distance from the cell under consideration to downstream nearest TRUE cell

            <a href="https://pcraster.geo.uu.nl/pcraster/4.3.1/documentation/pcraster_manual/sphinx/op_ldddist.html">PCRaster documentation</a>

            Parameters:

            * <b>Input Local Drain Direction raster</b> (required) - LDD raster
            * <b>Units</b> (required) - map units or cells
            * <b>Raster layer with cells to which distance is calculated</b> (required) - boolean raster layer
            * <b>Friction raster layer</b> (required) - The amount of increase in friction per unit distance
            * <b>Result distance layer</b> (required) - Scalar raster with friction-distance from the cell under consideration to downstream nearest TRUE cell
            """
        )

    def initAlgorithm(self, config=None):  # pylint: disable=missing-function-docstring,unused-argument
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_LDD,
                self.tr('LDD layer')
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
            QgsProcessingParameterRasterLayer(
                self.INPUT_POINTS,
                self.tr('Cells to which distance is calculated (Boolean)')
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
                self.OUTPUT_LDDDIST,
                self.tr('Result distance layer')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):  # pylint: disable=missing-function-docstring,unused-argument
        input_ldd = self.parameterAsRasterLayer(parameters, self.INPUT_LDD, context)
        lengthunits = self.parameterAsEnum(parameters, self.INPUT_UNITS, context)
        if lengthunits == 0:
            setglobaloption("unittrue")
        else:
            setglobaloption("unitcell")
        input_points = self.parameterAsRasterLayer(parameters, self.INPUT_POINTS, context)
        input_friction = self.parameterAsRasterLayer(parameters, self.INPUT_FRICTION, context)
        setclone(input_ldd.dataProvider().dataSourceUri())
        LDD = readmap(input_ldd.dataProvider().dataSourceUri())
        Points = readmap(input_points.dataProvider().dataSourceUri())
        Friction = readmap(input_friction.dataProvider().dataSourceUri())
        LDDDistance = ldddist(LDD, Points, Friction)
        outputFilePath = self.parameterAsOutputLayer(parameters, self.OUTPUT_LDDDIST, context)
        report(LDDDistance, outputFilePath)

        return {self.OUTPUT_LDDDIST: outputFilePath}
