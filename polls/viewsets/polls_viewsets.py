from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, BasePermission
from polls.models import Poll, Vote, Choice
from polls.serializers.choices_serializer import ChoiceSerializer
from polls.serializers.vote_serializer import VoteSerializer
from polls.serializers.polls_serializers import PollSerializer


class PollCreate(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Poll
    serializer_class = PollSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save(poll_creator=self.request.user)

    # def list(self, request):
    #     queryset = self.get_queryset()
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)


class PollList(generics.ListAPIView):
    serializer_class = PollSerializer
    queryset = Poll.objects.all()


class PollDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Poll.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = PollSerializer
    lookup_url_kwarg = 'pk'


# class ChoiceList(generics.ListCreateAPIView):
#     permission_classes = (IsAuthenticated,)

#     def get_queryset(self):
#         queryset = Choice.objects.filter(poll_id=self.kwargs.get("pk"))
#         return queryset
#     serializer_class = ChoiceSerializer

#     def perform_create(self, serializer):
#         poll = generics.get_object_or_404(Poll, id=self.kwargs.get("pk"))
#         serializer.save(poll=poll)


#     def update(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         if not request.user.is_authenticated:
#             return Response({'message':'Unable to process request, user is not authenticated'}, status=status.HTTP_403_FORBIDDEN)
#         if instance.created_by != request.user:
#             return Response({'message':'Unable to process request'}, status=status.HTTP_403_FORBIDDEN)
#         if instance.poll_vote.count() > 0:
#             return Response({'message':"Can't edit poll because voting has started"}, status=status.HTTP_403_FORBIDDEN)
#         self.perform_update(serializer)
#         return Response(serializer.data)

#     def get_permissions(self):
#         if self.request.method == "GET":
#             self.permission_classes = (AllowAny,)

#         elif self.request.method == "PUT" or self.request.method == "PATCH":
#             self.permission_classes = (IsAuthenticated, IsPollOwner)

#         return super(PollDetail, self).get_permissions()
