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

import os

from qgis.core import (QgsProcessingParameterRasterLayer,
                       QgsProcessingParameterEnum,
                       QgsProcessingParameterFile,
                       QgsProcessingParameterRasterDestination
                       )

from pcraster_tools.processing.algorithm import PCRasterAlgorithm


class Col2mapAlgorithm(PCRasterAlgorithm):
    """
    Convert CSV files to PCRaster format with control of the output data type
    """

    INPUT_CSV = 'INPUT'
    INPUT_MASK = 'INPUT1'
    INPUT_DATATYPE = 'INPUT2'
    OUTPUT_PCRASTER = 'OUTPUT'

    def createInstance(self):  # pylint: disable=missing-function-docstring
        return Col2mapAlgorithm()

    def name(self):  # pylint: disable=missing-function-docstring
        return 'col2map'

    def displayName(self):  # pylint: disable=missing-function-docstring
        return self.tr('Column file to PCRaster Map')

    def group(self):  # pylint: disable=missing-function-docstring
        return self.tr('Data management')

    def groupId(self):  # pylint: disable=missing-function-docstring
        return self.tr('data')

    def shortHelpString(self):  # pylint: disable=missing-function-docstring
        return self.tr(
            """
            Convert CSV files to PCRaster format with control of the output data type. The algorithm uses <a href="{}">col2map</a>
            For nominal and ordinal maps you can choose between small and large integers. With small integers you can store values from 0 to 255. Only choose large when you have higher numbers.
            """).format(PCRasterAlgorithm.documentation_url('app_col2map.html'))

    def initAlgorithm(self, config=None):  # pylint: disable=missing-function-docstring,unused-argument
        self.addParameter(
            QgsProcessingParameterFile(
                self.INPUT_CSV,
                self.tr('Input column table text file')
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_MASK,
                self.tr('Raster mask layer')
            )
        )

        datatypes = [self.tr('Boolean'), self.tr('Nominal (small)'), self.tr('Ordinal (small)'), self.tr('Scalar'), self.tr('Directional (degrees)'),
                     self.tr('LDD'), self.tr('Nominal (large)'), self.tr('Ordinal (large)'), self.tr('Directional (radians)')]
        self.addParameter(
            QgsProcessingParameterEnum(
                self.INPUT_DATATYPE,
                self.tr('Output data type'),
                datatypes,
                defaultValue=0
            )
        )

        # We add a feature sink in which to store our processed features (this
        # usually takes the form of a newly created vector layer when the
        # algorithm is run in QGIS).
        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.OUTPUT_PCRASTER,
                self.tr('PCRaster layer')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):  # pylint: disable=missing-function-docstring,unused-argument,too-many-locals
        input_mask = self.parameterAsRasterLayer(parameters, self.INPUT_MASK, context)
        clone = input_mask.dataProvider().dataSourceUri()
        # print(input_dem.dataProvider().dataSourceUri())

        table = self.parameterAsFile(parameters, self.INPUT_CSV, context)

        dst_filename = self.parameterAsOutputLayer(parameters, self.OUTPUT_PCRASTER, context)

        input_datatype = self.parameterAsEnum(parameters, self.INPUT_DATATYPE, context)
        if input_datatype == 0:
            cmd = 'col2map -B "{}" "{}" --clone "{}"'.format(table, dst_filename, clone)
            feedback.pushInfo('Running command {}'.format(cmd))
        elif input_datatype == 1:
            cmd = 'col2map -N "{}" "{}" --clone "{}"'.format(table, dst_filename, clone)
            feedback.pushInfo('Running command {}'.format(cmd))
        elif input_datatype == 2:
            cmd = 'col2map -O "{}" "{}" --clone "{}"'.format(table, dst_filename, clone)
            feedback.pushInfo('Running command {}'.format(cmd))
        elif input_datatype == 3:
            cmd = 'col2map -S "{}" "{}" --clone "{}"'.format(table, dst_filename, clone)
            feedback.pushInfo('Running command {}'.format(cmd))
        elif input_datatype == 4:
            cmd = 'col2map -D "{}" "{}" --clone "{}"'.format(table, dst_filename, clone)
            feedback.pushInfo('Running command {}'.format(cmd))
        elif input_datatype == 5:
            cmd = 'col2map -L "{}" "{}" --clone "{}"'.format(table, dst_filename, clone)
            feedback.pushInfo('Running command {}'.format(cmd))
        elif input_datatype == 6:
            cmd = 'col2map -N --large "{}" "{}" --clone "{}"'.format(table, dst_filename, clone)
            feedback.pushInfo('Running command {}'.format(cmd))
        elif input_datatype == 7:
            cmd = 'col2map -O --large "{}" "{}" --clone "{}"'.format(table, dst_filename, clone)
            feedback.pushInfo('Running command {}'.format(cmd))
        else:
            cmd = 'col2map -D --radians "{}" "{}" --clone "{}"'.format(table, dst_filename, clone)
            feedback.pushInfo('Running command {}'.format(cmd))

        os.system(cmd)

        self.set_output_crs(output_file=dst_filename, crs=input_mask.crs(), feedback=feedback, context=context)

        return {self.OUTPUT_PCRASTER: dst_filename}
