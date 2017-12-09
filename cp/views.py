from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework import permissions, response, pagination
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout
from . import models
from .serializers import faq


class ShowAuthPageView(APIView):
    permission_classes = [permissions.AllowAny]
    template_name='auth.html'

    def get(self, request, *args, **kwargs):
        return response.Response()


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        logout(request)

        return HttpResponseRedirect(redirect_to=reverse('cp:auth', args=('html')))

class FAQView(ListAPIView):
    permission_classes = [ permissions.AllowAny ]
    model = models.FAQ
    template_name='faq.html'
    queryset = models.FAQ.objects.language().filter(published=True).order_by('-id')
    serializer_class = faq.SimpleFaqSerializer
