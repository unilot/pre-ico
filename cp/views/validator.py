from rest_framework import generics
from rest_framework import permissions, response, status
from django.contrib.auth import models as django_models
from .. import models
from ..serializers import validator


class GenericValidatorAPIView(generics.GenericAPIView):
    validation_field = None

    def process_validation(self, request, value):
        serializer = self.get_serializer(data={self.validation_field: value})

        serializer.is_valid(raise_exception=True)

        return response.Response(data={}, status=status.HTTP_200_OK)


class UserEmailValidator(GenericValidatorAPIView):
    permission_classes = [ permissions.AllowAny ]
    model = django_models.User
    serializer_class = validator.UserEmailSerializer
    validation_field = 'email'

    def post(self, request, *args, **kwargs):
        return self.process_validation(request, request.data.get('email',
                                                        request.data.get('username')))


class UserProfileWalletValidator(GenericValidatorAPIView):
    permission_classes = [permissions.AllowAny]
    model = models.Profile
    serializer_class = validator.UserWalletSerializer
    validation_field = 'wallet'

    def post(self, request, *args, **kwargs):
        return self.process_validation(request, request.data.get('wallet'))
