from django.contrib.auth import login, logout
from rest_framework import generics, permissions, views, status
from rest_framework.response import Response
from .serializers import *


class LoginView(views.APIView):
  authentication_classes = []
  permissions_classes = [permissions.AllowAny]

  def post(self, request, format=None):
    serializer = LoginSerializer(data=self.request.data,
                                 context={'request': self.request})
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']
    login(request, user)
    return Response(None, status=status.HTTP_202_ACCEPTED)


class ProfileView(generics.RetrieveAPIView):
  permissions_classes = [permissions.AllowAny]
  serializer_class = UserSerializer

  def get_object(self):
    return self.request.user


class LogoutView(views.APIView):
  authentication_classes = []
  permissions_classes = [permissions.AllowAny]

  def post(self, request, format=None):
    logout(request)
    return Response(None, status=status.HTTP_204_NO_CONTENT)


class RegisterView(generics.CreateAPIView):
  queryset = User.objects.all()
  permission_classes = [permissions.AllowAny]
  serializer_class = RegisterSerializer
