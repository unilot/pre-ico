class FiatCurrency():
    USD = 'USD'

class CurrencySource():
    COINBASE = 'coinbase',
    COINPAYMENTS = 'coinpayments'

    DETAILS = {
        COINBASE: {
            'title': 'Coinbase'
        },
        COINPAYMENTS: {
            'title': 'Coinpayments'
        }
    }

    @classmethod
    def get_title(cls, source):
        return cls.DETAILS.get(source, {}).get('title')
