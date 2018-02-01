import json

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

from cp.templatetags.referral import referral_code
from preico.document import TermsAndConditions
from .. import models
from ..serializers import auth
from preico.rest_framework import permissions as p_permissions
from preico.mandrill.templates import Templates
from preico import utils


class ShowAuthPageView(APIView):
    permission_classes = [p_permissions.isGuest]
    template_name='cp/auth.html'

    def get(self, request, *args, **kwargs):
        data = {
            'tab': 'sign-in',
            'sign_up_url': reverse('cp:sign-up', kwargs={'format': 'html'})
        }

        if kwargs.get('referrer_code'):
            try:
                referrer_profile = models.Profile.objects.get(referral_code=kwargs.pop('referrer_code'))
                data['referrer_code'] = referrer_profile.referral_code
                data['sign_up_url'] = reverse('cp:sign-up-referred',
                                              kwargs={'format': 'html', 'referrer_code': referrer_profile.referral_code})
            except models.Profile.DoesNotExist:
                pass

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
    template_name = 'cp/auth.html'

    def get(self, request, *args, **kwargs):
        data = {
            'tab': 'sign-up',
            'terms_and_conditions': TermsAndConditions.get_content(),
        }

        submit_url = reverse('cp:sign-up', kwargs={'format': 'json'})

        referrer_code = kwargs.get('referrer_code')

        try:
            if not referrer_code:
                referrer_code = request.COOKIES['referrer_code']
        except KeyError:
            pass

        if referrer_code and len(referrer_code) >= 32:
            submit_url = reverse('cp:sign-up-referred',
                                 kwargs={'format': 'json', 'referrer_code': referrer_code})

        data['submit_url'] = submit_url

        return response.Response(data=data)

    def create(self, request, *args, **kwargs):
        referrer_code = kwargs.get('referrer_code', request.COOKIES.get('referrer_code'))

        try:
            if not referrer_code:
                referrer_code = request.COOKIES['referrer_code']
        except KeyError:
            pass

        if referrer_code and len(referrer_code) >= 32:
            try:
                referrer_profile = models.Profile.objects.get(referral_code=referrer_code)
            except models.Profile.DoesNotExist:
                pass

        user_password = utils.generate_password(12)
        input_data = request.data.copy()
        input_data['password'] = user_password
        serializer = self.get_serializer(data=input_data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            user = serializer.save()

            if referrer_code:
                user.profile.referrer = referrer_profile
                user.profile.referal_level = referrer_profile.referal_level + 1

                user.profile.save()

            # Sending email
            msg = EmailMessage(to=[user.email])
            msg.template_name = Templates.get_template_key(Templates.USER_READY_TO_BUY)
            msg.merge_vars = {
                user.email: {
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'password': user_password,
                    'dashboard_url': request.build_absolute_uri(
                        reverse('cp:dashboard', kwargs={'format': 'html'}))
                }
            }

            msg.send()

            login(request, user)

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
    serializer_class = auth.ResetPasswordSerializer

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
                                        and (not isinstance(user.profile, models.Profile) or user.profile.referral_code))

        self.template_name = 'cp/set-password.html'

        return response.Response(data)


    def post(self, request, *args, **kwargs):
        verification_key = kwargs.pop('verification_key', '')
        request_format = kwargs.get('format', 'html')

        user = get_object_or_404(auth_models.User.objects, profile__verification_key=verification_key)
        profile = user.profile

        serializer = self.get_serializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)

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

        if not user.first_name or not user.last_name or user.profile.country or user.profile.phone_number:
            return http_response.HttpResponseRedirect(reverse('cp:profile', kwargs={'format': 'html'}))

        return http_response.HttpResponseRedirect(reverse('cp:dashboard', kwargs={'format': 'html'}))


class ChangePasswordView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = auth.PasswordChangeSerializer

    def get_object(self):
        return self.request.user

    def change_password(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)

        if not user.check_password(serializer.validated_data.get('current_password')):
            return http_response.HttpResponseBadRequest(
                json.dumps({'current_password': [_('Invalid password')]}))

        user.set_password(serializer.validated_data.get('password'))
        user.save()

        return response.Response(data={})

    def post(self, request, *args, **kwargs):
        return self.change_password(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.change_password(request, *args, **kwargs)


class RecoverPassword(generics.GenericAPIView):
    permission_classes = ( p_permissions.isGuest, )
    serializer_class = auth.RecoverPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        try:
            user = serializer.Meta.model.objects.get(username=serializer.validated_data.get('email'))
            verification_key = utils.generate_password(32)
            user.profile.verification_key = verification_key
            user.profile.save()

            # Sending email
            msg = EmailMessage(to=[user.email])
            msg.template_name = Templates.get_template_key(Templates.USER_RESET_PASSWORD)
            msg.merge_vars = {
                user.email: {
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'verify_url': request.build_absolute_uri(
                        reverse('cp:verify',
                                kwargs={'verification_key': verification_key, 'format': 'html'}))
                }
            }

            msg.send()
        except:
            pass

        return response.Response(data=serializer.data)
