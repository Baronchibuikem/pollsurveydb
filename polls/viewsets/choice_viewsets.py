from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, BasePermission
from polls.models import Poll, Vote, Choice
from polls.serializers.choices_serializer import ChoiceSerializer
from polls.permissions import IsPollChoiceOwner, IsPollOwner


class ChoiceList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChoiceSerializer

    def get_queryset(self):
        queryset = Choice.objects.filter(poll_name_id=self.kwargs.get("pk"))
        return queryset

    def perform_create(self, serializer):
        poll = generics.get_object_or_404(Poll, id=self.kwargs.get("pk"))
        serializer.save(poll=poll)


class ChoiceDelete(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated, IsPollChoiceOwner)
    serializer_class = ChoiceSerializer
    lookup_url_kwarg = 'pk'
    queryset = Choice

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.votes.count() > 0:
            return Response({'message': 'Poll ongoing unable to delete poll choice '}, status=status.HTTP_403_FORBIDDEN)
        return super().delete(request, *args, **kwargs)

    def get_object(self):
        obj = generics.get_object_or_404(
            self.queryset, id=self.kwargs["pk"], poll_name_id=self.kwargs["poll_name_id"])
        # May raise a permission denied
        self.check_object_permissions(self.request, obj)
        return obj


class ChoiceEdit(generics.UpdateAPIView):
    queryset = Choice
    permission_classes = (IsAuthenticated, IsPollChoiceOwner)
    serializer_class = ChoiceSerializer
    lookup_url_kwarg = 'pk'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.votes.count() > 0:
            return Response({'message': 'Poll ongoing unable to edit poll choice '}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def get_object(self):

        obj = generics.get_object_or_404(
            self.queryset, id=self.kwargs["pk"], poll_id=self.kwargs["poll_id"])
        # May raise a permission denied
        self.check_object_permissions(self.request, obj)
        return obj
