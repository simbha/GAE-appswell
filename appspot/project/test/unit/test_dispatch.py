"""
    test_dispatch.py

    PURPOSE
    Test the dispatch module that drives the MVC framework.

    NOTES
    If you change test class name and the command line block is operational, be
    sure to update run_test_from_command_line at bottom.

    REFERENCES


    LICENSE
    Tom at klenwell@gmail.com
    some rights reserved, 2011
"""
#
# IMPORTS
#
# Python Imports
import pdb, logging, os
from datetime import(datetime, date, timedelta)
from random import (choice, sample)

# App Engine Imports
from google.appengine.ext import (testbed, db)
from google.appengine.ext import (webapp)

# Appswell Imports
from framework.lib.testing import (AppswellUnitTest, run_test_from_command_line)
from framework.vendor.webtest import TestApp
from framework.lib.base_controller import (BaseController)
from framework.dispatch import (DispatchHandler, ControllerError)
from config import core as c


#
# MODULE ATTRIBUTES
#
# Test Configuration
TEST_CONFIG = {
    'VERBOSE'           : False,
    'BREAK'             : False,
}

# Exception Classes
class NullException(Exception): pass

# Dev Class
class MockObject: pass

class DevHandler(DispatchHandler):

    def initialize(self, request, response):
        """Initializes this request handler with the given Request and Response."""
        #logging.info(request)
        #logging.info(response)
        DispatchHandler.initialize(self, request, response)

        # set necessary handler properties
        self.is_dev_server = True
        self.mode = c.TEST_MODE
        self.request_type = 'GET'



#
# TEST CLASS
#
class DispatchTest(AppswellUnitTest):

    #
    # Harness
    #
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        self.application = webapp.WSGIApplication(
            [(r'/(.*)', DevHandler)], debug=True)
        self.handler = DevHandler()
        self.handler.initialize(webapp.Request(
            dict(os.environ)), webapp.Response())
        logging.info('start test %s' % (self.id()))

    def tearDown(self):
        self.testbed.deactivate()
        self.application = None
        logging.info('end test %s' % (self.id()))


    #
    # Unit Tests
    #
    def test_get_layout_path(self):
        test_cases = [
            ('n/a', None, None),
            ('mako', '/layout', '<BASE>/layout/to_be_clipped.mako'),
            ('mako', 'controller/action', '<BASE>/layouts/controller/action.mako'),
            ('django', '/layouts/default', '<BASE>/layouts/default.tpl'),
            ('django', 'default', '<BASE>/layouts/default.tpl'),
        ]

        self.handler.controller_ = BaseController()
        for (type,path,expect) in test_cases:
            if expect:
                expect = expect.replace('<BASE>', self.handler.controller_.view_dir)
            self.handler.controller_.template_type = type
            self.handler.controller_.layout = path
            layout_path = self.handler._get_layout_path()
            self.assertEqual(layout_path, expect)

    def test_render_mako_view(self):
        self.handler.controller_ = BaseController()
        self.handler.controller_.template_type = 'mako'

        expect = 'dispatch unit test'
        self.handler.controller_.set('menu', 'n/a')
        self.handler.controller_.set('head_content', '')
        self.handler.controller_.set('headline', expect)
        self.handler.controller_.set('explanation', expect)
        self.handler.controller_.render('/demo/test', '/layouts')
        output = self.handler._render_view('')
        #self.note(output)

        # test
        self.assertTrue(output.find(expect) != -1)

    def test_render_django_view(self):
        self.handler.controller_ = BaseController()
        self.handler.controller_.template_type = 'django'
        self.handler.controller_.render('/presents/home', 'home')
        action_output = self.handler.controller_.output
        output = self.handler._render_view(action_output)
        #self.note(output)

        # test
        expect = '<a href="http://appswell.appspot.com/">appswell</a>'
        self.assertTrue(output.find(expect) != -1)

    def test_render_view_pre_rendered(self):
        action_output = 'lorem ipsum whatever'
        self.handler.controller_ = MockObject()
        self.handler.controller_.output_is_written = True
        output = self.handler._render_view(action_output)
        self.assertEqual(output, action_output)

    def test_call_action(self):
        requested = {'action': 'home', 'path': 'presents/home',
                     'controller': 'presents', 'params': []}

        # reproduce load routine
        controller = self.handler._load_controller(requested)
        action_output = self.handler._call_action(controller)
        #self.note(action_output)

        # test
        expect = '<a href="http://appswell.appspot.com/">appswell</a>'
        self.assertTrue(action_output.find(expect) != -1)
        self.assertEqual(action_output, controller.output.strip())

    def test_missing_controller(self):
        requested = {'action': 'index', 'path': '/null/index',
                     'controller': 'null', 'params': []}
        self.assertRaises(ControllerError, self.handler._load_controller, requested)

    def test_load_controller(self):
        requested = {'action': 'dispatch', 'path': '/test/dispatch/param1/param2',
                     'controller': 'test', 'params': ['param1', 'param2']}
        controller = self.handler._load_controller(requested, dir='framework')
        self.assertTrue(isinstance(controller, BaseController))
        self.assertEqual(controller.requested, requested)
        self.assertEqual(controller.params, requested['params'])

    def test_parse_request(self):
        test_cases = [
            ('', '', 'index', []),
            ('presents/home', 'presents', 'home', []),
            ('controller/action/param1/param2/param3',
             'controller', 'action', ['param1','param2','param3']),
        ]

        for t in test_cases:
            (path, expected_controller, expected_action, expected_params) = t
            requested = self.handler._parse_request(path)
            self.assertEqual(requested['path'], path)
            self.assertEqual(requested['controller'], expected_controller)
            self.assertEqual(requested['action'], expected_action)
            self.assertEqual(requested['params'], expected_params)

    def test_path(self):
        test_cases = [
            ('', 'demo/home'),
            ('controller/action', 'controller/action'),
        ]

        for t in test_cases:
            path, expect = t
            route_path =  self.handler._route(path)
            self.assertEqual(route_path, expect)


    def test_set_mode(self):
        mode = self.handler._set_mode()
        self.note({
            'server_name'   : self.handler.server_name,
            'is_dev_server' : self.handler.is_dev_server,
            'mode'          : mode
        })

    def test_basic_dispatch(self):
        # simulate request
        path = '/usage/param1/param2'
        response = self.handler.get(path)

        # debug
        self.note(self.handler.requested)

        # test
        self.assertEqual(self.handler.requested['path'], path)
        self.assertEqual(self.handler.requested['action'], 'usage')
        self.assertEqual(self.handler.requested['params'], ['param1', 'param2'])


    def test_ga_code(self):
        ga_code = c.GOOGLE_GA_CODE

        # load application and fetch pages
        app = TestApp(self.application)
        home = app.get('/')
        usage = app.get('/presents/usage')

        # test
        self.assertTrue(ga_code in home)
        self.assertTrue(ga_code in usage)

    def test_basic_webapp(self):
        app = TestApp(self.application)
        response = app.get('/')
        self.assertEqual('200 OK', response.status)
        #self.note(dir(response))


    #
    # Dev Tests
    #
    def test_instantiate_dispatch(self):
        # simulate request
        response = self.handler.get('/presents/usage')

        # debug
        #self.note(response)
        #self.note(self.handler.requested)


    #
    # Smoke Tests
    #
    def test_instance(self):
        """adapt to your purposes, I like to always include this as a sanity check"""
        self.note('now: %s' % (datetime.now()))
        self.assertTrue(isinstance(self, AppswellUnitTest))


#
# Main
#
"""
# Not yet operational
if __name__ == "__main__":
    run_test_from_command_line(TemplateTest)
"""
