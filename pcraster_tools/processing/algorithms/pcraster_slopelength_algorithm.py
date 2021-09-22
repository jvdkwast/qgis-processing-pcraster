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


class PCRasterSlopelengthAlgorithm(PCRasterAlgorithm):
    """
    Accumulative-friction-distance of the longest accumulative-friction-path upstream over the local drain direction network cells against waterbasin divides
    """

    INPUT_LDD = 'INPUT'
    INPUT_UNITS = 'INPUT1'
    INPUT_FRICTION = 'INPUT2'
    OUTPUT_RASTER = 'OUTPUT'

    def createInstance(self):  # pylint: disable=missing-function-docstring
        return PCRasterSlopelengthAlgorithm()

    def name(self):  # pylint: disable=missing-function-docstring
        return 'slopelength'

    def displayName(self):  # pylint: disable=missing-function-docstring
        return self.tr('slopelength')

    def group(self):  # pylint: disable=missing-function-docstring
        return self.tr('Hydrological and material transport operations')

    def groupId(self):  # pylint: disable=missing-function-docstring
        return 'hydrological'

    def shortHelpString(self):  # pylint: disable=missing-function-docstring
        return self.tr(
            """Accumulative-friction-distance of the longest accumulative-friction-path upstream over the local drain direction network cells against waterbasin divides

            <a href="https://pcraster.geo.uu.nl/pcraster/4.3.1/documentation/pcraster_manual/sphinx/op_slopelength.html">PCRaster documentation</a>

            Parameters:

            * <b>Input Local Drain Direction raster</b> (required) - LDD raster
            * <b>Units</b> (required) - map units or cells
            * <b>Friction raster layer</b> (required) - The amount of increase in friction per unit distance, scalar data type
            * <b>Result slope length layer</b> (required) - Scalar raster with accumulative-friction-distance of the longest accumulative-friction-path upstream over the local drain direction network cells against waterbasin divides
            """
        )

    def initAlgorithm(self, config=None):  # pylint: disable=missing-function-docstring,unused-argument
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_LDD,
                self.tr('LDD layer')
            )
        )

        unitoption = [self.tr('Map units'), self.tr('Cells')]
        self.addParameter(
            QgsProcessingParameterEnum(
                self.INPUT_UNITS,
                self.tr('Units'),
                unitoption,
                defaultValue=0
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_FRICTION,
                self.tr('Friction layer')
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.OUTPUT_RASTER,
                self.tr('Result slope length layer')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):  # pylint: disable=missing-function-docstring,unused-argument,too-many-locals
        try:
            from pcraster import (   # pylint: disable=import-outside-toplevel
                setclone,
                readmap,
                report,
                slopelength,
                setglobaloption
            )
        except ImportError as e:
            raise QgsProcessingException('PCRaster library is not available') from e

        input_ldd = self.parameterAsRasterLayer(parameters, self.INPUT_LDD, context)
        lengthunits = self.parameterAsEnum(parameters, self.INPUT_UNITS, context)
        if lengthunits == 0:
            setglobaloption("unittrue")
        else:
            setglobaloption("unitcell")
        input_friction = self.parameterAsRasterLayer(parameters, self.INPUT_FRICTION, context)
        setclone(input_ldd.dataProvider().dataSourceUri())
        LDD = readmap(input_ldd.dataProvider().dataSourceUri())
        Friction = readmap(input_friction.dataProvider().dataSourceUri())
        resultRaster = slopelength(LDD, Friction)
        outputFilePath = self.parameterAsOutputLayer(parameters, self.OUTPUT_RASTER, context)
        report(resultRaster, outputFilePath)

        self.set_output_crs(output_file=outputFilePath, crs=input_ldd.crs(), feedback=feedback, context=context)

        return {self.OUTPUT_RASTER: outputFilePath}
