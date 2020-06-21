from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, BasePermission
from polls.models import Poll, Vote
from polls.permissions import IsPollChoiceOwner, IsPollOwner
from polls.serializers.vote_serializer import VoteSerializer


class CreateVote(generics.CreateAPIView):
    serializer_class = VoteSerializer
    queryset = Vote

    def create(self, request, pk, choice_pk):
        data = {'choice_id': choice_pk, 'poll_id': pk}
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        if request.user.is_authenticated:
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, instance):
        instance.save(voted_by=self.request.user)
        return instance
