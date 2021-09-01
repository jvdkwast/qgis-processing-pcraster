# coding=utf-8
"""GUI Utils Test.

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""

__author__ = '(C) 2021 by Nyall Dawson'
__date__ = '01/09/2021'
__copyright__ = 'Copyright 2021, North Road'
# This will get replaced with a git SHA1 when you do a git archive
__revision__ = '$Format:%H$'

import unittest

from qgis.core import QgsApplication

from pcraster_tools.processing import PCRasterAlgorithmProvider
from pcraster_tools.pcraster_plugin import PCRasterToolsPlugin

from .utilities import get_qgis_app

QGIS_APP = get_qgis_app()


class PCRasterProviderTest(unittest.TestCase):
    """Test PCRasterAlgorithmProvider work."""

    def test_create(self):
        """
        Test that provider can be created
        """
        provider = PCRasterAlgorithmProvider()
        self.assertIsNotNone(provider)

        # make sure provider has some algorithms
        provider.loadAlgorithms()
        algorithm_ids = [a.id() for a in provider.algorithms()]
        self.assertIn('pcraster:col2map', algorithm_ids)
        self.assertIn('pcraster:downstream', algorithm_ids)
        self.assertIn('pcraster:ifthenelse', algorithm_ids)

    def test_create_on_load_plugin(self):
        """
        Test that provider is created on plugin load
        """
        p = PCRasterToolsPlugin(iface=None)
        self.assertIsNone(QgsApplication.processingRegistry().providerById('pcraster'))

        p.initProcessing()
        self.assertIsNotNone(QgsApplication.processingRegistry().providerById('pcraster'))

        # provider should be unloaded with plugin
        p.unload()
        self.assertIsNone(QgsApplication.processingRegistry().providerById('pcraster'))

        p = PCRasterToolsPlugin(iface=None)
        # initGui must also init provider for compatibility with older QGIS versions
        p.initGui()
        self.assertIsNotNone(QgsApplication.processingRegistry().providerById('pcraster'))
        p.unload()
        self.assertIsNone(QgsApplication.processingRegistry().providerById('pcraster'))


if __name__ == "__main__":
    suite = unittest.makeSuite(PCRasterProviderTest)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
