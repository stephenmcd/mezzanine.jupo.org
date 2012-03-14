
import os

from PIL import Image

from django.conf import settings
from django.core.management.base import NoArgsCommand
from django.template.defaultfilters import slugify


class Command(NoArgsCommand):
    """
    Resets the Mezzanine models for the Mezzanine demo site.
    """

    def handle_noargs(self, **options):
        from demo import home_context
        script = os.path.join(settings.PROJECT_ROOT, "bin", "webkit2png.py")
        for url, title in home_context["sites"]:
            title = slugify(title)
            thumb_dir = os.path.join(settings.STATIC_ROOT, "img", "sites")
            thumb_path = os.path.join(thumb_dir, title + "-thumb.png")
            if not os.path.exists(thumb_path):
                os.system("python %s -T -s 0.18 -D %s -o %s %s" %
                          (script, thumb_dir, title, url))
                Image.open(thumb_path).crop((0, 0, 200, 150)).save(thumb_path)
