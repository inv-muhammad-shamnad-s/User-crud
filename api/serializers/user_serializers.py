from rest_framework import serializers
from ..validators.user_field_validator import (
    email_field_validation,
    username_field_validation,
    name_field_validation,
    password_validation,
    confirm_password_validation,
    role_validation,
)
from ..messages.error_messages import (
    EMAIL_ERROR_MESSAGES,
    USERNAME_ERROR_MESSAGES,
    NAME_ERROR_MESSAGES,
    COMMON_ERROR_MESSAGES,
    ROLE_ERROR_MESSAGES,
)
from django.contrib.auth.hashers import make_password
from ..models.user_model import User


class UserCreateSerializer(serializers.Serializer):
    email = serializers.EmailField(
        validators=[email_field_validation],
        error_messages=EMAIL_ERROR_MESSAGES,
    )
    username = serializers.CharField(
        validators=[username_field_validation], error_messages=USERNAME_ERROR_MESSAGES
    )
    name = serializers.CharField(
        validators=[name_field_validation], error_messages=NAME_ERROR_MESSAGES
    )
    password = serializers.CharField(
        validators=[password_validation],
        write_only=True,
        error_messages=COMMON_ERROR_MESSAGES,
    )
    confirm_password = serializers.CharField(
        write_only=True, error_messages=COMMON_ERROR_MESSAGES
    )
    role = serializers.IntegerField(
        validators=[role_validation], error_messages=ROLE_ERROR_MESSAGES
    )

    def validate(self, data):
        password = data.get("password")
        confirm_password = data.get("confirm_password")
        confirm_password_validation(confirm_password, password)
        return data

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        password = validated_data.get("password")
        validated_data.pop("password")
        hashed_password = make_password(password)

        user = User.objects.create(**validated_data, password=hashed_password)
        return user


class UserListSerializer(serializers.ModelSerializer):
    user_role = serializers.CharField(source="get_role_display", read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "name", "user_role"]


class UserManagementSerializer(serializers.ModelSerializer):

    role = serializers.IntegerField(validators=[role_validation], error_messages = ROLE_ERROR_MESSAGES)
    class Meta:
        model = User
        fields = [
            "id",
            "name",
            "email",
            "username",
            "role"
        ]

    def validate_email(self, email):
        return email_field_validation(email, instance=self.instance)

    def validate_name(self, name):
        return name_field_validation(name)

    def validate_username(self, username):
        return username_field_validation(username, instance=self.instance)
    
    def validate_role(self, role):
        return role_validation(role)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            if value:
                print(value)
                setattr(instance, key, value)
        instance.save()
        return instance
