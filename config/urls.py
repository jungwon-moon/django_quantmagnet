from django.contrib import admin
from django.urls import path, include

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView, SpectacularJSONAPIView

from rest_framework.schemas import get_schema_view

urlpatterns = [
    # admin
    path('admin/', admin.site.urls),
    # 로그인/회원가입
    path('auth/', include('account.urls')),
    # API
    path('api/', include('api.urls')),

    # Documentation
    path('schema/',
         SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/',
         SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/',
         SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
