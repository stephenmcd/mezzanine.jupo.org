
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from mezzanine.project_template.urls import urlpatterns

from demo import home_context

home_dict = {"template": "index.html", "extra_context": home_context}
new_dict = dict(home_dict, template="new.html")
sites_dict = dict(home_dict, template="sites.html")

urlpatterns = patterns("",
    url("^$", direct_to_template, home_dict, name="home"),
    url("^new/$", direct_to_template, new_dict, name="new"),
    url("^sites/$", direct_to_template, sites_dict, name="sites"),
    ("^shop/", include("cartridge.shop.urls")),
) + urlpatterns
