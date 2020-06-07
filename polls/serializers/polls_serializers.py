from rest_framework import serializers, status
from polls.models import Poll
from rest_framework.validators import ValidationError
from django.utils import timezone


class Poll_Serializer(serializers.ModelSerializer):

    class meta:
        models = Poll
        fields = ("poll_question", "id", "poll_creator",
                  "poll_expiration", "poll_has_expired")
        read_only_fields = ["expired"]

    def get_poller_creator(self, instance):
        return instance.poll_creator.username

    def get_poll_has_expired(self, instance):
        return instance. poll_expiration_date == timezone.now().date() or timezone.now().date() > instance.expire_date

    def get_poller_username_id(self, instance):
        return instance.poll_creator.id

    def get_poller_image(self, instance):
        try:
            return instance.created_by.profile.image.url
        except AttributeError:
            return None

    def create(self, validated_data):
        choices = validated_data.pop('choices', None)
        poll = Poll.objects.create(**validated_data)

        if choices is not None:
            for choice in choices:
                Choice.objects.create(poll=poll, **choice)

        return poll

    def update(self, instance, validated_data):
        instance.question = validated_data.get('question', instance.question)
        instance.expire_date = validated_data.get(
            'expire_date', instance.expire_date)
        instance.choice_type = validated_data.get(
            'choice_type', instance.choice_type)
        instance.save()
        poll_choices = validated_data.get('choices', None)
        if poll_choices is not None:
            for choices in poll_choices:
                try:
                    choice = Choice.objects.get(
                        poll=instance, id=choices.get('id'))

                    if choice.votes.count() > 0:
                        raise serializers.ValidationError(
                            'Poll ongoing unable to edit poll choice ')
                    choice.choice_text = choices.get(
                        'choice_text', choice.choice_text)
                    choice.choice_audio = choices.get(
                        'choice_audio', choice.choice_audio)
                    choice.choice_video = choices.get(
                        'choice_video', choice.choice_video)
                except Choice.DoesNotExist:
                    pass

        return instance

    def to_representation(self, instance):
        ret = super(PollSerializer, self).to_representation(instance)
        request = self.context['request']
        poll_has_been_bookmarked = False
        poll_has_been_liked = False
        poll_has_been_shared = False
        if request.user.is_authenticated:
            if BookMark.objects.filter(user=request.user, poll=instance).exists():
                poll_has_been_bookmarked = True

            if Likes.objects.filter(user=request.user, poll=instance).exists():
                poll_has_been_liked = True

            ret['poll_has_been_bookmarked'] = poll_has_been_bookmarked
            ret['poll_has_been_liked'] = poll_has_been_liked

        ret['total_likes'] = instance.poll_likes.all().count()
        ret['vote_count'] = instance.poll_vote.count()
        return ret
