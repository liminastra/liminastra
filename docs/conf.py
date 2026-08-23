# docs/conf.py
"""Sphinx configuration for liminastra's documentation.

Built by Read the Docs; see .readthedocs.yaml for the build environment and
the ``docs`` extra in pyproject.toml for the Sphinx dependencies.
"""

from __future__ import annotations

import liminastra

project = "liminastra"
copyright = "2026, Michael Smith"
author = "Michael Smith"
release = liminastra.__version__

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "myst_parser",
]

source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

master_doc = "index"

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# liminastra docstrings are NumPy-style (see CLAUDE.md).
napoleon_numpy_docstring = True
napoleon_google_docstring = False

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "astropy": ("https://docs.astropy.org/en/stable/", None),
}

html_theme = "furo"
