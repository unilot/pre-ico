from rest_framework import generics
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
from ..serializers import auth
from preico.rest_framework import permissions as p_permissions
from preico.mandrill.templates import Templates


class ShowAuthPageView(APIView):
    permission_classes = [p_permissions.isGuest]
    template_name='auth.html'

    def get(self, request, *args, **kwargs):
        data = {}

        if kwargs.get('referrer_code'):
            referrer_profile = get_object_or_404(
                models.Profile.objects, wallet=kwargs.pop('referrer_code'))
            data['referrer_code'] = referrer_profile.wallet

        return response.Response(data)


class SignOutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        logout(request)

        return http_response.HttpResponseRedirect(
            redirect_to=reverse('cp:auth', kwargs={'format': 'html'}))


class SignUpView(generics.CreateAPIView):
    permission_classes = [ p_permissions.isGuest ]
    serializer_class = auth.SignUpSerializer

    def create(self, request, *args, **kwargs):
        referrer_code = kwargs.get('referrer_code')
        referrer_profile = None
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if referrer_code:
            referrer_profile = get_object_or_404(models.Profile.objects, wallet=referrer_code)

        with transaction.atomic():
            user = serializer.save()
            verification_key = auth_models.User.objects \
                .make_random_password(length=32, allowed_chars='abcdefghjkmnpqrstuvwxyz'
                                                               'ABCDEFGHJKLMNPQRSTUVWXYZ'
                                                               '23456789'
                                                               '@.,;:\|{}!@#$%^&*)(+=_-')
            user.set_unusable_password()
            user.save()

            profile_create_data = {
                'user': user,
                'verification_key': verification_key
            }

            if referrer_profile:
                profile_create_data['referal_level'] = referrer_profile.referal_level + 1
                profile_create_data['referrer'] = referrer_profile

            profile = models.Profile.objects.create(**profile_create_data)

            # Sending email
            msg = EmailMessage(to=[user.email])
            msg.template_name = Templates.get_template_key(Templates.USER_VERIFY_EMAIL)
            msg.merge_vars = {
                user.email: {
                    'email': user.email,
                    'verify_url': request.build_absolute_uri(
                        reverse('cp:verify',
                                kwargs={'verification_key': verification_key, 'format': 'html'}))
                }
            }

            msg.send()

        headers = self.get_success_headers(serializer.data)

        return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class SignInView(generics.GenericAPIView):
    permission_classes = [ permissions.AllowAny ]
    serializer_class = auth.SignInSerializer
    queryset = auth_models.User.objects.filter(is_active=True)

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(username=email, password=password)

        if user is None:
            return http_response.HttpResponseBadRequest(_('Invalid username or password'))

        login(request, user)

        serializer = self.get_serializer(user)

        return response.Response(serializer.data)


class VerifyEmailView(generics.GenericAPIView):
    permission_classes = [ p_permissions.isGuest ]
    serializer_class = auth.SignUpSerializer

    def get(self, request, *args, **kwargs):
        verification_key = kwargs.pop('verification_key', '')
        request_format = kwargs.get('format', 'html')
        data = {}

        user = get_object_or_404(auth_models.User.objects, profile__verification_key=verification_key)

        if request_format == 'json':
            serializer = self.get_serializer(user)
            data = serializer.data
        else:
            data['verification_key'] = verification_key
            data['is_valid_profile'] = (user.first_name
                                        and user.last_name
                                        #Check with instance is dirty hash to avoid panel usage by admins
                                        #Admins to not have profiles created automatically
                                        and (not isinstance(user.profile, models.Profile) or user.profile.wallet))

        self.template_name = 'set-password.html'

        return response.Response(data)


    def post(self, request, *args, **kwargs):
        verification_key = kwargs.pop('verification_key', '')
        request_format = kwargs.get('format', 'html')
        data = {}

        user = get_object_or_404(auth_models.User.objects, profile__verification_key=verification_key)
        profile = user.profile

        with transaction.atomic():
            user.set_password(request.data.get('password'))
            user.is_active = True
            user.profile.verification_key = None
            user.profile.save()
            user.save()

            login(request, user)

        if request_format == 'json':
            serializer = self.get_serializer(user)
            data = serializer.data
            return response.Response(data, status=status.HTTP_200_OK)

        if not user.first_name or not user.last_name or not profile.wallet:
            return http_response.HttpResponseRedirect(reverse('cp:profile', kwargs={'format': 'html'}))

        return http_response.HttpResponseRedirect(reverse('cp:dashboard', kwargs={'format': 'html'}))
