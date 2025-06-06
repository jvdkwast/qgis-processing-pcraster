# -*- coding: utf-8 -*-

"""
***************************************************************************
    AlgorithmsTest.py
    ---------------------
    Date                 : January 2016
    Copyright            : (C) 2016 by Matthias Kuhn
    Email                : matthias@opengis.ch
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

__author__ = 'Matthias Kuhn'
__date__ = 'January 2016'
__copyright__ = '(C) 2016, Matthias Kuhn'

import glob
import hashlib
import os
import re
import shutil
import tempfile
from copy import deepcopy

import nose2
import yaml
from numpy import nan_to_num
from osgeo import gdal
from osgeo.gdalconst import GA_ReadOnly
from qgis.core import (QgsVectorLayer,
                       QgsRasterLayer,
                       QgsCoordinateReferenceSystem,
                       QgsFeatureRequest,
                       QgsMapLayer,
                       QgsProject,
                       QgsApplication,
                       QgsProcessingContext,
                       QgsProcessingUtils,
                       QgsProcessingFeedback)
from qgis.testing import (_UnexpectedSuccess)


def processingTestDataPath():
    """
    Returns the path to the test data
    """
    return os.path.join(os.path.dirname(__file__), 'testdata')


class AlgorithmsTest:  # pylint: disable=no-member,missing-function-docstring
    """
    Tests execution of algorithms
    """

    def __init__(self):
        self.vector_layer_params = {}

    def get_definition_file(self):
        """
        Returns the path to the test definition file
        """
        return ''

    def test_algorithms(self):
        """
        This is the main test function. All others will be executed based on the definitions in testdata/algorithm_tests.yaml
        """
        with open(os.path.join(processingTestDataPath(), self.get_definition_file()), 'r', encoding='utf8') as stream:
            algorithm_tests = yaml.load(stream, Loader=yaml.SafeLoader)

        test_data = algorithm_tests['tests']
        for idx, algtest in enumerate(test_data):
            print('About to start {} of {}: "{}"'.format(idx, len(algorithm_tests['tests']), algtest['name']))

            with self.subTest(msg=algtest['name']):
                self.check_algorithm(algtest['name'], algtest)

    def check_algorithm(self, name,  # pylint:disable=too-many-locals,unused-argument,too-many-branches,too-many-statements
                        defs):
        """
        Will run an algorithm definition and check if it generates the expected result
        :param name: The identifier name used in the test output heading
        :param defs: A python dict containing a test algorithm definition
        """
        self.vector_layer_params = {}
        QgsProject.instance().clear()

        if 'project' in defs:
            full_project_path = os.path.join(processingTestDataPath(), defs['project'])
            project_read_success = QgsProject.instance().read(full_project_path)
            self.assertTrue(project_read_success, 'Failed to load project file: ' + defs['project'])

        if 'project_crs' in defs:
            QgsProject.instance().setCrs(QgsCoordinateReferenceSystem(defs['project_crs']))
        else:
            QgsProject.instance().setCrs(QgsCoordinateReferenceSystem())

        if 'ellipsoid' in defs:
            QgsProject.instance().setEllipsoid(defs['ellipsoid'])
        else:
            QgsProject.instance().setEllipsoid('')

        params = self.load_params(defs['params'])

        print('Running alg: "{}"'.format(defs['algorithm']))
        alg = QgsApplication.processingRegistry().createAlgorithmById(defs['algorithm'])

        parameters = {}
        if isinstance(params, list):
            for param in zip(alg.parameterDefinitions(), params):
                parameters[param[0].name()] = param[1]
        else:
            for k, p in params.items():
                parameters[k] = p

        for r, p in list(defs['results'].items()):
            if 'in_place_result' not in p or not p['in_place_result']:
                parameters[r] = self.load_result_param(p)

        expectFailure = False
        if 'expectedFailure' in defs:
            exec(('\n'.join(defs['expectedFailure'][:-1])), globals(), locals())  # pylint:disable=exec-used
            expectFailure = eval(defs['expectedFailure'][-1])  # pylint:disable=eval-used

        if 'expectedException' in defs:
            expectFailure = True

        # ignore user setting for invalid geometry handling
        context = QgsProcessingContext()
        context.setProject(QgsProject.instance())

        if 'skipInvalid' in defs and defs['skipInvalid']:
            context.setInvalidGeometryCheck(QgsFeatureRequest.GeometrySkipInvalid)

        feedback = QgsProcessingFeedback()

        print('Algorithm parameters are {}'.format(parameters))

        # first check that algorithm accepts the parameters we pass...
        ok, msg = alg.checkParameterValues(parameters, context)
        self.assertTrue(ok, 'Algorithm failed checkParameterValues with result {}'.format(msg))

        if expectFailure:
            try:
                results, ok = alg.run(parameters, context, feedback)
                self.check_results(results, context, parameters, defs['results'])
                if ok:
                    raise _UnexpectedSuccess
            except Exception:  # pylint:disable=broad-except
                pass
        else:
            results, ok = alg.run(parameters, context, feedback)
            self.assertTrue(ok, 'params: {}, results: {}'.format(parameters, results))
            self.check_results(results, context, parameters, defs['results'])

    def load_params(self, params):
        """
        Loads an array of parameters
        """
        if isinstance(params, list):
            return [self.load_param(p) for p in params]
        if isinstance(params, dict):
            return {key: self.load_param(p, key) for key, p in params.items()}

        return params

    def load_param(self, param, param_id=None):
        """
        Loads a parameter. If it's not a map, the parameter will be returned as-is. If it is a map, it will process the
        parameter based on its key `type` and return the appropriate parameter to pass to the algorithm.
        """
        try:
            if param['type'] in ('vector', 'raster', 'table'):
                return self.load_layer(param_id, param).id()
            if param['type'] == 'vrtlayers':
                vals = []
                for p in param['params']:
                    p['layer'] = self.load_layer(None, {'type': 'vector', 'name': p['layer']})
                    vals.append(p)
                return vals
            if param['type'] == 'multi':
                return [self.load_param(p) for p in param['params']]
            if param['type'] == 'file':
                return self.filepath_from_param(param)
            if param['type'] == 'interpolation':
                prefix = processingTestDataPath()
                tmp = ''
                for r in param['name'].split('::|::'):
                    v = r.split('::~::')
                    tmp += '{}::~::{}::~::{}::~::{};'.format(os.path.join(prefix, v[0]),
                                                             v[1], v[2], v[3])
                return tmp[:-1]
        except TypeError:
            # No type specified, use whatever is there
            return param

        raise KeyError("Unknown type '{}' specified for parameter".format(param['type']))

    def load_result_param(self, param):
        """
        Loads a result parameter. Creates a temporary destination where the result should go to and returns this location
        so it can be sent to the algorithm as parameter.
        """
        if param['type'] in ['vector', 'file', 'table', 'regex']:
            outdir = tempfile.mkdtemp()
            self.cleanup_paths.append(outdir)
            if isinstance(param['name'], str):
                basename = os.path.basename(param['name'])
            else:
                basename = os.path.basename(param['name'][0])

            filepath = self.uri_path_join(outdir, basename)
            return filepath
        if param['type'] == 'rasterhash':
            outdir = tempfile.mkdtemp()
            self.cleanup_paths.append(outdir)
            if self.get_definition_file().lower().startswith('saga'):
                basename = 'raster.sdat'
            else:
                basename = 'raster.tif'
            filepath = os.path.join(outdir, basename)
            return filepath
        if param['type'] == 'directory':
            outdir = tempfile.mkdtemp()
            return outdir

        raise KeyError("Unknown type '{}' specified for parameter".format(param['type']))

    def load_layers(self, param_id, param):
        layers = []
        if param['type'] in ('vector', 'table'):
            if isinstance(param['name'], str) or 'uri' in param:
                layers.append(self.load_layer(param_id, param))
            else:
                for n in param['name']:
                    layer_param = deepcopy(param)
                    layer_param['name'] = n
                    layers.append(self.load_layer(param_id, layer_param))
        else:
            layers.append(self.load_layer(param_id, param))
        return layers

    def load_layer(self, param_id, param):
        """
        Loads a layer which was specified as parameter.
        """

        filepath = self.filepath_from_param(param)

        if 'in_place' in param and param['in_place']:
            # check if alg modifies layer in place
            tmpdir = tempfile.mkdtemp()
            self.cleanup_paths.append(tmpdir)
            path, file_name = os.path.split(filepath)
            base, _ = os.path.splitext(file_name)
            for file in glob.glob(os.path.join(path, '{}.*'.format(base))):
                shutil.copy(os.path.join(path, file), tmpdir)
            filepath = os.path.join(tmpdir, file_name)
            self.in_place_layers[param_id] = filepath

        if param['type'] in ('vector', 'table'):
            gmlrex = r'\.gml\b'
            if re.search(gmlrex, filepath, re.IGNORECASE):
                # ewwwww - we have to force SRS detection for GML files, otherwise they'll be loaded
                # with no srs
                filepath += '|option:FORCE_SRS_DETECTION=YES'

            if filepath in self.vector_layer_params:
                return self.vector_layer_params[filepath]

            options = QgsVectorLayer.LayerOptions()
            options.loadDefaultStyle = False
            lyr = QgsVectorLayer(filepath, param['name'], 'ogr', options)
            self.vector_layer_params[filepath] = lyr
        elif param['type'] == 'raster':
            options = QgsRasterLayer.LayerOptions()
            options.loadDefaultStyle = False
            lyr = QgsRasterLayer(filepath, param['name'], 'gdal', options)

        self.assertTrue(lyr.isValid(), 'Could not load layer "{}" from param {}'.format(filepath, param))
        QgsProject.instance().addMapLayer(lyr)
        return lyr

    def filepath_from_param(self, param):
        """
        Creates a filepath from a param
        """
        prefix = processingTestDataPath()
        if 'location' in param and param['location'] == 'qgs':
            from utilities import unitTestDataPath  # pylint:disable=import-outside-toplevel
            prefix = unitTestDataPath()

        if 'uri' in param:
            path = param['uri']
        else:
            path = param['name']

        if not path:
            return None

        return self.uri_path_join(prefix, path)

    def uri_path_join(self, prefix, filepath):
        if filepath.startswith('ogr:'):
            if not prefix[-1] == os.path.sep:
                prefix += os.path.sep
            filepath = re.sub(r"dbname='", "dbname='{}".format(prefix), filepath)
        else:
            filepath = os.path.join(prefix, filepath)

        return filepath

    def check_results(self, results, context, params, expected):  # pylint:disable=too-many-statements,too-many-branches,too-many-locals
        """
        Checks if result produced by an algorithm matches with the expected specification.
        """
        for result_id, expected_result in expected.items():
            if expected_result['type'] in ('vector', 'table'):
                if 'compare' in expected_result and not expected_result['compare']:
                    # skipping the comparison, so just make sure output is valid
                    if isinstance(results[result_id], QgsMapLayer):
                        result_lyr = results[result_id]
                    else:
                        result_lyr = QgsProcessingUtils.mapLayerFromString(results[result_id], context)
                    self.assertTrue(result_lyr.isValid())
                    continue

                expected_lyrs = self.load_layers(result_id, expected_result)
                if 'in_place_result' in expected_result:
                    result_lyr = QgsProcessingUtils.mapLayerFromString(self.in_place_layers[result_id], context)
                    self.assertTrue(result_lyr.isValid(), self.in_place_layers[result_id])
                else:
                    try:
                        results[result_id]
                    except KeyError as e:
                        raise KeyError('Expected result {} does not exist in {}'.format(str(e), list(results.keys()))) from e

                    if isinstance(results[result_id], QgsMapLayer):
                        result_lyr = results[result_id]
                    else:
                        string = results[result_id]

                        gmlrex = r'\.gml\b'
                        if re.search(gmlrex, string, re.IGNORECASE):
                            # ewwwww - we have to force SRS detection for GML files, otherwise they'll be loaded
                            # with no srs
                            string += '|option:FORCE_SRS_DETECTION=YES'

                        result_lyr = QgsProcessingUtils.mapLayerFromString(string, context)
                    self.assertTrue(result_lyr, results[result_id])

                compare = expected_result.get('compare', {})
                pk = expected_result.get('pk', None)

                if len(expected_lyrs) == 1:
                    self.assertLayersEqual(expected_lyrs[0], result_lyr, compare=compare, pk=pk)
                else:
                    res = False
                    for layer in expected_lyrs:
                        if self.checkLayersEqual(layer, result_lyr, compare=compare, pk=pk):
                            res = True
                            break
                    self.assertTrue(res, 'Could not find matching layer in expected results')

            elif expected_result['type'] == 'rasterhash':
                print("id:{} result:{}".format(result_id, results[result_id]))
                self.assertTrue(os.path.exists(results[result_id]), 'File does not exist: {}, {}'.format(results[result_id], params))
                dataset = gdal.Open(results[result_id], GA_ReadOnly)
                dataArray = nan_to_num(dataset.ReadAsArray(0))
                strhash = hashlib.sha224(dataArray.data).hexdigest()

                if not isinstance(expected_result['hash'], str):
                    self.assertIn(strhash, expected_result['hash'])
                else:
                    self.assertEqual(strhash, expected_result['hash'])
            elif expected_result['type'] == 'file':
                result_filepath = results[result_id]
                if isinstance(expected_result.get('name'), list):
                    # test to see if any match expected
                    for path in expected_result['name']:
                        expected_filepath = self.filepath_from_param({'name': path})
                        if self.checkFilesEqual(expected_filepath, result_filepath):
                            break
                    else:
                        expected_filepath = self.filepath_from_param({'name': expected_result['name'][0]})
                else:
                    expected_filepath = self.filepath_from_param(expected_result)

                self.assertFilesEqual(expected_filepath, result_filepath)
            elif expected_result['type'] == 'directory':
                expected_dirpath = self.filepath_from_param(expected_result)
                result_dirpath = results[result_id]

                self.assertDirectoriesEqual(expected_dirpath, result_dirpath)
            elif expected_result['type'] == 'regex':
                with open(results[result_id], 'r', encoding='utf8') as file:
                    data = file.read()

                for rule in expected_result.get('rules', []):
                    self.assertRegex(data, rule)


if __name__ == '__main__':
    nose2.main()
