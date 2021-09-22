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


class PCRasterCatchmentAlgorithm(PCRasterAlgorithm):
    """
    Catchment(s) of one or more specified cells
    """

    INPUT_LDD = 'INPUT1'
    INPUT_OUTLET = 'INPUT2'
    OUTPUT_CATCHMENT = 'OUTPUT'

    def createInstance(self):  # pylint: disable=missing-function-docstring
        return PCRasterCatchmentAlgorithm()

    def name(self):  # pylint: disable=missing-function-docstring
        return 'catchment'

    def displayName(self):  # pylint: disable=missing-function-docstring
        return self.tr('catchment')

    def group(self):  # pylint: disable=missing-function-docstring
        return self.tr('Hydrological and material transport operations')

    def groupId(self):  # pylint: disable=missing-function-docstring
        return 'hydrological'

    def shortHelpString(self):  # pylint: disable=missing-function-docstring
        return self.tr(
            """Catchment(s) of one or more specified cells

            <a href="https://pcraster.geo.uu.nl/pcraster/4.3.1/documentation/pcraster_manual/sphinx/op_catchment.html">PCRaster documentation</a>

            Parameters:

            * <b>Input flow direction raster</b> (required) - Flow direction raster in PCRaster LDD format (see lddcreate)
            * <b>Input outlet raster</b> (required) - Boolean, nominal or ordinal raster with outlet locations
            * <b>Result catchment layer</b> (required) - Raster with same data type as outlet raster containing catchment(s)
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
                self.INPUT_OUTLET,
                self.tr('Outlet layer')
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.OUTPUT_CATCHMENT,
                self.tr('Catchment layer')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):  # pylint: disable=missing-function-docstring,unused-argument,too-many-locals
        try:
            from pcraster import (   # pylint: disable=import-outside-toplevel
                setclone,
                readmap,
                report,
                catchment
            )
        except ImportError as e:
            raise QgsProcessingException('PCRaster library is not available') from e

        input_ldd = self.parameterAsRasterLayer(parameters, self.INPUT_LDD, context)
        input_outlet = self.parameterAsRasterLayer(parameters, self.INPUT_OUTLET, context)
        setclone(input_ldd.dataProvider().dataSourceUri())
        LDD = readmap(input_ldd.dataProvider().dataSourceUri())
        Outlets = readmap(input_outlet.dataProvider().dataSourceUri())
        CatchmentOfOutlets = catchment(LDD, Outlets)
        outputFilePath = self.parameterAsOutputLayer(parameters, self.OUTPUT_CATCHMENT, context)
        report(CatchmentOfOutlets, outputFilePath)

        self.set_output_crs(output_file=outputFilePath, crs=input_ldd.crs(), feedback=feedback, context=context)

        return {self.OUTPUT_CATCHMENT: outputFilePath}
