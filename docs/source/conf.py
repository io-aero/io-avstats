#!/usr/bin/env python3

"""Configuration file for the Sphinx documentation builder."""

import sys
import warnings
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import tomli
from docutils.nodes import inline  # type: ignore
from sphinx.application import Sphinx

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

warnings.filterwarnings(
    "ignore",
    message="'imghdr' is deprecated and slated for removal in Python 3.13",
    category=DeprecationWarning,
)

warnings.filterwarnings("ignore", category=DeprecationWarning, module="visions.utils.monkeypatches.imghdr_patch")

warnings.filterwarnings(
    "ignore",
    message="missing ScriptRunContext!.*",
    category=UserWarning,
)

# Suppress specific warnings
warnings.filterwarnings("ignore", message="No runtime found, using MemoryCacheStorageManager")
warnings.filterwarnings("ignore", message="missing ScriptRunContext! This warning can be ignored when running in bare mode.")


# -----------------------------------------------------------------------------

def get_version_from_pyproject() -> str:
    """Retrieve the version from pyproject.toml if available.

    This function looks for the pyproject.toml file in the expected project root directory,
    parses it using the `tomli` library, and retrieves the version specified under the
    `[project]` section.

    Returns:
        str: The version string from pyproject.toml, or "unknown" if the file is not found,
        if the file is not structured as expected, or if no version is specified.

    """
    # Path to the pyproject.toml file
    pyproject_path = Path(__file__).resolve().parent.parent.parent / "pyproject.toml"

    # Check if the file exists
    if not pyproject_path.exists():
        return "unknown"

    try:
        # Attempt to open and parse the pyproject.toml file
        with pyproject_path.open("rb") as f:
            pyproject_data = tomli.load(f)

        # Retrieve the version if available, otherwise return "unknown"
        version_local: str | None = pyproject_data.get("project", {}).get("version")
        return version_local if version_local is not None else "unknown"  # noqa: TRY300
    except (tomli.TOMLDecodeError, OSError) as e:
        # Print an error message if reading the file fails
        print(f"==========> Error reading pyproject.toml: {e}")  # noqa: T201
        # If any error occurs while reading the file, return "unknown"
        return "unknown"


# -----------------------------------------------------------------------------

def skip_private_members(
    _app: Sphinx,
    _what: str,
    name: str,
    _obj: Any,  # noqa: ANN401
    skip: bool,  # noqa: FBT001
    _options: Any,  # noqa: ANN401
) -> bool:
    """Skip private members (starting with a single underscore).

    This function is used as a callback to the autodoc-skip-member event. It allows special members
    like __init__ to be included based on configuration.

    """
    # Skip members that start with a single underscore, but not special members
    # starting with double underscore
    if name.startswith("_") and not name.startswith("__"):
        # Skip private members
        return True
    # Use default behavior
    return skip


# Debug: Print the current working directory and sys.path
print("==========>")  # noqa: T201
print("==========> Current working directory:", Path.cwd())  # noqa: T201
print("==========>")  # noqa: T201
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
sys.path.insert(0, str(Path(f"../../{MODULE_NAME}").resolve()))
print("==========>")  # noqa: T201
print("==========> Updated sys.path:", sys.path)  # noqa: T201
print("==========>")  # noqa: T201

# -- Project information -----------------------------------------------------

author = "IO-Aero Team"
copyright = "2022 - 2024, IO-Aero"  # noqa: A001
github_url = f"https://github.com/io-aero/{REPOSITORY_NAME}"
project = REPOSITORY_NAME.upper()

version = get_version_from_pyproject()
if version == "unknown":
    release = version
    print("==========>")  # noqa: T201
    print("==========> Warning: Version not found, defaulting to 'unknown'.")  # noqa: T201
    print("==========>")  # noqa: T201
else:
    release = version.replace(".", "-")

todays_date = datetime.now(tz=UTC)

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

exclude_patterns = [
    "*.pyi",
    ".DS_Store",
    "README.md",
    "Thumbs.db",
    "_build",
    "img/README.md",
]

# Check if building with RinohType for PDF
if "rinoh" in sys.argv:
    # Add the files you want to exclude specifically from PDF
    exclude_patterns.extend(EXCLUDE_FROM_PDF)

extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.extlinks",
    "sphinx.ext.githubpages",
    "sphinx.ext.napoleon",
]

# Configuration for autodoc extension
autodoc_default_options = {
    "members": True,  # Include all public members
    "private-members": False,  # Exclude private members (starting with _)
    "undoc-members": False,  # Exclude members without docstrings
    "special-members": "__init__",  # Include the __init__ method specifically
    "exclude-members": "__weakref__",  # Exclude specific members, such as __weakref__
    "inherited-members": False,  # Exclude inherited members unless explicitly documented
    "member-order": "alphabetical",  # Order members alphabetically
    "show-inheritance": True,  # Show inheritance relationships in class documentation
}

# Separate setting for type hints
autodoc_typehints = "description"  # Render type hints in the description

# Mock imports that Sphinx should ignore
autodoc_mock_imports = ["streamlit"]

extlinks = {
    "repo": (f"https://github.com/io-aero/{MODULE_NAME}%s", "GitHub Repository"),
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
    {
        "doc": "index",
        "logo": "img/IO-Aero_1_Logo.png",
        "subtitle": "Manual",
        "target": "manual",
        "title": REPOSITORY_TITLE,
        "toctree_only": False,
    },
]

source_suffix = {
    ".rst": "restructuredtext",
    ".txt": "markdown",
    ".md": "markdown",
}


# -----------------------------------------------------------------------------

class Desc_Sig_Space(inline):  # noqa: N801
    """A custom inline node for managing space in document signatures.

    This class extends `docutils.nodes.inline` to provide specific handling
    for spacing within descriptive parts of a document, such as signatures.
    It can be used to insert custom spacing or separation where the standard
    docutils nodes do not suffice, ensuring that the document's formatting
    meets specific requirements or aesthetics.

    Attributes
    ----------
        None specific to this class. Inherits attributes from `docutils.nodes.inline`.

    Methods
    -------
        Inherits all methods from `docutils.nodes.inline` and does not override or extend them.

    Usage:
        This node should be instantiated and manipulated via docutils' mechanisms
        for handling custom inline nodes. It's primarily intended for extensions
        or custom processing within Sphinx documentation projects.

    """


# -----------------------------------------------------------------------------

def setup(app: Any) -> None:  # noqa: ANN401
    """Connect the skip_private_members function to the autodoc-skip-member event.

    This setup function is called when Sphinx initializes the extension. It
    connects the skip_private_members function to the autodoc-skip-member event, which
    allows the function to filter out TypedDict fields from the documentation.

    Args:
        app: The Sphinx application object.

    """
    # Connect the skip_private_members function to the autodoc-skip-member event
    app.connect("autodoc-skip-member", skip_private_members)
