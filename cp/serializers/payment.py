from rest_framework import serializers
from preico import settings

class CoinPayments(serializers.Serializer):
    amount = serializers.FloatField(required=True)
    currency = serializers.ChoiceField(
        choices=[(coin, '%s (%s)' % (data.get('NAME', ''), coin)) for coin, data in settings.TOKEN_SETTINGS.get('COINS', {}).items()]
        , required=True)
    # address = serializers.CharField()
    # txn_id = serializers.CharField()
    # confirms_needed = serializers.IntegerField()
    # timeout = serializers.IntegerField()
    # status_url = serializers.URLField()
    # qrcode_url = serializers.URLField()

    def validate(self, attrs):
        token_settings = settings.TOKEN_SETTINGS

        price = token_settings.get('COIN_PRICE', {}).get(attrs['currency'], 0)
        min_amount = price * token_settings.get('MIN_CAP', {}).get(attrs['currency'], 0)

        if attrs['amount'] < min_amount:
            raise serializers.ValidationError(
                {'amount': self.amount.error_messages['min_value'].format(min_value=min_amount)})

        return super().validate(attrs)
