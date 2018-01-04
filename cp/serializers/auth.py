from django.contrib.auth.password_validation import get_default_password_validators
from rest_framework import serializers, validators
from django.contrib.auth import models as django_models
from django.core import validators as django_validators
from django.db import transaction
from preico.rest_framework import validators as p_validators
from .. import models


def validate_password(password):
    for validator in get_default_password_validators():
        validator.validate(password)


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.ModelField(
        django_models.User._meta.get_field(django_models.User.EMAIL_FIELD), required=True, validators=[
        validators.UniqueValidator(queryset=django_models.User.objects.all()),
        django_validators.EmailValidator()
    ])

    password = serializers.ModelField(django_models.User._meta.get_field('password'), required=True,
                                      validators=(validate_password, ))

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
        password = data.pop('password')

        ModelClass = self.Meta.model
        profile_data = validated_data.pop('profile') if validated_data.get('profile') else None

        with transaction.atomic():
            instance = ModelClass(**validated_data)
            instance.set_password(password)
            instance.save()

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


class PasswordChangeSerializer(serializers.ModelSerializer):
    current_password = serializers.CharField(required=True)
    password = serializers.ModelField(django_models.User._meta.get_field('password'), required=True,
                                      validators=(validate_password, ))

    def create(self, validated_data):
        raise NotImplementedError()

    class Meta:
        model = django_models.User
        fields = ('current_password', 'password')
        extra_kwargs = {
            'current_password': {'write_only': True},
            'password': {'write_only': True}
        }


class RecoverPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = django_models.User
        fields = (django_models.User.EMAIL_FIELD,)


class ResetPasswordSerializer(serializers.ModelSerializer):
    password = serializers.ModelField(django_models.User._meta.get_field('password'), required=True,
                                      validators=(validate_password,))

    class Meta:
        model = django_models.User
        fields = ('password',)
