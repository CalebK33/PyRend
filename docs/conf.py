import os
import sys
sys.path.insert(0, os.path.abspath(".."))

project = "pyrend"
html_title = "PyRend 0.1.3 Documentation"
html_logo = "_static/favicon.ico"
author = "Caleb Keenan"
release = "0.1.3"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
]

templates_path = ["_templates"]
exclude_patterns = []

html_theme = "furo"
html_static_path = ["_static"]
html_favicon = '_static/favicon.ico'
