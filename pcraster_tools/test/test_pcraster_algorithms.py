# -*- coding: utf-8 -*-

"""
***************************************************************************
    SagaAlgorithmsTests.py
    ---------------------
    Date                 : September 2017
    Copyright            : (C) 2017 by Alexander Bruy
    Email                : alexander dot bruy at gmail dot com
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

__author__ = 'Alexander Bruy'
__date__ = 'September 2017'
__copyright__ = '(C) 2017, Alexander Bruy'

import os
import shutil
import tempfile

import nose2
from qgis.core import (QgsApplication)
from qgis.testing import unittest

from pcraster_tools.processing import PCRasterAlgorithmProvider
from pcraster_tools.test import AlgorithmsTestBase


class TestPCRasterAlgorithms(unittest.TestCase, AlgorithmsTestBase.AlgorithmsTest):
    """
    Test running some PCRaster algorithms
    """

    @classmethod
    def setUpClass(cls):  # pylint:disable=missing-function-docstring
        cls.provider = PCRasterAlgorithmProvider()
        QgsApplication.processingRegistry().addProvider(cls.provider)
        cls.cleanup_paths = []

        cls.temp_dir = tempfile.mkdtemp()
        cls.cleanup_paths.append(cls.temp_dir)

        os.environ["IS_TEST_RUN"] = "1"

    @classmethod
    def tearDownClass(cls):  # pylint:disable=missing-function-docstring
        QgsApplication.processingRegistry().removeProvider(cls.provider)
        for path in cls.cleanup_paths:
            shutil.rmtree(path)

    def get_definition_file(self):
        return 'pcraster_algorithm_tests.yaml'


if __name__ == '__main__':
    nose2.main()
