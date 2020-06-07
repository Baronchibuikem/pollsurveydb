from rest_framework import serializers, status
from polls.models import Choice
from rest_framework.validators import ValidationError
from django.utils import timezone


class ChoiceSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, read_only=True)
    votes = VoteSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Choice
        fields = ['id', 'choice_text', 'votes', ]

    def create
