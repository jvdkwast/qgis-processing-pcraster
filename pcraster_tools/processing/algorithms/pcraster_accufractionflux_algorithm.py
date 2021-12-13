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


class PCRasterAccufractionfluxAlgorithm(PCRasterAlgorithm):
    """
    Fractional material transport downstream over local drain direction network
    """

    INPUT_FLOWDIRECTION = 'INPUT'
    INPUT_MATERIAL = 'INPUT2'
    INPUT_FRACTION = 'INPUT3'
    OUTPUT_FLUX = 'OUTPUT'
    OUTPUT_STATE = 'OUTPUT2'

    def createInstance(self):  # pylint: disable=missing-function-docstring
        return PCRasterAccufractionfluxAlgorithm()

    def name(self):  # pylint: disable=missing-function-docstring
        return 'accufractionflux'

    def displayName(self):  # pylint: disable=missing-function-docstring
        return self.tr('accufractionflux and accufractionstate')

    def group(self):  # pylint: disable=missing-function-docstring
        return self.tr('Hydrological and material transport operations')

    def groupId(self):  # pylint: disable=missing-function-docstring
        return 'hydrological'

    def shortHelpString(self):  # pylint: disable=missing-function-docstring
        return self.tr(
            """Fractional material transport downstream over local drain direction network

            <a href="https://pcraster.geo.uu.nl/pcraster/4.3.2/documentation/pcraster_manual/sphinx/op_accufraction.html">PCRaster documentation</a>

            Parameters:

            * <b>Input flow direction raster</b> (required) - Flow direction in PCRaster LDD format (see lddcreate)
            * <b>Input material raster</b> (required) - Scalar raster with amount of material input (>= 0)
            * <b>Input transport fraction raster</b> (required) - Scalar raster with transport fraction values equal to or between 0 and 1
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
                self.INPUT_FRACTION,
                self.tr('Input Transport Fraction Raster Layer')
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
                accufractionflux,
                accufractionstate,
                report
            )
        except ImportError as e:
            raise QgsProcessingException('PCRaster library is not available') from e

        input_flow_direction = self.parameterAsRasterLayer(parameters, self.INPUT_FLOWDIRECTION, context)
        input_material = self.parameterAsRasterLayer(parameters, self.INPUT_MATERIAL, context)
        input_fraction = self.parameterAsRasterLayer(parameters, self.INPUT_FRACTION, context)
        setclone(input_flow_direction.dataProvider().dataSourceUri())
        ldd = readmap(input_flow_direction.dataProvider().dataSourceUri())
        material = readmap(input_material.dataProvider().dataSourceUri())
        transport_fraction = readmap(input_fraction.dataProvider().dataSourceUri())
        result_flux = accufractionflux(ldd, material, transport_fraction)
        result_state = accufractionstate(ldd, material, transport_fraction)

        output_flux = self.parameterAsOutputLayer(parameters, self.OUTPUT_FLUX, context)
        output_state = self.parameterAsOutputLayer(parameters, self.OUTPUT_STATE, context)

        report(result_flux, output_flux)
        report(result_state, output_state)

        self.set_output_crs(output_file=output_flux, crs=input_flow_direction.crs(), feedback=feedback, context=context)
        self.set_output_crs(output_file=output_state, crs=input_flow_direction.crs(), feedback=feedback, context=context)

        return {self.OUTPUT_FLUX: output_flux, self.OUTPUT_STATE: output_state}
