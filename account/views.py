from .serializers import *
from django.contrib.auth import login, logout
from rest_framework import generics, views, status
from rest_framework.response import Response


class LoginView(views.APIView):
  authentication_classes = []

  def post(self, request, format=None):
    serializer = LoginSerializer(data=self.request.data,
                                 context={'request': self.request})
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']
    login(request, user)
    return Response(None, status=status.HTTP_202_ACCEPTED)


class ProfileView(generics.RetrieveAPIView):
  serializer_class = UserSerializer

  def get_object(self):
    return self.request.user


class LogoutView(views.APIView):
  authentication_classes = []

  def post(self, request, format=None):
    logout(request)
    return Response(None, status=status.HTTP_204_NO_CONTENT)


class RegisterView(generics.CreateAPIView):
  authentication_classes = []
  queryset = User.objects.all()
  serializer_class = RegisterSerializer


# # UniqueCheck
class EmailUniqueCheck(generics.CreateAPIView):
  authentication_classes = []
  serializer_class = EmailUniqueCheckSerializer

  def post(self, request, format=None):
    serializer = self.get_serializer(data=request.data, context={'request': request})  
    if serializer.is_valid():
      return Response(data={'detail':['사용할 수 있는 이메일입니다.']}, status=status.HTTP_200_OK)
    else:
      detail = dict()
      detail['detail'] = serializer.errors['email']
      return Response(data=detail, status=status.HTTP_400_BAD_REQUEST)


class UsernameUniqueCheck(generics.CreateAPIView):
  authentication_classes = []
  serializer_class = UsernameUniqueCheckSerializer

  def post(self, request, format=None):
    serializer = self.get_serializer(data=request.data, context={'request': request})
    if serializer.is_valid():
      return Response(data={'detail':['사용할 수 있는 아이디입니다.']}, status=status.HTTP_200_OK)
    else:
      detail = dict()
      detail['detail'] = serializer.errors['username']
      return Response(data=detail, status=status.HTTP_400_BAD_REQUEST)