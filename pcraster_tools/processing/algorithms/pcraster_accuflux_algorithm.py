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


class PCRasterAccuFluxAlgorithm(PCRasterAlgorithm):
    """
    Accumulated material flowing into downstream cell
    """

    INPUT_LDD = 'INPUT'
    INPUT_MATERIAL = 'INPUT2'
    OUTPUT_ACCUFLUX = 'OUTPUT'

    def createInstance(self):  # pylint: disable=missing-function-docstring
        return PCRasterAccuFluxAlgorithm()

    def name(self):  # pylint: disable=missing-function-docstring
        return 'accuflux'

    def displayName(self):  # pylint: disable=missing-function-docstring
        return self.tr('accuflux')

    def group(self):  # pylint: disable=missing-function-docstring
        return self.tr('Hydrological and material transport operations')

    def groupId(self):  # pylint: disable=missing-function-docstring
        return 'hydrological'

    def shortHelpString(self):  # pylint: disable=missing-function-docstring
        return self.tr(
            """Accumulated material flowing into downstream cell

            <a href="{}">PCRaster documentation</a>

            Parameters:

            * <b>Input flow direction raster</b> (required) - Flow direction raster in PCRaster LDD format (see lddcreate)
            * <b>Input material raster</b> (required) - Scalar raster with material (>= 0)
            * <b>Result flux layer</b> (required) - Scalar raster with accumulated amount of material
            """
        ).format(PCRasterAlgorithm.documentation_url('op_accuflux.html'))

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
                self.INPUT_MATERIAL,
                self.tr('Material layer')
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.OUTPUT_ACCUFLUX,
                self.tr('Result flux layer')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):  # pylint: disable=missing-function-docstring,unused-argument,too-many-locals
        try:
            from pcraster import (   # pylint: disable=import-outside-toplevel
                setclone,
                readmap,
                accuflux,
                report
            )
        except ImportError as e:
            raise QgsProcessingException('PCRaster library is not available') from e

        input_ldd = self.parameterAsRasterLayer(parameters, self.INPUT_LDD, context)
        input_material = self.parameterAsRasterLayer(parameters, self.INPUT_MATERIAL, context)
        setclone(input_ldd.dataProvider().dataSourceUri())
        ldd = readmap(input_ldd.dataProvider().dataSourceUri())
        material = readmap(input_material.dataProvider().dataSourceUri())
        result_flux = accuflux(ldd, material)
        output_file_path = self.parameterAsOutputLayer(parameters, self.OUTPUT_ACCUFLUX, context)
        report(result_flux, output_file_path)

        self.set_output_crs(output_file=output_file_path, crs=input_ldd.crs(), feedback=feedback, context=context)

        return {self.OUTPUT_ACCUFLUX: output_file_path}
