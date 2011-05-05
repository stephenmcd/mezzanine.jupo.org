
import sys, os

import os, sys;
sys.path.insert(0, os.path.join("..", "mezzanine"))
sys.path.insert(0, os.path.join("..", "cartridge"))

from cartridge.project_template.settings import *

# Cartridge Settings.
SHOP_SSL_ENABLED = False

# Main Django settings.
DEBUG = False
DEV_SERVER = False
MANAGERS = ADMINS = ()
TIME_ZONE = "Australia/Melbourne"
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
LANGUAGE_CODE = "en"
SITE_ID = 1
USE_I18N = False
SECRET_KEY = "dgfdsg98sdgg54545B$Wv#$#4#$ZDvdfvbfvv"
INTERNAL_IPS = ("127.0.0.1",)

# Databases.
DATABASES = {
    "default": {
        "ENGINE": "",
        "HOST": "",
        "NAME": "",
        "PASSWORD": "",
        "PORT": "",
        "USER": "",
    }
}

# Paths.
import os
_project_path = os.path.dirname(os.path.abspath(__file__))
_project_dir = _project_path.split(os.sep)[-1]
ADMIN_MEDIA_PREFIX = "/media/"
CACHE_MIDDLEWARE_KEY_PREFIX = _project_dir
MEDIA_URL = "/site_media/"
MEDIA_ROOT = os.path.join(_project_path, MEDIA_URL.strip("/"))
ROOT_URLCONF = "%s.urls" % _project_dir
TEMPLATE_DIRS = (os.path.join(_project_path, "templates"),)

# Apps/
INSTALLED_APPS = list(INSTALLED_APPS)
INSTALLED_APPS.remove("django.contrib.sites")
INSTALLED_APPS = tuple(INSTALLED_APPS)
INSTALLED_APPS = ("django.contrib.sites", "cartridge.shop") + INSTALLED_APPS

TEMPLATE_CONTEXT_PROCESSORS += (
    "cartridge.shop.context_processors.shop_globals",
)

MIDDLEWARE_CLASSES += (
    "cartridge.shop.middleware.SSLRedirect",
    "demo.middleware.BlockPasswordChange",
)

# Mezzanine settings.
from django.utils.translation import ugettext_lazy as _
ADMIN_MENU_ORDER = (
    (_("Content"), ("pages.Page", "blog.BlogPost", "generic.ThreadedComment",
        (_("Media Library"), "fb_browse"),)),
    (_("Shop"), ("shop.Product", "shop.ProductOption", "shop.DiscountCode",
        "shop.Sale", "shop.Order")),
    (_("Site"), ("sites.Site", "redirects.Redirect", "conf.Setting")),
    (_("Users"), ("auth.User", "auth.Group",)),
)

# Local settings.
try:
    from local_settings import *
except ImportError:
    pass

# Dynamic settings.
from mezzanine.utils.conf import set_dynamic_settings
set_dynamic_settings(globals())
