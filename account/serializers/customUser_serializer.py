from rest_framework import serializers, status
from account.models import CustomUser
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import ValidationError


class GetUserSerializer(serializers.ModelSerializer):
    """
    Used to convert python objects stored in the database to json objects
    """
    class Meta:
        model = CustomUser
        fields = ("id", "first_name", "last_name", "username",
                  "gender", "email", "position", "bio")


class RegistrationSerializer(serializers.Serializer):
    """
    For user registration
    """
    Gender = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()
    username = serializers.CharField()
    gender = serializers.ChoiceField(choices=Gender, required=False)
    position = serializers.CharField(required=False)
    bio = serializers.CharField(required=False)

    # used for registering a user into the database
    def create(self, validated_data):
        user = CustomUser(first_name=validated_data["first_name"],
                          last_name=validated_data['last_name'],
                          email=validated_data["email"])
        user.set_password(validated_data["password"])
        user.save()
        return user

    def validate_email(self, payload):
        if CustomUser.objects.filter(email__iexact=payload).exists():
            raise serializers.ValidationError({
                "error": 'A user with that email already exists'})
        return payload

    def validate_username(self, payload):
        if CustomUser.objects.filter(username__iexact=payload).exists():
            raise serializers.ValidationError({
                "error": 'A user with that username already exists'})
        return payload


class LoginSerializer(serializers.Serializer):
    """
    Used to convert login data enter by a user from json objects to python objects 
    before saving them in the database
    """
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError({
            "data": "Incorrect Credentials",
            "status": status.HTTP_400_BAD_REQUEST
        })


class ChangePasswordSerializer(serializers.ModelSerializer):
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value

    class Meta:
        model = CustomUser
        fields = ('old_password', 'new_password')
