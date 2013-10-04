"""
    Appswell Html Helper

    USAGE
    from lib.html_helper import HtmlHelper as html
    link = html.link('/', 'home')
"""
import sys, os, logging, inspect
from os.path import dirname, join



class HtmlHelper:

    def __init__(self):
        pass

    def link(self, path, label=None, new_window=None):
        t_ = '<a href="%s"%s>%s</a>'
        new = new_window and ' onclick="window.open(this.href,\'_blank\');return false;"' or ''
        if not label: label = path
        return t_ % ( path, new, label )

    def css_link(self, path, type='text/css'):
        t_ = '<link href="%s" rel="stylesheet" type="%s" />'
        return t_ % ( path, type )
