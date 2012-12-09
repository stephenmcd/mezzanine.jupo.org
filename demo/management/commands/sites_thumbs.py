
import os
from optparse import make_option

from PIL import Image

from django.conf import settings
from django.core.management.base import BaseCommand
from django.template.defaultfilters import slugify


SIZES = {
    "homepage": (200, 150),
    "gallery": (260, 195),
}

class Command(BaseCommand):
    """
    Generates thumbnails for the Mezzanine project sites, for each
    site powered by Mezzanine, as listed in Mezzanine's README.
    """
    option_list = BaseCommand.option_list + (make_option(
        "--delay", dest="delay",
        help="Seconds to wait for site to load before taking screenshot"),)

    def handle(self, **options):
        from demo import project_context
        script = os.path.join(settings.PROJECT_ROOT, "bin", "webkit2png.py")
        thumb_dir = os.path.join(settings.STATIC_ROOT, "img", "sites")
        for url, title in project_context["all_sites"]:
            title = slugify(title)
            full_path = os.path.join(thumb_dir, title + "-full.jpg")
            if not os.path.exists(full_path):
                if options["delay"]:
                    delay = "--delay=%s" % options["delay"]
                else:
                    delay = ""
                args = (script, delay, thumb_dir, title, url)
                cmd = "python %s %s -W 1280 -H 960 -F -D %s -o %s %s"
                os.system(cmd % args)
                screen_path = full_path.replace(".jpg", ".png")
                Image.open(screen_path).save(full_path, quality=60)
                os.remove(screen_path)
            for name, size in SIZES.items():
                size_path = os.path.join(thumb_dir, title + "-%s.jpg" % name)
                if not os.path.exists(size_path):
                    img = Image.open(full_path)
                    resize = (size[0], img.size[1] * size[0] / img.size[0])
                    crop = (0, 0, size[0], size[1])
                    img = img.resize(resize, Image.ANTIALIAS).crop(crop)
                    img.save(size_path, quality=95)
