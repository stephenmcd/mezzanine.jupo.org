
import os.path

from docutils.core import publish_string
from docutils.writers.html4css1 import Writer,HTMLTranslator

import mezzanine
from mezzanine.utils.importing import path_for_import


def quotes():
    """
    Pulls the list of quotes about Mezzanine from the README file 
    and converts it from RST to HTML. Will only exist if Mezzanine 
    is installed from the repo, which is the case for the demo site.
    """

    writer = Writer()
    writer.translator_class = HTMLTranslator
    readme = os.path.join(path_for_import("mezzanine"), "..", "README.rst")

    try:
        with open(readme, "r") as f:
            data = f.read()
    except IOError:
        return ""
    else:
        data = publish_string(data, writer=writer)
        data = data.split("<h1>Quotes</h1>")[1].split("</div>")[0]
        data = data.replace(" - <a", "<br /> - <a")
        data = data.replace("<li", "<li class=\"first\"", 1)
        return data

