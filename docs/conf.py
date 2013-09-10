# -*- coding: utf-8 -*-
import os
import sys

sys.path.append(os.path.split(os.path.dirname(__file__))[0])

import zss
from better import better_theme_path

# -- General configuration ----------------------------------------------------

needs_sphinx = '1.0'
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.viewcode']
templates_path = ['_templates']
exclude_patterns = ['_build', 'subsections']
source_suffix = '.rst'

master_doc = 'index'

project = u'Zhang-Shasha'
copyright = u'2013 Tim Henderson and Steve Johnson'

# The short X.Y version.
version = zss.__version__.split('-')[0]
# The full version, including alpha/beta/rc tags.
release = zss.__version__

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# -- Options for HTML output --------------------------------------------------

html_theme = 'better'
html_theme_options = {
    'showrelbartop': False,
    'showrelbarbottom': False,
}
html_theme_path = [better_theme_path]
html_sidebars = {
    'index': ['localtoc.html'],
}

html_title = "%(project)s v%(release)s" % {
    'project': project,
    'release': release,
}

# these are included in index.rst
unused_docs = ['api.rst', 'examples.rst', 'references.rst']

html_short_title = "Home"
#html_logo = None
#html_favicon = None
html_static_path = ['_static']
html_use_smartypants = True

html_show_sphinx = True
html_show_copyright = True

# Output file base name for HTML help builder.
htmlhelp_basename = 'Zhang-Shashadoc'

html_context = {
    'docstitle': html_title,
}
