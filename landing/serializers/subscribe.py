from rest_framework import serializers
from rest_framework import validators

from preico.utils import MarketHero
from .. import models
from cp import models as cp_models
from django.contrib.auth import models as django_models
from django.db import transaction
from django.utils.translation import ugettext as _


class SubscribeSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[
        validators.UniqueValidator(queryset=models.Lead.objects.all()),
        validators.UniqueValidator(queryset=django_models.User.objects.all())
    ])

    def create(self, validated_data):
        result = super().create(validated_data)

        try:
            MarketHero.tag_lead(validated_data.get('email'), '', '', ('unilot',))
        except Exception:
            pass

        return result

    class Meta:
        model = models.Lead
        fields = ('email',)

class BetaTesterSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='lead.name', required=True)
    email = serializers.EmailField(required=True, validators=[
        validators.UniqueValidator(queryset=cp_models.BetaTester.objects.all()),
        validators.UniqueValidator(queryset=django_models.User.objects.all())
    ])
    phone = serializers.CharField(source='lead.phone_number', required=True)
    is_receive_updates = serializers.BooleanField(source='lead.is_receive_updates', required=False)

    def validate(self, attrs):
        if attrs['is_ios'] or attrs['is_android']:
            return super().validate(attrs)
        else:
            error_message = _('At least one OS must be selected')
            raise serializers.ValidationError({
                'is_ios': [error_message],
                'is_android': [error_message]
            })

    def create(self, validated_data):
        beta_tester_data = validated_data.copy()
        lead_data = beta_tester_data.pop('lead', {})
        lead_data['email'] = beta_tester_data.get('email')

        with transaction.atomic():
            try:
                beta_tester_data['lead'] = models.Lead.objects.get(
                    email=beta_tester_data.get('email'))
            except models.Lead.DoesNotExist:
                beta_tester_data['lead'] = models.Lead.objects.create(**lead_data)

            os_type = []

            if beta_tester_data['is_android']:
                os_type.append(2403)

            if beta_tester_data['is_ios']:
                os_type.append(2404)

            return super().create(beta_tester_data)

    class Meta:
        model = cp_models.BetaTester
        fields = ('name', 'email', 'phone', 'lead', 'is_ios', 'is_android', 'is_receive_updates')
        extra_kwargs = {
            'lead': {'write_only': True}
        }