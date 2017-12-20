from rest_framework import generics, permissions, response
from cp import models as cp_models


class LandingView(generics.GenericAPIView):
    permission_classes = [ permissions.AllowAny ]
    template_name = 'landing.html'

    def get(self, request, *args, **kwargs):
        faqs_qs = cp_models.FAQ.objects\
            .filter(published=True).order_by('-id')

        faqs_total = faqs_qs.count()
        faqs = faqs_qs[:12]

        return response.Response({'faqs': faqs, 'faqs_total': faqs_total})
