from hvad.admin import TranslatableAdmin, TranslatableModelForm
from django.forms.utils import ErrorList
from django import forms
from .. import models


class RoadshowAdminForm(TranslatableModelForm):
    cover_image = forms.ImageField(required=False)

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None, initial=None, error_class=ErrorList,
                 label_suffix=':', empty_permitted=False, instance=None, **kwargs):
        super().__init__(data, files, auto_id, prefix, initial, error_class, label_suffix, empty_permitted, instance,
                         **kwargs)

        if not self.instance.pk:
            self.fields['cover_image'].required = True

    class Meta:
        model = models.Roadshow
        exclude = ()


class RoadshowAdmin(TranslatableAdmin):
    form = RoadshowAdminForm
    list_display = ('title_', )
