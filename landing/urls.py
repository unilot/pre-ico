from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^', views.LandingView.as_view()),
    url(r'^index.html', views.LandingView.as_view())
]
