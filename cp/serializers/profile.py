from rest_framework import serializers, validators
from django.contrib.auth import models as auth_models
from django_countries import serializer_fields as country_serializer
from preico.rest_framework import validators as p_validators
from .. import models


class ProfileSerializer(serializers.ModelSerializer):
    wallet = serializers.CharField(source='profile.wallet', validators=[
        p_validators.EthWalletValidator()
    ], required=False, read_only=True)
    phone_number = serializers.CharField(source='profile.phone_number', required=True)
    country = country_serializer.CountryField(source='profile.country', required=True)
    company_name = serializers.CharField(source='profile.company_name', required=True)


    def update(self, instance, validated_data):
        """
        :param instance:
        :type instance: auth_models.User
        :param validated_data:
        :type validated_data: dict
        """

        if isinstance(instance.profile, models.Profile):
            profile_data = validated_data.pop('profile')

            if instance.profile:
                for field, value in profile_data.items():
                    setattr(instance.profile, field, value)

                instance.profile.save()

        return super().update(instance, validated_data)

    class Meta:
        model=auth_models.User
        fields = ('first_name', 'last_name', 'wallet', 'phone_number', 'country', 'company_name')
