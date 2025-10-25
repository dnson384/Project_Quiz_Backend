from rest_framework import serializers
from django.contrib.auth.hashers import make_password, check_password
from django.db import transaction
from user.models import User, UserEmail


class RegisterWithEmailSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(required=True, min_length=8, max_length=32)
    confirm_password = serializers.CharField(required=True)
    role = serializers.ChoiceField(choices=User.Role.choices)

    # Check existed email
    def validate_email(self, email_input):
        if User.objects.filter(email=email_input).exists():
            raise serializers.ValidationError("Existed Email")
        return email_input

    # Check equal password & confirm_password
    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                "Password and confirm password do not match"
            )
        attrs.pop("confirm_password")
        return attrs

    def create(self, validated_data):
        password = validated_data.pop("password")
        password_hashed = make_password(password)

        validated_data["login_method"] = "EMAIL"

        try:
            with transaction.atomic():
                user = User.objects.create(**validated_data)

                UserEmail.objects.create(user=user, password_hashed=password_hashed)

            return user
        except Exception as e:
            raise serializers.ValidationError(f"Không thể tạo tài khoản: {str(e)}")


class LoginWithEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is not existed")
        return value

    def validate(self, attrs):
        user = User.objects.filter(email=attrs.get("email")).first()
        user_email = UserEmail.objects.filter(user_id=user.user_id).first()

        if not user_email or not check_password(
            attrs.get("password"), user_email.password_hashed
        ):
            raise serializers.ValidationError("Password incorrect")

        attrs["user"] = user
        return attrs
