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
                       QgsProcessingException)

from pcraster_tools.processing.algorithm import PCRasterAlgorithm


class PCRasterAccutraveltimefractionfluxAlgorithm(PCRasterAlgorithm):
    """
    Transports material downstream over a distance dependent on a given velocity.
    """

    INPUT_FLOWDIRECTION = 'INPUT'
    INPUT_MATERIAL = 'INPUT2'
    INPUT_VELOCITY = 'INPUT3'
    INPUT_FRACTION = 'INPUT4'
    OUTPUT_FLUX = 'OUTPUT'
    OUTPUT_STATE = 'OUTPUT2'
    OUTPUT_REMOVED = 'OUTPUT3'

    def createInstance(self):  # pylint: disable=missing-function-docstring
        return PCRasterAccutraveltimefractionfluxAlgorithm()

    def name(self):  # pylint: disable=missing-function-docstring
        return 'accutraveltimefractionflux'

    def displayName(self):  # pylint: disable=missing-function-docstring
        return self.tr('accutraveltimefractionflux, accutraveltimefractionstate and accutraveltimefractionremoved')

    def group(self):  # pylint: disable=missing-function-docstring
        return self.tr('Hydrological and material transport operations')

    def groupId(self):  # pylint: disable=missing-function-docstring
        return 'hydrological'

    def shortHelpString(self):  # pylint: disable=missing-function-docstring
        return self.tr(
            """Transports material downstream over a distance dependent on a given velocity.

            <a href="https://pcraster.geo.uu.nl/pcraster/4.3.1/documentation/pcraster_manual/sphinx/op_accutraveltimefraction.html">PCRaster documentation</a>

            Parameters:

            * <b>Input flow direction raster</b> (required) - Flow direction in PCRaster LDD format (see lddcreate)
            * <b>Input material raster</b> (required) - Scalar raster with amount of material input (>= 0)
            * <b>Input velocity raster</b> (required) - Scalar raster with the distance per time step in map units (>=0)
            * <b>Input fraction raster</b> (required) - Scalar raster with fraction equal to or between 0 and 1
            * <b>Output Flux raster</b> (required) - Scalar raster with result flux of material
            * <b>Output State raster</b> (required) - Scalar raster with result state of stored material
            * <b>Output Removed raster</b> (required) - Scalar raster with removed material
            """
        )

    def initAlgorithm(self, config=None):  # pylint: disable=missing-function-docstring,unused-argument
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_FLOWDIRECTION,
                self.tr('Input Flow Direction Raster Layer')
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_MATERIAL,
                self.tr('Input Material Raster Layer')
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_VELOCITY,
                self.tr('Input Velocity Raster Layer')
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_FRACTION,
                self.tr('Input Fraction Raster Layer')
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.OUTPUT_FLUX,
                self.tr('Output Material Flux Raster Layer')
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.OUTPUT_STATE,
                self.tr('Output State Raster Layer')
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.OUTPUT_REMOVED,
                self.tr('Output Removed Raster Layer')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):  # pylint: disable=missing-function-docstring,unused-argument,too-many-locals,too-many-variables,too-many-locals
        try:
            from pcraster import (   # pylint: disable=import-outside-toplevel
                setclone,
                readmap,
                report,
                accutraveltimefractionflux,
                accutraveltimefractionstate,
                accutraveltimefractionremoved
            )
        except ImportError as e:
            raise QgsProcessingException('PCRaster library is not available') from e

        input_flowdirection = self.parameterAsRasterLayer(parameters, self.INPUT_FLOWDIRECTION, context)
        input_material = self.parameterAsRasterLayer(parameters, self.INPUT_MATERIAL, context)
        input_velocity = self.parameterAsRasterLayer(parameters, self.INPUT_VELOCITY, context)
        input_fraction = self.parameterAsRasterLayer(parameters, self.INPUT_FRACTION, context)
        setclone(input_flowdirection.dataProvider().dataSourceUri())
        LDD = readmap(input_flowdirection.dataProvider().dataSourceUri())
        material = readmap(input_material.dataProvider().dataSourceUri())
        transportvelocity = readmap(input_velocity.dataProvider().dataSourceUri())
        transportfraction = readmap(input_fraction.dataProvider().dataSourceUri())
        resultflux = accutraveltimefractionflux(LDD, material, transportvelocity, transportfraction)
        resultstate = accutraveltimefractionstate(LDD, material, transportvelocity, transportfraction)
        resultremoved = accutraveltimefractionremoved(LDD, material, transportvelocity, transportfraction)

        outputFlux = self.parameterAsOutputLayer(parameters, self.OUTPUT_FLUX, context)
        outputState = self.parameterAsOutputLayer(parameters, self.OUTPUT_STATE, context)
        outputRemoved = self.parameterAsOutputLayer(parameters, self.OUTPUT_REMOVED, context)

        report(resultflux, outputFlux)
        report(resultstate, outputState)
        report(resultremoved, outputRemoved)

        self.set_output_crs(output_file=outputFlux, crs=input_flow_direction.crs(), feedback=feedback, context=context)
        self.set_output_crs(output_file=outputState, crs=input_flow_direction.crs(), feedback=feedback, context=context)
        self.set_output_crs(output_file=outputRemoved, crs=input_flow_direction.crs(), feedback=feedback, context=context)

        return {self.OUTPUT_FLUX: outputFlux, self.OUTPUT_STATE: outputState, self.OUTPUT_REMOVED: outputRemoved}
