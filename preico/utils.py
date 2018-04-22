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


class MarketHero():
    TAG_UNILOT = 'unilot'
    TAG_CONTRIBUTOR = 'unilotcontribution'

    URL = 'http://api.markethero.io/v1/api/'

    @staticmethod
    def API_KEY():
        return settings.MARKET_HERO.get('API_KEY')

    @staticmethod
    def tag_lead(email, first_name, last_name, tags = ('unilot',)):
        url = MarketHero.URL + 'tag-lead'
        result = None

        if MarketHero.API_KEY():
            result = requests.post(url, json={
                'apiKey': MarketHero.API_KEY(),
                'email': email,
                'firstName': first_name,
                'lastName': last_name,
                'tags': tags
            })

        return result
