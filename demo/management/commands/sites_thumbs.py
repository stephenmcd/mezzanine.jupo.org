
import os
from optparse import make_option
from urllib import urlretrieve

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
    option_list = BaseCommand.option_list + (
        make_option("--delay", dest="delay",
            help="Seconds to wait for site to load before taking screenshot"),
        make_option("--service", dest="service",
            help="Screenshot service to use"),
    )

    def create_webkit(self, url, full_path, thumb_dir, title, delay):
        if delay:
            delay = "--delay=%s" % delay
        else:
            delay = ""
        script = os.path.join(settings.PROJECT_ROOT, "bin", "webkit2png.py")
        os.system("python %s %s -W 1280 -H 960 -F -D %s -o %s %s" % (
            script, delay, thumb_dir, title, url))
        return full_path.replace(".jpg", ".png")

    def create_snapito(self, url, delay):
        # if delay:
        #     delay = "&delay=%s" % delay
        # else:
        #     delay = ""
        # api_key = settings.SNAPITO_KEY
        # api_url = "http://api.snapito.com/web/%s/full?freshness=1&url=%s%s" % (
        #     api_key, url, delay)
        api_url = "http://api.snapito.com/free/full/%s" % url
        return urlretrieve(api_url)[0]

    def create_phantomjs(self, url):
        script = os.path.join(settings.PROJECT_ROOT, "bin",
                              "phantomjs-screenshot.js")
        temp = "screenshot.jpg"
        os.system("phantomjs %s %s %s" % (script, url, temp))
        return os.path.join(settings.PROJECT_ROOT, temp)

    def handle(self, **options):
        from demo import project_context
        thumb_dir = os.path.join(settings.STATIC_ROOT, "img", "sites")
        if not options["service"]:
            if os.system("which phantomjs") == 0:
                options["service"] = "phantomjs"
            elif hasattr(settings, "SNAPITO_KEY"):
                options["service"] = "snapito"
            else:
                options["service"] = "webkit2png"
        for url, title in project_context["all_sites"]:
            title = slugify(title)
            full_path = os.path.join(thumb_dir, title + "-full.jpg")
            if not os.path.exists(full_path):
                if options["service"] == "phantomjs":
                    screen_path = self.create_phantomjs(url)
                elif options["service"] == "snapito":
                    screen_path = self.create_snapito(url, options["delay"])
                elif options["service"] == "webkit2png":
                    screen_path = self.create_webkit(url, full_path, thumb_dir,
                                                     title, options["delay"])
                else:
                    continue
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
