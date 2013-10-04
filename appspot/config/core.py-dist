"""
    Appswell Core Configuration File for Google App Engine

    USAGE
        from config import core as c

    Configurable Settings in this File:

    ROUTE_MAP
    Maps path (0-index) to new path (1-index).  I use a list of tuples instead
    of a dict because ordering is significant if we're to allow multiple
    routings.  ROUTE_MAP entries will override each other, so given:

        ROUTE_MAP = [
            ('hello', 'hello/world'),
            ('hello/world', 'mock/test')
        ]

    a request to /hello would be directed to /mock/test

    MODE_MAP
    These can be used to vary settings and behavior according to the server
    environment in which app is being run.  MODE_MAP values are a tuple of
    server names (os.environ['SERVER_NAME']).  Defaults to the more restrictive
    PROD (production) setting.

    ADDITIONAL CONFIG FILES
    Import other config files here to incorporate them into the core module.
    For instance, by creating a file acme.py in the config dir with settings
    user and password and then importing it here, you can use config.acme.user
    anywhere you import config.
"""
# Import some magical values from __init__ file
from __init__ import (SDK_VERSION, IS_DEV_SERVER, TEST_MODE, PROD_MODE)

#
# Project Config Settings
#

# Route Map: simplified routing
ROUTE_MAP = [
    # (path, substitute)
    ('', 'presents/home'),
    ('index', 'presents/home'),
    ('usage', 'presents/usage'),
    ('routemap/test', 'presents/home'),
    ('sitemap.txt', 'demo/sitemap'),
]

# Mode Map: sets debug mode according to domain
MODE_MAP = {
    TEST_MODE   : ( 'localhost' ),
    PROD_MODE   : ( 'appswell.appspot.com', 'appswell.klenwell.com' )
}

# ReCaptcha Keys
RECAPTCHA_PUBLIC_KEY    = 'FOO'
RECAPTCHA_PRIVATE_KEY   = 'FOO'

# Twitter Settings (See http://goo.gl/rxhl)
TWITTER_CONSUMER_KEY    = 'FOO'
TWITTER_CONSUMER_SECRET = 'FOO'
TWITTER_ACCESS_KEY      = 'FOO'
TWITTER_ACCESS_SECRET   = 'FOO'

# Google Settings
GOOGLE_GA_CODE          = 'UA-XXXXXXX-XX'
GOOGLE_WEBTOOL_META     = 'FOO'
