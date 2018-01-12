from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^faq.html', views.FAQView.as_view(), name='faq-html'),
    url(r'^(?P<document>%s)\.html' %
        ('|'.join(
            list(
                list(views.DocumentView.documents.keys()) + list(views.DocumentView.alias.keys()))
            )
        ),
        views.DocumentView.as_view(), name='document'),
    url(r'(white-paper|wp)\.html', views.WhitePaperView.as_view(), name='white-paper'),
    url(r'^(?P<referrer_code>.{32,64})/index\.html', views.LandingView.as_view(), name='index-html-referred'),
    url(r'^index.html', views.LandingView.as_view(), name='index-html'),
    url(r'^', views.LandingView.as_view(), name='index'),
]
