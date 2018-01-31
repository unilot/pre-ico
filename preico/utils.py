from django_countries.data import COUNTRIES
from . import settings
from collections import OrderedDict
from phonenumbers.phonenumberutil import COUNTRY_CODE_TO_REGION_CODE
from django.contrib.auth import models as django_models


def get_investing_countries():
    return OrderedDict(
        (
            (key, COUNTRIES[key])
            if key not in settings.COUNTRIES_EXCLUDED else None
            for key in sorted(COUNTRIES, key=COUNTRIES.get) if not key in settings.COUNTRIES_EXCLUDED
        )
    )


def get_none_investing_countries():
    return OrderedDict(
        (
            (key, COUNTRIES[key]) for key in sorted(settings.COUNTRIES_EXCLUDED)
        )
    )

def get_phone_codes():
    return OrderedDict(
        ( (code, '+%s' % code) for code in sorted(COUNTRY_CODE_TO_REGION_CODE.keys()) )
    )

def generate_password(length=12):
    return django_models.User.objects\
        .make_random_password(length=length,
                              allowed_chars='abcdefghjkmnpqrstuvwxyz'
                                                               'ABCDEFGHJKLMNPQRSTUVWXYZ'
                                                               '23456789'
                                                               '@.,;:\|{}!@#$%^&*)(+=_-')


def get_wallet_app_choice():
    return settings.WALLET_APPS
