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


class PCRasterAreaareaAlgorithm(PCRasterAlgorithm):
    """
    The area of the area to which a cell belongs
    """

    INPUT_DISCRETE = 'INPUT'
    INPUT_UNITS = 'INPUT1'
    OUTPUT_AREA = 'OUTPUT'

    def createInstance(self):  # pylint: disable=missing-function-docstring
        return PCRasterAreaareaAlgorithm()

    def name(self):  # pylint: disable=missing-function-docstring
        return 'areaarea'

    def displayName(self):  # pylint: disable=missing-function-docstring
        return self.tr('areaarea')

    def group(self):  # pylint: disable=missing-function-docstring
        return self.tr('Area operations')

    def groupId(self):  # pylint: disable=missing-function-docstring
        return 'area'

    def shortHelpString(self):  # pylint: disable=missing-function-docstring
        return self.tr(
            """The area of the area to which a cell belongs

            <a href="{}">PCRaster documentation</a>

            Parameters:

            * <b>Input class raster layer</b> (required) - boolean, nominal or ordinal raster layer
            * <b>Units</b> (required) - map units or cells
            * <b>Output area raster</b> (required) - Scalar raster with true area (map units)
            """
        ).format(PCRasterAlgorithm.documentation_url('op_areaarea.html'))

    def initAlgorithm(self, config=None):  # pylint: disable=missing-function-docstring,unused-argument
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_DISCRETE,
                self.tr('Class raster layer')
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
                self.OUTPUT_AREA,
                self.tr('Output area layer')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):  # pylint: disable=missing-function-docstring,unused-argument,too-many-locals
        try:
            from pcraster import (   # pylint: disable=import-outside-toplevel
                setglobaloption,
                setclone,
                readmap,
                areaarea,
                report
            )
        except ImportError as e:
            raise QgsProcessingException('PCRaster library is not available') from e

        input_discrete = self.parameterAsRasterLayer(parameters, self.INPUT_DISCRETE, context)
        lengthunits = self.parameterAsEnum(parameters, self.INPUT_UNITS, context)
        if lengthunits == 0:
            setglobaloption("unittrue")
        else:
            setglobaloption("unitcell")
        setclone(input_discrete.dataProvider().dataSourceUri())
        ClassLayer = readmap(input_discrete.dataProvider().dataSourceUri())
        AreaLayer = areaarea(ClassLayer)
        outputFilePath = self.parameterAsOutputLayer(parameters, self.OUTPUT_AREA, context)

        report(AreaLayer, outputFilePath)

        self.set_output_crs(output_file=outputFilePath, crs=input_discrete.crs(), feedback=feedback, context=context)

        return {self.OUTPUT_AREA: outputFilePath}
