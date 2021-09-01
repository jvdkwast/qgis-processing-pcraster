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


class PCRasterCatchmenttotalAlgorithm(PCRasterAlgorithm):
    """
    Total catchment for the entire upstream area
    """

    INPUT_LDD = 'INPUT'
    INPUT_MATERIAL = 'INPUT2'
    OUTPUT_ACCUFLUX = 'OUTPUT'

    def createInstance(self):  # pylint: disable=missing-function-docstring
        return PCRasterCatchmenttotalAlgorithm()

    def name(self):  # pylint: disable=missing-function-docstring
        return 'catchmenttotal'

    def displayName(self):  # pylint: disable=missing-function-docstring
        return self.tr('catchmenttotal')

    def group(self):  # pylint: disable=missing-function-docstring
        return self.tr('Hydrological and material transport operations')

    def groupId(self):  # pylint: disable=missing-function-docstring
        return 'hydrological'

    def shortHelpString(self):  # pylint: disable=missing-function-docstring
        return self.tr(
            """Total catchment for the entire upstream area

            <a href="https://pcraster.geo.uu.nl/pcraster/4.3.1/documentation/pcraster_manual/sphinx/op_catchmenttotal.html">PCRaster documentation</a>

            Parameters:

            * <b>Input flow direction raster</b> (required) - Flow direction raster in PCRaster LDD format (see lddcreate)
            * <b>Input material raster</b> (required) - Scalar raster with material (>= 0)
            * <b>Result catchment total layer</b> (required) - Scalar raster with catchment total
            """
        )

    def initAlgorithm(self, config=None):  # pylint: disable=missing-function-docstring,unused-argument
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_LDD,
                self.tr('LDD layer')
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_MATERIAL,
                self.tr('Material layer')
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.OUTPUT_ACCUFLUX,
                self.tr('Result catchment total layer')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):  # pylint: disable=missing-function-docstring,unused-argument,too-many-locals
        try:
            from pcraster import (   # pylint: disable=import-outside-toplevel
                setclone,
                readmap,
                report,
                catchmenttotal
            )
        except ImportError as e:
            raise QgsProcessingException('PCRaster library is not available') from e

        input_ldd = self.parameterAsRasterLayer(parameters, self.INPUT_LDD, context)
        input_material = self.parameterAsRasterLayer(parameters, self.INPUT_MATERIAL, context)
        setclone(input_ldd.dataProvider().dataSourceUri())
        LDD = readmap(input_ldd.dataProvider().dataSourceUri())
        Material = readmap(input_material.dataProvider().dataSourceUri())
        ResultFlux = catchmenttotal(LDD, Material)
        outputFilePath = self.parameterAsOutputLayer(parameters, self.OUTPUT_ACCUFLUX, context)
        report(ResultFlux, outputFilePath)

        return {self.OUTPUT_ACCUFLUX: outputFilePath}
