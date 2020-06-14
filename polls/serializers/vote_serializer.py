from rest_framework import serializers, status
from polls.models import Vote
from rest_framework.validators import ValidationError
from django.utils import timezone


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ('id', 'choice_name', 'poll_name', "voted_by")

    def validate_poll_name(self, instance):
        if self.context['request'].user.is_authenticated:
            if instance.poll_creator.id == self.context['request'].user:
                raise serializers.ValidationError(
                    "Can't vote on your own poll")
        if instance.poll_expiration_date == timezone.now().date() or instance.poll_expiration_date <= timezone.now().date():
            raise serializers.ValidationError("Poll Ended, Unable to vote")
        return instance
