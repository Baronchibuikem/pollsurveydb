from rest_framework import serializers, status
from polls.models import Poll, Choice
from account.models import BookMark, Likes
from rest_framework.validators import ValidationError
from django.utils import timezone
from polls.serializers.choices_serializer import ChoiceSerializer


class PollSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, required=False)
    poll_creator = serializers.SerializerMethodField()
    poll_has_expired = serializers.SerializerMethodField()
    poll_creator_image = serializers.SerializerMethodField()
    poll_creator_fullname = serializers.SerializerMethodField()
    image = serializers.ImageField(source="poll_creator.image", required=False)

    # poll_creator_id = serializers.SerializerMethodField()

    class Meta:
        model = Poll
        fields = ("poll_question", "id", "poll_creator", 'poll_creator_image', "poll_creator_id",
                  "poll_expiration_date", "poll_has_expired", 'image',
                  "poll_creator_fullname", "choices")
        read_only_fields = ["expired", 'poll_has_expired']

    # Read up serializerMethod on the official doc to get what the methods below are doing
    def get_poll_creator(self, instance):
        return instance.poll_creator.username

    def get_poll_creator_fullname(self, instance):
        fullname = f'{instance.poll_creator.first_name} {instance.poll_creator.last_name}'
        return fullname

    def get_poll_has_expired(self, instance):
        return instance.poll_expiration_date == timezone.now().date() or timezone.now().date() > instance.poll_expiration_date

    def get_poll_creator_id(self, instance):
        return instance.poll_creator.customuser.id

    def get_poll_creator_image(self, instance):
        try:
            return instance.poll_creator.image.url
        except ValueError:
            return None

    def create(self, validated_data):
        choices = validated_data.pop('choices', None)
        poll = Poll.objects.create(**validated_data)

        if choices is not None:
            for choice in choices:
                Choice.objects.create(poll_name=poll, **choice)

        return poll

    def update(self, instance, validated_data):
        instance.question = validated_data.get(
            'poll_question', instance.poll_question)
        # instance.expire_date = validated_data.get(
        #     'expire_date', instance.expire_date)

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
