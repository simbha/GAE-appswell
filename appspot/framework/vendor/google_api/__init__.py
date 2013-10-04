"""
    Google Data Libraries

    The google vendor path must be inserted to the sys.path to work properly.

    USAGE
    import framework.vendor.google_api
    from gdata.service import GDataService
    client = GDataService()

    REFERENCES
    http://code.google.com/apis/gdata/articles/python_client_lib.html#library
"""
#
# IMPORTS
#
# framework imports
import framework.lib.utilities as ut



#
# MODULE CONSTANTS
#
IS_LOADED = True

# Load Google Data modules at runtime
ut.extend_syspath(ut.FRAMEWORK_PATH, 'vendor/google_api')



#
# MODULE FUNCTIONS
#
