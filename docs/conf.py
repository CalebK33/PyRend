import os
import sys
sys.path.insert(0, os.path.abspath(".."))

project = "pyrend"
html_title = "PyRend 0.1.46 Documentation"
html_logo = "_static/favicon.png"
author = "CalebK33"
release = "0.1.46"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
]
pygments_style = "friendly"         
pygments_dark_style = "dracula"   

templates_path = ["_templates"]
exclude_patterns = []

html_theme = "furo"
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_favicon = '_static/favicon.png'
