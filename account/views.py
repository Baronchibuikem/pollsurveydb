from django.contrib.auth.models import User
from rest_framework import status, generics, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from account.models import CustomUser, BookMark, Likes, Follow
from polls.models import Poll, Choice
from knox.models import AuthToken
from rest_framework.permissions import AllowAny
from account.permissions import IsOwnerOrReadonly
from account.serializers import (RegistrationSerializer, LoginSerializer, GetUserSerializer, BookmarkSerializer,
                                 LikeSerializer, FollowSerializer)
from collections import OrderedDict
from django.db.models import F, Count


class LoginViewSet(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data
            return Response({
                # "user": GetUserSerializer(user, context=self.get_serializer_context()).data,
                'user': user.pk,
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
                "user": user.pk,
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
        # choice = Choice.objects.values_list("choice_name")
        poll = Poll.objects.filter(poll_creator=user).values(
            'poll_question', 'poll_created', 'poll_expiration_date', 'pk', "poll_creator__username", "poll_has_expired")
        bookmark = BookMark.objects.filter(user=user).values(
            'created', 'poll__pk', question=F('poll__poll_question'))
        like = Likes.objects.filter(user=user).values('like_date', question=F('poll__poll_question'),
                                                      pk=F('poll__pk'), pub_date=F('poll__poll_created'),
                                                      poll_creator_username=F(
                                                          "poll__poll_creator__username"),
                                                      poll_creator_firstname=F(
                                                          'poll__poll_creator__first_name'),
                                                      poll_creator_lastname=F(
                                                          'poll__poll_creator__last_name'),
                                                      poll_creator_bio=F('poll__poll_creator__bio'))
        user_info['user'] = serializer.data
        user_info['followers'] = Follow.objects.get_followers(user)
        user_info['followed'] = Follow.objects.get_followings(user)
        user_info['polls'] = poll
        user_info['bookmarks'] = bookmark
        user_info['likes'] = like
        # print(user_info)
        return Response(user_info, status=status.HTTP_200_OK)


class BookMarkAPIView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    """ get all the user bookmarks
    """
    queryset = BookMark.objects.all()
    serializer_class = BookmarkSerializer

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user).all()


class LikesAPIView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Likes.objects.all()
    serializer_class = LikeSerializer

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user).all()


class DeleteBookMarkedAPIView(generics.DestroyAPIView):
    queryset = BookMark
    serializer_class = BookmarkSerializer
    lookup_field = 'pk'


class DeleteLikesAPIView(generics.DestroyAPIView):
    queryset = Likes
    serializer_class = LikeSerializer
    lookup_field = 'pk'


class FollowUserAPIView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = FollowSerializer
    queryset = Follow


class ListFollowersAPIView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = FollowSerializer
    queryset = Follow

    def get_queryset(self):
        return self.queryset.objects.get_followers(self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            return self.get_paginated_response(queryset)
        return Response(queryset)


class ListFollowingAPIView(ListFollowersAPIView):

    def get_queryset(self):
        return self.queryset.objects.get_followings(self.request.user)


class UnfollowAPIView(generics.DestroyAPIView):
    # This is used to delete a user from a logged in users followers list.
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Follow
    serializer_class = FollowSerializer
    lookup_field = 'id'
