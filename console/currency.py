from django.utils.translation import ugettext as _


class CryptoCurrency():
    ETH = 'ETH'

class FiatCurrency():
    USD = 'USD'

class CurrencySource():
    COINBASE = 'coinbase'

    DETAILS = {
        COINBASE: {
            'title': 'Coinbase'
        }
    }

    @classmethod
    def get_title(cls, source):
        return cls.DETAILS.get(source, {}).get('title')
