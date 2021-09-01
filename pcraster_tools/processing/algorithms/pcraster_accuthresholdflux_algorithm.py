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
    accuthresholdflux,
    accuthresholdstate,
    report
)
from qgis.core import (QgsProcessingParameterRasterDestination,
                       QgsProcessingParameterRasterLayer)

from pcraster_tools.processing.algorithm import PCRasterAlgorithm


class PCRasterAccuthresholdfluxAlgorithm(PCRasterAlgorithm):
    """
    Input of material downstream over a local drain direction network when transport threshold is exceeded
    """

    INPUT_FLOWDIRECTION = 'INPUT'
    INPUT_MATERIAL = 'INPUT2'
    INPUT_THRESHOLD = 'INPUT3'
    OUTPUT_FLUX = 'OUTPUT'
    OUTPUT_STATE = 'OUTPUT2'

    def createInstance(self):  # pylint: disable=missing-function-docstring
        return PCRasterAccuthresholdfluxAlgorithm()

    def name(self):  # pylint: disable=missing-function-docstring
        return 'accuthresholdflux'

    def displayName(self):  # pylint: disable=missing-function-docstring
        return self.tr('accuthresholdflux and accuthresholdstate')

    def group(self):  # pylint: disable=missing-function-docstring
        return self.tr('Hydrological and material transport operations')

    def groupId(self):  # pylint: disable=missing-function-docstring
        return 'hydrological'

    def shortHelpString(self):  # pylint: disable=missing-function-docstring
        return self.tr(
            """Input of material downstream over a local drain direction network when transport threshold is exceeded

            <a href="https://pcraster.geo.uu.nl/pcraster/4.3.1/documentation/pcraster_manual/sphinx/op_accuthreshold.html">PCRaster documentation</a>

            Parameters:

            * <b>Input flow direction raster</b> (required) - Flow direction in PCRaster LDD format (see lddcreate)
            * <b>Input material raster</b> (required) - Scalar raster with amount of material input (>= 0)
            * <b>Input transport threshold raster</b> (required) - Scalar raster with transport threshold values (>= 0)
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
                self.INPUT_THRESHOLD,
                self.tr('Input Transport Threshold Raster Layer')
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

    def processAlgorithm(self, parameters, context, feedback):  # pylint: disable=missing-function-docstring,unused-argument
        input_flow_direction = self.parameterAsRasterLayer(parameters, self.INPUT_FLOWDIRECTION, context)
        input_material = self.parameterAsRasterLayer(parameters, self.INPUT_MATERIAL, context)
        input_threshold = self.parameterAsRasterLayer(parameters, self.INPUT_THRESHOLD, context)
        setclone(input_flow_direction.dataProvider().dataSourceUri())
        ldd = readmap(input_flow_direction.dataProvider().dataSourceUri())
        material = readmap(input_material.dataProvider().dataSourceUri())
        transport_threshold = readmap(input_threshold.dataProvider().dataSourceUri())
        result_flux = accuthresholdflux(ldd, material, transport_threshold)
        result_state = accuthresholdstate(ldd, material, transport_threshold)

        output_flux = self.parameterAsOutputLayer(parameters, self.OUTPUT_FLUX, context)
        output_state = self.parameterAsOutputLayer(parameters, self.OUTPUT_STATE, context)

        report(result_flux, output_flux)
        report(result_state, output_state)

        return {self.OUTPUT_FLUX: output_flux, self.OUTPUT_STATE: output_state}
