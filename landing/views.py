from django.http.response import HttpResponseNotFound
from django.utils import translation
from rest_framework import generics, permissions, response
from rest_framework.reverse import reverse

from cp import models as cp_models
from cp.serializers import faq
from landing.serializers import subscribe
from preico.document import TermsAndConditions, AffiliateTermsAndConditions, BountyProgram
from . import models
from preico.rest_framework import renderers, permissions as p_permissions


class LandingView(generics.GenericAPIView):
    permission_classes = [ permissions.AllowAny ]
    template_name = 'landing/landing.html'
    renderer_classes = (renderers.TemplateHTMLRenderer, )

    def get(self, request, *args, **kwargs):
        faqs_qs = cp_models.FAQ.objects\
            .filter(published=True).order_by('id')

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
            contribute_url = reverse('cp:sign-up-referred', kwargs={'referrer_code': referrer_code, 'format': 'html'})
        else:
            contribute_url = reverse('cp:sign-up', format='html')

        data['contribute_url'] = contribute_url

        data['publications_list'] = models.Publication.objects.language().filter(published=True).order_by('-id')

        data['roadshow_list'] = models.Roadshow.objects.language().filter(published=True).order_by('id')

        data['advisors_list'] = models.Adviser.objects.language().filter(published=True).order_by('id')

        data['team_members_list'] = models.TeamMember.objects.language().filter(published=True).order_by('id')

        result = response.Response(data)

        if referrer_code:
            result.set_cookie('referrer_code', referrer_code)

        return result


class DocumentView(generics.GenericAPIView):
    permission_classes = [ permissions.AllowAny ]
    renderer_classes = (renderers.TemplateHTMLRenderer,)
    documents = {
        'terms-and-conditions': TermsAndConditions(),
        'affiliate-terms-and-conditions': AffiliateTermsAndConditions(),
        'bounty-program': BountyProgram(),
    }
    alias = {
        'terms': 'terms-and-conditions',
        'tnc': 'terms-and-conditions',
        'affiliate': 'affiliate-terms-and-conditions',
        'bounty': 'bounty-program',
    }
    template_name = 'landing/document.html'

    def get(self, request, *args, **kwargs):
        document_name = kwargs.get('document')

        if document_name:
            document = self.documents.get(document_name)

            if not document and self.alias.get(document_name):
                document = self.documents.get(self.alias.get(document_name))

        if not document:
            raise HttpResponseNotFound()

        data = {
            'document': document
        }

        return response.Response(data)

class WhitePaperView(generics.GenericAPIView):
    permission_classes = ( permissions.AllowAny, )
    renderer_classes = (renderers.TemplateHTMLRenderer,)
    template_name='landing/documents/%(locale)s/White-Paper.html'

    def get(self, request, *args, **kwargs):
        self.template_name = self.template_name % {'locale': translation.get_language()}
        return response.Response({
            'advisors_list': models.Adviser.objects.language().filter(published=True).order_by('id'),
            'team_members_list': models.TeamMember.objects.language().filter(published=True).order_by('id')
        })


class FAQView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    renderer_classes = (renderers.TemplateHTMLRenderer,)
    template_name='landing/faq.html'
    queryset = cp_models.FAQ.objects.language().filter(published=True).order_by('id')
    serializer_class = faq.SimpleFaqSerializer


class Subscribe(generics.CreateAPIView):
    permission_classes = (p_permissions.isGuest,)
    serializer_class = subscribe.SubscribeSerializer


class BetaTester(generics.CreateAPIView):
    permission_classes = (p_permissions.isGuest,)
    serializer_class = subscribe.BetaTesterSerializer
