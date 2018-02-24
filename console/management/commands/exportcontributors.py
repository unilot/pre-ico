from pprint import pprint

from django.core.management.base import BaseCommand
from django.db.models.query_utils import Q
from django.utils import timezone

from console.utils import AppWeb3, ContractHelper, AccountHelper
from preico import settings
from cp import models
from cp.serializers import auth
from django.contrib.auth import models as django_models
from django_countries.data import COUNTRIES

from preico.utils import MarketHero


class Command(BaseCommand):
    help = 'Exports contributors'

    def handle(self, *args, **options):
        # MarketHero.tag_lead('alexander.aka.alegz@gmail.com', 'Alexander', 'Lushnikov', ('unilot', 'unilotcontribution'))

        profiles = models.Profile.objects \
            .exclude(Q(token_balance__isnull=True) | Q(token_balance__exact='') | Q(token_balance__exact='0'))

        # for profile in profiles:


