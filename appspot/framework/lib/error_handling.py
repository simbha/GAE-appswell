"""
    Appswell Error Handling Lib

    functions for handling errors

    USAGE
    from lib import error_handling
    error_details = error_handling.get_error_details()
    error_page = error_handling.render_error_page(error_details)
"""
#
# IMPORTS
#
import sys, os, logging, inspect
from os.path import (abspath, dirname, join as pathjoin)
import traceback

VIEW_DIR = abspath(pathjoin( dirname(__file__), '../views' ))
LAYOUT_DIR = pathjoin( VIEW_DIR, 'layouts' )
VIEW_PATH = pathjoin( VIEW_DIR, 'error/default.mako' )


def get_error_details():
    exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
    detail = {
        'error_type'    : exceptionValue,
        'tracelist'     : traceback.extract_tb(exceptionTraceback),
        'trace'         : traceback.format_exc(),
        'syspath'       : sys.path
    }
    return detail


def render_error_page(detail):

    from framework.vendor.mako.template import Template
    from framework.vendor.mako.lookup import TemplateLookup

    # create mako objects and render
    mako_lookup = TemplateLookup( directories=[LAYOUT_DIR],
                                  output_encoding='utf-8',
                                  encoding_errors='replace' )
    mako_template = Template(filename=VIEW_PATH, lookup=mako_lookup)

    return mako_template.render_unicode(**detail).encode('utf-8', 'replace')
