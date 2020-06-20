from django.urls import path, include
from account.viewsets.customUser_viewset import LoginViewSet, RegisterViewSet, UserListAPIView, UserDetailAPIView
from knox import views as knox_views
from rest_framework import routers

router = routers.DefaultRouter()

# router.register('login', LoginViewSet)

urlpatterns = [
    path("login/", LoginViewSet.as_view(), name="login"),
    path("register/", RegisterViewSet.as_view(), name="register"),
    path("logout/", knox_views.LogoutView.as_view(), name="knox_logout"),
    path("users/", UserListAPIView.as_view(), name="user_list"),
    path("user/<int:pk>/", UserDetailAPIView.as_view(), name="user_detail")
]

urlpatterns += router.urls
