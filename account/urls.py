from django.urls import path, include
from account.views import (LoginViewSet, RegisterViewSet, UserListAPIView,
                           UserDetailAPIView, LikesAPIView, BookMarkAPIView,
                           DeleteBookMarkedAPIView, DeleteLikesAPIView, ListFollowingAPIView,
                           FollowUserAPIView, ListFollowersAPIView, UnfollowAPIView)
from knox import views as knox_views
from rest_framework import routers

router = routers.DefaultRouter()

# router.register('login', LoginViewSet)

urlpatterns = [
    path("login/", LoginViewSet.as_view(), name="login"),
    path("register/", RegisterViewSet.as_view(), name="register"),
    path("logout/", knox_views.LogoutView.as_view(), name="knox_logout"),
    path("users/", UserListAPIView.as_view(), name="user_list"),
    path("user/<int:pk>/", UserDetailAPIView.as_view(), name="user_detail"),
    path('bookmark-poll/', BookMarkAPIView.as_view(), name='bookmark'),
    path('like-poll/', LikesAPIView.as_view(), name='like'),
    path('delete-bookmark/<int:pk>/',
         DeleteBookMarkedAPIView.as_view(), name='delete_bookmark'),
    path('delete-like/<int:pk>/', DeleteLikesAPIView.as_view(), name='delete-like'),
    path('follow-user/', FollowUserAPIView.as_view(), name='follow_user'),
    path('followers/', ListFollowersAPIView.as_view(), name='followers'),
    path('followings/', ListFollowingAPIView.as_view(), name='followings'),
    path('unfollow-user/<int:id>/', UnfollowAPIView.as_view(), name='unfollow')
]

urlpatterns += router.urls
