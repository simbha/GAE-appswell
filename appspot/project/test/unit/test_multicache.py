"""
    test_multicache.py

    PURPOSE
    Tests the multicache library -- a wrapper for memcache that allows for
    the storage of arbitrarily large objects

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
import sys, os, pdb, logging
from os.path import (abspath, dirname, join as osjoin, exists)
from datetime import(datetime, date, timedelta)
from random import (randint, choice, sample)
import hashlib

# Extend sys.path
PROJECT_PATH = abspath(osjoin(dirname(__file__), '../..'))
if PROJECT_PATH not in sys.path:
    sys.path.append(PROJECT_PATH)

# App Engine Imports
from google.appengine.ext import (testbed, db)

# Appswell Imports
from framework.lib.testing import (AppswellUnitTest, run_test_from_command_line)
from framework.lib import (multicache)


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
class MulticacheTest(AppswellUnitTest):

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

    def get_cache_data(self, num_items):
        cache_data = {}

        for i in range(num_items):
            key = 'key_%s' % (i)
            value = hashlib.md5(str(i)).hexdigest()
            cache_data[key] = value

        return cache_data

    #
    # Unit Tests
    #
    def test_shallow_deep_object(self):
        """a dict of a 60 items, each a dict of 20000 items"""
        # cache params
        cache_key = 'test_shallow_deep_object'
        cache_len = 60
        num_items = 3
        num_sub_items = 20000

        # prepare cache data and save
        cache_data = {}
        for n in range(num_items):
            cache_data[n] = self.get_cache_data(num_sub_items)
        multicache.set(cache_key, cache_data, cache_len)

        # retrieve data
        retrieved_data = multicache.get(cache_key)

        # test
        self.assertEqual(cache_data[2].items().sort(),
            retrieved_data[2].items().sort())
        self.assertEqual(cache_data.keys().sort(), retrieved_data.keys().sort())

    def test_complex_multi_cache(self):
        """a dict of a 5000 items, each a dict of 20 items"""
        # cache params
        cache_key = 'test_complex_multi_cache'
        cache_len = 60
        num_items = 5000
        num_sub_items = 20

        # prepare cache data and save
        cache_data = {}
        for n in range(num_items):
            cache_data[n] = self.get_cache_data(num_sub_items)
        multicache.set(cache_key, cache_data, cache_len)

        # retrieve data
        retrieved_data = multicache.get(cache_key)

        # test
        logging.info([cache_data[1000], retrieved_data[1000]])
        self.assertEqual(cache_data[1000].items().sort(),
            retrieved_data[1000].items().sort())
        self.assertEqual(cache_data.keys().sort(), retrieved_data.keys().sort())

    def test_multi_cache(self):
        """this should just save using memcache"""
        # cache params
        cache_key = 'test_multi_cache'
        cache_len = 60
        num_items = 20000

        # prepare cache data and save
        cache_data = self.get_cache_data(num_items)
        multicache.set(cache_key, cache_data, cache_len)

        # retrieve data
        retrieved_data = multicache.get(cache_key)

        # test
        self.assertEqual(cache_data.keys().sort(), retrieved_data.keys().sort())

    def test_simple_multi_cache(self):
        """this should just save using memcache"""
        # cache params
        cache_key = 'test_simple_multi_cache'
        cache_len = 60

        # prepare cache data and save
        cache_data = self.get_cache_data(5000)
        multicache.set(cache_key, cache_data, cache_len)

        # retrieve data
        retrieved_data = multicache.get(cache_key)

        # test
        self.assertEqual(cache_data.keys().sort(), retrieved_data.keys().sort())

    def test_split_string_into_parts(self):
        num_parts = 3
        test_cases = [
            ('123456789012345678901234567890', ['1234567890'] * 3),
            ('1234567890', ['123', '456', '7890']),
        ]
        for case in test_cases:
            split_string = list(multicache.split_string_into_parts(case[0], 3))
            self.assertEqual(split_string, case[1])


    #
    # Smoke Tests
    #
    def testInstance(self):
        """adapt to your purposes, I like to always include this as a sanity check"""
        self.assertTrue(isinstance(self, AppswellUnitTest))


#
# Main
#
if __name__ == "__main__":
    run_test_from_command_line(MulticacheTest)
