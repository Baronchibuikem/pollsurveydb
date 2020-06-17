from rest_framework import serializers, status
from polls.models import Choice, Vote
from rest_framework.validators import ValidationError
from django.utils import timezone
from polls.serializers.vote_serializer import VoteSerializer


class ChoiceSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, read_only=True)
    votes = VoteSerializer(many=True, required=False, read_only=True)
    poll_name = serializers.SerializerMethodField()

    class Meta:
        model = Choice
        fields = ['id', 'poll_name', 'votes', "choice_name"]

    def get_poll_name(self, instance):
        return f"{instance.poll_name.poll_question}"

    def create(self, validated_data):
        votes = validated_data.pop('votes', None)
        choice = Choice.objects.create(**validated_data)

        if votes is not None:
            for vote in votes:
                Vote.objects.create(choice=choice, **votes)

        return choice
