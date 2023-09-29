# -*- coding: utf-8 -*-

"""
***************************************************************************
    provider.py
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

import inspect

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsProcessingProvider)

from pcraster_tools.gui.gui_utils import GuiUtils
from pcraster_tools.processing import algorithms
from pcraster_tools.processing.algorithm import PCRasterAlgorithm


class PCRasterAlgorithmProvider(QgsProcessingProvider):
    """
    Processing provider for executing PCRaster tools
    """

    VERSION = '0.3.0'

    def __init__(self):  # pylint: disable=useless-super-delegation
        super().__init__()

    def load(self):
        """
        Called when first loading provider
        """
        self.refreshAlgorithms()
        return True

    def unload(self):
        """
        Called when unloading provider
        """

    def icon(self):
        """
        Returns the provider's icon
        """
        return GuiUtils.get_icon("pcraster.svg")

    def svgIconPath(self):
        """
        Returns a path to the provider's icon as a SVG file
        """
        return GuiUtils.get_icon_svg("pcraster.svg")

    def name(self):
        """
        Display name for provider
        """
        return self.tr('PCRaster')

    def versionInfo(self):
        """
        Provider plugin version
        """
        return "QGIS PCRaster Provider version {}".format(self.VERSION)

    def id(self):
        """
        Unique ID for provider
        """
        return 'pcraster'

    def loadAlgorithms(self):
        """
        Called when provider must populate its available algorithms
        """

        alg_classes = [m[1] for m in inspect.getmembers(algorithms, inspect.isclass) if
                       issubclass(m[1], PCRasterAlgorithm)]

        for alg_class in alg_classes:
            self.addAlgorithm(alg_class())

    def tr(self, string, context=''):
        """
        Translates a string
        """
        if context == '':
            context = 'PCRasterTools'
        return QCoreApplication.translate(context, string)

    def supportsNonFileBasedOutput(self):
        """
        Provider cannot handle memory layers/db sources
        """
        return False

    def supportedOutputRasterLayerExtensions(self):
        """
        Only the PCRaster format is output
        """
        return ['map']
