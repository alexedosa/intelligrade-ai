from rest_framework import serializers
from django.contrib.auth.hashers import make_password, check_password
from .models import CustomUser


class CreateUserSerializer(serializers.ModelSerializer):
    """
    Reusable serializer for creating any user account.
    Role is always forced by the view — never trusted from request body.
    """
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = CustomUser
        fields = [
            'username',
            'email',
            'password',
            'password2',
            'first_name',
            'last_name',
        ]

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "An account with this email already exists."
            )
        return value

    def validate_username(self, value):
        if CustomUser.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                "This username is already taken."
            )
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        
        validated_data['password'] = make_password(validated_data['password'])

        user = CustomUser.objects.create(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    """
    Validates email and password.
    Passes the authenticated user object forward to the view.
    """
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate_email(self, value):
        if not CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "No account found with this email."
            )
        return value

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Invalid credentials.")

        if not check_password(password, user.password):
            raise serializers.ValidationError("Incorrect password.")

        if not user.is_active:
            raise serializers.ValidationError(
                "This account has been deactivated."
            )

        attrs['user'] = user
        return attrs