from rest_framework import views, response, permissions


class DashboardView(views.APIView):
    permission_classes = [ permissions.IsAuthenticated ]
    template_name = 'cp/dashboard.html'

    def get(self, request, *args, **kwargs):
        thank_you = 'thank-you' in request.GET.keys()

        return response.Response(data={'thank_you': thank_you})
