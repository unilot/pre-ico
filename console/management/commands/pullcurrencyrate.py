from django.core.management.base import BaseCommand, CommandError
from coinbase.wallet.client import Client
from coinpayments.utils.api import APIClient as CoinpaymentsAPIClient
from django.db import transaction

from console.currency import CurrencySource
from preico.settings import COINBASE_CONFIG, TOKEN_SETTINGS
from console.models import ExchangeRate


class Command(BaseCommand):
    help = 'Pulls latest exchange rates'

    __coinbase_client__ = None

    def get_coinbase_api(self):
        if not self.__coinbase_client__:
            self.__coinbase_client__ = Client(api_key=COINBASE_CONFIG['API_KEY'],
                                api_secret=COINBASE_CONFIG['API_SECRET'],
                                api_version=COINBASE_CONFIG['API_VERSION'])

        return self.__coinbase_client__

    def handle(self, *args, **options):
        rates = {}

        rates['ETH'] = {
            'rate': self.pull_coinbase_rate('ETH'),
            'source': CurrencySource.COINBASE
        }
        rates['BTC'] = {
            'rate': self.pull_coinbase_rate('BTC'),
            'source': CurrencySource.COINBASE
        }

        coinpayments_client = CoinpaymentsAPIClient.get_client()

        raw_response = coinpayments_client.rates({
            'short': 1,
            'accepted': 1
        })

        if raw_response.get('error') != 'ok':
            raise RuntimeError('Failed to get rates from coinpayments')

        coinpayments_rates = raw_response.get('result', {})

        for coin in TOKEN_SETTINGS.get('COINS', {}).keys():
            if coin in rates:
                continue

            btc_rate = float(coinpayments_rates.get(coin, {}).get('rate_btc', 0))

            if btc_rate > 0:
                rates[coin] = {
                    'rate': btc_rate * rates['BTC']['rate'],
                    'source': CurrencySource.COINPAYMENTS
                }

        for coin, rate_data in rates.items():
            with transaction.atomic():
                exchange_rate = ExchangeRate.objects.create(
                    currency=coin,
                    source=rate_data['source'],
                    rate=rate_data['rate']
                )

                exchange_rate.save()

    def pull_coinbase_rate(self, currency):
        api_client = self.get_coinbase_api()
        base_currency = 'USD'

        rate = api_client.get_spot_price(
            currency_pair=('%s-%s' % (currency, base_currency)))


        if rate.base != currency or rate.currency != base_currency:
            raise RuntimeError('Invalid rate')

        return float(rate.amount)