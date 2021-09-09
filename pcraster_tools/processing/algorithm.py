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

import os

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
    def set_output_crs(output_file: str, crs, context, feedback):
        """
        Sets the projection information for a destination file
        """
        if not crs.isValid():
            return

        # we can't run this on CI!
        if not os.environ.get('IS_TEST_RUN'):
            import processing  # pylint: disable=import-outside-toplevel
            processing.run("gdal:assignprojection",
                           {'INPUT': output_file,
                            'CRS': crs},
                           context=context,
                           feedback=feedback,
                           is_child_algorithm=True)
