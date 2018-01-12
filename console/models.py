from django.db import models
from django.utils.translation import ugettext as _

from console.currency import CryptoCurrency, CurrencySource, FiatCurrency


class ExchangeRate(models.Model):
    SOURCE_LIST = (
        (CurrencySource.COINBASE, CurrencySource.get_title(CurrencySource.COINBASE)),
    )

    CURRENCY_LIST = {
        (CryptoCurrency.ETH, _(CryptoCurrency.ETH)),
    }

    currency = models.CharField(null=False, choices=CURRENCY_LIST, max_length=3)
    rate = models.FloatField(null=False)
    source = models.CharField(null=False, choices=SOURCE_LIST, max_length=8)
    created_at = models.DateTimeField(auto_now_add=True)
    tokens_left = models.CharField(null=True, blank=True, max_length=27)
    total_tokens = models.CharField(null=True, blank=True, max_length=27)
    eth_raised = models.CharField(null=True, blank=True, max_length=27)

    def __str__(self):
        return '%s: %s > %s : %f' % (
            CurrencySource.get_title(self.source), self.currency, FiatCurrency.USD, self.rate)
