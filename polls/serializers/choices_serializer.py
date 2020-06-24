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

    def to_representation(self, instance):
        """
        Used to return total number of votes in a choice and name of registered voters
        """
        from polls.utils import filter_votes
        # this extends the instances of ChoiceSerializer
        ret = super(ChoiceSerializer, self).to_representation(instance)
        try:
            choice_vote_count = instance.votes.all().count()
        except AttributeError:
            return ret
        else:
            ret['choice_vote_count'] = choice_vote_count

        ret['registered_voter'] = filter_votes(
            instance.votes.values('voted_by__username'))

        return ret
