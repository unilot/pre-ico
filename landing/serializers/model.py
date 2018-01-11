from rest_framework import serializers
from hvad.contrib.restframework import serializers as hvad_serializers
from .. import models


class PublictionModelSerializer(hvad_serializers.TranslatableModelSerializer):
    class Meta:
        model = models.Publication
        fields = '__all__'


class AdvisorModelSerializer(hvad_serializers.TranslatableModelSerializer):
    class Meta:
        model = models.Adviser
        fields = '__all__'


class TeamMemberModelSerializer(hvad_serializers.TranslatableModelSerializer):
    class Meta:
        model = models.TeamMember
        fields = '__all__'


class RoadshowModelSerializer(hvad_serializers.TranslatableModelSerializer):
    class Meta:
        model = models.Roadshow
        fields = '__all__'
