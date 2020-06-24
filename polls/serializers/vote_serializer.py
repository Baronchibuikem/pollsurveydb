from rest_framework import serializers, status
from polls.models import Vote
from rest_framework.validators import ValidationError, UniqueTogetherValidator
from django.utils import timezone


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ('choice_id', 'poll_id')
        validators = [
            UniqueTogetherValidator(
                queryset=Vote.objects.all(),
                fields=['choice_id', 'poll_id'],
                message=('you have already voted for a choice in this poll')
            )
        ]

    def validate_poll_id(self, instance):
        if self.context['request'].user.is_authenticated:
            if instance.poll_creator.username == self.context['request'].user:
                raise serializers.ValidationError(
                    "Can't vote on your own poll")
            if instance.poll_expiration_date == timezone.now().date() or instance.poll_expiration_date <= timezone.now().date():
                raise serializers.ValidationError("Poll Ended, Unable to vote")
        return instance
