from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views


adoptive_urls = format_suffix_patterns([
    url(r'^faq', views.FAQView.as_view(), name='faq')
], suffix_required=True, allowed=('json', 'html'))

urlpatterns = format_suffix_patterns([
    url(r'^auth', views.ShowAuthPageView.as_view(), name='auth'),
], True, ('html',))

urlpatterns += [
    url(r'^sign-out$', views.LogoutView.as_view(), name='sign-out')
]

urlpatterns += adoptive_urls
