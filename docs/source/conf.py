# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# http://www.sphinx-doc.org/en/master/config
from docutils.parsers.rst import Directive

import sphinxemoji

import pydata_sphinx_theme

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath('../..'))


# -- Project information -----------------------------------------------------

project = 'fossdocs'
copyright = '2025, GlobalTech Translations'
author = 'Faycal Alami-Hassani'

# The full version, including alpha/beta/rc tags.
# release = sphinxemoji.__version__
# The short X.Y version.
# version = release.split('-')[0]


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "sphinx_design",
    "sphinx_copybutton",
    # For extension examples and demos
    "jupyter_sphinx",
    "matplotlib.sphinxext.plot_directive",
    # "nbsphinx",  # Uncomment and comment-out MyST-NB for local testing purposes.
    "numpydoc",
    "sphinx_togglebutton",
    'sphinxemoji.sphinxemoji',
    'myst_parser',
    'sphinx_markdown_tables',
    'sphinxcontrib.inkscapeconverter',
    'sphinxcontrib.httpdomain',
    'sphinxemoji.sphinxemoji',
    'sphinxext.photofinish',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# Dark mode as default

html_context = {
   "default_mode": "dark",
}


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.

html_title = "Fossdocs - technical docs made easy"

html_theme = 'pydata_sphinx_theme'
html_theme_options = {
    "logo": {
        "text": "fossdocs",
        "link": "https://fosstodon.org/@gnufcl",
    },
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/ka2in",
            "icon": "fab fa-github-square",
            "type": "fontawesome",
        },
        {
            "name": "Mastodon",
            "url": "https://fosstodon.org/@gnufcl",
            "icon": "fab fa-mastodon",
        },
   ],
    "navbar_start": "navbar-logo",
    "pygment_light_style": "tango",
    "pygment_dark_style": "native",
    "footer_start": "copyright",
    "footer_end": [],
    'collapse_navigation': True, # ToC options
    'navigation_depth': 4, # ToC options
}

source_suffix = {
    '.rst': 'restructuredtext',
    '.txt': 'markdown',
    '.md': 'markdown',
}

html_show_sphinx = False # Removing the mention "Built with Sphinx using a theme provided by Read the Docs."

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.

html_logo = "_static/circular-geometry.png"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']


# -- Options for LaTeX output -----------------------------------

latex_engine = 'lualatex'

latex_elements = {
    'fontpkg': r'''
\\usepackage{fontspec}
\setmainfont{Symbola}
''',
    'preamble': r'''
\usepackage[titles]{tocloft}
\cftsetpnumwidth {1.25cm}\cftsetrmarg{1.5cm}
\setlength{\cftchapnumwidth}{0.75cm}
\setlength{\cftsecindent}{\cftchapnumwidth}
\setlength{\cftsecnumwidth}{1.25cm}
''',
}

latex_show_urls = 'footnote'

# Grouping the document tree into LaTeX files. List of tuples# (source start file, target name, title, author, documentclass [howto/manual]).
latex_documents = [
 ('index', 'yourdoc.tex', u'bits4docs Documentation', u'GlobalTech Translations', 'manual'),
 ]

# Options for LaTeX output
latex_elements = {
  'extraclassoptions': 'openany,oneside',
  'fncychap' : r'\usepackage[Bjornstrup]{fncychap}',
  'printindex': r'\footnotesize\raggedright\printindex',
  'geometry': r'\usepackage{geometry}',
  'preamble': r'\usepackage[bottom]{footmisc}',

# Paper size ('letterpaper' or 'a4paper').
    'papersize': 'a4paper',

# Latex figure (float) alignment
    'figure_align': 'H',
}


class SphinxEmojiTable(Directive):
    """Directive to display all supported emoji codes in a table"""
    has_content = False
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = False

    def run(self):
        doc_source_name = self.state.document.attributes['source']

        codes = sphinxemoji.sphinxemoji.load_emoji_codes()

        lines = []
        lines.append('.. csv-table:: Supported emoji codes')
        lines.append('   :header: "Emoji", "Code"')
        lines.append('   :widths: 10, 40')
        lines.append('')
        for code in codes.items():
            lines.append('   {1},``{0}``'.format(*code))
        lines.extend(['', ''])
        self.state_machine.insert_input(lines, source=doc_source_name)

        return []

def setup(app):
    app.add_directive('sphinxemojitable', SphinxEmojiTable)
