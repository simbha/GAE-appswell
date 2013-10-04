"""
    backend_controller.py

    Intended for backend tasks, esp. cron tasks.
"""
#
# IMPORTS
#
# Python Standard Library
import logging
from datetime import (datetime)

# Appswell
from config import core as c
from lib.base_controller import BaseController
from models.simple_log import (AppswellSimpleLog)


#
# MODULE ATTRIBUTES
#


#
# CONTROLLER CLASS
#
class BackendController(BaseController):

    layout          = None
    auto_render     = False

    def index(self):
        return self.test()

    def simple_log(self):
        SimpleLog = AppswellSimpleLog()
        SimpleLog.log('cron',
            'backend.simple_log',
            'system')
        logging.info('running simple_log')
        self.write('simple_log runs sucessfully')

    def test(self):
        self.write('backend test called with params: %s' % (self.Params))
