
import os
from distutils.dir_util import mkpath
from shutil import rmtree

from django.apps import apps
from django.db.models import Q
from django.conf import settings
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.core.management import call_command
from django.core.management.base import BaseCommand

from mezzanine.blog.models import BlogPost
from mezzanine.core.management.commands.createdb import Command as DemoData
from mezzanine.core.models import SitePermission


class Command(BaseCommand):
    """
    Resets the Mezzanine models for the Mezzanine demo site.
    """

    def handle(self, **options):

        # Build a list of demo-editable models, which is everything
        # in Cartridge and Mezzanine, apart from mezzanine.twitter
        packages = ("mezzanine", "cartridge")
        keep_apps = ("mezzanine.conf", "mezzanine.twitter")
        reset = lambda a: a.split(".")[0] in packages and a not in keep_apps
        installled_apps = [a.split(".")[-1] for a in settings.INSTALLED_APPS
            if reset(a)]
        models = [m for m in apps.get_models()
            if m._meta.app_label in installled_apps]

        # Delete all demo-editable data.
        for model in models:
            meta = model._meta
            print "Flushing %s.%s" % (meta.app_label, meta.object_name)
            model.objects.all().delete()

        # Maintain permissons for the demo account.
        demo_username = "demo"
        demo_user, created = User.objects.get_or_create(username=demo_username)
        if created:
            demo_user.set_password("demo")
            demo_user.is_staff = True
            demo_user.save()
        demo_user.user_permissions.remove()
        demo_user.first_name = "Demo"
        demo_user.last_name = "User"
        demo_user.save()
        for model in models:
            ct = ContentType.objects.get_for_model(model)
            for permission in Permission.objects.filter(content_type=ct):
                demo_user.user_permissions.add(permission)

        sp = SitePermission.objects.create(user=demo_user)
        for site in Site.objects.all():
            sp.sites.add(site)

        # Delete any created user accounts.
        keep_users = Q(is_superuser=True) | Q(username=demo_username)
        User.objects.exclude(keep_users).delete()

        # Delete any uploaded files.
        uploads = os.path.join(settings.MEDIA_ROOT, "uploads")
        if os.path.exists(uploads):
            rmtree(uploads)
        mkpath(uploads)

        # Load initial demo data.
        print("")
        demo_data = DemoData()
        demo_data.verbosity = 1
        demo_data.interactive = 0
        demo_data.no_data = 0
        demo_data.create_pages()
        demo_data.create_shop()
        call_command("import_rss", rss_url="http://blog.jupo.org/atom.xml",
                     mezzanine_user=demo_username, **options)
        mezzanine_posts = Q(title__icontains="mezzanine")
        cartridge_posts = Q(title__icontains="cartridge")
        BlogPost.objects.exclude(mezzanine_posts | cartridge_posts).delete()
        BlogPost.objects.filter(keywords__keyword__title="speaking").delete()
