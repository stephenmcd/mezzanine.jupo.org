
import os.path

from docutils.core import publish_string
from docutils.writers.html4css1 import Writer,HTMLTranslator

import mezzanine
from mezzanine.utils.importing import path_for_import


# Convert the README file from RST to HTML.
writer = Writer()
writer.translator_class = HTMLTranslator
path = os.path.join(path_for_import("mezzanine"), "..", "README.rst")
try:
    with open(path, "r") as f:
        data = f.read()
except IOError:
    README = ""
else:
    README = publish_string(data, writer=writer)


# Grap the list items inside a blockquote after each title, and
# assign them to variables for the homepage.
home_context = {"version": mezzanine.__version__}
for section in ("Sites Using Mezzanine", "Quotes", "Features"):
    items = README.split("<h2>%s</h2>" % section)[1] \
                  .split("<li>", 1)[1].split("</li>\n</ul>")[0] \
                  .split("</li>\n<li>")
    home_context[section.split()[0].lower()] = items

sites_ignore = ['daon.ru', 'Imageinary', 'mezzanine.jupo.org']
home_context["sites"] = [s for s in home_context["sites"]
                         if not [i for i in sites_ignore if i in s]]
home_context["sites"].reverse()
home_context["overview"] = README.split("Overview</h1>")[1].split("<p>Visit")[0]


path = os.path.join(path_for_import("mezzanine"), "..", "AUTHORS")
with open(path, "r") as f:
    data = f.read()
home_context["authors"] = [a.strip("* ") for a in data.split("\n")][1:-1]
