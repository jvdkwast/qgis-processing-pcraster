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

import csv

from osgeo import gdal
from qgis.core import (QgsProcessingParameterRasterLayer,
                       QgsProcessingParameterFileDestination)

from pcraster_tools.processing.algorithm import PCRasterAlgorithm


class LookupTableFromRat(PCRasterAlgorithm):
    """
    Creates a lookup table from the Value and Class columns of the Raster Attribute Table.
    """

    INPUT_RASTER = 'INPUT'
    OUTPUT_TABLE = 'OUTPUT'

    def createInstance(self):  # pylint: disable=missing-function-docstring
        return LookupTableFromRat()

    def name(self):  # pylint: disable=missing-function-docstring
        return 'lookuptablefromrat'

    def displayName(self):  # pylint: disable=missing-function-docstring
        return self.tr('Lookup table from RAT')

    def group(self):  # pylint: disable=missing-function-docstring
        return self.tr('PCRaster')

    def groupId(self):  # pylint: disable=missing-function-docstring
        return 'pcraster'

    def shortHelpString(self):  # pylint: disable=missing-function-docstring
        return self.tr(
            """Creates a lookup table from the Value and Class columns of the Raster Attribute Table.

            Parameters:

            * <b>Input Raster layer</b> (required) - raster layer with RAT
            * <b>Output lookup table</b> (required) - lookup table in ASCII text format.
            """
        )

    def initAlgorithm(self, config=None):  # pylint: disable=missing-function-docstring
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_RASTER,
                self.tr('Raster layer')
            )
        )

        self.addParameter(
            QgsProcessingParameterFileDestination(
                self.OUTPUT_TABLE,
                self.tr('Output Lookup Table'),
                'CSV files (*.csv)',
            )
        )

    @staticmethod
    def to_csv(rat, filepath, table_type):
        """
        Converts a file to CSV
        """
        with open(filepath, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=' ')

            # Write out column headers
            col_count = rat.GetColumnCount()
            cols = []
            skip_cols = ['Count', 'R', 'G', 'B', 'A']
            for col in range(col_count):
                if rat.GetNameOfCol(col) not in skip_cols:
                    cols.append(rat.GetNameOfCol(col))
            # csv_writer.writerow(cols)

            # Write out each row.
            row_count = rat.GetRowCount()

            for row in range(row_count):
                cols = []
                if table_type == 'thematic':
                    for col in range(col_count):
                        if rat.GetNameOfCol(col) not in skip_cols:
                            col_type = rat.GetTypeOfCol(col)
                            if col_type == gdal.GFT_Integer:
                                value = '%s' % rat.GetValueAsInt(row, col)
                            elif col_type == gdal.GFT_Real:
                                value = '%.16g' % rat.GetValueAsDouble(row, col)
                            else:
                                value = '%s' % rat.GetValueAsString(row, col)
                            cols.append(value)
                    csv_writer.writerow(cols)

                if table_type == 'athematic':
                    for col in range(3):
                        if rat.GetNameOfCol(col) not in skip_cols:
                            col_type = rat.GetTypeOfCol(col)
                            if col_type == gdal.GFT_Integer:
                                value = '%s' % rat.GetValueAsInt(row, col)
                            elif col_type == gdal.GFT_Real:
                                # value='%.16g'%rat.GetValueAsDouble(row,col)
                                if col == 0 and row == 0:
                                    value = '[%s' % rat.GetValueAsString(row, col)
                                elif col == 1:
                                    value = '%s]' % rat.GetValueAsString(row, col)
                                else:
                                    value = '<%s' % rat.GetValueAsString(row, col)
                            else:
                                value = '%s' % rat.GetValueAsString(row, col)
                            cols.append(value)
                    cols[0:2] = [','.join(cols[0:2])]
                    csv_writer.writerow(cols)

    def processAlgorithm(self, parameters, context, feedback):  # pylint: disable=missing-function-docstring
        output_lookup_table = self.parameterAsFile(parameters, self.OUTPUT_TABLE, context)
        input_raster = self.parameterAsRasterLayer(parameters, self.INPUT_RASTER, context)
        ds = gdal.Open(input_raster.dataProvider().dataSourceUri())
        rat = ds.GetRasterBand(1).GetDefaultRAT()
        metadata = ds.GetMetadata()
        if metadata['PCRASTER_VALUESCALE'] == 'VS_SCALAR':
            table_type = 'athematic'
        else:
            table_type = 'thematic'

        self.to_csv(rat, output_lookup_table, table_type)

        return {self.OUTPUT_TABLE: output_lookup_table}
