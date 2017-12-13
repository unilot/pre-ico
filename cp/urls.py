from django.conf.urls import url
from django.views.generic import TemplateView, RedirectView
from rest_framework.urlpatterns import format_suffix_patterns
from .views import auth, faq, profile


adoptive_urls = format_suffix_patterns([
    url(r'^faq', faq.FAQView.as_view(), name='faq'),
    url(r'^sign-up', auth.SignUpView.as_view(), name='sign-up'),
    url(r'^(?P<referrer_code>.{32,64})/sign-up', auth.SignUpView.as_view(), name='sign-up-referred'),
    url(r'^sign-in', auth.SignInView.as_view(), name='sign-in'),
    url(r'^sign-out', auth.SignOutView.as_view(), name='sign-out'),
    url(r'^user/(?P<verification_key>.{32})/verify', auth.VerifyEmailView.as_view(), name='verify'),
    url(r'^profile', profile.ProfileView.as_view(), name='profile')
], suffix_required=True, allowed=('json', 'html'))

urlpatterns = format_suffix_patterns([
    url(r'^auth', auth.ShowAuthPageView.as_view(), name='auth'),
    url(r'^(?P<referrer_code>.{32,64})/auth', auth.ShowAuthPageView.as_view(), name='auth-referred'),
    url('^dashboard', TemplateView.as_view(template_name='dashboard.html'), name='dashboard'),
], True, ('html',))

urlpatterns += [
    url('', RedirectView.as_view(pattern_name='dashboard'), name='index')
]

urlpatterns += adoptive_urls
