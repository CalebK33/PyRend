import os
import sys
sys.path.insert(0, os.path.abspath(".."))

project = "pyrend"
html_title = "PyRend 0.1.47 Documentation"
html_logo = "_static/favicon.png"
author = "CalebK33"
release = "0.1.47"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
]
pygments_style = "friendly"         
pygments_dark_style = "dracula"   

templates_path = ["_templates"]
exclude_patterns = []

html_theme = "furo"
html_meta = {
    "google-site-verification": "WJ5tQFHzKxZIWF-XQ3fb7RaSPFMsIk_tYL1sqS__yn4",
}
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_favicon = '_static/favicon.png'
