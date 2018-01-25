from rest_framework import serializers, validators
from .. import models
from django.utils.translation import ugettext as _


class SimpleBetaTesterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[
        validators.UniqueValidator(models.BetaTester.objects.all()),
    ])

    def validate(self, attrs):
        if attrs['is_ios'] or attrs['is_android']:
            return super().validate(attrs)
        else:
            error_message = _('At least one OS must be selected')
            raise serializers.ValidationError({
                'is_ios': [error_message],
                'is_android': [error_message]
            })

    class Meta:
        model = models.BetaTester
        fields = ('email', 'is_ios', 'is_android', 'tester',)
        extra_kwargs = {
            'tester': {'write_only': True}
        }
