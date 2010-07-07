
from django.contrib.auth.models import User, Permission
from django.contrib.sites.models import Site
from django.core.management import call_command
from django.core.management.base import NoArgsCommand


perms = ["Blog post", "Page", "Comment"]


class Command(NoArgsCommand):
    """
    Resets the entire Mezzanine demo site on a scheduled basis, steps are:
    
    1) Destroy the database.
    2) Rebuild the database.
    3) Create the demo user.
    4) Give the demo user permissions to the Mezzanine apps.
    5) Import a Tumblr blog.
    6) Set the current site domain.
    """

    def handle_noargs(self, **options):
        options["interactive"] = False
        call_command("reset_db", **options)
        call_command("syncdb", **options)
        user = User.objects.create_user("demo", "example@example.com", "demo")
        user.is_staff = True
        for perm in Permission.objects.filter(content_type__name__in=perms):
            user.user_permissions.add(perm)
            user.save()
        call_command("import_tumblr", "steve-mc", "demo", **options)
        Site.objects.all().update(domain="mezzanine.jupo.org", 
            name="Mezzanine Demo")
