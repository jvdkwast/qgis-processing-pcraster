# coding=utf-8
"""Tests for PCRaster availability

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""
__author__ = 'Nyall Dawson'
__date__ = '31/07/2021'
__copyright__ = 'Copyright 2021, North Road Consulting'

import unittest


class PCRasterTest(unittest.TestCase):
    """Test the PCRaster Environment"""

    def test_pcraster_environment(self):
        """
        Test that pcraster is available
        """
        import pcraster  # pylint: disable=import-outside-toplevel,unused-import


if __name__ == '__main__':
    unittest.main()
