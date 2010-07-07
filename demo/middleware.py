
from django.core.urlresolvers import reverse
from django.http import HttpResponse


class BlockPasswordChange(object):

    def process_request(self, request):
        """
        Prevent the demo user from changing their password.
        """
        if (request.path == reverse("admin:password_change") and    
            request.user.is_authenticated() and 
            request.user.username == "demo"):
            return HttpResponse("<h1>Unavailable</h1>"
                "<p>This featured is disabled for the demo account.</p>")
        
