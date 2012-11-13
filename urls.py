
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.shortcuts import redirect

from mezzanine.project_template.urls import urlpatterns

from demo import project_context


urlpatterns = patterns("",
    url("^$", direct_to_template, {
        "template": "index.html",
        "extra_context": project_context
    }, name="home"),
    url("^sites/$", direct_to_template, {
        "template": "sites.html",
        "extra_context": project_context
    }, name="sites"),
    ("^irc/", include("gnotty.urls")),
    ("^shop/", include("cartridge.shop.urls")),
    url("^account/orders/$", "cartridge.shop.views.order_history",
        name="shop_order_history"),
) + urlpatterns
