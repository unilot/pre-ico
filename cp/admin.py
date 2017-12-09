from django.contrib import admin, messages
from hvad.admin import TranslatableAdmin
from martor.widgets import AdminMartorWidget
from django.db import models as django_models, IntegrityError, DatabaseError

from . import models


class FAQAdmin(TranslatableAdmin):
    list_display = ('question_', 'published')

    formfield_overrides = {
        django_models.TextField: {'widget': AdminMartorWidget}
    }

    def add_view(self, request, form_url='', extra_context=None):
        try:
            return super(FAQAdmin, self).add_view(request, form_url, extra_context)
        except (IntegrityError, DatabaseError) as e:

            request.method = 'GET'
            messages.error(request, e.message)
            return super(FAQAdmin, self).add_view(request, form_url, extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        try:
            return super(FAQAdmin, self).change_view(request, object_id, form_url, extra_context)
        except (IntegrityError, DatabaseError) as e:

            request.method = 'GET'
            messages.error(request, e.message)
            return super(FAQAdmin, self).change_view(request, object_id, form_url, extra_context)

admin.site.register(models.FAQ, FAQAdmin)
