"""Configuration file for the Sphinx documentation builder."""

import importlib.metadata
import sys
from datetime import UTC, datetime
from pathlib import Path

from rinoh.frontend.rst import DocutilsInlineNode  # type: ignore

EXCLUDE_FROM_PDF = [
    "2023_*.md",
    "2024_*.md",
    "data_master_logs.rst",
    "data_transaction_logs.rst",
    "pre2008_*.md",
]
MODULE_NAME = "ioavstats"
REPOSITORY_NAME = "io-avstats"
REPOSITORY_TITLE = "Aviation Event Statistics"

# Set the path to include the relevant directories
project_root = Path(__file__).parents[2]
sys.path.insert(0, str(project_root / MODULE_NAME))
sys.path.insert(0, str(project_root / "scripts"))

# Debug: Print the current working directory and sys.path
print("==========>")  # noqa: T201
print("==========> Current working directory:", Path.cwd())  # noqa: T201
print("==========>")  # noqa: T201
print("==========> Updated sys.path:", sys.path)  # noqa: T201
print("==========>")  # noqa: T201

# -- Project information -----------------------------------------------------

author = "IO-Aero Team"  # pylint: disable=invalid-name
copyright: str = (  # pylint: disable=redefined-builtin # noqa: A001
    "2022 - 2024, IO-Aero"  # pylint: disable=redefined-builtin
)
github_url = (  # pylint: disable=invalid-name
    f"https://github.com/io-aero/{REPOSITORY_NAME}"
)
project = REPOSITORY_NAME.upper()  # pylint: disable=invalid-name

try:
    version = importlib.metadata.version(MODULE_NAME)
except importlib.metadata.PackageNotFoundError:
    version = "unknown"  # pylint: disable=invalid-name
    print("==========>")  # noqa: T201
    print(  # noqa: T201
        "==========> Warning: Version not found, defaulting to 'unknown'.",
    )
    print("==========>")  # noqa: T201

release = version.replace(".", "-")

todays_date = datetime.now(tz=UTC).strftime(
    "%Y-%m-%d",
)  # pylint: disable=invalid-name

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

exclude_patterns = [
    "*.pyi",  # Exclude all .pyi files
    ".DS_Store",
    "README.md",
    "Thumbs.db",
    "_build",
    "img/README.md",
]

# Check if building with RinohType for PDF
if "rinoh" in sys.argv:
    exclude_patterns.extend(EXCLUDE_FROM_PDF)

# pylint: disable=line-too-long
extensions = [
    "sphinx.ext.autodoc",  # Automatically generates documentation from docstrings in the source code. # noqa: E501
    "sphinx.ext.extlinks",  # Simplifies linking to external sites with short aliases instead of full URLs. # noqa: E501
    "sphinx.ext.githubpages",  # Creates .nojekyll file to publish the doc as GitHub Pages correctly. # noqa: E501
    "sphinx.ext.napoleon",  # Allows for support of NumPy and Google style docstrings, improving docstring readability. # noqa: E501
    "myst_parser",  # Adds support for Markdown sources, allowing Sphinx to read and parse Markdown files. # noqa: E501
]
# pylint: enable=line-too-long

# Configuration for autodoc extension
autodoc_default_options = {
    "member-order": "bysource",  # Order members by source order
    "special-members": "__init__",  # Document special members such as __init__
    "undoc-members": True,  # Document members without docstrings
    "exclude-members": "__weakref__",  # Exclude specific members
}

# Mocking external modules that are not needed for documentation
autodoc_mock_imports = [
    "ioavstats.pages.Association_Rule_Analysis",
    "ioavstats.pages.Aviation_Event_Analysis",
    "ioavstats.pages.Database_Profiling",
    "streamlit_pandas_profiling",
    "streamlit",
    "pandas_profiling",
]

extlinks = {
    "repo": (f"https://github.com/io-aero/{MODULE_NAME}%s", "GitHub Repository"),
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_favicon = "img/IO-Aero_1_Favicon.ico"  # pylint: disable=invalid-name
html_logo = "img/IO-Aero_1_Logo.png"  # pylint: disable=invalid-name
html_show_sourcelink = False  # pylint: disable=invalid-name
# pylint: disable=line-too-long
html_theme = "furo"  # Chosen for its clean and modern design that improves navigation and readability.  # pylint: disable=invalid-name # noqa: E501
# pylint: enable=line-too-long
html_theme_options = {
    "sidebar_hide_name": True,
}

# The master toctree document.
master_doc = "index"  # pylint: disable=invalid-name

# -- Options for PDF output --------------------------------------------------
rinoh_documents = [
    dict(  # pylint: disable=use-dict-literal # noqa: C408
        doc="index",
        logo="img/IO-Aero_1_Logo.png",
        subtitle="Manual",
        target="manual",
        title=REPOSITORY_TITLE,
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


class Desc_Sig_Space(DocutilsInlineNode):  # noqa: N801 # pylint: disable=invalid-name
    """A custom inline node for managing space in document signatures.

    This class extends `DocutilsInlineNode` to provide specific handling
    for spacing within descriptive parts of a document, such as signatures.
    It can be used to insert custom spacing or separation where the standard
    docutils nodes do not suffice, ensuring that the document's formatting
    meets specific requirements or aesthetics.

    Attributes
        None specific to this class. Inherits attributes from `DocutilsInlineNode`.

    Methods
        Inherits all methods from `DocutilsInlineNode` and does not override or extend them.

    Usage:
        This node should be instantiated and manipulated via docutils' mechanisms
        for handling custom inline nodes. It's primarily intended for extensions
        or custom processing within Sphinx documentation projects.

    """
