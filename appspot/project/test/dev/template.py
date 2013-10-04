"""
    template.py

    PURPOSE
    A working dev test template for the Appswell Google App Engine framework.

    NOTES
    If you change test class name and the command line block is operational, be
    sure to update run_test_from_command_line at bottom.

    REFERENCES
    http://code.google.com/p/appswell/source/browse/appspot/test/dev/dev_multicache.py

    LICENSE
    Tom at klenwell@gmail.com
    some rights reserved, 2011
"""
#
# IMPORTS
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
# MODULE ATTRIBUTES
#
# Test Configuration
TEST_CONFIG = {
    'VERBOSE'           : False,
    'BREAK'             : False,
}

# Exception Classes
class TemplateException(Exception): pass


#
# DEV OBJECTS
#
class DevObject(object):

    dict_proxy = {}

    @staticmethod
    def set(key, value):
        DevObject.dict_proxy[key] = value

    @staticmethod
    def get(key):
        return DevObject.dict_proxy.get(key)

    @staticmethod
    def inspect():
        return DevObject.dict_proxy


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


    #
    # Dev Tests
    #
    def test_dev_object(self):
        DevObject.set('hello', 'world')
        self.assertEqual(DevObject.get('hello'), 'world')
        self.note(DevObject.get('hello'))
        self.note(DevObject.inspect())


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
