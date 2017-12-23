from rest_framework import serializers, validators
from .. import models
from django.contrib.auth import models as django_models
from django.core import validators as django_validators
from preico.rest_framework import validators as preico_validators


class UserEmailSerializer(serializers.ModelSerializer):
    email = serializers.ModelField(
        django_models.User._meta.get_field(django_models.User.EMAIL_FIELD), required=True, validators=[
            validators.UniqueValidator(queryset=django_models.User.objects.all()),
            django_validators.EmailValidator()
        ])

    class Meta:
        model = django_models.User
        fields = (django_models.User.EMAIL_FIELD,)


class UserWalletSerializer(serializers.ModelSerializer):
    wallet = serializers.ModelField(
        models.Profile._meta.get_field('wallet'), required=True, validators=[
            validators.UniqueValidator(queryset=models.Profile.objects.all()),
            preico_validators.EthWalletValidator
        ])
    class Meta:
        model = models.Profile
        fields = ('wallet',)
