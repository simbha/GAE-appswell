"""
    presents_controller.py

    This controller is intended as the standard public-facing interface.
"""
#
# IMPORTS
#
# Python Standard Library
import logging
from datetime import (datetime)

# Appswell
from config import core as c
from framework.lib.base_controller import BaseController


#
# MODULE ATTRIBUTES
#


#
# CONTROLLER CLASS
#
class PresentsController(BaseController):

    name            = 'Presentation Controller'
    layout          = 'default'
    auto_render     = True

    def index(self):
        return self.home()

    def home(self):
        """note django template type"""
        self.t['head_content'] += self.Html.css_link('/css/home.css')
        self.template_type = 'django'
        self.render('home', 'home')

    def changelog(self):
        # build template header
        head_content = []
        head_content.append(self.Html.css_link('/css/demo.css'))
        head_content.append(self.Html.css_link('/css/changelog.css'))

        # render view
        self.set('head_content', '\n'.join(head_content))
        self.render('changelog')

    def usage(self):
        self.render('usage')
