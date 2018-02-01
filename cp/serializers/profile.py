import re

from rest_framework import serializers, validators
from django.contrib.auth import models as auth_models
from django.utils.translation import ugettext as _
from django_countries import serializer_fields as country_serializer
from preico.rest_framework import validators as p_validators
from .. import models
from preico import utils


class ProfileSerializer(serializers.ModelSerializer):
    wallet = serializers.CharField(source='profile.wallet', validators=[
        p_validators.EthWalletValidator()
    ], required=False, read_only=True)
    phone_code = serializers.ChoiceField(choices=utils.get_phone_codes(), required=True, write_only=True)
    phone_number = serializers.CharField(source='profile.phone_number', required=True)
    country = country_serializer.CountryField(source='profile.country', required=True)
    company_name = serializers.CharField(source='profile.company_name', required=False)


    def update(self, instance, validated_data):
        """
        :param instance:
        :type instance: auth_models.User
        :param validated_data:
        :type validated_data: dict
        """
        phone_code = validated_data.pop('phone_code')

        if isinstance(instance.profile, models.Profile):
            profile_data = validated_data.pop('profile')
            profile_data['phone_number'] = '+%s%s' % (
            phone_code,
            re.sub( '[^\d]', '', profile_data.get('phone_number', '') )
        )

            if instance.profile:
                for field, value in profile_data.items():
                    setattr(instance.profile, field, value)

                instance.profile.save()

        return super().update(instance, validated_data)

    class Meta:
        model=auth_models.User
        fields = ('first_name', 'last_name', 'wallet', 'phone_code', 'phone_number', 'country', 'company_name')


class WalletSerializer(serializers.ModelSerializer):
    wallet = serializers.CharField(required=True, validators=[
        p_validators.EthWalletValidator(),
        validators.UniqueValidator(queryset=models.Profile.objects.all())
    ])

    def update(self, instance, validated_data):
        if instance.wallet:
            raise serializers.ValidationError({
                'wallet': [_('Wallet cannot be changed')]
            })

        return super().update(instance, validated_data)

    class Meta:
        model=models.Profile
        fields = ('wallet',)
