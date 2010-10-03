
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from mezzanine import __version__
from mezzanine.project_template.urls import urlpatterns

urlpatterns = patterns("",
    url("^$", direct_to_template, {"template": "index.html", 
        "extra_context": {"version": __version__}}, name="home"),
    ("^shop/", include("cartridge.shop.urls")),
) + urlpatterns

