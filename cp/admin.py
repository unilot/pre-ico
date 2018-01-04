from django.contrib import admin
from hvad.admin import TranslatableAdmin
from martor.widgets import AdminMartorWidget
from django.db import models as django_models

from . import models


class FAQAdmin(TranslatableAdmin):
    list_display = ('question_', 'published')

    formfield_overrides = {
        django_models.TextField: {'widget': AdminMartorWidget}
    }


admin.site.register(models.FAQ, FAQAdmin)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'wallet')


admin.site.register(models.Profile, ProfileAdmin)


class TextAdmin(TranslatableAdmin):
    list_display = ('key',)
    formfield_overrides = {
        django_models.TextField: {'widget': AdminMartorWidget}
    }

admin.site.register(models.Text, TextAdmin)
