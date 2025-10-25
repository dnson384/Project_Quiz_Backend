from rest_framework import serializers
from .models import User, UserEmail


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "user_id",
            "username",
            "email",
            "role",
            "login_method",
            "avatar_url",
            "created_at",
            "updated_at",
        ]

class UserEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEmail
        fields = [
            "user_id",
            "password_hashed"
        ]