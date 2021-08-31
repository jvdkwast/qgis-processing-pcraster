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
    accucapacityflux,
    accucapacitystate,
    report
)
from qgis.core import (QgsProcessingParameterRasterDestination,
                       QgsProcessingParameterRasterLayer)

from pcraster_tools.processing.algorithm import PCRasterAlgorithm


class PCRasterAccucapacityfluxAlgorithm(PCRasterAlgorithm):
    """
    Transport of material downstream over a local drain direction network
    """

    INPUT_FLOWDIRECTION = 'INPUT'
    INPUT_MATERIAL = 'INPUT2'
    INPUT_CAPACITY = 'INPUT3'
    OUTPUT_FLUX = 'OUTPUT'
    OUTPUT_STATE = 'OUTPUT2'

    def createInstance(self):  # pylint: disable=missing-function-docstring
        return PCRasterAccucapacityfluxAlgorithm()

    def name(self):  # pylint: disable=missing-function-docstring
        return 'accucapacityflux'

    def displayName(self):  # pylint: disable=missing-function-docstring
        return self.tr('accucapacityflux and accucapicitystate')

    def group(self):  # pylint: disable=missing-function-docstring
        return self.tr('PCRaster')

    def groupId(self):  # pylint: disable=missing-function-docstring
        return 'pcraster'

    def shortHelpString(self):  # pylint: disable=missing-function-docstring
        return self.tr(
            """Transport of material downstream over a local drain direction network
            
            <a href="https://pcraster.geo.uu.nl/pcraster/4.3.1/documentation/pcraster_manual/sphinx/op_accucapacity.html">PCRaster documentation</a>
            
            Parameters:
            
            * <b>Input flow direction raster</b> (required) - Flow direction in PCRaster LDD format (see lddcreate)
            * <b>Input material raster</b> (required) - Scalar raster with amount of material input (>= 0)
            * <b>Input transport capacity raster</b> (required) - Scalar raster with transport capacity (>= 0)
            * <b>Output Flux raster</b> (required) - Scalar raster with result flux of material
            * <b>Output State raster</b> (required) - Scalar raster with result state of stored material
            """
        )

    def initAlgorithm(self, config=None):  # pylint: disable=missing-function-docstring
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
                self.INPUT_CAPACITY,
                self.tr('Input Storage Capacity Raster Layer')
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

    def processAlgorithm(self, parameters, context, feedback):  # pylint: disable=missing-function-docstring
        input_flow_direction = self.parameterAsRasterLayer(parameters, self.INPUT_FLOWDIRECTION, context)
        input_material = self.parameterAsRasterLayer(parameters, self.INPUT_MATERIAL, context)
        input_capacity = self.parameterAsRasterLayer(parameters, self.INPUT_CAPACITY, context)
        setclone(input_flow_direction.dataProvider().dataSourceUri())
        ldd = readmap(input_flow_direction.dataProvider().dataSourceUri())
        material = readmap(input_material.dataProvider().dataSourceUri())
        transport_capacity = readmap(input_capacity.dataProvider().dataSourceUri())
        result_flux = accucapacityflux(ldd, material, transport_capacity)
        result_state = accucapacitystate(ldd, material, transport_capacity)

        output_flux = self.parameterAsOutputLayer(parameters, self.OUTPUT_FLUX, context)
        output_state = self.parameterAsOutputLayer(parameters, self.OUTPUT_STATE, context)

        report(result_flux, output_flux)
        report(result_state, output_state)

        return {self.OUTPUT_FLUX: output_flux, self.OUTPUT_STATE: output_state}
