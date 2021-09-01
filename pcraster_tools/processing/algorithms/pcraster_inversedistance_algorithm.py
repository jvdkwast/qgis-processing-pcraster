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
    setglobaloption,
    inversedistance
)
from qgis.core import (QgsProcessingParameterRasterDestination,
                       QgsProcessingParameterRasterLayer,
                       QgsProcessingParameterEnum,
                       QgsProcessingParameterNumber)

from pcraster_tools.processing.algorithm import PCRasterAlgorithm


class PCRasterInversedistanceAlgorithm(PCRasterAlgorithm):
    """
    Interpolate values using inverse distance weighting
    """

    INPUT_MASK = 'INPUT'
    INPUT_UNITS = 'INPUT1'
    INPUT_POINTS = 'INPUT2'
    INPUT_IDP = 'INPUT3'
    INPUT_RADIUS = 'INPUT4'
    INPUT_MAXNR = 'INPUT5'
    OUTPUT_INVERSEDISTANCE = 'OUTPUT'

    def createInstance(self):  # pylint: disable=missing-function-docstring
        return PCRasterInversedistanceAlgorithm()

    def name(self):  # pylint: disable=missing-function-docstring
        return 'inversedistance'

    def displayName(self):  # pylint: disable=missing-function-docstring
        return self.tr('inversedistance')

    def group(self):  # pylint: disable=missing-function-docstring
        return self.tr('Missing value creation, detection, alteration')

    def groupId(self):  # pylint: disable=missing-function-docstring
        return 'missingvalues'

    def shortHelpString(self):  # pylint: disable=missing-function-docstring
        return self.tr(
            """Interpolate values using inverse distance weighting

            <a href="https://pcraster.geo.uu.nl/pcraster/4.3.1/documentation/pcraster_manual/sphinx/op_inversedistance.html">PCRaster documentation</a>

            Parameters:

            * <b>Input mask raster layer</b> (required) - boolean raster layer with mask
            * <b>Raster layer with values to be interpolated</b> (required) - scalar raster layer
            * <b>Power</b> (required) - power of the weight function (default 2)
            * <b>Units</b> (required) - unit of radius in map units or cells
            * <b>Radius</b> (required) - select only the points at a distance less or equal to the cell. Default 0 includes all points.
            * <b>Maximum number of closest points</b> (required) - the maximum number of points used in the computation. Default 0 includes all points.
            * <b>Inverse Distance Interpolation output</b> (required) - Scalar raster with interpolation result.
            """
        )

    def initAlgorithm(self, config=None):  # pylint: disable=missing-function-docstring,unused-argument
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_MASK,
                self.tr('Mask layer')
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_POINTS,
                self.tr('Raster layer with values to be interpolated')
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.INPUT_IDP,
                self.tr('Power'),
                defaultValue=2
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
            QgsProcessingParameterNumber(
                self.INPUT_RADIUS,
                self.tr('Radius'),
                defaultValue=0
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.INPUT_MAXNR,
                self.tr('Maximum number of closest points'),
                defaultValue=0
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.OUTPUT_INVERSEDISTANCE,
                self.tr('Inverse Distance Interpolation output')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):  # pylint: disable=missing-function-docstring,unused-argument
        input_mask = self.parameterAsRasterLayer(parameters, self.INPUT_MASK, context)
        input_points = self.parameterAsRasterLayer(parameters, self.INPUT_POINTS, context)
        input_idp = self.parameterAsDouble(parameters, self.INPUT_IDP, context)
        lengthunits = self.parameterAsEnum(parameters, self.INPUT_UNITS, context)
        if lengthunits == 0:
            setglobaloption("unittrue")
        else:
            setglobaloption("unitcell")
        input_radius = self.parameterAsDouble(parameters, self.INPUT_RADIUS, context)
        input_maxnr = self.parameterAsDouble(parameters, self.INPUT_MAXNR, context)
        setclone(input_mask.dataProvider().dataSourceUri())
        MaskLayer = readmap(input_mask.dataProvider().dataSourceUri())
        PointsLayer = readmap(input_points.dataProvider().dataSourceUri())
        IDW = inversedistance(MaskLayer, PointsLayer, input_idp, input_radius, input_maxnr)
        outputFilePath = self.parameterAsOutputLayer(parameters, self.OUTPUT_INVERSEDISTANCE, context)
        report(IDW, outputFilePath)

        return {self.OUTPUT_INVERSEDISTANCE: outputFilePath}
