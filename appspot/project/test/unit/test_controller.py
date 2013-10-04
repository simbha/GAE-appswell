"""
    test_controller.py

    PURPOSE
    Test the Appswell BaseController class

    NOTES
    If you change test class name, be sure to update in main block at bottom.
    _create_suite

    REFERENCES

    LICENSE
    Tom at klenwell@gmail.com
    some rights reserved, 2011
"""
#
# Imports
#
# Python Imports
import sys, os, pdb
from os.path import (abspath, dirname, join as osjoin, exists)
from datetime import(datetime, date, timedelta)
from random import (choice, sample)
from pprint import (pformat)

# Extend sys.path
PROJECT_PATH = abspath(osjoin(dirname(__file__), '../..'))
sys.path.append(PROJECT_PATH)
sys.path.append(osjoin(PROJECT_PATH, 'lib'))

# Appswell Imports
from framework.lib.testing import (AppswellUnitTest, run_test_from_command_line)
from framework.lib.base_controller import (BaseController)


#
# Overrides
#
class TestingController(BaseController): pass


#
# Module Parameters
#
# Test Configuration
TEST_CONFIG = {
    'BREAK'             : False,
    'VERBOSE'           : False,
}

# Exception Classes
class TemplateException(Exception): pass


#
# Test Class
#
class ControllerTest(AppswellUnitTest):

    # Overhead
    def setUp(self):
        self.controller = TestingController()

    def tearDown(self):
        self.controller = None


    # Tests
    def testParams(self):
        # simulate request: /test/controller/one/two
        self.controller.params = ['one', 'two']

        # has_param
        self.assertFalse(self.controller.has_param(0))
        self.assertTrue(self.controller.has_param('one'))
        self.assertTrue(self.controller.has_param('two', 2))
        self.assertFalse(self.controller.has_param('two', 1))
        self.assertFalse(self.controller.has_param(3))

        # get_param
        self.assertEqual(self.controller.get_param(0), None)
        self.assertEqual(self.controller.get_param(1), 'one')
        self.assertEqual(self.controller.get_param(3), None)

    def testRequestedObject(self):
        """this is mainly to show what Requested dict entails"""
        # simulate request object
        self.controller.requested = {
            'action': 'test',
            'controller': 'unit',
            'params': ['one', 'two'],
            'path': 'test/unit/one/two'
        }
        self.note('self.controller.requested: %s' % (
            pformat(self.controller.requested)))

        # tests
        self.assertEqual(self.controller.requested['action'], 'test')

    def testInstance(self):
        """adapt to your purposes, I like to always include this as a sanity check"""
        self.note('now: %s' % (datetime.now()))
        self.assertTrue(isinstance(self.controller, BaseController))


#
# Main
#
if __name__ == "__main__":
    run_test_from_command_line(ControllerTest)
