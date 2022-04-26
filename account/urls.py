from django.urls import path
from account.views import *

app_name ="auth"

urlpatterns = [
  # path("register/", Register_views.as_view()),
  path("register/", RegisterView.as_view()),
  path("login/", LoginView.as_view()),
  path("profile/", ProfileView.as_view()),
  path("logout/", LogoutView.as_view()),
]
