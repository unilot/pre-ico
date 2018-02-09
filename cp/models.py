import re

from django.contrib.auth.models import User
from django.db import models
from hvad.models import TranslatableModel, TranslatedFields
from martor.models import MartorField
from django_countries import fields as countries_fields
from landing import models as landing_models
from preico import utils


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

def generate_referral_code(*args):
    return utils.generate_password(42, False)


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', null=False, on_delete=models.deletion.PROTECT)
    company_name = models.CharField(max_length=128, null=True, blank=True)
    phone_number = models.CharField(max_length=24, null=True,blank=True)
    country = countries_fields.CountryField(null=True, blank=False)
    wallet = models.CharField(max_length=64, null=True, blank=True)
    token_amount_reserved = models.FloatField(null=True, blank=True)
    verification_key = models.CharField(max_length=32, null=True, blank=True)
    referrer = models.ForeignKey('Profile', to_field='user', null=True, blank=True, related_name='referral',
                                 unique=False, on_delete=models.deletion.DO_NOTHING)
    referal_level = models.IntegerField(default=0)
    referral_code = models.CharField(max_length=42, null=False, blank=False, default=generate_referral_code)
    referral_token_balance = models.CharField(max_length=27, null=True, blank=True)

    token_balance = models.CharField(max_length=27, null=True, blank=True)
    token_balance_last_update = models.DateTimeField(null=True, blank=True,
                                                     auto_now=False, auto_created=False, auto_now_add=False)

    @property
    def username(self):
        return self.user.username


    def __str__(self):
        return self.username


class Text(TranslatableModel):
    key = models.CharField(max_length=64, null=False, blank=False)
    translations = TranslatedFields(
        text = MartorField(null=False, blank=False)
    )


class BetaTester(models.Model):
    is_ios = models.BooleanField(null=False, blank=False)
    is_android = models.BooleanField(null=False, blank=False)
    email = models.EmailField(null=False, blank=False)
    tester = models.OneToOneField(User, null=True, blank=True, related_name='beta_tester',
                                  on_delete=models.deletion.DO_NOTHING)
    lead = models.OneToOneField(landing_models.Lead, null=True, blank=False, related_name='contact',
                                   on_delete=models.deletion.DO_NOTHING)

    def __str__(self):
        return self.email
