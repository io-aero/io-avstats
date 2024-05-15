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

# Debug: Print the current working directory and sys.path
print("==========>")
print("==========> Current working directory:", Path.cwd())
print("==========>")
sys.path.insert(0, str(Path(f"../../{MODULE_NAME}").resolve()))
sys.path.insert(0, str(Path("../../scripts").resolve()))
print("==========>")
print("==========> Updated sys.path:", sys.path)
print("==========>")

# -- Project information -----------------------------------------------------

author = "IO-Aero Team"
copyright = "2022 - 2024, IO-Aero"
github_url = f"https://github.com/io-aero/{REPOSITORY_NAME}"
project = REPOSITORY_NAME.upper()

try:
    version = importlib.metadata.version(MODULE_NAME)
except importlib.metadata.PackageNotFoundError:
    version = "unknown"
    print("==========>")
    print("==========> Warning: Version not found, defaulting to 'unknown'.")
    print("==========>")

release = version.replace(".", "-")
todays_date = datetime.now(tz=UTC).strftime("%Y-%m-%d")

# -- General configuration ---------------------------------------------------

exclude_patterns = [
    ".DS_Store",
    "README.md",
    "Thumbs.db",
    "_build",
    "img/README.md",
]

if "rinoh" in sys.argv:
    exclude_patterns.extend(EXCLUDE_FROM_PDF)

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.extlinks",
    "sphinx.ext.githubpages",
    "sphinx.ext.napoleon",
    "myst_parser",
]

# Configuration for autodoc extension
autodoc_default_options = {
    "member-order": "bysource",
    "special-members": "__init__",
    "undoc-members": True,
    "exclude-members": "__weakref__",
}

extlinks = {
    "repo": (f"https://github.com/io-aero/{MODULE_NAME}%s", "GitHub Repository"),
}

# -- Options for HTML output -------------------------------------------------

html_favicon = "img/IO-Aero_1_Favicon.ico"
html_logo = "img/IO-Aero_1_Logo.png"
html_show_sourcelink = False
html_theme = "furo"
html_theme_options = {
    "sidebar_hide_name": True,
}

master_doc = "index"

# -- Options for PDF output --------------------------------------------------
rinoh_documents = [
    dict(
        doc="index",
        logo="img/IO-Aero_1_Logo.png",
        subtitle="Manual",
        target="manual",
        title=REPOSITORY_TITLE,
        toctree_only=False,
    ),
]

source_suffix = {
    ".rst": "restructuredtext",
    ".txt": "markdown",
    ".md": "markdown",
}

class Desc_Sig_Space(DocutilsInlineNode):
    """A custom inline node for managing space in document signatures."""

    # Usage example and details...
