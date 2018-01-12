from django.core.management.base import BaseCommand, CommandError
from coinbase.wallet.client import Client
from django.db import transaction

from console.currency import CryptoCurrency, CurrencySource
from console.utils import ContractHelper, AppWeb3, AccountHelper
from preico.settings import COINBASE_CONFIG
from console.models import ExchangeRate
from preico import settings


class Command(BaseCommand):
    help = 'Pulls latest exchange rate (ETH -> USD) from coinbase'
    base_currency = 'ETH'
    currency = 'USD'

    def handle(self, *args, **options):
        api_client = Client(api_key = COINBASE_CONFIG['API_KEY'],
                            api_secret= COINBASE_CONFIG['API_SECRET'],
                            api_version= COINBASE_CONFIG['API_VERSION'])

        rate = api_client.get_spot_price(
            currency_pair = ( '%s-%s' % (self.base_currency, self.currency)))

        with transaction.atomic():
            if rate.base == self.base_currency and rate.currency == self.currency:
                exchange_rate = ExchangeRate.objects.create(
                    currency = CryptoCurrency.ETH,
                    source = CurrencySource.COINBASE,
                    rate = float(rate.amount)
                )

                exchange_rate.save()

                web3 = AppWeb3.get_web3()

                contract = web3.eth.contract(abi=ContractHelper.get_abi(settings.TOKEN_SETTINGS.get('CONTRACT_NAME')),
                                             bytecode=ContractHelper.get_bytecode(
                                                 settings.TOKEN_SETTINGS.get('CONTRACT_NAME')),
                                             contract_name=settings.TOKEN_SETTINGS.get('CONTRACT_NAME'),
                                             address=settings.TOKEN_ADDRESS)

                AccountHelper.unlock_base_account()

                exchange_rate.total_tokens = contract.call().TOKEN_AMOUNT_PRE_ICO()
                exchange_rate.tokens_left = contract.call().getAvailableCoinsForCurrentStage()
                exchange_rate.eth_raised = web3.eth.getBalance('0xE2A8F147fc808738Cab152b01C7245F386fD8d89')

                exchange_rate.save()
