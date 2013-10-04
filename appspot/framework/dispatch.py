#!/usr/bin/env python
"""
    Dispatch Request Handler

    A Google App Engine webapp request handler configured to support
    conventions more like those used in Ruby-On-Rails or other MVC frameworks.
    The request gets directed here by app.yaml

    NOTES
    extend_framework_syspath
        This used to extend the syspath to all the base directories
        (controllers, models, etc.)  Now a more modular design is used for
        imports. Currently, however, this is needed for mako lib (viz 'from
        mako.lexer import Lexer' in mako/template.py).

        Because of way App Engine caching works, this must be called in the
        main function, not at top of file.

    rendering views
        django:
        The django view rendering method assign the output of the action to
        the controller's output property, which then gets returned to the
        dispatch handler which invokes the layout template and inserts the
        action output into it.

        mako:
        The mako view handler does not produce the action output but rather
        sets the view and template paths on the controller object, which the
        dispatch handler then passes to the mako layout and template objects
        to produce the output.


    REFERENCES
    http://code.google.com/appengine/docs/python/gettingstarted/usingwebapp.html

"""
# python imports
import sys, os, logging, traceback
from os.path import (dirname, join as pathjoin)
from pprint import pformat

# google imports
import wsgiref.handlers
from google.appengine.api import users
import webapp2 as webapp

# framework imports
import config.core as c
import framework.lib.utilities as ut

# Exceptions
class ControllerError(Exception): pass
class ViewError(Exception): pass



def extend_framework_syspath():
    """ see note above for more info """
    ut.extend_syspath(ut.FRAMEWORK_PATH, 'vendor')


# Dispatch Handler CLass
class DispatchHandler(webapp.RequestHandler):

    request_type    = ''            # POST or GET
    server_name     = ''
    is_dev_server   = False
    mode            = ''            # test or prod (see map in config.core)
    path            = ''            # original request path
    route_path      = ''            # path returned by route method
    requested       = ''            # Dict of controller, action, param values
    controller_     = None          # controller object

    #
    # Main Handler Methods
    #
    def get(self, path):
        self.request_type = 'GET'
        return self._process(path)

    def post(self, path):
        self.request_type = 'POST'
        return self._process(path)

    def _process(self, path):
        """
            Processes the request and invokes the appropriate controller method
            based on the request url
        """
        try:
            self.path        = path
            self.mode        = self._set_mode()
            self.route_path  = self._route(self.path)
            self.requested   = self._parse_request(self.route_path)
            self.controller_ = self._load_controller(self.requested)
            action_output    = self._call_action(self.controller_)
            output           = self._render_view(action_output)
        except:
            output = self._handle_exception()

        self._respond(output)

    def _handle_exception(self):
        from framework.lib import error_handling
        from framework.lib.base_controller import BaseController

        # set details
        details = error_handling.get_error_details()
        details.update({
            'head_content'  : '',
            '__flash__'     : '',
            'is_dev_server' : self.is_dev_server,
        })

        # need a controller
        if not self.controller_:
            self.controller_ = BaseController()
        details['head_content'] = self.controller_.Html.css_link('/css/error.css')

        # log and render
        logging.error(details['trace'])
        error_page = error_handling.render_error_page(details)
        return error_page


    #
    # Process Methods
    #
    def _set_mode(self):
        """
            Sets version based on MODE_MAP in config/core.py.  In event server
            name cannot be matched to a key, defaults to production mode.
        """
        self.server_name = os.environ.get('SERVER_NAME', 'unknown')
        self.is_dev_server = os.environ.get('SERVER_SOFTWARE', '').startswith(
            'Development')

        if not c.MODE_MAP:
            c.MODE_MAP = {}

        for mode_key,server_names in c.MODE_MAP.items():
            if self.server_name in server_names:
                return mode_key

        # version key not set: log and default to production
        t_ = "server name '%s' not found in mode map; defaulting to production mode"
        logging.warning(t_ % (self.server_name))
        return c.PROD_MODE

    def _route(self, path):
        """
            Uses ROUTE_MAP in config.core to replace current path with mapped
            path (second index of ROUTE_MAP tuple)

            This is not very sophisticated and may need to be updated to avoid
            collisions in the future.
        """
        if not c.ROUTE_MAP:
            logging.warning('c.ROUTE_MAP not found: add to config/core.py')
            c.ROUTE_MAP = []

        for mapped,replace in c.ROUTE_MAP:
            # url root (e.g. http://appswell.appspot.com/)
            if mapped == '':
                if path == '':
                    path = replace
            # a hit
            elif path.startswith(mapped):
                path = path.replace(mapped, replace)
        return path

    def _parse_request(self, path):
        """
            parses the path to organize the request path into a dict with
            controller name, action name, and any parameter values according
            to format:

            /controller/action/param1/param2/.../paramn
        """
        request_dict = {
            'path'      : path,
            'controller': '',
            'action'    : 'index',
            'params'    : []
        }

        path_split = path.split('/')

        request_dict['controller'] = path_split[0]

        if len(path_split) > 1 and path_split[1] != '':
            request_dict['action'] = path_split[1]

        if len(path_split) > 2 :
            request_dict['params'] = [p for p in path_split[2:] if p != '']

        logging.debug('request_dict: %s' % ( request_dict ))
        return request_dict

    def _load_controller(self, requested, dir='project'):
        """
            Based on url (by way of Request dict), set controller module and
            controller object.  Follows Rails-like conventions.
        """
        # set module
        try:
            requested_controller = requested['controller'].replace('-', '_')
            controller_name = '%s_controller' % (requested_controller)
            module_name = '%s.controllers.%s' % (dir, controller_name)
            controller_module = __import__(module_name, globals(), locals(),
                [controller_name], -1)

        except ImportError, e:
            if module_name in str(e):
                t_ = "expected file '%s.py' not found in controllers directory"
                raise ControllerError(t_ % (module_name))
            else:
                t_ = "controller import error: %s"
                raise ControllerError(t_ % (str(e)))

        # set controller instance
        try:
            class_name = '%sController' % (
                ''.join([p.capitalize() for p in (
                    requested_controller.split('_'))]))
            controller_class = getattr(controller_module, class_name)
            controller = controller_class()
        except AttributeError, e:
            t_ = "expected class '%s' not found in 'controllers/%s.py' file: %s"
            raise ControllerError(t_ % (class_name, module_name, str(e)))

        # assign request values to Controller properties
        controller.requested = requested
        controller.params = requested['params']
        controller.is_dev_server = self.is_dev_server
        controller.mode = self.mode
        controller.request_type = self.request_type
        controller.request = self.request

        # assign necessary Handler methods to Controller
        controller.redirect = self.redirect
        
        # return controller
        return controller

    def _call_action(self, controller):
        try:
            controller.init()
            requested_action = controller.requested['action'].replace('-', '_')
            method_ = getattr(controller, requested_action)
            method_()
            return controller.output.strip()
        except AttributeError, e:
            t_ = "unable to execute method '%s' in controller '%s' [controllers/%s.py]: %s"
            raise ControllerError( t_ % ( requested_action,
                controller.__class__.__name__,
                controller.requested['controller'],
                str(e) ))

    def _render_view(self, action_output):
        """
            Wrapper for render view types.  Default is mako.
        """
        # output_is_rendered flag signals final output is prepared (no need to
        # wrap in a layout template)
        if self.controller_.output_is_written:
            return action_output

        # use django templating
        if self.controller_.template_type == 'django':
            return self._render_django_view(action_output)

        # use mako templating (default)
        else:
            # note: action output was not produced by controller so is not
            # passed in method call
            return self._render_mako_view()

    def _respond(self, output):
        """sets response headers and sends http response to client"""
        # set controller headers
        if self.controller_.response_headers:
            for header,value in self.controller_.response_headers.items():
                self.response.headers[header] = value

        # write response
        self.response.out.write(output)

    #
    # view methods
    #
    def _render_mako_view(self):
        """
            Unlike django, the template must be included from the view template.
            re unicode: http://www.makotemplates.org/docs/usage.html#usage_using

            Note: action output is not used. The output is not prepared by
            the controller's render method.

            USAGE IN CONTROLLER:
            template_type   = 'mako'
            layout          = 'layout_name'
            ...
            self.set('content', 'lorem ipsum...)
            self.set('head_content', self.Html.css_link('/css/demo.css'))
            return self.render('view_name', '/layouts')
        """
        # these must be imported here, trying to import at top of module raises
        # an error
        from framework.vendor.mako.template import Template
        from framework.vendor.mako.lookup import TemplateLookup

        # view auto-rendering
        if self.controller_.auto_render and not self.controller_.render_was_called:
            self.controller_.render()

        # set layout dir
        layout_path = self._get_layout_path()
        layout_dir = dirname(layout_path)

        # create mako objects and render
        mako_lookup = TemplateLookup( directories=[layout_dir],
                                      output_encoding='utf-8',
                                      encoding_errors='replace' )
        mako_template = Template(filename=self.controller_.view_path,
            lookup=mako_lookup)
        return mako_template.render_unicode(**self.controller_.t).encode(
            'utf-8', 'replace')

    def _render_django_view(self, action_output):
        """
            Calls controller's render method (defined in BaseController) to
            write out output.

            If auto_render is set, method will call the controller's render
            method even if it was not called explicity in the action method

            If the Controller sets layout to empty, then the GAE response object
            should write out the output directly.
        """
        from google.appengine.ext.webapp import template as DjangoTpl

        # view auto-rendering
        if self.controller_.auto_render and not self.controller_.render_was_called:
            self.controller_.render()
            action_output = self.controller_.output

        layout_path = self._get_layout_path()

        if not layout_path:
            return action_output

        if not os.path.exists(layout_path):
            t_ = "expected view template file '%s' not found"
            raise ViewError(t_ % (layout_path))

        t = { 'controller_output' : action_output }
        t['head_content'] = self.controller_.t.get('head_content')
        t['flash'] = self.controller_.t.get('__flash__', '')
        t['config'] = c
        return DjangoTpl.render(layout_path, t)

    def _get_layout_path(self):
        """
            builds absolute layout path for view based on controller layout
            setting and template type
        """
        # set relative layout path based on controller's layout setting
        if not self.controller_.layout:
            layout_path = None
        elif self.controller_.layout.startswith('/') and (
            self.controller_.template_type != 'mako'):
            layout_path = self.controller_.layout[1:]
        elif self.controller_.layout.startswith('/') and (
            self.controller_.template_type == 'mako'):
            # for mako layout settings, we're looking for dir rather than full
            # path.  _render_mako_view will clip at the dirname, so we need
            # to add a dummy here
            layout_path = '%s/to_be_clipped' % self.controller_.layout[1:]
        else:
            layout_path = 'layouts/%s' % ( self.controller_.layout )

        # set full layout path and render layout
        ext = self.controller_.template_extension_map.get(
            self.controller_.template_type, '')
        if layout_path:
            layout_path = pathjoin(self.controller_.view_dir, layout_path + ext)

        return layout_path



class TestHandler(DispatchHandler):
    """
        Overrides DispatchHandler for test handling
    """
    def _call_action(self, ControllerObject):
        """for test handler, alway call dispatch method. That will handle the rest"""
        # limit to dev server only
        if not self.is_dev_server:
            ControllerObject.flash('testing is only available on the dev server')
            self.redirect('/demo/testing')

        method_ = getattr(ControllerObject, 'dispatch')
        return method_()

    def _load_controller(self, requested, dir='framework'):
        """test controller is in framwork directory rather than project"""
        return DispatchHandler._load_controller(self, requested, 'framework')


class SandboxHandler(webapp.RequestHandler):
    """
        A minimalistic example of a handler.  Useful for quick and dirty
        testing.
    """
    def test(self):
        """ test here """
        from random import randint
        Data = {
            'randint(1,100)' : randint(1,100),
            'note' : 'to update: edit SandboxHandler.test in dispatch.py'
        }
        self.render(Data)

    def get(self, path):
        return self.test()

    def post(self, path):
        return self.test()

    def render(self, Data={}):
        tpl = """<html><body>
<h2>Appswell Sandbox</h2>
<h5><a href="%s">logout</a> | <a href="/">home</a></h5>
<h4>Result</h4>
<pre>%s</pre>
</body></html>
"""
        return self.response.out.write( tpl % \
            (users.create_logout_url('/'), pformat(Data)) )



extend_framework_syspath()

app = webapp.WSGIApplication([
    (r'/sandbox(/?.*)', SandboxHandler),
    (r'/(test.*)', TestHandler),
    (r'/(.*)', DispatchHandler) ],
    debug=True)

