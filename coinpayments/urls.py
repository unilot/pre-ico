from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = []

urlpatterns += format_suffix_patterns([
    url(r'^payment/transaction', views.Transaction.as_view(), name='transaction'),
    url(r'^payment/transaction/(?P<user_id>\d+)/result', views.Transaction.as_view(), name='transaction-callback'),
])