from rest_framework import serializers, status
from account.models import CustomUser, Follow, BookMark, Follow, Likes
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import ValidationError
from polls.serializers.polls_serializers import PollSerializer


class FollowSerializer(serializers.ModelSerializer):
    """Follower Serializer"""

    class Meta:
        model = Follow
        fields = '__all__'


class GetUserSerializer(serializers.ModelSerializer):
    """
    Used to convert python objects stored in the database to json objects
    """
    polls = PollSerializer(many=True, required=False)
    user_fullname = serializers.SerializerMethodField()
    follow_status = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ("id", "user_fullname", "username",
                  "gender", "email", "position", "bio", "follow_status", "polls")

    def get_user_fullname(self, instance):
        return f"{self.instance.first_name} {self.instance.last_name}"

    def get_follow_status(self, instance):
        follow_stat = {}
        request = self.context.get('request',  None)
        if request is not None:
            user = request.user
            if user.is_authenticated:
                follower_list = Follow.objects.get_followers_list(instance)
                if instance == user:
                    return follow_stat

                if user.pk in follower_list:
                    follow_stat['is_following'] = True
                else:
                    follow_stat['is_following'] = False

                following_list = Follow.objects.get_followings_list(instance)

                if user.pk in following_list:
                    follow_stat['is_followed'] = True
                else:
                    follow_stat['is_followed'] = False

        return follow_stat


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


# class ChangePasswordSerializer(serializers.ModelSerializer):
#     """
#     Serializer for password change endpoint.
#     """
#     old_password = serializers.CharField(required=True)
#     new_password = serializers.CharField(required=True)

#     def validate_new_password(self, value):
#         validate_password(value)
#         return value

#     class Meta:
#         model = CustomUser
#         fields = ('old_password', 'new_password')


class BookmarkSerializer(serializers.ModelSerializer):
    poll_question_text = serializers.SerializerMethodField()

    def get_poll_question_text(self, instance):
        return str(instance.poll)

    class Meta:
        model = BookMark
        fields = ('id', 'poll', 'user', 'created', 'poll_question_text')


class LikeSerializer(serializers.ModelSerializer):
    poll_question_text = serializers.SerializerMethodField()

    class Meta:
        model = Likes
        fields = ('id', 'poll', 'user', 'like_date',  'poll_question_text')

    def get_poll_question_text(self, instance):
        return str(instance.poll.poll_question)
