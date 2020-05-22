from django.contrib.auth.models import User
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from account.models import CustomUser
from account.serializers.customUser_serializer import RegistrationSerializer, LoginSerializer


class LoginViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = LoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data
            return Response({
                "user": UserSerializer(user, context=self.get_serializer_context()).data,
                "token": AuthToken.objects.create(user)[1],
                "status": status.HTTP_201_CREATED,
                "message": "Account created successfully"
            })
        else:
            return Response({
                "error": serializer.errors,
                "status": status.HTTP_400_BAD_REQUEST
            })
