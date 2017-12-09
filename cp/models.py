from django.db import models
from hvad.models import TranslatableModel, TranslatedFields
from martor.models import MartorField


class FAQ(TranslatableModel):
    published = models.BooleanField(default=False)
    translations = TranslatedFields(
        question=models.CharField(max_length=255, null=False),
        answer = MartorField(null=False)
    )

    @property
    def question_(self):
        return self.question

    def __unicode__(self):
        return self.question
