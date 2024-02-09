# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
from datetime import date
from rinoh.frontend.rst import DocutilsInlineNode

sys.path.insert(0, os.path.abspath("../../"))

import importlib.metadata

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

author = "IO-Aero Team"
copyright = "2022 - 2024, IO-Aero"
github_url = "https://github.com/io-aero/io-avstats"
project = "IO-AVSTATS"

try:
    version = importlib.metadata.version("ioavstats")
except importlib.metadata.PackageNotFoundError:
    version = "?.?.?"

release = version.replace(".", "-")
todays_date = date.today()

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

exclude_patterns = ["__archive__", "_build", "Thumbs.db", ".DS_Store", "README.md", "img/README.md",]

# Check if building with RinohType for PDF
if 'rinoh' in sys.argv:
    # Add the files you want to exclude specifically from PDF
    exclude_patterns.extend([
        '2023_*.md',
        '2024_*.md',
        'data_master_logs.rst',
        'data_transaction_logs.rst',
        'pre2008_*.md'
    ])

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.extlinks",
    "sphinx.ext.githubpages",
    "sphinx.ext.napoleon",
    "myst_parser"
]

extlinks = {
    'repo': ('https://github.com/io-aero/io-avstats%s', 'GitHub Repository')
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_favicon = "img/IO-Aero_1_Favicon.ico"
html_logo = "img/IO-Aero_1_Logo.png"
html_show_sourcelink = False
html_theme = "furo"
html_theme_options = {
    "sidebar_hide_name": True,
}

# The master toctree document.
master_doc = "index"

# -- Options for PDF output --------------------------------------------------
rinoh_documents = [
    dict(
        doc="index",
        logo="img/IO-Aero_1_Logo.png",
        subtitle="Manual",
        target="manual",
        title="IO-AVSTATS - Aviation Event Statistics",
        toctree_only=False,
    ),
]

# rst_epilog = f"""
#             .. |version| replace:: {version}
#             .. |today| replace:: {todays_date}
#             .. |release| replace:: {release}
#             """

source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

class Desc_Sig_Space(DocutilsInlineNode):
    pass
