
import os
from shutil import rmtree

from django.db.models import get_models
from django.conf import settings
from django.core.management import call_command
from django.core.management.base import NoArgsCommand


class Command(NoArgsCommand):
    """
    Resets the Mezzanine models for the Mezzanine demo site.
    """

    def handle_noargs(self, **options):
        reset_apps = [a.split(".")[-1] for a in settings.INSTALLED_APPS if
            a.startswith("mezzanine.") or a.startswith("cartridge.")]
        for model in get_models():
            meta = model._meta
            if meta.app_label in reset_apps and meta.app_label != "twitter":
                print "Flushing %s.%s" % (meta.app_label, meta.object_name)
                model.objects.all().delete()
        call_command("loaddata", "mezzanine", **options)
        call_command("loaddata", "cartridge", **options)
        uploads = os.path.join(settings.MEDIA_ROOT, "uploads")
        if os.path.exists(uploads):
            rmtree(uploads)
        os.mkdir(uploads)

