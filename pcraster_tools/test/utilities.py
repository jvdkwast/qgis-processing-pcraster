# coding=utf-8
"""Common functionality used by regression tests."""

import sys
import logging
import os
import atexit

from qgis.core import QgsApplication

LOGGER = logging.getLogger('QGIS')
QGIS_APP = None  # Static variable used to hold hand to running QGIS app
CANVAS = None
PARENT = None
IFACE = None


def get_qgis_app(cleanup=True):
    """ Start one QGIS application to test against.

    :returns: Handle to QGIS app, canvas, iface and parent. If there are any
        errors the tuple members will be returned as None.
    :rtype: (QgsApplication, CANVAS, IFACE, PARENT)

    If QGIS is already running the handle to that app will be returned.
    """

    global QGIS_APP  # pylint: disable=W0603

    global QGISAPP  # pylint: disable=global-variable-undefined

    try:
        QGISAPP
    except NameError:
        myGuiFlag = True  # All test will run qgis in gui mode

        # In python3 we need to convert to a bytes object (or should
        # QgsApplication accept a QString instead of const char* ?)
        try:
            argvb = list(map(os.fsencode, sys.argv))
        except AttributeError:
            argvb = sys.argv

        # Note: QGIS_PREFIX_PATH is evaluated in QgsApplication -
        # no need to mess with it here.
        QGISAPP = QgsApplication(argvb, myGuiFlag)

        QGISAPP.initQgis()
        s = QGISAPP.showSettings()
        LOGGER.debug(s)

        def debug_log_message(message, tag, level):
            """
            Prints a debug message to a log
            :param message: message to print
            :param tag: log tag
            :param level: log message level (severity)
            :return:
            """
            print('{}({}): {}'.format(tag, level, message))

        QgsApplication.instance().messageLog().messageReceived.connect(
            debug_log_message)

        if cleanup:
            @atexit.register
            def exitQgis():  # pylint: disable=unused-variable
                """
                Gracefully closes the QgsApplication instance
                """
                try:
                    QGISAPP.exitQgis()  # pylint: disable=used-before-assignment
                    QGISAPP = None  # pylint: disable=redefined-outer-name
                except NameError:
                    pass

    return QGISAPP
