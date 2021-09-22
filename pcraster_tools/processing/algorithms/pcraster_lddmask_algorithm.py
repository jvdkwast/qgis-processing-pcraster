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


class PCRasterLddMaskAlgorithm(PCRasterAlgorithm):
    """
    Local drain direction map cut into a (smaller) sound local drain direction map
    """

    INPUT_LDD = 'INPUT'
    INPUT_MASK = 'INPUT2'
    OUTPUT_RASTER = 'OUTPUT'

    def createInstance(self):  # pylint: disable=missing-function-docstring
        return PCRasterLddMaskAlgorithm()

    def name(self):  # pylint: disable=missing-function-docstring
        return 'lddmask'

    def displayName(self):  # pylint: disable=missing-function-docstring
        return self.tr('lddmask')

    def group(self):  # pylint: disable=missing-function-docstring
        return self.tr('Missing value creation, detection, alteration')

    def groupId(self):  # pylint: disable=missing-function-docstring
        return 'missingvalues'

    def shortHelpString(self):  # pylint: disable=missing-function-docstring
        return self.tr(
            """Local drain direction map cut into a (smaller) sound local drain direction map

            <a href="https://pcraster.geo.uu.nl/pcraster/4.3.1/documentation/pcraster_manual/sphinx/op_lddmask.html">PCRaster documentation</a>

            Parameters:

            * <b>Input flow direction raster</b> (required) - Flow direction raster in PCRaster LDD format (see lddcreate)
            * <b>Input mask raster</b> (required) - Boolean raster
            * <b>Result lddmask layer</b> (required) - Flow direction raster in PCRaster LDD format for TRUE values in mask raster
            """
        )

    def initAlgorithm(self, config=None):  # pylint: disable=missing-function-docstring,unused-argument
        # We add the input DEM.
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_LDD,
                self.tr('LDD layer')
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_MASK,
                self.tr('Mask layer')
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.OUTPUT_RASTER,
                self.tr('Result lddmask layer')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):  # pylint: disable=missing-function-docstring,unused-argument,too-many-locals
        try:
            from pcraster import (   # pylint: disable=import-outside-toplevel
                setclone,
                readmap,
                report,
                lddmask
            )
        except ImportError as e:
            raise QgsProcessingException('PCRaster library is not available') from e

        input_ldd = self.parameterAsRasterLayer(parameters, self.INPUT_LDD, context)
        input_mask = self.parameterAsRasterLayer(parameters, self.INPUT_MASK, context)
        setclone(input_ldd.dataProvider().dataSourceUri())
        LDD = readmap(input_ldd.dataProvider().dataSourceUri())
        Mask = readmap(input_mask.dataProvider().dataSourceUri())
        ResultRaster = lddmask(LDD, Mask)
        outputFilePath = self.parameterAsOutputLayer(parameters, self.OUTPUT_RASTER, context)
        report(ResultRaster, outputFilePath)

        self.set_output_crs(output_file=outputFilePath, crs=input_ldd.crs(), feedback=feedback, context=context)

        return {self.OUTPUT_RASTER: outputFilePath}
