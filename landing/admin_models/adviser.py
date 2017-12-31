from hvad.admin import TranslatableAdmin, TranslatableModelForm
from martor.widgets import AdminMartorWidget
from django.forms.utils import ErrorList
from django.db import models as django_models
from django import forms
from .. import models


class AdviserAdminForm(TranslatableModelForm):
    photo = forms.ImageField(required=False)

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None, initial=None, error_class=ErrorList,
                 label_suffix=':', empty_permitted=False, instance=None, **kwargs):
        super().__init__(data, files, auto_id, prefix, initial, error_class, label_suffix, empty_permitted, instance,
                         **kwargs)

        if not self.instance.pk:
            self.fields['photo'].required = True

    class Meta:
        model = models.Adviser


class AdvisorAdmin(TranslatableAdmin):
    form = AdviserAdminForm
    list_display = ('full_name_', )


    formfield_overrides = {
        django_models.TextField: {'widget': AdminMartorWidget}
    }
