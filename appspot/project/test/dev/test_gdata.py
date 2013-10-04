"""
    test_framework.py

    PURPOSE
    Test the Google App Engine Framework

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
from os.path import (abspath, dirname, join as pathjoin, exists)
from datetime import(datetime, date, timedelta)
from random import (choice, sample)
from pprint import (pformat)

# Extend sys.path

# Appswell Imports
from framework.lib.testing import (AppswellUnitTest, run_test_from_command_line)
import framework.lib.utilities as ut


#
# Overrides
#


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
class GdataUnitTest(AppswellUnitTest):

    # Overhead
    def setUp(self):
        pass

    def tearDown(self):
        pass


    # Tests
    def testExtendSysPath(self):

        # add atom and gdata to sys.path
        google_api_path = abspath(pathjoin(ut.FRAMEWORK_PATH, 'vendor/google_api'))
        self.note(google_api_path)
        if google_api_path not in sys.path:
            sys.path.insert(0, google_api_path)
        self.note(pformat(sys.path))
        self.assertTrue(google_api_path in sys.path)
        self.assertTrue('gdata' in os.listdir(google_api_path))

        # import
        import gdata.docs.service
        client = gdata.docs.service.DocsService()
        self.assertTrue(isinstance(client, gdata.docs.service.DocsService))

    def testImportGDataService(self):
        """see http://stackoverflow.com/questions/279237/"""

        # add atom and gdata to sys.path
        google_api_path = abspath(pathjoin(ut.FRAMEWORK_PATH, 'vendor/google_api'))
        if google_api_path not in sys.path:
            sys.path.insert(0, google_api_path)

        # import
        from gdata.service import GDataService
        client = GDataService()
        self.assertTrue(isinstance(client, GDataService))

    def testInstance(self):
        """adapt to your purposes, I like to always include this as a sanity check"""
        self.note('now: %s' % (datetime.now()))
        self.assertTrue(isinstance(self, AppswellUnitTest))


#
# Main
#
if __name__ == "__main__":
    run_test_from_command_line(GdataUnitTest)
