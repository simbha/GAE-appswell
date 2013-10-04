"""
    Appswell Test Controller

    Controller tuned to running and displaying results from Python unit tests

    REFERENCES
    http://code.google.com/p/gaeunit/source/browse/trunk/gaeunit.py
"""
# Python Imports
import sys, os, logging, time
from random import randint, sample
from pprint import pformat
from decimal import Decimal
from os.path import (abspath, dirname, join as pathjoin)
import unittest
import traceback
from datetime import (datetime)

# App Engine Imports
from google.appengine.api import apiproxy_stub_map
from google.appengine.api import datastore_file_stub

# Appswell Imports
from framework.lib.base_controller import BaseController
from framework.lib.testing import (AppswellTestResult, AppswellTestRunner)
import framework.lib.utilities as ut
from project.test import TEST_GROUPS

# Extend sys.path Using ut
TEST_DIR = ut.append_syspath(ut.PROJECT_PATH, 'test')


class TestController(BaseController):

    name            = 'TestController'
    view_dir        = pathjoin( ut.FRAMEWORK_PATH, 'views' )
    template_type   = 'mako'
    layout          = 'test'
    auto_render     = True

    def dispatch(self):
        """run tests and returns output to dispatch handler"""
        # use path to identify subdirectory of test and module
        module_name = self.load_module_path(self.requested)

        if not module_name:
            return self.index()
        else:
            return self.run_module_test(module_name)

    #
    # Viewable Methods
    #
    def index(self):
        groups = self.load_groups()
        links = {}
        for g in groups:
            links[g] = {}
            for n in range(len(groups[g])):
                links[g][n] = '<a href="%s">%s</a>' % (groups[g][n], groups[g][n].split('/')[-1])
        d = { 'groups': groups, 'links': links, 'requested': self.requested}
        #self.debug(d)

        # template variables
        #self.set('head_content', self.Html.css_link('/css/demo.css'))
        self.set('groups', groups)
        return self.render('index', '/layouts')

    def run_module_test(self, module_name):
        """
        Acts as test runner for given module and display results
        """
        module = reload(__import__(module_name))

        # create suite
        loader = unittest.defaultTestLoader
        suite = unittest.TestSuite()
        suite.addTest(loader.loadTestsFromModule(module))

        # create runner and fixture
        runner = AppswellTestRunner()
        #original_apiproxy = self.setup_datastore_fixture()

        # run tests
        runner.run(suite)

        # prepare results
        test_details = runner.result.get_detail()

        # template variables
        self.set('module', module_name)
        #self.set('head_content', self.Html.css_link('/css/demo.css'))
        self.set('headline', 'mako auto-rendering test')
        self.set('test_results', test_details.get('results', []))
        self.set('test_notes', test_details.get('notes', []))
        self.set('tests_passed', test_details['passed'])
        self.set('total_tests', test_details['total'])
        self.set('successful', test_details['success'])
        self.set('project_root', ut.PROJECT_PATH)
        self.set('completed_in', test_details['duration'])
        return self.render('template', '/layouts')

    #
    # Helper Methods
    #
    def load_module_path(self, request):
        """Does two things: returns the module name for the request test. Also
        adds module's parent dir to the sys.path"""
        path = request['path']
        path_split = path.split('test/')

        # index/no child path
        if len(path_split) < 2 or path_split[1] == 'index':
            return None

        # identify module's sys path
        child_path = path_split[1]
        module_dir = child_path.rsplit('/',1)[0]
        module_dir_path = ut.append_syspath(TEST_DIR, module_dir)

        # identify and return module
        module = child_path.split('/')[-1].replace('-', '_')
        logging.info('test module: %s' % (module))
        return module

    def load_groups(self):
        groups = {}
        for name in os.listdir(TEST_DIR):
            full_path = pathjoin(TEST_DIR, name)
            if os.path.isdir(full_path) and name in TEST_GROUPS:
                groups[name] = self.get_tests_for_group(full_path)
        return groups

    def get_tests_for_group(self, dir_path):
        test_modules = []
        for name in os.listdir(dir_path):
            if name.endswith(".py") and not name.startswith("__"):
                module_path = pathjoin(dir_path, name)
                url_path = module_path.replace(TEST_DIR, '/test').replace('.py', '')
                test_modules.append(url_path)
        return test_modules

    def setup_datastore_fixture(self):
        original_apiproxy = apiproxy_stub_map.apiproxy
        apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap()

        # trusted keyword raises error:
        temp_stub = datastore_file_stub.DatastoreFileStub('GAEUnitDataStore', None, None, trusted=True)
        apiproxy_stub_map.apiproxy.RegisterStub('datastore', temp_stub)

        # Allow the other services to be used as-is for tests.
        for name in ['user', 'urlfetch', 'mail', 'memcache', 'images']:
            apiproxy_stub_map.apiproxy.RegisterStub(name, original_apiproxy.GetStub(name))

        return original_apiproxy

    def teardown_datastore_fixture(self, original_apiproxy):
        apiproxy_stub_map.apiproxy = original_apiproxy

    def _load_default_test_modules():
        if not _LOCAL_TEST_DIR in sys.path:
            sys.path.append(_LOCAL_TEST_DIR)
        module_names = [mf[0:-3] for mf in os.listdir(_LOCAL_TEST_DIR) \
            if mf.endswith(".py") and not mf.startswith("__")]
        return [reload(__import__(name)) for name in module_names]

    def debug(self, whatever):
        self.write('<pre>%s</pre>' % (pformat(whatever)))
