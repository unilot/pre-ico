from rest_framework import serializers
from rest_framework import validators
from .. import models
from django.contrib.auth import models as django_models


class SubscribeSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[
        validators.UniqueValidator(queryset=models.Lead.objects.all()),
        validators.UniqueValidator(queryset=django_models.User.objects.all())
    ])

    class Meta:
        model = models.Lead
        fields = ('email',)