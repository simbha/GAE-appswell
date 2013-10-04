"""
    Appswell Utilities Lib

    assorted functions of general utility

    USAGE
    import lib.utilities as ut
    ut.append_syspath(ut.PROJECT_PATH, 'test')
"""

import sys, os, logging, inspect
from os.path import (abspath, dirname, join as pathjoin)

ROOT_PATH = abspath(pathjoin(dirname(__file__), '../..'))
FRAMEWORK_PATH = abspath(pathjoin(ROOT_PATH, 'framework'))
PROJECT_PATH = abspath(pathjoin(ROOT_PATH, 'project'))


def extend_syspath(basepath, subpath=None):

    if subpath:
        new_path = abspath(pathjoin(basepath, subpath))
    else:
        new_path = basepath

    if not new_path in sys.path:
        sys.path.insert(0, new_path)
        logging.info('sys.path inserted: %s' % (new_path))

    return new_path

def append_syspath(basepath, subpath=None):
    """this is kept for backwards compatability"""
    return extend_syspath(basepath, subpath)
