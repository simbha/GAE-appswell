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
from os.path import (abspath, dirname, join as osjoin, exists)
from datetime import(datetime, date, timedelta)
from random import (choice, sample)
from pprint import (pformat)

# Extend sys.path

# Appswell Imports
from framework.lib.testing import (AppswellUnitTest, run_test_from_command_line)


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
class FrameworkUnitTest(AppswellUnitTest):

    # Overhead
    def setUp(self):
        pass

    def tearDown(self):
        pass


    # Tests
    def testGdataImport(self):
        import framework.vendor.google_api
        from gdata.service import GDataService
        client = GDataService()
        self.assertTrue(GDataService)
        self.assertTrue(isinstance(client, GDataService))

    def testGdata(self):
        import framework.vendor.google_api
        from gdata import (test_data, GDataEntryFromString)

        try:
            from xml.etree import ElementTree
            self.note("ElementTree found in xml.etree")
        except ImportError:
            from elementtree import ElementTree
            self.note("ElementTree found in elementtree")
        entry = GDataEntryFromString(test_data.XML_ENTRY_1)
        element_tree = ElementTree.fromstring(test_data.XML_ENTRY_1)

        # note
        self.note(element_tree)

        # test
        self.assert_(element_tree.findall(
            '{http://www.w3.org/2005/Atom}id')[0].text != entry.id.text)
        self.assert_(entry.id.text == 'http://www.google.com/test/id/url')

    def testVendorImports(self):
        from framework.vendor import tweepy
        self.assertTrue(tweepy)

    def testInstance(self):
        """adapt to your purposes, I like to always include this as a sanity check"""
        self.note('now: %s' % (datetime.now()))
        self.assertTrue(isinstance(self, FrameworkUnitTest))


#
# Main
#
if __name__ == "__main__":
    run_test_from_command_line(FrameworkUnitTest)
