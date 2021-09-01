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
                       QgsProcessingParameterNumber,
                       QgsProcessingParameterRasterLayer,
                       QgsProcessingException)

from pcraster_tools.processing.algorithm import PCRasterAlgorithm


class PCRasterSpatialAlgorithm(PCRasterAlgorithm):
    """
    Conversion of a non-spatial value to a spatial data type.
    """

    INPUT_NONSPATIAL = 'INPUT'
    INPUT_DATATYPE = 'INPUT1'
    INPUT_CLONE = 'INPUT2'
    OUTPUT_RASTER = 'OUTPUT'

    def createInstance(self):  # pylint: disable=missing-function-docstring
        return PCRasterSpatialAlgorithm()

    def name(self):  # pylint: disable=missing-function-docstring
        return 'spatial'

    def displayName(self):  # pylint: disable=missing-function-docstring
        return self.tr('spatial')

    def group(self):  # pylint: disable=missing-function-docstring
        return self.tr('Data management')

    def groupId(self):  # pylint: disable=missing-function-docstring
        return self.tr('data')

    def shortHelpString(self):  # pylint: disable=missing-function-docstring
        return self.tr(
            """Conversion of a non-spatial value to a spatial data type.

            <a href="https://pcraster.geo.uu.nl/pcraster/4.3.1/documentation/pcraster_manual/sphinx/op_spatial.html">PCRaster documentation</a>

            Parameters:

            * <b>Input nonspatial</b> (required) - value to be assigned to cells in mask layer
            * <b>Output data type</b> (required) - data type of output raster
            * <b>Mask layer</b> - value of input nonspatial will be assigned to all values in mask layer (any data type)
            * <b>Output raster</b> (required) - raster with result in chosen data type
            """
        )

    def initAlgorithm(self, config=None):  # pylint: disable=missing-function-docstring,unused-argument
        self.addParameter(
            QgsProcessingParameterNumber(
                self.INPUT_NONSPATIAL,
                self.tr('Input nonspatial'),
                type=QgsProcessingParameterNumber.Double
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
            QgsProcessingParameterRasterLayer(
                self.INPUT_CLONE,
                self.tr('Mask layer')
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
                setclone,
                report,
                spatial,
                boolean,
                nominal,
                ordinal,
                scalar,
                directional,
                ldd
            )
        except ImportError as e:
            raise QgsProcessingException('PCRaster library is not available') from e

        input_nonspatial = self.parameterAsDouble(parameters, self.INPUT_NONSPATIAL, context)
        input_clone = self.parameterAsRasterLayer(parameters, self.INPUT_CLONE, context)
        setclone(input_clone.dataProvider().dataSourceUri())
        input_datatype = self.parameterAsEnum(parameters, self.INPUT_DATATYPE, context)
        if input_datatype == 0:
            SpatialResult = spatial(boolean(input_nonspatial))
        elif input_datatype == 1:
            SpatialResult = spatial(nominal(input_nonspatial))
        elif input_datatype == 2:
            SpatialResult = spatial(ordinal(input_nonspatial))
        elif input_datatype == 3:
            SpatialResult = spatial(scalar(input_nonspatial))
        elif input_datatype == 4:
            SpatialResult = spatial(directional(input_nonspatial))
        elif input_datatype == 5:
            SpatialResult = spatial(ldd(input_nonspatial))
        else:
            print("no choice")
        print(input_datatype)
        outputFilePath = self.parameterAsOutputLayer(parameters, self.OUTPUT_RASTER, context)

        report(SpatialResult, outputFilePath)

        return {self.OUTPUT_RASTER: outputFilePath}
