
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.shortcuts import redirect

from mezzanine.project_template.urls import urlpatterns

from demo import home_context

home_dict = {"template": "index.html", "extra_context": home_context}

urlpatterns = patterns("",
    url("^$", direct_to_template, home_dict, name="home"),
    url("^sites/$", lambda r: redirect("/"), name="sites"),
    ("^shop/", include("cartridge.shop.urls")),
) + urlpatterns
