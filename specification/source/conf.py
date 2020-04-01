#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
import sphinx_bootstrap_theme

sys.path.append(os.path.abspath('.'))

# General information about the project.
project = 'LinkageJS'
doc_title = 'LinkageJS Requirements Specification'
doc_version = 'V1 - First Release for Solicitation'
copyright = '2017-2019 The Regents of the University of California through Lawrence Berkeley National Laboratory. All rights reserved'

# Extensions

extensions = [
    'sphinxcontrib.bibtex',
    'sphinx.ext.autodoc',
    'sphinx.ext.mathjax',
    'sphinx.ext.todo',
]

# Rst_prolog is a string of reStructuredText that will be included at the beginning of every source file that is read.

rst_prolog = '''
.. role:: underline
   :class: underline

.. |project| replace:: {project}

.. |doc_title| replace:: {doc_title}

.. |doc_version| replace:: {doc_version}
'''.format(project=project, doc_title=doc_title, doc_version=doc_version)

# mathjax_path
mathjax_path = 'https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.6/MathJax.js?config=TeX-AMS-MML_HTMLorMML'

todo_include_todos = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The encoding of source files.
source_encoding = 'utf-8'

# The master toctree document.
master_doc = 'index'

# The short X.Y version.
version = ''
# The full version, including alpha/beta/rc tags.
release = ''

# List of documents that shouldn't be included in the build.
#unused_docs = []

# List of directories, relative to source directory, that shouldn't be searched
# for source files.
exclude_trees = []
exclude_patterns = ['templates']

# If true, '()' will be appended to :func: etc. cross-reference text.
add_function_parentheses = True

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# -- Options for HTML output ---------------------------------------------------

# Activate the theme.
html_theme = 'bootstrap'
html_theme_path = sphinx_bootstrap_theme.get_html_theme_path()

# Theme options are theme-specific and customize the look and feel
html_theme_options = {
    'navbar_title': project,
    'nosidebar': True,
    'body_min_width': '100%',
    # Render the next and previous page links in navbar. (Default: true)
    'navbar_sidebarrel': True,
    # Render the current pages TOC in the navbar. (Default: true)
    'navbar_pagenav': True,
    # Tab name for the current pages TOC. (Default: 'Page')
    'navbar_site_name': 'Site',
    'navbar_pagenav_name': 'Page',
    # Global TOC depth for 'site' navbar tab. (Default: 1)
    # Switching to -1 shows all levels.
    'globaltoc_depth': 3,
    # Include hidden TOCs in Site navbar?
    'globaltoc_includehidden': True,
    # HTML navbar class (Default: 'navbar') to attach to <div> element.
    # For black navbar, do 'navbar navbar-inverse'
    'navbar_class': 'navbar',
    # Fix navigation bar to top of page?
    'navbar_fixed_top': True,
    # Location of link to source.
    'source_link_position': 'footer',
}

html_last_updated_fmt = '%b, %d, %Y'

# The name for this set of Sphinx documents.
html_title = doc_title

# The name of an image file (within the static path) to use as favicon of the
# docs. This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
html_favicon = '_static/lbl-icon.ico'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named 'default.css' will overwrite the builtin 'default.css'.
html_static_path = ['_static']

# If true, links to the reST sources are added to the pages.
html_show_sourcelink = False

# Output file base name for HTML help builder.
htmlhelp_basename = 'Documentation'

#supported_image_types
supported_image_types = ['image/svg+xml', 'image/png', 'image/gif', 'image/jpeg']

# Number figures in html output
numfig = True

# -- Options for LaTeX output --------------------------------------------------

latex_additional_files = ['_static/latex-note.png', '_static/latex-warning.png']

# Grouping the document tree into LaTeX files.
latex_documents = [
  ('index',
   '{}.tex'.format(project),
   doc_title,
   doc_version,
   'manual'),
]

release = ''
latex_elements = {
  'classoptions': ', openany',  # remove blank pages in PDF.
  'releasename': '',
  'babel': '\\usepackage[english]{babel}',
}

latex_logo = '_static/lbl-icon.png'

latex_use_parts = False

# Additional stuff for the LaTeX preamble.
latex_elements['preamble'] = r'''
% The pdf output has too large picture compared to the html output.
% The next statement reduces the figure size
\pdfpxdimen=0.75\sphinxpxdimen

% Format of chapter fonts
\makeatletter
\ChNameVar{\raggedleft\sf\bfseries\Large} % sets the style for name
\ChNumVar{\raggedleft\sf\bfseries\Large} % sets the style for name
\ChTitleVar{\raggedleft\sf\bfseries\Large} % sets the style for name
\makeatother


\usepackage[scaled]{helvet}
\usepackage[helvet]{sfmath}

%% Fontsizes according to guideline from Andreas Eckmanns, Aug. 2018
\usepackage{sectsty}
\chapterfont{\fontsize{24}{26}\selectfont}
\sectionfont{\fontsize{14}{16}\selectfont}
\subsectionfont{\fontsize{12}{14}\selectfont}

%\usepackage[T1]{fontenc}
%%\titleformat*{\chapter}{\fontencoding{OT1}\fontfamily{cmr}\fontseries{m}%
%%  \fontshape{n}\fontsize{24pt}{24}\selectfont}
%%\titleformat*{\section}{\fontencoding{OT1}\fontfamily{cmr}\fontseries{m}%
%%  \fontshape{n}\fontsize{6pt}{6}\selectfont}
%%\titleformat*{\subsection}{\fontencoding{OT1}\fontfamily{cmr}\fontseries{m}%
%%  \fontshape{n}\fontsize{12pt}{12}\selectfont}
%%\titleformat*{\subsubsection}{\fontencoding{OT1}\fontfamily{cmr}\fontseries{m}%
%%  \fontshape{n}\fontsize{11pt}{11}\selectfont}
\titleformat*{\paragraph}
  {\rmfamily\slshape}
  {}{}{}
  \titlespacing{\paragraph}
  {0pc}{1.5ex minus .1 ex}{0pc}

\renewcommand\familydefault{\sfdefault}
\renewcommand{\baselinestretch}{1.1}


\usepackage{xcolor}
\definecolor{OldLace}{rgb}{0.99, 0.96, 0.9}
\definecolor{light-gray}{gray}{0.95}
\sphinxsetup{%
  verbatimwithframe=false,
  VerbatimColor={named}{light-gray},
%  TitleColor={named}{DarkGoldenrod},
%  hintBorderColor={named}{LightCoral},
  attentionborder=3pt,
%  attentionBorderColor={named}{Crimson},
%  attentionBgColor={named}{FloralWhite},
  noteborder=2pt,
  noteBorderColor={named}{light-gray},
  cautionborder=3pt,
%  cautionBorderColor={named}{Cyan},
%  cautionBgColor={named}{LightCyan}
}


\usepackage{sectsty}
\definecolor{lbl}{RGB}{2, 46, 77}
\chapterfont{\color{lbl}}  % sets colour of chapters
\sectionfont{\color{lbl}}  % sets colour of sections
\subsectionfont{\color{lbl}}  % sets colour of sections


% Reduce the list spacing
\usepackage{enumitem}
\setlist{nosep} % or \setlist{noitemsep} to leave space around whole list

% This allows adding :cite: in the label of figures.
% It is a work-around for https://github.com/mcmtroffaes/sphinxcontrib-bibtex/issues/92
\usepackage{etoolbox}
\AtBeginEnvironment{figure}{\renewcommand{\phantomsection}{}}



\renewcommand{\chaptermark}[1]{\markboth{#1}{}}
\renewcommand{\sectionmark}[1]{\markright{\thesection\ #1}}


\setcounter{secnumdepth}{3}
\usepackage{amssymb,amsmath}

% Figure and table caption in italic fonts
\makeatletter
\renewcommand{\fnum@figure}[1]{\small \textit{\figurename~\thefigure}: \it }
\renewcommand{\fnum@table}[1]{\small \textit{\tablename~\thetable}: \it }
\makeatother

% The next two lines patch the References title
\usepackage{etoolbox}
\patchcmd{\thebibliography}{\chapter*}{\phantom}{}{}

\definecolor{TitleColor}{rgb}{0 ,0 ,0} % black rathern than blue titles

\renewcommand{\Re}{{\mathbb R}}
\newcommand{\Na}{{\mathbb N}}
\newcommand{\Z}{{\mathbb Z}}

\usepackage{listings}
% see: http://mirror.aarnet.edu.au/pub/CTAN/macros/latex/contrib/listings/listings-1.3.pdf
\lstset{%
  basicstyle=\small, % print whole listing small
  keywordstyle=\color{red},
  identifierstyle=, % nothing happens
  commentstyle=\color{blue}, % white comments
  stringstyle=\color{OliveGreen}\it, % typewriter type for strings
  showstringspaces=false,
  numbers=left,
  numberstyle=\tiny,
  numbersep=5pt} % no special string space

\lstset{
    frame=single,
    breaklines=true,
    postbreak=\raisebox{0ex}[0ex][0ex]{\ensuremath{\color{red}\hookrightarrow\space}}
}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\lstdefinelanguage{Modelica}{%
  morekeywords={Thermal,HeatTransfer,Interfaces, flow, %
    SI,Temperature,HeatFlowRate,HeatPort},
  morecomment=[l]{//},
  morecomment=[s]{/*}{*/},
  morestring=[b]",
  emph={equation, partial, connector, model, public, end, %
    extends, parameter}, emphstyle=\color{blue},
}

\usepackage[margin=0.75in, includehead, includefoot, centering]{geometry}

% Replace the threeparttable as it causes the caption to
% be no wider than the table, which looks quite bad.
% Also, center the caption and table.
%\renewenvironment{threeparttable}{ \begin{table}\centering }{ \end{table} }
% Increase distance of caption
\belowcaptionskip=5pt


\pagestyle{normal}
\renewcommand{\chaptermark}[1]{\markboth{#1}{}}
\renewcommand{\sectionmark}[1]{\markright{\thesection\ #1}}
\fancyhf{}
\fancyhead[LE,RO]{\thepage}
\fancyhead[RE]{\leftmark}
\fancyhead[LO]{\rightmark}
\fancypagestyle{plain}{%
   \fancyhead{} % get rid of headers
   \fancyhead[R]{\leftmark}
   \fancyfoot[R]{\thepage}
   \fancyfoot[L]{}
   \renewcommand{\headrulewidth}{0.5pt} % and the line
}

%%\rfoot[LE,RO]{\thepage}
%%\renewcommand{\headrulewidth}{0.4pt}
%%\renewcommand{\footrulewidth}{0.4pt}

\renewcommand{\chaptermark}[1]{\markboth{#1}{}}
\renewcommand{\sectionmark}[1]{\markright{\thesection\ #1}}

\renewcommand{\chaptermark}[1]{\markboth{#1}{}}
\renewcommand{\sectionmark}[1]{\markright{\thesection\ #1}}

%\hypersetup{hidelinks = true} % Makefile enables this for the 2 page printout

% Set format of table of content. Otherwise, the titles stick to the page numbers in some cases
\usepackage[tocgraduated]{tocstyle}
\usetocstyle{nopagecolumn}
\usepackage{pdfpages}

\usepackage{tikz}
\usepackage{graphicx}
\usetikzlibrary{calc}
\usepackage{textcomp}
'''

def setup(app):
    app.add_stylesheet('my-styles.css')
