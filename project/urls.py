
from django.conf.urls import url, include
from django.shortcuts import redirect, render
from cartridge.shop.views import order_history
from mezzanine.project_template.project_name.urls import urlpatterns

from demo import project_context


def direct_to_template(request, template, extra_context=None):
    return render(request, template, extra_context)

urlpatterns = [
    url("^$", direct_to_template, {
        "template": "index.html",
        "extra_context": project_context
    }, name="home"),
    url("^sites/$", direct_to_template, {
        "template": "sites.html",
        "extra_context": project_context
    }, name="sites"),
    #("^irc/", include("gnotty.urls")),
    url("^shop/", include("cartridge.shop.urls")),
    url("^account/orders/$", order_history, name="shop_order_history"),
] + urlpatterns
