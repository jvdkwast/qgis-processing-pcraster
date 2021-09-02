# -*- coding: utf-8 -*-
"""QGIS PCRaster Tools Plugin

.. note:: This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.
"""

__author__ = '(C) 2021 by Nyall Dawson'
__date__ = '30/08/2021'
__copyright__ = 'Copyright 2021, North Road'
# This will get replaced with a git SHA1 when you do a git archive
__revision__ = '$Format:%H$'

import os

from qgis.PyQt.QtCore import (QTranslator,
                              QCoreApplication)
from qgis.core import (
    QgsApplication,
    Qgis,
    QgsMessageOutput
)
from qgis.gui import QgisInterface
from qgis.PyQt.QtWidgets import QPushButton

from pcraster_tools.processing import PCRasterAlgorithmProvider

VERSION = '0.0.1'


def show_warning(message_bar, short_message, title, long_message, level=Qgis.Warning):
    """
    Shows a warning via the QGIS message bar
    """

    def show_details(_):
        dialog = QgsMessageOutput.createMessageOutput()
        dialog.setTitle(title)
        dialog.setMessage(long_message, QgsMessageOutput.MessageHtml)
        dialog.showMessage()

    message_widget = message_bar.createMessage(PCRasterToolsPlugin.tr('PCRaster Tools Plugin'), short_message)
    details_button = QPushButton("Details")
    details_button.clicked.connect(show_details)
    message_widget.layout().addWidget(details_button)
    return message_bar.pushWidget(message_widget, level, 0)


class PCRasterToolsPlugin:
    """QGIS Plugin Implementation."""

    def __init__(self, iface: QgisInterface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        super().__init__()
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QgsApplication.locale()
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            '{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        self.provider = PCRasterAlgorithmProvider()

    @staticmethod
    def tr(message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('PCRasterTools', message)

    def initGui(self):
        """
        Called when QGIS is ready for the plugin's GUI to be created
        """
        self.initProcessing()

        # Show a warning if PCRaster isn't available
        try:
            import pcraster  # pylint: disable=import-outside-toplevel,unused-import
        except ImportError:
            show_warning(self.iface.messageBar(),
                         self.tr(
                             'PCRaster is not installed -- algorithms will not be available'),
                         self.tr('PCRaster Not Available'),
                         self.tr('PCRaster must be installed and available in the current Python environment before the '
                                 'PCRaster algorithms can be used.\n\n'
                                 'Please see the plugin documentation for further details on how to install PCRaster.'),
                         Qgis.MessageLevel.Critical)

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        QgsApplication.processingRegistry().removeProvider(self.provider)

    def initProcessing(self):
        """Create the Processing provider"""
        QgsApplication.processingRegistry().addProvider(self.provider)
