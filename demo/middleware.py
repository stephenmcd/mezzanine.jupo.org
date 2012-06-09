
from uuid import uuid4

from django.core.urlresolvers import reverse
from django.http import HttpResponse


class BlockPasswordChangeMiddleware(object):

    def process_request(self, request):
        """
        Prevent the demo user from changing their password.
        """
        disallowed = (request.POST.get("password1") or
                      request.POST.get("new_password1") or
                      request.POST.get("username", "demo") != "demo")
        if request.user.username == "demo" and disallowed:
            msg = "Username/password change disabled for the demo account."
            return HttpResponse("<h1>Unavailable</h1><p>%s</p>" % msg)


class CompactHTMLMiddleware(object):

    def process_response(self, request, response):
        if 'text/html' in response['Content-Type']:
            from slimmer import xhtml_slimmer
            content = response.content.replace("</a> <a", "</a>&nbsp;<a")
            pre_tokens = {}
            while "<pre" in content:
                pre  = content[content.find("<pre"):content.find("</pre>") + 6]
                token = str(uuid4())
                content = content.replace(pre, token)
                pre_tokens[token] = pre
            content = xhtml_slimmer(content).replace("</a>&nbsp;<a", "</a> <a")
            for token, pre in pre_tokens.items():
                content = content.replace(token, pre)
            response.content = content
        return response
