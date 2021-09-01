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

from osgeo import gdal, gdalconst
from qgis.core import (QgsProcessingParameterRasterLayer,
                       QgsProcessingParameterEnum,
                       QgsProcessingParameterRasterDestination
                       )

from pcraster_tools.processing.algorithm import PCRasterAlgorithm


class ConvertToPCRasterAlgorithm(PCRasterAlgorithm):
    """
    Converts GDAL supported raster layers to PCRaster format
    """

    INPUT_RASTER = 'INPUT'
    INPUT_DATATYPE = 'INPUT2'
    OUTPUT_PCRASTER = 'OUTPUT'

    def createInstance(self):  # pylint: disable=missing-function-docstring
        return ConvertToPCRasterAlgorithm()

    def name(self):  # pylint: disable=missing-function-docstring
        return 'converttopcrasterformat'

    def displayName(self):  # pylint: disable=missing-function-docstring
        return self.tr('Convert to PCRaster Format')

    def group(self):  # pylint: disable=missing-function-docstring
        return self.tr('PCRaster')

    def groupId(self):  # pylint: disable=missing-function-docstring
        return self.tr('pcraster')

    def shortHelpString(self):  # pylint: disable=missing-function-docstring
        return self.tr("Convert GDAL supported raster layers to PCRaster format with control of the output data type")

    def initAlgorithm(self, config=None):  # pylint: disable=missing-function-docstring,unused-argument
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_RASTER,
                self.tr('Raster layer')
            )
        )

        data_types = [self.tr('Boolean'), self.tr('Nominal'), self.tr('Ordinal'), self.tr('Scalar'),
                      self.tr('Directional'), self.tr('LDD')]
        self.addParameter(
            QgsProcessingParameterEnum(
                self.INPUT_DATATYPE,
                self.tr('Output data type'),
                data_types,
                defaultValue=0
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.OUTPUT_PCRASTER,
                self.tr('PCRaster layer')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):  # pylint: disable=missing-function-docstring,unused-argument
        input_raster = self.parameterAsRasterLayer(parameters, self.INPUT_RASTER, context)
        # print(input_dem.dataProvider().dataSourceUri())

        # Open existing dataset
        src_ds = gdal.Open(input_raster.dataProvider().dataSourceUri())

        # GDAL Translate
        dst_filename = self.parameterAsOutputLayer(parameters, self.OUTPUT_PCRASTER, context)

        input_datatype = self.parameterAsEnum(parameters, self.INPUT_DATATYPE, context)
        if input_datatype == 0:
            gdal.Translate(dst_filename, src_ds, format='PCRaster', outputType=gdalconst.GDT_Byte,
                           metadataOptions="VS_BOOLEAN")
        elif input_datatype == 1:
            gdal.Translate(dst_filename, src_ds, format='PCRaster', outputType=gdalconst.GDT_Int32,
                           metadataOptions="VS_NOMINAL")
        elif input_datatype == 2:
            gdal.Translate(dst_filename, src_ds, format='PCRaster', outputType=gdalconst.GDT_Int32,
                           metadataOptions="VS_ORDINAL")
        elif input_datatype == 3:
            gdal.Translate(dst_filename, src_ds, format='PCRaster', outputType=gdalconst.GDT_Float32,
                           metadataOptions="VS_SCALAR")
        elif input_datatype == 4:
            gdal.Translate(dst_filename, src_ds, format='PCRaster', outputType=gdalconst.GDT_Float32,
                           metadataOptions="VS_DIRECTION")
        else:
            gdal.Translate(dst_filename, src_ds, format='PCRaster', outputType=gdalconst.GDT_Byte,
                           metadataOptions="VS_LDD")

        return {self.OUTPUT_PCRASTER: dst_filename}
