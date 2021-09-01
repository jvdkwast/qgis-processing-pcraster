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

from pcraster import *
from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsProcessingAlgorithm,
                       QgsProcessingParameterRasterDestination,
                       QgsProcessingParameterRasterLayer,
                       QgsProcessingParameterEnum)


class PCRasterSpreadlddAlgorithm(QgsProcessingAlgorithm):
    """
    This is an example algorithm that takes a vector layer and
    creates a new identical one.

    It is meant to be used as an example of how to create your own
    algorithms and explain methods and variables used to do it. An
    algorithm like this will be available in all elements, and there
    is not need for additional work.

    All Processing algorithms should extend the QgsProcessingAlgorithm
    class.
    """

    # Constants used to refer to parameters and outputs. They will be
    # used when calling the algorithm from another algorithm, or when
    # calling from the QGIS console.

    INPUT_LDD = 'INPUT'
    INPUT_POINTS = 'INPUT1'
    INPUT_UNITS = 'INPUT4'
    INPUT_INITIALFRICTION = 'INPUT2'
    INPUT_FRICTION = 'INPUT3'
    OUTPUT_SPREAD = 'OUTPUT'

    def tr(self, string):
        """
        Returns a translatable string with the self.tr() function.
        """
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return PCRasterSpreadlddAlgorithm()

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'spreadldd'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('spreadldd')

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr('PCRaster')

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'pcraster'

    def shortHelpString(self):
        """
        Returns a localised short helper string for the algorithm. This string
        should provide a basic description about what the algorithm does and the
        parameters and outputs associated with it..
        """
        return self.tr(
            """Total friction of the shortest accumulated friction downstream path over map with friction values from an source cell to cell under consideration
            
            <a href="https://pcraster.geo.uu.nl/pcraster/4.3.1/documentation/pcraster_manual/sphinx/op_spreadldd.html">PCRaster documentation</a>
            
            Parameters:
            
            * <b>LDD raster</b> (required) - Raster with local drain direction with LDD data type
            * <b>Points raster</b> (required) - boolean, nominal or ordinal raster layer with cells from which the shortest accumulated friction path to every cell centre is calculated
            * <b>Units</b> (required) - map units or cells
            * <b>Initial friction layer</b> (required) - initial friction at start of spreading, scalar data type
            * <b>Friction raster layer</b> (required) - The amount of increase in friction per unit distance, scalar data type
            * <b>Result spread ldd layer</b> (required) - Scalar raster with total friction of the shortest accumulated friction downstream path over map with friction values from an source cell to cell under consideration in map units, scalar data type
            """
        )

    def initAlgorithm(self, config=None):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_LDD,
                self.tr('Local drain direction raster')
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_POINTS,
                self.tr('Points raster')
            )
        )

        self.unitoption = [self.tr('Map units'), self.tr('Cells')]
        self.addParameter(
            QgsProcessingParameterEnum(
                self.INPUT_UNITS,
                self.tr('Distance units'),
                self.unitoption,
                defaultValue=0
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_INITIALFRICTION,
                self.tr('Initial friction layer'),
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_FRICTION,
                self.tr('Friction layer')
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.OUTPUT_SPREAD,
                self.tr('Output spread ldd result')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """

        input_ldd = self.parameterAsRasterLayer(parameters, self.INPUT_LDD, context)
        input_points = self.parameterAsRasterLayer(parameters, self.INPUT_POINTS, context)
        lengthunits = self.parameterAsEnum(parameters, self.INPUT_UNITS, context)
        if lengthunits == 0:
            setglobaloption("unittrue")
        else:
            setglobaloption("unitcell")
        input_initial = self.parameterAsRasterLayer(parameters, self.INPUT_INITIALFRICTION, context)
        input_friction = self.parameterAsRasterLayer(parameters, self.INPUT_FRICTION, context)
        output_spread = self.parameterAsRasterLayer(parameters, self.OUTPUT_SPREAD, context)
        setclone(input_ldd.dataProvider().dataSourceUri())
        LDD = readmap(input_ldd.dataProvider().dataSourceUri())
        PointsLayer = readmap(input_points.dataProvider().dataSourceUri())
        InitialFriction = readmap(input_initial.dataProvider().dataSourceUri())
        Friction = readmap(input_friction.dataProvider().dataSourceUri())
        SpreadLayer = spreadldd(LDD, PointsLayer, InitialFriction, Friction)
        outputFilePath = self.parameterAsOutputLayer(parameters, self.OUTPUT_SPREAD, context)
        report(SpreadLayer, outputFilePath)

        results = {}
        results[self.OUTPUT_SPREAD] = outputFilePath

        return results
