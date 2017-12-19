from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^', views.LandingView.as_view(), name='index'),
    url(r'^index.html', views.LandingView.as_view(), name='index-html'),
    url(r'^(?P<referrer_code>.{32,64})/index.html', views.LandingView.as_view(), name='index-html-referred')
]
