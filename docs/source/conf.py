# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

project = "Toms Structures"
copyright = "2025, Thomas Duffett"
author = "Thomas Duffett"
release = "latest"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "nbsphinx",
]

templates_path = ["_templates"]
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
html_static_path = ["../_static"]
#html_favicon = "_static/favicon.ico"
html_theme_options = {
    "light_logo": "logo-light.png",  # add light mode logo
    "dark_logo": "logo-dark.png",  # add dark mode logo
    "sidebar_hide_name": True,  # hide name of project in sidebar (already in logo)
    "source_repository": "https://github.com/Revelate123/structures",
    "source_branch": "main",
    "source_directory": "docs/source",
}
pygments_style = "sphinx"
#pygments_dark_style = "monokai"