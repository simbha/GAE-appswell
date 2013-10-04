"""
    services_controller.py

    Intended for ajax requests.
"""
#
# IMPORTS
#
# Standard
import logging
import random

# Google App Engine
import json as simplejson

# Appswell
from framework.lib.base_controller import BaseController
from config import core as c


#
# CONTROLLER CLASS
#
class ServicesController(BaseController):

    name            = 'Services Controller'
    layout          = None
    auto_render     = False

    def dice(self):
        """This can be called in an AJAX request to return a number a unicode
        die symbol between 1 and 6.

        See code here for example of usage:
        http://code.google.com/p/appswell/source/browse/appspot/views/demo/ajax.mako#40
        """
        base_die_code = 9855
        rolled = random.randint(1,6)
        die_html = '&#%s;' % ( base_die_code + rolled )

        JsonData = {
            'rolled' : rolled,
            'die' : die_html
        }

        callback = self.request.GET.get('callback')
        self.render_jsonp(JsonData, callback)

    def test(self):
        self.render_plain('backend test called with params: %s' % (self.Params))
