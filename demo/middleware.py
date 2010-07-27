
from django.core.urlresolvers import reverse
from django.http import HttpResponse


class BlockPasswordChange(object):

    def process_request(self, request):
        """
        Prevent the demo user from changing their password.
        """
        if (request.user.is_authenticated() and 
            request.user.username == "demo" and 
            request.path == reverse("admin:password_change")):
            return HttpResponse("<h1>Unavailable</h1>"
                "<p>This featured is disabled for the demo account.</p>")
        
