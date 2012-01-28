
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

import os

# Full filesystem path to the project.
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Name of the directory for the project.
PROJECT_DIRNAME = PROJECT_ROOT.split(os.sep)[-1]

# Every cache key will get prefixed with this value - here we set it to
# the name of the directory the project is in to try and use something
# project specific.
CACHE_MIDDLEWARE_KEY_PREFIX = PROJECT_DIRNAME

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = "/static/"

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, STATIC_URL.strip("/"))

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = STATIC_URL + "media/"

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, *MEDIA_URL.strip("/").split("/"))

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = STATIC_URL + "grappelli/"

# Package/module name to import the root urlpatterns from for the project.
ROOT_URLCONF = "%s.urls" % PROJECT_DIRNAME

# Put strings here, like "/home/html/django_templates"
# or "C:/www/django/templates".
# Always use forward slashes, even on Windows.
# Don't forget to use absolute paths, not relative paths.
TEMPLATE_DIRS = (os.path.join(PROJECT_ROOT, "templates"),)

LOGIN_URL = "/shop/account/"


################
# APPLICATIONS #
################

# django.contrib.sites should be before cartridge.shop to avoid a
# foreign key error when installing the test fixtures with Postgres,
# and cartridge.shop should be before mezzanine.core so that the
# shop's base template is loaded over mezzanine's.

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
