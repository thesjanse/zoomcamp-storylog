"""Serializers for account registration."""

from django.contrib.auth import get_user_model
from rest_framework import serializers


class RegisterSerializer(serializers.Serializer):
    """Validate registration input and create a hashed-password user."""

    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True, trim_whitespace=False)
    password_confirm = serializers.CharField(
        write_only=True,
        trim_whitespace=False,
    )

    def validate_username(self, value):
        user_model = get_user_model()
        if user_model.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                "A user with that username already exists."
            )
        return value

    def validate(self, attrs):
        password = attrs.get("password")
        password_confirm = attrs.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            raise serializers.ValidationError(
                {"password_confirm": ["Passwords do not match."]}
            )
        return attrs

    def create(self, validated_data):
        user_model = get_user_model()
        return user_model.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
        )
