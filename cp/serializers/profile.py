from rest_framework import serializers, validators
from django.contrib.auth import models as auth_models
from preico.rest_framework import validators as p_validators
from .. import models


class ProfileSerializer(serializers.ModelSerializer):
    wallet = serializers.CharField(source='profile.wallet', validators=[
        p_validators.EthWalletValidator()
    ], required=True)

    def update(self, instance, validated_data):
        """
        :param instance:
        :type instance: auth_models.User
        :param validated_data:
        :type validated_data: dict
        """

        if isinstance(instance.profile, models.Profile):
            wallet = validated_data.pop('profile').pop('wallet')

            if not instance.profile.wallet:
                instance.profile.wallet = wallet
                instance.profile.save()

        return super().update(instance, validated_data)

    class Meta:
        model=auth_models.User
        fields = ('first_name', 'last_name', 'wallet')