from django.http.response import HttpResponseRedirect
from django.urls import reverse
from rest_framework.views import exception_handler as rf_exception_handler
from django.core.exceptions import PermissionDenied


def exception_handler(exc, context):
    format = context.get('kwargs', {}).get('format', 'html')
    request = context.get('request', {})

    if format == 'html':
        if request.user.is_anonymous():
            if getattr(exc, 'status_code', None) in (401, 403) or isinstance(exc, PermissionDenied):
                return HttpResponseRedirect(redirect_to=reverse('cp:auth', kwargs={'format': 'html'}))
        else:
            if getattr(exc, 'status_code', None) in (401, 403) or isinstance(exc, PermissionDenied):
                return HttpResponseRedirect(redirect_to=reverse('cp:dashboard', kwargs={'format': 'html'}))

    return rf_exception_handler(exc, context)
