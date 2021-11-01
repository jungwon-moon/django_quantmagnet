from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


app_name = 'common'

urlpatterns = [
    path('signin/', auth_views.LoginView.as_view(template_name='common/signin.html',
         redirect_authenticated_user=True), name='signin'),
    path('signout/', auth_views.LogoutView.as_view(), name='signout'),
    path('register/', views.register, name='register'),
]
