from rest_framework import serializers


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField()