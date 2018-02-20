import requests
from django.core.management.base import BaseCommand
from django.db.models.query_utils import Q
from django.utils import timezone

from console.utils import AppWeb3, ContractHelper, AccountHelper
from preico import settings
from cp import models
from preico.utils import MarketHero


class Command(BaseCommand):
    help = 'Reads balances from contract based on submitted wallets'
    CONTRACT_NAME='PreSaleUNIT'

    def handle(self, *args, **options):
        web3 = AppWeb3.get_web3()

        contract = web3.eth.contract(abi=ContractHelper.get_abi(self.CONTRACT_NAME),
                                     bytecode=ContractHelper.get_bytecode(self.CONTRACT_NAME),
                                     contract_name=self.CONTRACT_NAME,
                                     address=settings.TOKEN_ADDRESS)

        AccountHelper.unlock_base_account()

        now = timezone.now()
        earlier = now - timezone.timedelta(hours=1)

        profiles = models.Profile.objects\
            .filter(
            Q(token_balance_last_update__lte=earlier)
            | Q(token_balance_last_update=None))\
            .exclude(wallet__isnull=True)\
            .exclude(wallet='')

        for profile in profiles:
            if not AppWeb3.get_web3().isAddress(profile.wallet):
                continue

            start_balance = profile.token_balance

            profile.token_balance = contract.call().balanceOf(profile.wallet)
            profile.token_balance_last_update = now
            user = profile.user

            if int(start_balance) < int(profile.token_balance):
                MarketHero.tag_lead(user.email, user.first_name, user.last_name,
                                    (MarketHero.TAG_UNILOT, MarketHero.TAG_CONTRIBUTOR,))
                requests.get('http://15813.tracking.markethero.io/v1/image/pixel-rendered/2d679555e9e778d598bca39b1dabbb17afc1618a306c2e7dd38c8de4e6a142d7')

            profile.save()
