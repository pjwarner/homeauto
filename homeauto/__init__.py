#!/usr/bin/env python
#!/usr/bin/env python

from flask import Flask
app = Flask(__name__)

import pyjade
import markdown
from CommonMark import CommonMark

@pyjade.register_filter('markdown')
@pyjade.register_filter('md')
def filter_markdown(text, ast):
    return markdown.markdown(text)

@pyjade.register_filter('commonmark')
@pyjade.register_filter('cm')
def filter_commonmark(text, ast):
    parser = CommonMark.DocParser()
    renderer = CommonMark.HTMLRenderer()
    return renderer.render(parser.parse(text))

app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')

import homeauto.views
