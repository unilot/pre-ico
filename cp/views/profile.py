from rest_framework import generics, mixins
from rest_framework import permissions
from django.http import response as http_response
from ..serializers import profile


class ProfileView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                  generics.GenericAPIView):
    permission_classes = [ permissions.IsAuthenticated ]
    serializer_class = profile.ProfileSerializer
    template_name = 'profile.html'

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        format = kwargs.get('format', 'html')

        if format == 'json':
            return http_response.HttpResponseForbidden()

        return self.update(request, *args, **kwargs)
