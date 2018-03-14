from rest_framework import serializers
from preico import settings
from . import models

class Transaction(serializers.ModelSerializer):
    amount = serializers.FloatField(required=True)
    currency = serializers.ChoiceField(
        choices=[(coin, '%s (%s)' % (data.get('NAME', ''), coin)) for coin, data in settings.TOKEN_SETTINGS.get('COINS', {}).items()]
        , required=True)
    address = serializers.CharField(max_length=64, required=False)
    txn_id = serializers.CharField(required=False)
    timeout = serializers.IntegerField(required=False)
    status_url = serializers.URLField(required=False)
    qrcode_url = serializers.URLField(required=False)
    confirms_needed = serializers.IntegerField(required=False)
    user = serializers.PrimaryKeyRelatedField(queryset=models.User.objects.all(), write_only=True, required=False)

    def validate(self, attrs):
        coins_data = settings.TOKEN_SETTINGS.get('COINS', {}).get(attrs['currency'], {})
        result = super().validate(attrs)

        min_amount = coins_data.get('PRICE', 0) * coins_data.get('MIN_CAP', 0)

        if attrs.get('amount', 0) < min_amount:
            raise serializers.ValidationError(
                {'amount': serializers.FloatField().error_messages['min_value'].format(min_value=min_amount)})

        return result

    def create(self, validated_data):
        data = validated_data.copy()
        data['user'] = self.context['request'].user

        return super(Transaction, self).create(data)

    class Meta:
        model = models.Transaction
        exclude = ('created_at', 'updated_at',)
