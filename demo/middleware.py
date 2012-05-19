
from django.core.urlresolvers import reverse
from django.http import HttpResponse


class BlockPasswordChange(object):

    def process_request(self, request):
        """
        Prevent the demo user from changing their password.
        """
        password_posted = (request.POST.get("password1") or
                           request.POST.get("new_password1"))
        if password_posted and request.user.username == "demo":
            message = "Password change disabled for the demo account."
            return HttpResponse("<h1>Unavailable</h1><p>%s</p>" % message)

