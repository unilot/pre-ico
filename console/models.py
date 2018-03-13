from django.db import models
from preico.settings import TOKEN_SETTINGS

from console.currency import CurrencySource


class ExchangeRate(models.Model):
    SOURCE_LIST = (
        (CurrencySource.COINBASE, CurrencySource.get_title(CurrencySource.COINBASE)),
        (CurrencySource.COINPAYMENTS, CurrencySource.get_title(CurrencySource.COINPAYMENTS)),
    )

    CURRENCY_LIST = [
        (coin, '%s (%s)' % (data.get('NAME', ''), coin)) for coin, data in TOKEN_SETTINGS.get('COINS', {}).items()
    ] + [
        ('ETH', 'Ethereum (ETH)')
    ]

    currency = models.CharField(null=False, choices=CURRENCY_LIST, max_length=5)
    rate = models.FloatField(null=False)
    source = models.CharField(null=False, choices=SOURCE_LIST, max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s: %s > USD : %f' % (
            CurrencySource.get_title(self.source), self.currency, self.rate)
