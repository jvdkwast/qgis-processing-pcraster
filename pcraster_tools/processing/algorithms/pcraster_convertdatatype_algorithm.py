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
                       QgsProcessingParameterEnum,
                       QgsProcessingParameterRasterLayer,
                       QgsProcessingException)

from pcraster_tools.processing.algorithm import PCRasterAlgorithm


class PCRasterConvertdatatypeAlgorithm(PCRasterAlgorithm):
    """
    Conversion of the layer data type
    """

    INPUT_RASTER = 'INPUT'
    INPUT_DATATYPE = 'INPUT1'
    OUTPUT_RASTER = 'OUTPUT'

    def createInstance(self):  # pylint: disable=missing-function-docstring
        return PCRasterConvertdatatypeAlgorithm()

    def name(self):  # pylint: disable=missing-function-docstring
        return 'convertdatatype'

    def displayName(self):  # pylint: disable=missing-function-docstring
        return self.tr('convert layer data type')

    def group(self):  # pylint: disable=missing-function-docstring
        return self.tr('Data management')

    def groupId(self):  # pylint: disable=missing-function-docstring
        return self.tr('data')

    def shortHelpString(self):  # pylint: disable=missing-function-docstring
        return self.tr(
            """
            Conversion of the layer data type.<a href=https://pcraster.geo.uu.nl/pcraster/4.3.1/documentation/pcraster_manual/sphinx/secfunclist.html#data-types-conversion-and-assignment>PCRaster documentation</a>
            """
        )

    def initAlgorithm(self, config=None):  # pylint: disable=missing-function-docstring,unused-argument
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_RASTER,
                self.tr('Input raster layer')
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
                self.tr("Output raster layer")
            )
        )

    def processAlgorithm(self, parameters, context, feedback):  # pylint: disable=missing-function-docstring,unused-argument,too-many-locals
        try:
            from pcraster import (   # pylint: disable=import-outside-toplevel
                readmap,
                report,
                boolean,
                ordinal,
                scalar,
                directional,
                nominal,
                ldd
            )
        except ImportError as e:
            raise QgsProcessingException('PCRaster library is not available') from e

        input_raster = self.parameterAsRasterLayer(parameters, self.INPUT_RASTER, context)
        InputRaster = readmap(input_raster.dataProvider().dataSourceUri())
        # setclone(input_raster.dataProvider().dataSourceUri())
        input_datatype = self.parameterAsEnum(parameters, self.INPUT_DATATYPE, context)
        if input_datatype == 0:
            ConversionResult = boolean(InputRaster)
        elif input_datatype == 1:
            ConversionResult = nominal(InputRaster)
        elif input_datatype == 2:
            ConversionResult = ordinal(InputRaster)
        elif input_datatype == 3:
            ConversionResult = scalar(InputRaster)
        elif input_datatype == 4:
            ConversionResult = directional(InputRaster)
        else:
            ConversionResult = ldd(InputRaster)

        outputFilePath = self.parameterAsOutputLayer(parameters, self.OUTPUT_RASTER, context)

        report(ConversionResult, outputFilePath)

        return {self.OUTPUT_RASTER: outputFilePath}
