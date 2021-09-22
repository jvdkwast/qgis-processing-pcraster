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


class PCRasterDownstreamdistAlgorithm(PCRasterAlgorithm):
    """
    Distance to the first cell downstream
    """

    INPUT_LDD = 'INPUT'
    INPUT_UNITS = 'INPUT1'
    OUTPUT_DOWNSTREAMDIST = 'OUTPUT'

    def createInstance(self):  # pylint: disable=missing-function-docstring
        return PCRasterDownstreamdistAlgorithm()

    def name(self):  # pylint: disable=missing-function-docstring
        return 'downstreamdist'

    def displayName(self):  # pylint: disable=missing-function-docstring
        return self.tr('downstreamdist')

    def group(self):  # pylint: disable=missing-function-docstring
        return self.tr('Hydrological and material transport operations')

    def groupId(self):  # pylint: disable=missing-function-docstring
        return 'hydrological'

    def shortHelpString(self):  # pylint: disable=missing-function-docstring
        return self.tr(
            """Distance to the first cell downstream

            <a href="https://pcraster.geo.uu.nl/pcraster/4.3.1/documentation/pcraster_manual/sphinx/op_downstreamdist.html">PCRaster documentation</a>

            Parameters:

            * <b>Input flow direction raster</b> (required) - Flow direction raster in PCRaster LDD format (see lddcreate)
            * <b>Units</b> (required) - map units or cells
            * <b>Result downstream distance layer</b> (required) - Scalar raster layer with distance in map units to the first cell downstream
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
            QgsProcessingParameterRasterDestination(
                self.OUTPUT_DOWNSTREAMDIST,
                self.tr('Downstream distance layer')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):  # pylint: disable=missing-function-docstring,unused-argument,too-many-locals
        try:
            from pcraster import (   # pylint: disable=import-outside-toplevel
                setclone,
                readmap,
                report,
                setglobaloption,
                downstreamdist
            )
        except ImportError as e:
            raise QgsProcessingException('PCRaster library is not available') from e

        input_ldd = self.parameterAsRasterLayer(parameters, self.INPUT_LDD, context)
        lengthunits = self.parameterAsEnum(parameters, self.INPUT_UNITS, context)
        if lengthunits == 0:
            setglobaloption("unittrue")
        else:
            setglobaloption("unitcell")
        setclone(input_ldd.dataProvider().dataSourceUri())
        LDD = readmap(input_ldd.dataProvider().dataSourceUri())
        Distance = downstreamdist(LDD)
        outputFilePath = self.parameterAsOutputLayer(parameters, self.OUTPUT_DOWNSTREAMDIST, context)

        report(Distance, outputFilePath)

        self.set_output_crs(output_file=outputFilePath, crs=input_ldd.crs(), feedback=feedback, context=context)

        return {self.OUTPUT_DOWNSTREAMDIST: outputFilePath}
