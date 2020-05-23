#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'suzuke'
SITENAME = u"suzuke's blog"
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Asia/Taipei'

DEFAULT_LANG = u'zh'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

# Markdown
MARKDOWN = {
    'extension_configs': {
        'markdown.extensions.codehilite': {'css_class': 'highlight', 'guess_lang':'False'},
        'markdown.extensions.extra': {},
        'markdown.extensions.meta': {},
    },
}

# Themes
THEME = '/Users/suzuke/Documents/Blog/pelican-themes/aboutwilson'

# Gittalk
GITALK_GITHUB_ID = 'suzuke'
REPO_TO_STORE_COMMENTS = 'suzuke.github.io'
OAUTH_CLIENT_ID = '9ffd664cad78b4b2b3d9'
OAUTH_CLIENT_SECRET = '8b28b366159e9e8c9a953a8f5a7bf9fc42cd4844'
