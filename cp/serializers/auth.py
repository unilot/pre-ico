from rest_framework import serializers, validators
from django.contrib.auth import models as django_models
from django.core import validators as django_validators
from django.db import transaction
from preico.rest_framework import validators as p_validators
from .. import models


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.ModelField(
        django_models.User._meta.get_field(django_models.User.EMAIL_FIELD), required=True, validators=[
        validators.UniqueValidator(queryset=django_models.User.objects.all()),
        django_validators.EmailValidator()
    ])

    password = serializers.ModelField(django_models.User._meta.get_field('password'), required=True)

    first_name = serializers.ModelField(django_models.User._meta.get_field('first_name'), required=True)
    last_name = serializers.ModelField(django_models.User._meta.get_field('last_name'), required=True)

    company_name = serializers.CharField(source='profile.company_name', required=False)

    phone = serializers.CharField(source='profile.phone_number', required=True)

    country = serializers.CharField(source='profile.country', required=True)

    wallet = serializers.CharField(source='profile.wallet', validators=[
        p_validators.EthWalletValidator()
    ], required=True)

    ether_amount = serializers.FloatField(source='profile.token_amount_reserved', required=True)

    class Meta:
        model = django_models.User
        fields = ('email', 'password', 'first_name', 'last_name', 'company_name', 'phone',
                  'country', 'wallet', 'ether_amount')

    def create(self, validated_data):
        data = validated_data
        data[django_models.User.USERNAME_FIELD] = data[django_models.User.EMAIL_FIELD]

        ModelClass = self.Meta.model
        profile_data = validated_data.pop('profile') if validated_data.get('profile') else None

        with transaction.atomic():
            instance = ModelClass.objects.create(**validated_data)

            profile_data['user'] = instance

            models.Profile.objects.create(**profile_data)

        return instance


class SignInSerializer(serializers.ModelSerializer):
    email = serializers.ModelField(
        django_models.User._meta.get_field(django_models.User.EMAIL_FIELD), required=True)

    class Meta:
        model = django_models.User
        fields = (django_models.User.EMAIL_FIELD, 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }
