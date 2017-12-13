from rest_framework import generics, permissions, response


class LandingView(generics.GenericAPIView):
    permission_classes = [ permissions.AllowAny ]
    template_name = 'landing.html'

    def get(self, request, *args, **kwargs):
        return response.Response()