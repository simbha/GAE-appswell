"""
    template.py

    PURPOSE
    A working unit testing template for the Appswell Google App Engine
    framework. It should be able to be run either directly from the command
    line or in browser at /test/unit/template

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
import pdb, logging
from datetime import(datetime, date, timedelta)
from random import (choice, sample)

# App Engine Imports
from google.appengine.ext import (testbed, db)

# Appswell Imports
from framework.lib.testing import (AppswellUnitTest, run_test_from_command_line)


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
class TemplateTest(AppswellUnitTest):

    #
    # Harness
    #
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()

    def tearDown(self):
        self.testbed.deactivate()

    #
    # Unit Tests
    #
    def test_success(self):
        self.note('a simple passing test')
        self.assertEqual(1, 1)

    def test_failure(self):
        self.note('now: %s' % (datetime.now()))
        self.note('this test is intended to fail for demonstration purposes')
        self.note('now: %s' % (datetime.now()))
        self.fail('for demonstration purposes')

    def test_error(self):
        self.note('now: %s' % (datetime.now()))
        self.note('this test is intended to err for demonstration purposes')
        raise Exception('for demonstration purposes')

    #
    # Smoke Tests
    #
    def test_break(self):
        """Set BREAK property in TEST_CONFIG above to True to use Python
        debugger to break into test and interact from the command line"""
        if TEST_CONFIG.get('BREAK'):
            pdb.set_trace()

    def test_instance(self):
        """adapt to your purposes, I like to always include this as a sanity check"""
        self.note('now: %s' % (datetime.now()))
        self.assertTrue(isinstance(self, AppswellUnitTest))


#
# Main
#
if __name__ == "__main__":
    run_test_from_command_line(TemplateTest)
