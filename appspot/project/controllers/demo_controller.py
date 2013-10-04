"""
    Demo Controller

    NOTES
        self.Html is a helper class for generating output
"""
#
# IMPORTS
#
# Python Standard Library
import sys, os, logging, inspect
from random import randint, sample
from pprint import pformat
from decimal import Decimal
from os.path import dirname, join as osjoin
from datetime import datetime
from cgi import escape

# App Engine Imports
from google.appengine.api import users
from google.appengine.ext.webapp.util import login_required

# Appswell
from config import core as c
from framework.lib.base_controller import BaseController
from framework.lib.gatekeeper import Gatekeeper
from framework.lib import multicache as memcache
#from framework.vendor.appengine_utilities import sessions
from framework.vendor.recaptcha.client import captcha
from project.models.simple_form import AppswellSimpleForm, AppswellSimpleModelForm
from project.models.simple_log import AppswellSimpleLog, AppswellSimpleLogModelForm
from project.vendor.klenwell import demo



#
# MODULE ATTRIBUTES
#



#
# CONTROLLER CLASS
#
class DemoController(BaseController):

    name            = 'DemoController'
    layout          = 'default'
    auto_render     = True

    # helper objects
    Gatekeeper      = Gatekeeper()

    def home(self):
        self.t['head_content'] += self.Html.css_link('/css/home.css')
        self.template_type = 'django'
        self.render('home', 'home')

    def index(self):
        self.t['head_content'] += self.Html.css_link('/css/demo.css')
        self.set('header', 'demo index')
        self.set('menu', self.Gatekeeper.get_controller_menu(self))
        self.set('data', 'pick an action from the menu at right' )
        self.template_type = 'django'
        #self.render('index') <- auto-renders

    def changelog(self):
        self.redirect('/presents/changelog')

    def framework(self):
        """
            Dump information related to framework or environment
        """
        subaction = self.params and self.params[0] or 'index'
        subheader = 'details'
        subcontent = ''
        pref = '<pre>%s</pre>'

        # subactions
        if subaction == 'version':
            version = 'available only in development server'
            if c.IS_DEV_SERVER:
                from google.appengine.tools import appcfg
                version = appcfg.GetVersionObject()
            subheader = "google app engine version (<tt>appcfg.GetVersionObject()</tt>)"
            subcontent = pref % (pformat(version))
        elif subaction == 'routemap':
            subheader = 'ROUTE_MAP from config'
            subcontent = pref % (pformat(c.ROUTE_MAP))
        elif subaction == 'environment':
            environ_data = {}
            try:
                for k in os.environ:
                    environ_data[k] = os.environ[k]
            except Exception, e:
                logging.error(e)
                environ_data = { 'error': e }
            subheader = 'os.environ'
            subcontent = pref % (pformat(environ_data))
        elif subaction == 'controller':
            subheader = 'appswell controller object __dict__'
            subcontent = pref % (pformat(self._get_controller_dict()))
        elif subaction == 'config':
            subheader = 'from config import core as c'

            k1 = "c.IS_DEV_SERVER"
            k2 = "c.SDK_VERSION"
            k3 = "c.DEMO"
            k4 = "c.acme.user"
            k5 = "c.acme.password"
            data = {
                k1 : c.IS_DEV_SERVER,
                k2 : c.SDK_VERSION,
                k3 : c.DEMO,
                k4 : c.acme.user,
                k5 : c.acme.password
            }

            subcontent = '<pre>%s</pre>' % (pformat(data))
        else:   # index
            subheader = "framework index"
            subcontent = "choose an option above"

        submenu = """
<ul>
<li><a href="/demo/framework">index</a></li>
<li><a href="/demo/framework/version">version</a></li>
<li><a href="/demo/framework/environment">environment</a></li>
<li><a href="/demo/framework/config">config</a></li>
<li><a href="/demo/framework/routemap">routemap</a></li>
<li><a href="/demo/framework/controller">controller object</a></li>
</ul>
"""
        contentf = """
<h3>framework information</h3>
<p>select an option below to display information on framework</p>
%s
<br />

<h4>%s</h4>
%s
"""
        # output
        content = contentf % (submenu, subheader, subcontent)
        self.set('head_content', self.Html.css_link('/css/demo.css'))
        self.set('menu', self.Gatekeeper.get_controller_menu(self))
        self.set('headline', 'framework')
        self.set('content', content)
        self.render('content')


    def templates(self):
        """
            Demo mako and django templates
        """
        subaction = self.params and self.params[0] or 'index'
        subaction2 = len(self.params) > 1 and self.params[1] or None
        subheader = 'details'
        subcontent = ''
        pref = '<pre>%s</pre>'

        # subactions
        if subaction == 'mako':

            self.template_type = 'mako'

            if subaction2 == 'auto':
                explanation = "This examples uses the mako template, as \
                    integrated within the appswell framework."
                self.set('menu', self.Gatekeeper.get_controller_menu(self))
                self.set('head_content', self.Html.css_link('/css/demo.css'))
                self.set('headline', 'mako auto-rendering test')
                self.set('explanation', explanation)

                # these are all equivalent
                #return self.render('test')
                #return self.render('test', 'layouts')
                return self.render('test', '/layouts')

            else:   # mako template
                app_root = os.path.dirname(os.path.dirname(__file__))
                from framework.vendor.mako.template import Template
                from framework.vendor.mako.lookup import TemplateLookup

                view_dict = {
                    '__flash__' : '',
                    'head_content' : self.Html.css_link('/css/demo.css'),
                    'menu' : self.Gatekeeper.get_controller_menu(self),
                    'headline' : 'mako test',
                    'explanation' : "This is an example that makes explicit \
                        use of the mako template, outside any special \
                        integration done by the appswell framework."
                }

                # set layout to empty and auto_render to false so that dispatch
                # will not attempt to automagically render path and we can
                # print output below
                self.layout = None
                self.auto_render = False

                # manually set and render mako template
                view_path = osjoin(app_root, 'views/demo/test.mako')
                layout_path = osjoin(app_root, 'views/layouts')
                MakoLookup = TemplateLookup( directories=[layout_path] )
                MakoTpl = Template(filename=view_path, lookup=MakoLookup)
                output = MakoTpl.render(**view_dict)
                return self.write(output)

        elif subaction == 'django':
            content = """
<p>this examples uses the default django templating</p>
<a href="/demo/templates">return to templates</a>
"""
            self.set('header', 'django example')
            self.set('subheader', '')
            self.set('menu', self.Gatekeeper.get_controller_menu(self))
            self.set('data', content)
            self.set('head_content', self.Html.css_link('/css/demo.css'))
            self.template_type = 'django'
            return self.render('index')

        else:
            subheader = "templates index"
            subcontent = "choose an option above"

        submenu = """
<ul>
<li><a href="/demo/templates">index</a></li>
<li><a href="/demo/templates/mako/template">mako template</a></li>
<li><a href="/demo/templates/mako/auto">mako auto</a></li>
<li><a href="/demo/templates/django">django</a></li>
</ul>
"""
        contentf = """
<h3>templating samples</h3>
<p>select an option below to demo a template</p>
%s
<br />

<h4>%s</h4>
%s
"""
        # output
        content = contentf % (submenu, subheader, subcontent)
        self.set('head_content', self.Html.css_link('/css/demo.css'))
        self.set('menu', self.Gatekeeper.get_controller_menu(self))
        self.set('headline', 'templates')
        self.set('content', content)
        self.render('content')


    def ajax(self):
        """makes an ajax request in the template to the services backend"""
        self.set('menu', self.Gatekeeper.get_controller_menu(self))
        self.render('ajax')


    def atom(self):
        subaction = self.params and self.params[0] or 'index'
        subheader = 'details'
        subcontent = ''
        pref = '<pre>%s</pre>'

        # subactions
        if subaction == 'builder':
            return self._atom_builder();
        else:
            import cgi
            import framework.vendor.google_api as google_api
            from gdata.service import GDataService
            client = GDataService()

            feed_url = 'http://code.google.com/feeds/p/appswell/hgchanges/basic'
            feed = client.Get(feed_url, converter=None)
            #logging.info(dir(feed))

            data = {
                'feed' : feed.__dict__,
                'first entry' : feed.entry[0].__dict__
            }
            subheader = 'atom consumer'
            subcontent_t = """
<h4>sample feed data</h4>
    <table class="data">
        <tr>
            <td class="label">feed.GetSelfLink().href</td>
            <td class="value">%s</td>
        </tr>
        <tr>
            <td class="label">feed.title.text</td>
            <td class="value">%s</td>
        </tr>
        <tr>
            <td class="label">feed.entry[0].title.text</td>
            <td class="value">%s</td>
        </tr>
        <tr>
            <td class="label">feed.entry[0].content.text</td>
            <td class="value">%s</td>
        </tr>
        <tr>
            <td class="label">feed.entry[0].updated.text</td>
            <td class="value">%s</td>
        </tr>
    </table>
<br />
<h4>feed object</h4>
    <pre>%s</pre>
"""
            subcontent = subcontent_t % ( feed.GetSelfLink().href,
                                          feed.title.text,
                                          self._ascii(feed.entry[0].title.text),
                                          self._ascii(feed.entry[0].content.text),
                                          feed.entry[0].updated.text,
                                          cgi.escape(pformat(data, indent=2)) )

        submenu = """
<ul>
<li><a href="/demo/atom/consumer">consumer</a></li>
<li><a href="/demo/atom/builder">builder</a></li>
</ul>
"""
        contentf = """
<h5>
    powered by
    <a href="http://code.google.com/p/gdata-python-client/">google data library</a>
</h5>
<p>select an option below</p>
%s
<br />

<h3>%s</h3>
%s
"""
        # output
        content = contentf % (submenu, subheader, subcontent)
        self.set('head_content', self.Html.css_link('/css/demo.css'))
        self.set('menu', self.Gatekeeper.get_controller_menu(self))
        self.set('headline', 'atom')
        self.set('content', content)
        self.render('content')


    def _atom_builder(self):
        import framework.vendor.google_api
        import atom

        feedauthor = atom.Author(name = atom.Name(text='klenwell@gmail.com'))
        feedtitle = atom.Title(text = "Sample Atom Feed")
        feedlink = atom.Link(href = "http://appswell.appspot.com/demo/atom_builder")
        feedid = atom.Id(text="urn:uuid:aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee")
        #time = datetime.datetime.now().isoformat()
        feedupdated = atom.Updated("2010-01-27T12:00:00Z")

        entries = []
        e_title   = atom.Title(text="A Sample Atom Feed")
        e_link    = atom.Link(href= "/demo/atom")
        e_id      = atom.Id(text="urn:uuid:aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeef")
        e_updated = atom.Updated("2010-01-27T12:00:00Z")
        e_summary = atom.Summary(text="A sample feed entry.  Click title to return to demo atom menu.")
        entries.append( atom.Entry(title=e_title, link=e_link, atom_id=e_id, summary=e_summary))

        feed = atom.Feed(entry=entries, title=feedtitle, link=feedlink, atom_id=feedid, updated=feedupdated)

        self.set_header("Content-Type", "application/atom+xml")
        self.write(str(feed))


    def hello_world(self):
        self.t['head_content'] += self.Html.css_link('/css/demo.css')
        self.set('header', 'hello world')
        self.set('menu', self.Gatekeeper.get_controller_menu(self))
        self.set('data', 'a simple hello world example: also available as <a href="/hello">/hello</a>')
        self.template_type = 'django'
        self.render('index', 'default')


    def __sessions(self):
        """
            TODO(klenwell): re-enable when session replaced
        
            Session module part of gaeutilities package:
            http://code.google.com/p/gaeutilities/
        """
        Session = sessions.Session()
        if self.has_param('stop', 1):
            Session.delete_item('test_start')

        # session not yet started
        if not 'test_start' in Session:
            Session['test_start'] = datetime.now()
            session_age = 'new session started at %s' % (Session['test_start'])

        # session exists
        else:
            session_age = datetime.now() - Session['test_start']
            hm = 'session age is %s' % (session_age)

        Data = {
            'session age' : str(session_age),
            'stop session' : self.Html.link('/demo/sessions/stop', 'click here'),
            'source' : self.Html.link(
                'http://code.google.com/p/gaeutilities/source/browse/trunk/appengine_utilities/sessions.py',
                'click here', True),
            'session object': Session.__dict__
        }

        self.t['head_content'] += self.Html.css_link('/css/demo.css')
        self.set('header', 'session demo')
        self.set('subheader', '<h5>powered by %s</h5><br />' % \
            ( self.Html.link('http://code.google.com/p/gaeutilities/', \
                             'gaeutilities', True) ))
        self.set('menu', self.Gatekeeper.get_controller_menu(self))
        self.set('data', '<pre>%s</pre>' % pformat(Data))
        self.template_type = 'django'
        self.render('index', 'default')


    def sitemap(self):
        """TO DO: dynamic generation"""
        url_list = """\
http://appswell.appspot.com/
http://appswell.appspot.com/demo
"""

        # prepare output
        self.layout = None
        self.auto_render = False
        self.template_type = 'output'
        self.set_header("Content-Type", "text/plain")
        #self.output = str(feed)
        self.write(str(url_list))


    def vendor_test(self):
        from project.vendor.klenwell.demo import VendorDemo

        # test
        VendorTest = VendorDemo()
        Data = {
            'VendorTest.is_loaded' : VendorTest.is_loaded == True and 'success' or 'failure',
            'VendorTest.test()' : VendorTest.test() == 'success' and 'success' or 'failure'
        }

        # output
        self.t['head_content'] += self.Html.css_link('/css/demo.css')
        self.set('header', 'testing vendor import')
        self.set('subheader', 'test results')
        self.set('menu', self.Gatekeeper.get_controller_menu(self))
        self.set('data', '<pre>%s</pre>' % pformat(Data))
        self.template_type = 'django'
        self.render('index', 'default')


    def model(self):
        """
            Display last 10 SimpleLog records
        """
        num_records = 10
        RecentLogs = AppswellSimpleLog.gql('ORDER BY created DESC LIMIT %s' % \
            (num_records))

        self.t['head_content'] += self.Html.css_link('/css/demo.css')
        self.set('menu', self.Gatekeeper.get_controller_menu(self))
        self.set('RecentLogs', RecentLogs)
        self.set('num_records', num_records)
        self.render('model')

    #@login_required
    # NOTE: this decorator does not work with the appswell dispatcher
    def __email(self):
        """
            TODO(klenwell): re-enable when session replaced
        
            Allow user to email self.  Also demonstrates login requirement.

            The login_required decorator above is superfluous as the login
            requirement is also set in app.yaml for this action.

            google docs:
            http://code.google.com/appengine/docs/python/config/appconfig.html#Requiring_Login_or_Administrator_Status
            http://code.google.com/appengine/docs/python/users/userclass.html
            http://code.google.com/appengine/docs/python/mail/sendingmail.html
            http://code.google.com/appengine/docs/python/tools/devserver.html#Using_Mail
        """
        email_message_t = """
This message was sent from %s/demo/email.
It was sent as a demonstration of the Google App Engine
email function. The user was required to sign in to his
or her Gmail send this message.

If you did not request this message, we apologize for any
inconvenience. If you believe our service is being abused,
please feel free to contact Tom at klenwell@gmail.com.
"""
        feedback = ''
        show_form = False
        email_message = email_message_t % (os.environ.get('SERVER_NAME'))

        Session = sessions.Session()
        user = users.get_current_user()

        if not user:
            self.flash('you must log in with your Google account')
            self.redirect('/')

        # request email: send
        if self.request.POST.get('send_email'):
            from google.appengine.api import mail

            to_email = user.email()
            to_name = user.nickname()
            SimpleLog = AppswellSimpleLog()

            try:
                mail.send_mail(
                    sender='Appswell Email Demo <klenwell@gmail.com>',
                    to='%s <%s>' % (to_name, to_email),
                    subject='Appswell Email Demo',
                    body=email_message )

                feedback = 'Your message has been queued for delivery.  Check your Google Account email.'
                Session['sent_email'] = True
                log_msg = 'sent test email to %s' % (to_name)
                SimpleLog.log('email', log_msg, 'system')

            except Exception, e:
                feedback = 'there was a problem sending the email: %s' % (str(e))
                error_msg = 'unable to send test email: %s' % (str(e))
                SimpleLog.log('email', error_msg, 'error')
                logging.error(error_msg)

        # limit possible abuse
        elif Session.get('sent_email'):
            feedback = 'an email has been sent to your address %s' % (user.email())

        # else show form
        else:
            show_form = True

        # output
        self.set('head_content', self.Html.css_link('/css/demo.css'))
        self.set('menu', self.Gatekeeper.get_controller_menu(self))
        self.set('feedback', feedback)
        self.set('email_message', email_message)
        self.set('user_email', user.email())
        self.set('show_form', show_form)
        self.render('email')


    def multicache(self):
        """
            google docs:
            http://code.google.com/appengine/docs/python/memcache/functions.html
        """
        import config.cache

        cache_key = 'memcache_demo'
        CacheConfig = config.cache.Memcache.get(cache_key, 'default')
        cache_len = CacheConfig.get('duration', 60)
        display_t = '<span class="%s">%s</span>: %s';

        cache = memcache.get(cache_key)
        if cache is not None:
            display = display_t % ('hit', 'cache found', cache)
        else:
            cache = 'cache saved <b>%s</b> (will be saved for %s seconds)' % \
                ( datetime.now().strftime('%Y-%m-%d %H:%M:%S'), cache_len )
            memcache.set(cache_key, cache, cache_len)
            display = display_t % ('miss', 'cache not found', \
                'saving new cache (reload page to see content)')

        # prepare content
        content_t = """
<p>
Multicache is a simple wrapper for the Google App Engine's Memcache library that
enables it to store items larger than the 1 MB limit.
</p>
<p>
For additional details on usage, see the
<a href="http://code.google.com/p/appswell/source/browse/appspot/lib/multicache.py?spec=svn116329ce59bd52af14388fedf2cdac7015d67fbe&name=v1s11-branch&r=116329ce59bd52af14388fedf2cdac7015d67fbe">multicache</a>
and
<a href="http://code.google.com/p/appswell/source/browse/appspot/test/unit/test_multicache.py?spec=svn116329ce59bd52af14388fedf2cdac7015d67fbe&name=v1s11-branch&r=116329ce59bd52af14388fedf2cdac7015d67fbe">unit test</a>
source code.
</p>
<div class="cache_demo">
    <p>%s</p>
    <small>current time: %s</small>
</div>
"""
        content = content_t % (display, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        # prepare output
        self.set('head_content', self.Html.css_link('/css/demo.css'))
        self.set('menu', self.Gatekeeper.get_controller_menu(self))
        self.set('headline', 'multicache')
        self.set('content', content)
        self.render('content')


    def recaptcha(self):
        """
            Post recaptcha challenge to SimpleLog
            ref: http://daily.profeth.de/2008/04/using-recaptcha-with-google-app-engine.html
        """
        # recaptcha html
        recaptcha_html = captcha.displayhtml(
            public_key = c.RECAPTCHA_PUBLIC_KEY,
            use_ssl = False,
            error = None)

        if self.request_type == 'POST':
            #SimpleModelForm = AppswellSimpleModelForm(self.Request.POST)
            captcha_response = captcha.submit(
                self.request.POST.get("recaptcha_challenge_field", None),
                self.request.POST.get("recaptcha_response_field", None),
                c.RECAPTCHA_PRIVATE_KEY,
                self.request.remote_addr )

            if not captcha_response.is_valid:
                recaptcha_html = captcha.displayhtml(
                    public_key = c.RECAPTCHA_PUBLIC_KEY,
                    use_ssl = False,
                    error = captcha_response.error_code)
                self.flash('recaptcha failed: %s' % (captcha_response.error_code))

            #elif SimpleModelForm.is_valid():
            elif captcha_response.is_valid:
                SimpleLog = AppswellSimpleLog()
                SimpleLog.log('demo',
                    'recaptcha: %s' % (self.request.POST['recaptcha_response_field']),
                    'system')
                logging.info('successful recaptcha: %s' % self.request.POST['recaptcha_response_field'])
                self.flash('recaptcha successful: Simplelog update')
                return self.redirect('/demo/model')

        # render mako view
        self.template_type = 'mako'
        self.set('recaptcha_html', recaptcha_html)
        self.set('menu', self.Gatekeeper.get_controller_menu(self))
        self.set('head_content', self.Html.css_link('/css/demo.css'))
        self.render('recaptcha')


    def twitter(self):
        """
            Basic twitter API examples using tweepy
            see http://joshthecoder.github.com/tweepy/docs/api.html#timeline-methods
        """
        warning = ''
        UserTimeline = []
        lib_home = 'https://github.com/joshthecoder/tweepy'

        # set up twitter object
        from framework.vendor import tweepy

        # set screen name
        screen_name = self.params and self.params[0] or c.TWITTER_USER

        # dump option
        dump = (screen_name == 'dump')
        if dump:
            screen_name = c.TWITTER_USER

        # get recent posts
        try:
            public_tweets = tweepy.api.user_timeline(screen_name)
        except twython.core.TwythonError, e:
            logging.error('Twython Error: %s' % str(e))

        # prepare output
        if public_tweets and dump:
            tweet_object = public_tweets[0]
            subheader = 'most recent status object dump for %s' % (screen_name)
            subcontent = '<pre>%s</pre>' % (pformat(tweet_object.__getstate__()))
        elif public_tweets:
            lif = '<li><tt>[%s]</tt> %s</li>'
            TweetList = []
            for tweet in public_tweets:
                TweetList.append(lif % (str(tweet.created_at), tweet.text))
            subheader = 'user timeline for <a href="%s">%s</a>' % \
                ('http://twitter.com/klenwell', screen_name)
            subcontent = '<ul>%s</ul>' % ('\n'.join(TweetList))
        else:
            subheader = "unable to retrieve timeline for %s" % (screen_name)
            subcontent = 'try <a href="/demo/twitter/klenwell">klenwell</a>'

        # output
        contentf = """
<h5>
    powered by <a href="%s">tweepy</a>
</h5>
<br />

<h4>%s</h4>
%s
"""
        content = contentf % (lib_home, subheader, subcontent)
        self.set('head_content', self.Html.css_link('/css/demo.css'))
        self.set('menu', self.Gatekeeper.get_controller_menu(self))
        self.set('headline', 'twitter')
        self.set('content', content)
        self.render('content')


    def simple_form(self):
        """
            A simple form demonstrating the interaction of controller, model,
            modelform (see simple_form.py in models), and template.

            Notice the use of as_table method by modelform object SimpleModelForm
        """
        # form submitted
        if self.request_type == 'POST':
            SimpleModelForm = AppswellSimpleModelForm(self.request.POST)
            if SimpleModelForm.is_valid():      # this step technically redundant
                if SimpleModelForm.save():
                    self.flash('link <b>%s</b> saved : thank you!' % \
                        (SimpleModelForm.cleaned_data.get('url', 'n/a')))
                    SimpleModelForm = AppswellSimpleModelForm()     # resets form
            else:
                self.flash('there was a problem with the form : see below')

        # new form (no submission)
        else:
            SimpleModelForm = AppswellSimpleModelForm()

        # prepare view
        DataView = {
            'controller': self._get_controller_dict(),
            'POST' : self.request.POST.__dict__,
            #'self.request' : self.request,
            "self.Request.POST.get('url')" : self.request.POST.get('url'),
            'is_valid' : SimpleModelForm.is_valid(),
        }

        self.t['head_content'] += self.Html.css_link('/css/demo.css')
        self.set('menu', self.Gatekeeper.get_controller_menu(self))
        self.set('data', pformat(DataView))
        self.set('simple_form', SimpleModelForm.as_table())
        self.set('datastore', pformat(AppswellSimpleForm.find_last_n(5)))
        self.template_type = 'django'
        self.render('simple_form', 'default')

    def testing(self):
        # prepare content
        source_link = "%s%s" % (
        "http://code.google.com/p/appswell/source/browse",
        "/appspot/project/test/unit/template.py?name=appswell-core")

        content = """
<p>The Appswell package includes a testing harness. It is not available from the
appspot server but can be found locall on the dev_appserver at
<a href="/test">/test</a>.</p>

<p>A sample test can be found in the source code. It is available online here:
<a href="%s">unit test template</a></p>

<br />
<h4>screenshot</h4>
<img src="/img/appswell_tests_screenshot.png" title="unit test screenshot"
alt="unit test screenshot" style="padding:8px;" />
""" % (source_link)

        # prepare output
        self.set('head_content', self.Html.css_link('/css/demo.css'))
        self.set('menu', self.Gatekeeper.get_controller_menu(self))
        self.set('headline', 'testing')
        self.set('content', content)
        self.render('content')


    def _get_controller_dict(self):
        """
            Return controller's dict after stripping any sensitive information
        """
        # collect request attrs
        request_attrs = []
        for a in dir(self.request):
            try:
                if a.startswith('_'):
                    continue
                request_attr =(a, escape(str(type(getattr(self.request,a)))))
                request_attrs.append(request_attr)
            # need to catch some deprecation warnings added in 1.7.5
            except DeprecationWarning:
                pass

        co = self.__dict__.copy()

        # set view parameters
        co['config'] = {}
        co['Request'] = escape(str(type(self.request)))
        co['Request attrs'] = request_attrs
        co['self.request.POST'] = self.request.POST
        co['self.request.GET'] = self.request.GET
        co['self.has_param("controller")'] = self.has_param("controller")
        co['self.get_param(1)'] = self.get_param(1)
        return co

    def _ascii(self, text):
        return unicode(text, errors='ignore').replace("\0", "") \
            .encode('ascii', 'ignore')
