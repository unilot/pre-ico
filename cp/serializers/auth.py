from rest_framework import serializers, validators
from django.contrib.auth import models as django_models
from django.core import validators as django_validators


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.ModelField(
        django_models.User._meta.get_field(django_models.User.EMAIL_FIELD), required=True, validators=[
        validators.UniqueValidator(queryset=django_models.User.objects.all()),
        django_validators.EmailValidator()
    ])

    class Meta:
        model = django_models.User
        fields = (django_models.User.EMAIL_FIELD,)

    def create(self, validated_data):
        data = validated_data
        data[django_models.User.USERNAME_FIELD] = data[django_models.User.EMAIL_FIELD]

        return super(SignUpSerializer, self).create(data)


class SignInSerializer(serializers.ModelSerializer):
    email = serializers.ModelField(
        django_models.User._meta.get_field(django_models.User.EMAIL_FIELD), required=True)

    class Meta:
        model = django_models.User
        fields = (django_models.User.EMAIL_FIELD, 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }
