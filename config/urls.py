from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # admin
    path('admin/', admin.site.urls),
    # 로그인/회원가입
    path('auth/', include('account.urls')),
    # API
    path('api/', include('api.urls')),
]
