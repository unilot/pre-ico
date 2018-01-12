from django.core.management.base import BaseCommand
from django.db.models.query_utils import Q
from django.utils import timezone

from console.utils import AppWeb3, ContractHelper, AccountHelper
from preico import settings
from cp import models


class Command(BaseCommand):
    help = 'Reads balances from contract based on submitted wallets'
    CONTRACT_NAME='UnilotToken'

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
            Q(token_balance_last_update__range=(earlier, now))
            | Q(token_balance_last_update=None)).all()

        for profile in profiles:
            profile.token_balance = contract.call().balanceOf(profile.wallet)
            profile.token_balance_last_update = now

            profile.save()
