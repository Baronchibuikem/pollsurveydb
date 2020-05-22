from django.urls import path, include
from account.viewsets.customUser_viewset import LoginViewSet
from knox import views as knox_views
from rest_framework import routers

router = routers.DefaultRouter()

router.register('login', LoginViewSet)

urlpatterns = [
    path("auth", include('knox.urls')),
    path("logout", knox_views.LogoutView.as_view(), name="knox_logout")
]

urlpatterns += router.urls
