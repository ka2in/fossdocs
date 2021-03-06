# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = 'fossdocs'
copyright = '2022, GlobalTech Translations'
author = 'GlobalTech Translations'

# The full version, including alpha/beta/rc tags
release = '1.0'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
import sys, os, sphinx_rtd_theme

sys.path.insert(0, os.path.abspath('../..'))

extensions = [
    'myst_parser',
	'sphinx_rtd_theme',
    'sphinx_markdown_tables',
    'sphinxcontrib.inkscapeconverter',
    'sphinxcontrib.httpdomain',
    'sphinxemoji.sphinxemoji',
    'sphinxext.photofinish',
]

source_suffix = {
    '.rst': 'restructuredtext',
    '.txt': 'markdown',
    '.md': 'markdown',
}

# Setting a consistent emoji style

sphinxemoji_style = 'twemoji'

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# The encoding of source files.
#
# source_encoding = 'utf-8-sig'

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# The master toctree document.
master_doc = 'index'

# -- Adding options for TOC ------------------------------------------------

html_theme_options = {
    'collapse_navigation': True,
    'sticky_navigation': True,
    'navigation_depth': 4,
    'includehidden': True,
    'titles_only': False
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Adding settings for custom css file in the _Static folder
def setup(app):
  app.add_css_file('css/custom.css')

#Disable the option 'View page source' on the homepage

html_show_sourcelink = False

# Enable numref
# The numref role is used to reference numbered elements of the documentation. For example, tables and images.

#numfig = True
#numfig_secnum_depth = 1

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.

html_logo = "pics/circular-geometry.png"


# LaTeX customization for PDF
latex_engine = 'xelatex'

latex_elements = {
    'fontpkg': r'''
\usepackage{Noto Color Emoji}
''',
    'preamble': r'''
\usepackage[titles]{tocloft}
\cftsetpnumwidth {1.25cm}\cftsetrmarg{1.5cm}
\setlength{\cftchapnumwidth}{0.75cm}
\setlength{\cftsecindent}{\cftchapnumwidth}
\setlength{\cftsecnumwidth}{1.25cm}
''',
    'pxunit': '1bp',
}

# Using Symbola font to improve emoji support in PDFs

class SphinxEmojiTable:
    """Directive to display all supported emoji codes in a table"""
    has_content = False
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = False
    def run(self):
        doc_source_name = self.state.document.attributes['source']
        codes = get_data('sphinxemoji', 'codes.json')
        codes = json.loads(codes)
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
# Latex figure float alignment. Whenever an image doesn???t fit into the current page, it will be ???floated??? into the next page but may be preceded by any other text. 
# If you don???t like this behavior, use ???H??? which will disable floating and position figures strictly in the order they appear in the source.

    'figure_align': 'H',
}

# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'test', u'test Documentation',
     [author], 1)
]

# If true, show URL addresses after external links.
#
# man_show_urls = False


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'test', u'test Documentation',
     author, 'test', 'One line description of project.',
     'Miscellaneous'),
]