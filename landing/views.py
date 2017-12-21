from rest_framework import generics, permissions, response
from rest_framework.reverse import reverse

from cp import models as cp_models


class LandingView(generics.GenericAPIView):
    permission_classes = [ permissions.AllowAny ]
    template_name = 'landing/landing.html'

    def get(self, request, *args, **kwargs):
        faqs_qs = cp_models.FAQ.objects\
            .filter(published=True).order_by('-id')

        faqs_total = faqs_qs.count()
        faqs = faqs_qs[:12]

        data = dict({
            'faqs': faqs,
            'faqs_total': faqs_total
        })

        #TODO attach to condition or app configuration
        data['is_pre_ico'] = True

        referrer_code = kwargs.get('referrer_code')

        if request.user.is_authenticated:
            contribute_url = reverse('cp:dashboard', format='html')
        elif referrer_code:
            contribute_url = reverse('cp:auth-referrer', args=referrer_code, format='html')
        else:
            contribute_url = reverse('cp:auth', format='html')

        #TODO remove when action will be ready to go
        contribute_url = '#'

        data['contribute_url'] = contribute_url

        return response.Response(data)
