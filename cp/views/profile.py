from rest_framework import generics, mixins
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework import permissions, response, status
from django.utils.translation import ugettext as _
from django.http import response as http_response
from django.urls import reverse
from django.contrib.auth import logout, models as auth_models, authenticate, login
from django.db import transaction
from django.core.mail import EmailMessage
from .. import models
from ..serializers import profile
from preico.rest_framework import permissions as p_permissions
from preico.mandrill.templates import Templates


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
