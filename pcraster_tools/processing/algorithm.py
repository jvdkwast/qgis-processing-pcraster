# -*- coding: utf-8 -*-

"""
***************************************************************************
    algorithm.py
    ---------------------
    Date                 : September 2021
    Copyright            : (C) 2021 by Nyall Dawson
    Email                : nyall dot dawson at gmail dot com
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

from osgeo import gdal, osr

from qgis.PyQt.QtCore import (
    QCoreApplication
)
from qgis.core import (
    QgsProcessingAlgorithm
)

from pcraster_tools.gui.gui_utils import GuiUtils


class PCRasterAlgorithm(QgsProcessingAlgorithm):  # pylint: disable=too-many-public-methods
    """
    Base class for PCRaster Algorithms
    """

    def icon(self):
        """
        Returns the algorithm's icon
        """
        return GuiUtils.get_icon("pcraster.svg")

    def svgIconPath(self):
        """
        Returns a path to the algorithm's icon as a SVG file
        """
        return GuiUtils.get_icon_svg("pcraster.svg")

    def tr(self, string, context=''):
        """
        Translates a string
        """
        if context == '':
            context = 'PCRasterTools'
        return QCoreApplication.translate(context, string)

    @staticmethod
    def documentation_url(path: str) -> str:
        """
        Returns the URL to the PCRaster documentation at path
        """
        return 'https://pcraster.geo.uu.nl/pcraster/latest/documentation/pcraster_manual/sphinx/{}'.format(path)

    @staticmethod
    def set_output_crs(output_file: str, crs, context, feedback) -> bool:
        """
        Sets the projection information for a destination file
        """

        if not crs.isValid():
            return False

        # can't import this on CI -- causes a segfault
        from qgis.core import QgsCoordinateReferenceSystem  # pylint: disable=import-outside-toplevel
        crs_wkt = crs.toWkt(QgsCoordinateReferenceSystem.WKT_PREFERRED_GDAL)
        return PCRasterAlgorithm.set_output_crs_wkt(output_file, crs_wkt, context, feedback)

    @staticmethod
    def set_output_crs_wkt(output_file: str, crs_wkt: str, context, feedback) -> bool:  # pylint: disable=unused-argument
        """
        Sets the projection information for a destination file
        """
        if not crs_wkt:
            return False

        ds = gdal.Open(output_file, gdal.GA_Update)
        assert ds
        sr = osr.SpatialReference()
        res = sr.SetFromUserInput(str(crs_wkt))
        if res and feedback:
            feedback.reportError(QCoreApplication.translate('PCRasterTools', 'Could not create output layer CRS . GDAL result code {}').format(res))
        if res:
            return False

        wkt = sr.ExportToWkt()
        res = ds.SetProjection(wkt)
        if res and feedback:
            feedback.reportError(QCoreApplication.translate('PCRasterTools', 'Could not assign CRS to output layer. GDAL result code {}').format(res))
        if res:
            return False

        return True
