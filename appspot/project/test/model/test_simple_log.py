"""
    test_simple_log.py

    PURPOSE
    Test the SimpleLog model

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

# App Engine Imports
from google.appengine.ext import (testbed, db)

# Appswell Imports
from framework.lib.testing import (AppswellUnitTest, run_test_from_command_line)
from project.models.simple_log import (AppswellSimpleLog, AppswellSimpleLogModelForm)


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



#
# TEST CLASS
#
class SimpleLogTest(AppswellUnitTest):
#
    # Harness
    #
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        self.SimpleLog = AppswellSimpleLog()

    def tearDown(self):
        self.SimpleLog = None


    #
    # Unit Tests
    #
    def test_basic_save_find_delete(self):
        # test save
        SimpleLog = AppswellSimpleLog(
            type='debug',
            keyword='test',
            message='unit test'
        )
        SimpleLog.put()
        key = SimpleLog.key()

        # test find
        Record = db.get(key)
        self.assertEqual(Record.message, SimpleLog.message)

        # test delete
        Record.delete()
        Record = db.get(key)
        self.assertEqual(Record, None)

    def test_bad_log_type(self):
        """Error raised when model object instantiated"""
        try:
            SimpleLog = AppswellSimpleLog(
                type='invalid_type',
                keyword='test',
                message='unit test'
            )
        except db.BadValueError, e:
            self.note(e)
            expect = "Property type is 'invalid_type'"
            self.assertNotEqual(str(e).find(expect), -1)

    #
    # Smoke Tests
    #
    def test_instance(self):
        """adapt to your purposes, I like to always include this as a sanity check"""
        self.note('now: %s' % (datetime.now()))
        self.assertTrue(isinstance(self, AppswellUnitTest))
