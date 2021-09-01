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
    report,
    lookupboolean,
    lookupnominal,
    lookupordinal,
    lookupscalar,
    lookupdirectional,
    lookupldd
)
from qgis.core import (QgsProcessing,
                       QgsProcessingParameterRasterDestination,
                       QgsProcessingParameterFile,
                       QgsProcessingParameterEnum,
                       QgsProcessingParameterMultipleLayers)

from pcraster_tools.processing.algorithm import PCRasterAlgorithm


class PCRasterLookupAlgorithm(PCRasterAlgorithm):
    """
    Compares cell value(s) of one or more expression(s) with the search key in a table
    """

    INPUT_RASTERS = 'INPUT'
    INPUT_TABLE = 'INPUT1'
    INPUT_DATATYPE = 'INPUT2'
    OUTPUT_RASTER = 'OUTPUT'

    def createInstance(self):  # pylint: disable=missing-function-docstring
        return PCRasterLookupAlgorithm()

    def name(self):  # pylint: disable=missing-function-docstring
        return 'lookup'

    def displayName(self):  # pylint: disable=missing-function-docstring
        return self.tr('lookup')

    def group(self):  # pylint: disable=missing-function-docstring
        return self.tr('PCRaster')

    def groupId(self):  # pylint: disable=missing-function-docstring
        return 'pcraster'

    def shortHelpString(self):  # pylint: disable=missing-function-docstring
        return self.tr(
            """Compares cell value(s) of one or more expression(s) with the search key in a table
            
            <a href="https://pcraster.geo.uu.nl/pcraster/4.3.1/documentation/pcraster_manual/sphinx/op_lookup.html">PCRaster documentation</a>
            
            Parameters:
            
            * <b>Input Raster layer(s)</b> (required) - rasters layer from any data type
            * <b>Input lookup table</b> (required) - lookup table in ASCII text format. Nr of columns is number of input rasters plus one.
            * <b>Output data type</b> (required) - data type of output raster
            * <b>Output raster layer</b> (required) - raster layer with result of the lookup in output data type
            
            """
        )

    def initAlgorithm(self, config=None):  # pylint: disable=missing-function-docstring
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.INPUT_RASTERS,
                self.tr('Input Raster Layer(s)'),
                QgsProcessing.TypeRaster
            )
        )

        self.addParameter(
            QgsProcessingParameterFile(
                self.INPUT_TABLE,
                self.tr('Input lookup table')
            )
        )

        datatypes = [self.tr('Boolean'), self.tr('Nominal'), self.tr('Ordinal'), self.tr('Scalar'),
                     self.tr('Directional'), self.tr('LDD')]
        self.addParameter(
            QgsProcessingParameterEnum(
                self.INPUT_DATATYPE,
                self.tr('Output data type'),
                datatypes,
                defaultValue=0
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.OUTPUT_RASTER,
                self.tr('Output Raster Layer')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):  # pylint: disable=missing-function-docstring
        input_rasters = []
        for layer in self.parameterAsLayerList(parameters, self.INPUT_RASTERS, context):
            input_rasters.append(layer.source())
        input_lookuptable = self.parameterAsFile(parameters, self.INPUT_TABLE, context)
        setclone(input_rasters[0])
        outputFilePath = self.parameterAsOutputLayer(parameters, self.OUTPUT_RASTER, context)

        input_datatype = self.parameterAsEnum(parameters, self.INPUT_DATATYPE, context)
        if input_datatype == 0:
            Result = lookupboolean(input_lookuptable, *input_rasters)
        elif input_datatype == 1:
            Result = lookupnominal(input_lookuptable, *input_rasters)
        elif input_datatype == 2:
            Result = lookupordinal(input_lookuptable, *input_rasters)
        elif input_datatype == 3:
            Result = lookupscalar(input_lookuptable, *input_rasters)
        elif input_datatype == 4:
            Result = lookupdirectional(input_lookuptable, *input_rasters)
        else:
            Result = lookupldd(input_lookuptable, *input_rasters)

        report(Result, outputFilePath)

        return {self.OUTPUT_RASTER: outputFilePath}
