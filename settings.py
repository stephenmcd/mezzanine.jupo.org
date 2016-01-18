
AUTH_PROFILE_MODULE = "demo.Profile"
USE_TZ = True
AUTHENTICATION_BACKENDS = ("mezzanine.core.auth_backends.MezzanineBackend",)


# Main Django settings.
DEBUG = False
DEV_SERVER = False
MANAGERS = ADMINS = ()
TIME_ZONE = "Australia/Melbourne"
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
LANGUAGE_CODE = "en"
SITE_ID = 1
USE_I18N = USE_L10N = True
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

SHOP_CURRENCY_LOCALE = "en_US.UTF-8"

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


# URLs used for login/logout when ACCOUNTS_ENABLED is set to True.
LOGIN_URL = "/account/"
LOGOUT_URL = "/account/logout/"

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # other finders..
    'compressor.finders.CompressorFinder',
)

################
# APPLICATIONS #
################

INSTALLED_APPS = (
    #"gnotty",
    "demo",
    "compressor",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.redirects",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    "django.contrib.staticfiles",
    "cartridge.shop",
    "mezzanine.boot",
    "mezzanine.conf",
    "mezzanine.core",
    "mezzanine.generic",
    "mezzanine.blog",
    "mezzanine.forms",
    "mezzanine.pages",
    "mezzanine.galleries",
    "mezzanine.twitter",
    "mezzanine.mobile",
    "mezzanine.accounts",
)

# List of processors used by RequestContext to populate the context.
# Each one should be a callable that takes the request object as its
# only parameter and returns a dictionary to add to the context.
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.static",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "mezzanine.conf.context_processors.settings",
    "mezzanine.pages.context_processors.page",
)

# List of middleware classes to use. Order is important; in the request phase,
# this middleware classes will be applied in the order given, and in the
# response phase the middleware will be applied in reverse order.
MIDDLEWARE_CLASSES = (
    "mezzanine.core.middleware.UpdateCacheMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.redirects.middleware.RedirectFallbackMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "cartridge.shop.middleware.ShopMiddleware",
    "demo.middleware.BlockPasswordChangeMiddleware",
    "demo.middleware.CompactHTMLMiddleware",
    "mezzanine.core.request.CurrentRequestMiddleware",
    "mezzanine.core.middleware.TemplateForDeviceMiddleware",
    "mezzanine.core.middleware.TemplateForHostMiddleware",
    "mezzanine.core.middleware.AdminLoginInterfaceSelectorMiddleware",
    "mezzanine.pages.middleware.PageMiddleware",
    "mezzanine.core.middleware.FetchFromCacheMiddleware",
)


# Store these package names here as they may change in the future since
# at the moment we are using custom forks of them.
PACKAGE_NAME_FILEBROWSER = "filebrowser_safe"
PACKAGE_NAME_GRAPPELLI = "grappelli_safe"


#########################
# OPTIONAL APPLICATIONS #
#########################

# These will be added to ``INSTALLED_APPS``, only if available.
OPTIONAL_APPS = (
    "django_extensions",
    PACKAGE_NAME_FILEBROWSER,
    PACKAGE_NAME_GRAPPELLI,
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

FABRIC = {
    "HOSTS": ["mezzanine.jupo.org"], # List of hosts to deploy to
    "REQUIREMENTS_PATH": "requirements.txt",
    "REPO_URL": "git://github.com/stephenmcd/mezzanine.jupo.org.git",
}

GNOTTY_HTTP_HOST = "0.0.0.0"
GNOTTY_HTTP_PORT = 8081
GNOTTY_IRC_CHANNEL = "#mezzanine"
GNOTTY_BOT_NICKNAME = "mezzbott5000"
GNOTTY_BOT_CLASS = "demo.bot.MezzanineBot"

f = os.path.join(PROJECT_ROOT, "local_settings.py")
if os.path.exists(f):
    import sys
    import imp
    module_name = "%s.local_settings" % PROJECT_DIRNAME
    module = imp.new_module(module_name)
    module.__file__ = f
    sys.modules[module_name] = module
    exec(open(f, "rb").read())

# Dynamic settings.
from mezzanine.utils.conf import set_dynamic_settings
set_dynamic_settings(globals())
