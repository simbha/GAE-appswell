"""
    Appswell Base Controller

    This is the controller class from which others should inherit.
"""
#
# IMPORTS
#
# Python Standard
import sys, os, logging, inspect
from os.path import dirname, join as pathjoin
import hashlib
import time
import json

# Appswell
import config.core as c
from google.appengine.ext.webapp import template
from framework.lib.html_helper import HtmlHelper
import framework.lib.utilities as ut


#
# MODULE ATTRIBUTES
#
class ViewError(Exception): pass


#
# CLASS
#
class BaseController:

    name                = 'BaseController'
    output              = ''
    mode                = ''
    request_type        = ''
    params              = []
    requested           = {}
    request             = None
    response_headers    = {}
    template_type       = 'mako'
    view_dir            = pathjoin( ut.PROJECT_PATH, 'views' )
    view_path           = ''
    layout              = 'default'
    t                   = {}
    FlashList           = []
    auto_render         = True
    render_was_called   = False
    output_is_written   = False

    template_extension_map   = {
        'mako'   : '.mako',
        'django' : '.tpl'
    }

    # default helpers
    Html                = HtmlHelper()

    #
    # Constructor/Destructor
    #
    def __init__(self):
        """
            Remember, the App Engine caches the main request.  Use settings
            here to clear cache (e.g. self.t['head_content']).  For more info,
            see: http://code.google.com/appengine/docs/python/runtime.html#App_Caching
        """
        self.FlashList = []
        self.response_headers = {}
        self.t = {}
        self.t['head_content'] = ''
        self.t['__flash__'] = ''
        
    def init(self):
        """this gets called by dispatch before the action method is called but
        after all the controller prep has been done by dispatch (which occurs
        after the constructor is called"""
        # set some globals for layout
        pass

    #
    # API Methods
    #
    def redirect(self, url):
        """
            this gets overridden in the dispatch _load_controller method
        """
        pass

    def set_header(self, key, value):
        """sets response header"""
        self.response_headers[key] = value

    def set(self, key, value):
        """sets template value. Both Mako and Django templates are set up to
        work with it"""
        self.t[key] = value

    def has_param(self, expect, pos=None):
        """
            params are slash-separated values that follow the controller and
            action in the url:

            /controller/action/param1/param2/

            This method indicates whether the param is in the url.  If pos
            argument is set, it checks for param in that position (counting
            from 1 rather than 0)

            Usage:
            if self.has_param('param2', 2):
                do_something()
        """
        if not pos:
            return expect in self.params

        param = self.get_param(pos)
        return expect == param

    def get_param(self, pos):
        """
            Returns param by number (counting from 1 not 0). If param does not
            exist, returns 1.

            Usage:
            url = /controller/action/param1/param2/

            p1 = self.get_param(1)      # p1 = 'param1'
            p3 = self.get_param(3)      # p3 = None
        """
        if pos - 1 < 0:
            return None
        try:
            return self.params[pos-1]
        except:
            return None

    def flash(self, message):
        self.FlashList.append(message)
        self.t['__flash__'] = '<div class="flash">%s</div>' % (
            '<br />'.join(self.FlashList))

    #
    # Render Methods
    #
    def render(self, rel_path=None, layout_path=None):
        self.render_was_called = True

        if not self.template_type or self.template_type == 'raw':
            pass
        elif self.template_type == 'django':
            self.render_django(rel_path, layout_path)
        else:
            self.render_mako(rel_path, layout_path)

        return self.template_type

    def render_mako(self, rel_path=None, layout_dir=None):
        """Sets layout and view path. Dispath object will load Mako object,
        which renders the full output"""
        self.view_path = self._get_view_path(rel_path)

        if layout_dir:
            self.layout = layout_dir

        self.output = ''

    def render_django(self, rel_path=None, layout_path=None):
        """Produces the controller output and assigns it to the output
        property"""
        view_path = self._get_view_path(rel_path)

        if layout_path:
            self.layout = layout_path

        self.output = template.render(view_path, self.t)

    def render_json(self, JsonData):
        # jsonp output
        fx = self.request.GET.get('callback', '?')
        json_data = json.dumps(JsonData)
        jsonp = '%s(%s)' % (fx, json_data)

        # write
        self.set_header('Pragma', 'no-cache')
        self.set_header('Cache-Control', 'no-store, no-cache, max-age=0, must-revalidate')
        self.set_header('Content-Type', "application/json; charset=UTF-8")
        self.set_header('X-JSON', json_data)
        self.write(json_data)

    def render_jsonp(self, JsonData, wrapper=None):
        if not wrapper:
            wrapper = hashlib.md5(str(time.time())).hexdigest()[-9:]

        json_data = '%s(%s)' % ( wrapper, json.dumps(JsonData) )

        self.set_header('Pragma', 'no-cache')
        self.set_header('Cache-Control',
            'no-store, no-cache, max-age=0, must-revalidate')
        self.set_header('Content-Type', "application/x-javascript; charset=utf-8")
        self.write(json_data)

    def render_plain(self, content):
        self.set_header('Content-Type', 'text/plain; charset=UTF-8')
        self.write(content)

    def write(self, output):
        """render output without template"""
        self.output_is_written = True
        self.output = output


    #
    # Private Methods
    #
    def _controller_url(self):
        return self.__class__.__name__.replace('Controller', '').lower()

    def _get_controller_menu(self):
        menu = ''
        MethodList = self._get_public_method_list()
        for m in MethodList:
            menu += '<a href="/%s/%s">%s</a>\n' % (self._controller_url(), m, m)
        return '<ul>\n%s\n</ul>' % ( menu )

    def _get_public_method_list(self):
        MethodList = self._get_method_list()
        return set([m for m in MethodList if m.find('_') != 0])

    def _get_method_list(self):
        self_methods = BaseController._get_class_method_list(self)
        base_methods = self._get_base_method_list()
        return self_methods.difference(base_methods)

    def _get_view_path(self, path=''):
        """
            given a path value, returns absolute view file path
        """
        # no path defaults to controller/action
        if not path:
            view_path = '%s/%s' % ( self.requested['controller'],
                self.requested['action'] )

        # path starting with / should be a path within view
        elif path[0] == '/':
            view_path = path[1:]

        # default: path will be file name in dir named after controller
        else:
            view_path = '%s/%s' % ( self.requested['controller'], path )

        # find extension by template type
        ext = self.template_extension_map.get(self.template_type, '')

        absolute_view_path = pathjoin(self.view_dir, view_path + ext)
        return absolute_view_path

    @staticmethod
    def _get_class_method_list(klass):
        MethodList = []
        for name in dir(klass):
            logging.info('dict name: %s' % (name))
            item = getattr(klass, name)
            if inspect.ismethod(item):
                MethodList.append(item.__name__)
        logging.info('methods: %s' % MethodList)
        return set(MethodList)

    def _get_base_method_list(self):
        return BaseController._get_class_method_list(BaseController)
