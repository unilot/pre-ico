from django.utils.http import urlquote
from rest_framework import views, response, permissions


class DashboardView(views.APIView):
    permission_classes = [ permissions.IsAuthenticated ]
    template_name = 'dashboard.html'

    def get(self, request, *args, **kwargs):
        return response.Response()
