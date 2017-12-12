from django.contrib.auth.models import User
from django.db import models
from hvad.models import TranslatableModel, TranslatedFields
from martor.models import MartorField
from eth_utils import address
from rest_framework import validators


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


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', null=False, on_delete=models.deletion.PROTECT)
    wallet = models.CharField(max_length=64, null=True)
    verification_key = models.CharField(max_length=32, null=True, blank=True)
    referrer = models.ForeignKey('Profile', to_field='user', null=True, blank=True, related_name='referral',
                                 unique=False, on_delete=models.deletion.DO_NOTHING)
    referal_level = models.IntegerField(default=0)

    @property
    def username(self):
        return self.user.username

    def __str__(self):
        return self.username