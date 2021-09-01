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
    transient
)
from qgis.core import (QgsProcessingParameterRasterDestination,
                       QgsProcessingParameterNumber,
                       QgsProcessingParameterRasterLayer)

from pcraster_tools.processing.algorithm import PCRasterAlgorithm


class PCRasterTransientAlgorithm(PCRasterAlgorithm):
    """
    Simulates transient groundwater flow according to the implicit finite difference method.
    """

    INPUT_ELEVATION = 'INPUT'
    INPUT_RECHARGE = 'INPUT2'
    INPUT_TRANSMISSIVITY = 'INPUT3'
    INPUT_FLOWCONDITION = 'INPUT4'
    INPUT_STORAGE = 'INPUT5'
    INPUT_TIMESTEP = 'INPUT6'
    INPUT_TOLERANCE = 'INPUT7'
    OUTPUT_TRANSIENT = 'OUTPUT'

    def createInstance(self):  # pylint: disable=missing-function-docstring
        return PCRasterTransientAlgorithm()

    def name(self):  # pylint: disable=missing-function-docstring
        return 'transient'

    def displayName(self):  # pylint: disable=missing-function-docstring
        return self.tr('transient')

    def group(self):  # pylint: disable=missing-function-docstring
        return self.tr('PCRaster')

    def groupId(self):  # pylint: disable=missing-function-docstring
        return 'pcraster'

    def shortHelpString(self):  # pylint: disable=missing-function-docstring
        return self.tr(
            """Simulates transient groundwater flow according to the implicit finite difference method.

            <a href="https://pcraster.geo.uu.nl/pcraster/4.3.1/documentation/pcraster_manual/sphinx/op_transient.html">PCRaster documentation</a>

            Parameters:

            * <b>Input elevation raster</b> (required) - Scalar elevation raster
            * <b>Input recharge raster</b> (required) - Scalar raster with recharge [L T-1]
            * <b>Input transmissivity raster</b> (required) - Scalar raster transmissivity [L2 T-1]
            * <b>Input flow condition raster</b> (required) - Nominal raster with values for inactive (0), active (1) or constant head (2)
            * <b>Input storage coefficient raster</b> (required) - Scalar raster with storage coefficient [L3/L3]
            * <b>Input time step value</b> (required) - Time step [T]
            * <b>Input tolerance value</b> (required) - Value specifies the maximum difference between the current elevation and the new elevation
            * <b>Output transient raster</b> (required) - Scalar raster with result
            """
        )

    def initAlgorithm(self, config=None):  # pylint: disable=missing-function-docstring
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_ELEVATION,
                self.tr('Input Elevation Raster Layer')
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_RECHARGE,
                self.tr('Input Recharge Raster Layer')
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_TRANSMISSIVITY,
                self.tr('Input Transmissivity Raster Layer')
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_FLOWCONDITION,
                self.tr('Input Flow Condition Raster Layer')
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.INPUT_STORAGE,
                self.tr('Storage coefficient'),
                defaultValue=0.5
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.INPUT_TIMESTEP,
                self.tr('Time step'),
                defaultValue=10
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.INPUT_TOLERANCE,
                self.tr('Tolerance'),
                defaultValue=10
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.OUTPUT_TRANSIENT,
                self.tr('Output Transient Raster Layer')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):  # pylint: disable=missing-function-docstring
        input_elevation = self.parameterAsRasterLayer(parameters, self.INPUT_ELEVATION, context)
        input_recharge = self.parameterAsRasterLayer(parameters, self.INPUT_RECHARGE, context)
        input_transmissivity = self.parameterAsRasterLayer(parameters, self.INPUT_TRANSMISSIVITY, context)
        input_flowcondition = self.parameterAsRasterLayer(parameters, self.INPUT_FLOWCONDITION, context)
        input_storage = self.parameterAsRasterLayer(parameters, self.INPUT_STORAGE, context)
        timestep = self.parameterAsDouble(parameters, self.INPUT_TIMESTEP, context)
        tolerance = self.parameterAsDouble(parameters, self.INPUT_TOLERANCE, context)
        setclone(input_elevation.dataProvider().dataSourceUri())
        elevation = readmap(input_elevation.dataProvider().dataSourceUri())
        recharge = readmap(input_recharge.dataProvider().dataSourceUri())
        transmissivity = readmap(input_transmissivity.dataProvider().dataSourceUri())
        flowcondition = readmap(input_flowcondition.dataProvider().dataSourceUri())
        storage = readmap(input_storage.dataProvider().dataSourceUri())
        resulttransient = transient(elevation, recharge, transmissivity, flowcondition, storage, timestep, tolerance)

        outputTransient = self.parameterAsOutputLayer(parameters, self.OUTPUT_TRANSIENT, context)

        report(resulttransient, outputTransient)

        return {self.OUTPUT_TRANSIENT: outputTransient}
