from rest_framework import views, response, permissions

from cp.templatetags.dynamic_content import content_text
from .. import models


class DashboardView(views.APIView):
    permission_classes = [ permissions.IsAuthenticated ]
    template_name = 'dashboard.html'

    def get(self, request, *args, **kwargs):
        return response.Response()
