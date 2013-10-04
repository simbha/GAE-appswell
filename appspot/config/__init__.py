"""
    Appswell Configuration Module for Google App Engine

    This initializes some environmental values that may be of interest to
    developers.
"""
import logging
import os

TEST_MODE       = 0
PROD_MODE       = 1
IS_DEV_SERVER   = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')
SDK_VERSION     = 'n/a'

# Set SDK_VERSION
if IS_DEV_SERVER:
    try:
        from google.appengine.tools import appcfg
        version = appcfg.GetVersionObject()
        SDK_VERSION = version.get('release', 'not found')
    except Exception, e:
        logging.error('unable to programmatically determine SDK version: %s' % \
            (str(e)) )
