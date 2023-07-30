from django.contrib import admin
from django.urls import path, include

# from django.conf.urls import url
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


urlpatterns = [
    # admin
    path('admin/', admin.site.urls),
    # 로그인/회원가입
    path('auth/', include('account.urls')),
    # API
    path('api/', include('api.urls')),
]

schema_view = get_schema_view(
    openapi.Info(
        title='QuantMagnet API',
        default_version='v1',
        description='''
        https://quantmag.net
        웹 사이트에 사용되는 API를 작성한 문서입니다.
        ''',
        contact=openapi.Contact(email="quantmagnet@gmail.com")
    ),
    validators=['flex'],
    public=True,
    permission_classes=(permissions.AllowAny,),
    patterns=urlpatterns,
)

urlpatterns += [
    # Documentation
    path('swagger<str:format>', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

