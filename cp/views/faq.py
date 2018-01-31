from rest_framework import generics
from rest_framework import permissions, response, status
from .. import models
from ..serializers import faq


class FAQView(generics.ListAPIView):
    permission_classes = [ permissions.AllowAny ]
    model = models.FAQ
    template_name='cp/faq.html'
    queryset = models.FAQ.objects.language().filter(published=True).order_by('id')
    serializer_class = faq.SimpleFaqSerializer
