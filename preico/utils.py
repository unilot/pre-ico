import requests
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


def generate_password(length=12, with_special=True):
    chars = 'abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ0123456789'

    if with_special:
        chars += '@.,;:|{}!@#$%^&*)(+=_-'

    return django_models.User.objects\
        .make_random_password(length=length, allowed_chars= chars)


def get_wallet_app_choice():
    return settings.WALLET_APPS


class SendLane():
    url = 'https://realweb.sendlane.com/api/v1/list-subscriber-add'
    api_key = 'f7dd4c186f1c57a'
    hash_key = '47e896c79e6f6e36143569b986296a2f'

    @staticmethod
    def add_lead(email):
        return requests.post(SendLane.url,
                      {'api': SendLane.api_key, 'hash': SendLane.hash_key, 'list_id': 2, 'email': email})

    @staticmethod
    def add_beta_tester(email, name, phone_number, os_type):
        return requests.post(SendLane.url,
                             {'api': SendLane.api_key, 'hash': SendLane.hash_key, 'list_id': 1,
                              'email': email, 'name': name, 'phone_number': phone_number,
                              'phone_type': os_type})