
import os.path

from django.conf import settings
from django.template.defaultfilters import slugify
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

# Grab the list items inside a blockquote after each title, and
# assign them to variables for the homepage.
project_context = {"version": mezzanine.__version__}
for section in ("Sites Using Mezzanine", "Quotes", "Features"):
    items = README.split("<h2>%s</h2>" % section)[1] \
                  .split("<li>", 1)[1].split("</li>\n</ul>")[0] \
                  .split("</li>\n<li>")
    project_context[section.split()[0].lower()] = items

# Features are already ordered by user/developer focus - split them.
i = project_context["features"].index("Sharing via Facebook or Twitter") + 1
project_context["features_users"] = project_context["features"][:i]
project_context["features_devs"] = project_context["features"][i:]

# Pull out the featured sites and put them at the start of all sites.
project_context["featured_sites"] = []
project_context["all_sites"] = []
sites = [(s.split("href=\"")[1].split("\"")[0],
          s.split(">")[1].split("</a")[0])
         for s in reversed(project_context["sites"])]
for site in sites:
    key = "featured_sites" if site[0].endswith("/") else "all_sites"
    project_context[key].append(site)

# Only show sites with thumbnails.
project_context["all_sites"] = [site for site in
  (project_context["featured_sites"] + project_context["all_sites"])
  if os.path.exists(os.path.join(settings.STATIC_ROOT, "img/sites",
                                 slugify(site[1]) + "-gallery.jpg"))]

project_context["overview"] = README.split("Overview</h1>")[1]
project_context["overview"] = project_context["overview"].split("<p>Visit")[0]
project_context["quotes"] = ["<em>" + q.replace("- <a", "</em>- <a", 1)
                             for q in project_context["quotes"]]

# Build a list of authors.
path = os.path.join(path_for_import("mezzanine"), "..", "AUTHORS")
with open(path, "r") as f:
    data = f.read()
project_context["authors"] = [a.strip("* ") for a in data.split("\n")][1:-1]
