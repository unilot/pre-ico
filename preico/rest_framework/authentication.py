from __future__ import unicode_literals

from rest_framework.authentication import SessionAuthentication as BaseSessionAuthentication


class SessionAuthentication(BaseSessionAuthentication):
    def authenticate_header(self, request):
        return 'sessionid %s' % (request.COOKIES.get('sessionid'))
