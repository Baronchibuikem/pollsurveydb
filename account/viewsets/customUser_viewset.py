from django.contrib.auth.models import User
from rest_framework import status, generics, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from account.models import CustomUser, BookMark, Likes, Follow
from polls.models import Poll
from knox.models import AuthToken
from rest_framework.permissions import AllowAny
from account.permissions import IsOwnerOrReadonly
from account.serializers.customUser_serializer import RegistrationSerializer, LoginSerializer, GetUserSerializer
from collections import OrderedDict
from django.db.models import F, Count


class LoginViewSet(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data
            return Response({
                "user": GetUserSerializer(user, context=self.get_serializer_context()).data,
                "token": AuthToken.objects.create(user)[1],
                "status": status.HTTP_200_OK,
                "message": "Login successfully"
            })
        else:
            return Response({
                "error": serializer.errors,
                "status": status.HTTP_400_BAD_REQUEST
            })


class RegisterViewSet(generics.GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response({
                "user": GetUserSerializer(user, context=self.get_serializer_context()).data,
                "token": AuthToken.objects.create(user)[1],
                "status": status.HTTP_201_CREATED,
                "message": "Account created successfully"
            })


class UserListAPIView(generics.ListAPIView):
    """
    This endpoint is used for listing all registered users in the platform,
    but only an admin user can access the data in this endpoint
    """

    queryset = CustomUser.objects.all()
    serializer_class = GetUserSerializer
    permission_classes = (permissions.IsAdminUser,)


class UserDetailAPIView(generics.RetrieveUpdateAPIView):
    """
    For retrieving a single user from the database.
    """

    queryset = CustomUser.objects.all()
    serializer_class = GetUserSerializer
    permission_classes = (IsOwnerOrReadonly, )

    def get(self, request, pk, format=None):
        user_info = OrderedDict()
        user = self.get_object()
        serializer = GetUserSerializer(
            user, context=self.get_serializer_context())
        poll = Poll.objects.filter(poll_creator=user).values(
            'poll_question', 'poll_created', 'pk')
        bookmark = BookMark.objects.filter(user=user).values(
            'created', 'poll__pk', question=F('poll__poll_question'))
        like = Likes.objects.filter(user=user).values('like_date', question=F('poll__poll_question'),
                                                      pk=F('poll__pk'), pub_date=F('poll__poll_created'))
        user_info['user'] = serializer.data
        user_info['followers'] = Follow.objects.get_followers(user)
        user_info['followed'] = Follow.objects.get_followings(user)
        user_info['polls'] = poll
        user_info['bookmarks'] = bookmark
        user_info['likes'] = like
        return Response(user_info, status=status.HTTP_200_OK)
