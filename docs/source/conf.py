"""Configuration file for the Sphinx documentation builder.

This file contains settings for the Sphinx documentation generation process,
tailored for the IO-AVSTATS project. It defines project information, documentation
structure, and output formatting options. The configuration aligns with the Sphinx
documentation guidelines and includes custom settings for HTML and PDF output,
as well as internationalization options.

The configuration is designed to be flexible and to provide a good starting point
for projects. It includes dynamic retrieval of project versioning, ensures that
project source code is accessible to Sphinx for API documentation generation, and
configures various Sphinx extensions to enhance the documentation.

References
----------
    Sphinx Configuration Documentation:
    https://www.sphinx-doc.org/en/master/usage/configuration.html

Attributes
----------
    author (str): The name of the documentation author(s).
    copyright (str): The copyright statement for the project.
    github_url (str): The URL to the project's GitHub repository.
    project (str): The name of the project being documented.
    version (str): The project's version, dynamically retrieved or set to 'unknown'.
    release (str): The project's release version, derived from `version`.
    todays_date (datetime.date): Today's date, used for timestamping documentation builds.

Notes
-----
    - The configuration dynamically adjusts the `sys.path` to ensure Sphinx can
      locate and document the project's Python modules.
    - It includes options for both HTML and PDF output via Sphinx and RinohType,
      respectively.
    - Version and release information are dynamically retrieved to minimize manual
      updates required for each new project version.

Usage:
    This file is automatically used by Sphinx commands (`sphinx-build`, `make html`, etc.)
    and should not be executed directly. Modify it as needed to fit the project's
    documentation requirements.

"""
import importlib.metadata
import sys
from datetime import UTC, datetime
from pathlib import Path

from rinoh.frontend.rst import DocutilsInlineNode

sys.path.insert(0, str(Path(__file__).parent.parent.resolve()))

# -- Project information -----------------------------------------------------

author = "IO-Aero Team"
copyright: str = "2022 - 2024, IO-Aero" # noqa: A001
github_url = "https://github.com/io-aero/io-avstats"
project = "IO-AVSTATS"

try:
    version = importlib.metadata.version("ioavstats")
except importlib.metadata.PackageNotFoundError:
    version = "unknown"

release = version.replace(".", "-")

todays_date = datetime.now(tz=UTC)

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

exclude_patterns = ["__archive__", "_build", "Thumbs.db", ".DS_Store", "README.md", "img/README.md"]

# Check if building with RinohType for PDF
if "rinoh" in sys.argv:
    # Add the files you want to exclude specifically from PDF
    exclude_patterns.extend([
        "2023_*.md",
        "2024_*.md",
        "data_master_logs.rst",
        "data_transaction_logs.rst",
        "pre2008_*.md",
    ])

extensions = [
    "sphinx.ext.autodoc",  # Automatically document your Python modules
    "sphinx.ext.extlinks",
    "sphinx.ext.githubpages",
    "sphinx.ext.napoleon",  # Support for NumPy and Google style docstrings
    "myst_parser",  # Markdown support
]

# Configuration for autodoc extension
autodoc_default_options = {
    "member-order": "bysource",  # Order members by source order
    "special-members": "__init__",  # Document special members such as __init__
    "undoc-members": True,  # Document members without docstrings
    "exclude-members": "__weakref__",  # Exclude specific members
}

extlinks = {
    "repo": ("https://github.com/io-aero/io-avstats%s", "GitHub Repository"),
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
    dict( # noqa: C408
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
    ".txt": "markdown",
    ".md": "markdown",
}

class Desc_Sig_Space(DocutilsInlineNode):  # noqa: N801

    """A custom inline node for managing space in document signatures.

    This class extends `DocutilsInlineNode` to provide specific handling
    for spacing within descriptive parts of a document, such as signatures.
    It can be used to insert custom spacing or separation where the standard
    docutils nodes do not suffice, ensuring that the document's formatting
    meets specific requirements or aesthetics.

    Attributes
    ----------
        None specific to this class. Inherits attributes from `DocutilsInlineNode`.

    Methods
    -------
        Inherits all methods from `DocutilsInlineNode` and does not override or extend them.

    Usage:
        This node should be instantiated and manipulated via docutils' mechanisms
        for handling custom inline nodes. It's primarily intended for extensions
        or custom processing within Sphinx documentation projects.

    """
