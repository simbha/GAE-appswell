"""
    Appswell Gatekeeper Library
"""
#
# IMPORTS
#
# Python Standard Library
import sys, os, logging, inspect
from os.path import dirname, join

# App Engine Imports
from google.appengine.ext.webapp import template

# Appswell
from base_controller import BaseController


#
# GATEKEEPER CLASS
#
class Gatekeeper:

    def __init__(self):
        pass

    # API Methods
    def controller_url(self, klass):
        return klass.__class__.__name__.replace('Controller', '').lower()

    def get_controller_menu(self, klass):
        menu = ''
        li_ = '<li><a href="/%s/%s">%s</a></li>\n'
        MethodList = self.get_public_method_list(klass)
        for m in MethodList:
            menu += li_ % (self.controller_url(klass), m, m.replace('_', ' '))
        return '<ul>\n%s\n</ul>' % ( menu )

    def get_public_method_list(self, klass):
        MethodList = self.get_method_list(klass)
        return set([m for m in MethodList if m.find('_') != 0])

    def get_method_list(self, klass):
        controller_methods = self.get_class_method_list(klass)
        inherited_methods = self.get_base_method_list()
        return controller_methods.difference(inherited_methods)

    def get_class_method_list(self, klass):
        MethodList = []
        for name in dir(klass):
            item = getattr(klass, name)
            if inspect.ismethod(item):
                MethodList.append(item.__name__)
        return set(MethodList)

    def get_base_method_list(self):
        return self.get_class_method_list(BaseController)
