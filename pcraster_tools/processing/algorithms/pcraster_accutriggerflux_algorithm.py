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


class PCRasterAccutriggerfluxAlgorithm(PCRasterAlgorithm):
    """
    Input of material downstream over a local drain direction network when transport trigger is exceeded
    """

    INPUT_FLOWDIRECTION = 'INPUT'
    INPUT_MATERIAL = 'INPUT2'
    INPUT_TRIGGER = 'INPUT3'
    OUTPUT_FLUX = 'OUTPUT'
    OUTPUT_STATE = 'OUTPUT2'

    def createInstance(self):  # pylint: disable=missing-function-docstring
        return PCRasterAccutriggerfluxAlgorithm()

    def name(self):  # pylint: disable=missing-function-docstring
        return 'accutriggerflux'

    def displayName(self):  # pylint: disable=missing-function-docstring
        return self.tr('accutriggerflux and accutriggerstate')

    def group(self):  # pylint: disable=missing-function-docstring
        return self.tr('Hydrological and material transport operations')

    def groupId(self):  # pylint: disable=missing-function-docstring
        return 'hydrological'

    def shortHelpString(self):  # pylint: disable=missing-function-docstring
        return self.tr(
            """Input of material downstream over a local drain direction network when transport trigger is exceeded

            <a href="https://pcraster.geo.uu.nl/pcraster/4.3.1/documentation/pcraster_manual/sphinx/op_accutrigger.html">PCRaster documentation</a>

            Parameters:

            * <b>Input flow direction raster</b> (required) - Flow direction in PCRaster LDD format (see lddcreate)
            * <b>Input material raster</b> (required) - Scalar raster with amount of material input (>= 0)
            * <b>Input transport trigger raster</b> (required) - Scalar raster with transport trigger values (>= 0)
            * <b>Output Flux raster</b> (required) - Scalar raster with result flux of material
            * <b>Output State raster</b> (required) - Scalar raster with result state of stored material
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
                self.INPUT_TRIGGER,
                self.tr('Input Transport Trigger Raster Layer')
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

    def processAlgorithm(self, parameters, context, feedback):  # pylint: disable=missing-function-docstring,unused-argument,too-many-locals
        try:
            from pcraster import (   # pylint: disable=import-outside-toplevel
                setclone,
                readmap,
                accutriggerflux,
                accutriggerstate,
                report
            )
        except ImportError as e:
            raise QgsProcessingException('PCRaster library is not available') from e

        input_flowdirection = self.parameterAsRasterLayer(parameters, self.INPUT_FLOWDIRECTION, context)
        input_material = self.parameterAsRasterLayer(parameters, self.INPUT_MATERIAL, context)
        input_trigger = self.parameterAsRasterLayer(parameters, self.INPUT_TRIGGER, context)
        setclone(input_flowdirection.dataProvider().dataSourceUri())
        LDD = readmap(input_flowdirection.dataProvider().dataSourceUri())
        material = readmap(input_material.dataProvider().dataSourceUri())
        transporttrigger = readmap(input_trigger.dataProvider().dataSourceUri())
        resultflux = accutriggerflux(LDD, material, transporttrigger)
        resultstate = accutriggerstate(LDD, material, transporttrigger)

        outputFlux = self.parameterAsOutputLayer(parameters, self.OUTPUT_FLUX, context)
        outputState = self.parameterAsOutputLayer(parameters, self.OUTPUT_STATE, context)

        report(resultflux, outputFlux)
        report(resultstate, outputState)

        self.set_output_crs(output_file=outputFlux, crs=input_flow_direction.crs(), feedback=feedback, context=context)
        self.set_output_crs(output_file=outputState, crs=input_flow_direction.crs(), feedback=feedback, context=context)

        return {self.OUTPUT_FLUX: outputFlux, self.OUTPUT_STATE: outputState}
