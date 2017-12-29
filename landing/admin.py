from django.contrib import admin
from . import models
from hvad.admin import TranslatableAdmin, TranslatableModelForm
from martor.widgets import AdminMartorWidget
from django.db import models as django_models
from django import forms


class PublicationAdminForm(TranslatableModelForm):
    cover_image = forms.ImageField(required=False)
    class Meta:
        model = models.Publication
        exclude = ()
        widgets = {
            'caption': AdminMartorWidget
        }


class PublicationAdmin(TranslatableAdmin):
    form = PublicationAdminForm
    list_display = ('title_', )


    formfield_overrides = {
        django_models.TextField: {'widget': AdminMartorWidget}
    }


admin.site.register(models.Publication, PublicationAdmin)
