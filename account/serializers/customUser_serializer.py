from rest_framework import serializers
from account.models import CustomUser
from django.contrib.auth import authenticate


class GetUserSerializer(serializers.ModelSerializer):
    """
    Used to convert python objects stored in the database to json objects
    """
    class Meta:
        model = CustomUser
        fields = ("id", "first_name", "last_name", "username",
                  "gender", "email", "position", "bio")


class RegisterSerializer(serializers.ModelSerializer):
    """
    Used to convert data from json to python objects before saving them to 
    the database
    """
    class Meta:
        model = CustomUser
        fields = ("id", "fullname", "organization", "designation",
                  "purpose_of_data", "email", 'password', "image")
        extra_kwargs = {"password": {"write_only": True},
                        'id': {"read_only": True}}

    # def create(self, validated_data):
    #     user = CustomUser.objects.create_user(
    #             validated_data["email"],
    #             validated_data["password"],
    #             validated_data["fullname"],
    #             validated_data["organization"],
    #             validated_data["designation"],
    #             validated_data["purpose_of_data"],)
    #     return user


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
        raise serializers.ValidationError("Incorrect Credentials")