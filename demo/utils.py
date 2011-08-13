
import os.path

from docutils.core import publish_string
from docutils.writers.html4css1 import Writer,HTMLTranslator

import mezzanine
from mezzanine.utils.importing import path_for_import


def readme():
    """
    Converts the README file from RST to HTML.
    """
    writer = Writer()
    writer.translator_class = HTMLTranslator
    readme = os.path.join(path_for_import("mezzanine"), "..", "README.rst")
    try:
        with open(readme, "r") as f:
            data = f.read()
    except IOError:
        return ""
    return publish_string(data, writer=writer)

def quotes():
    """
    Pulls the list of quotes about Mezzanine from the README file.
    """
    html = readme()
    html = html.split("<h1>Quotes</h1>")[1].split("</div>")[0]
    html = html.replace(" - <a", "<br /> - <a")
    html = html.replace("<li", "<li class=\"first\"", 1)
    return html

def sites():
    """
    Pulls the list of sites using Mezzanine from the README file.
    """
    html = readme()
    html = html.split("<h1>Sites Using Mezzanine</h1>")[1].split("<blockquote>")[1].split("</blockquote>")[0]
    return html
