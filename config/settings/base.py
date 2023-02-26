import os
import sys
import json
from pathlib import Path
from qm.db.DB import DBINFO

SECRET_KEY = ""

BASE_DIR = Path(__file__).resolve().parent.parent.parent
PARENT_DIR = Path(__file__).resolve().parent.parent.parent.parent
SECRET_PATH = BASE_DIR / 'config/.config_secret'
SECRET_FILE = SECRET_PATH / 'base.json'

secrets = json.loads(open(SECRET_FILE).read())

for key, value in secrets.items():
    if key == "default_db":
        default_db = DBINFO(value)
    elif key == "lightsail_db":
        lightsail_db = DBINFO(value)
    else:
        setattr(sys.modules[__name__], key, value)


INSTALLED_APPS = [
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',  # 인증
    'django.contrib.sessions',  # 세션
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.contenttypes',

    'rest_framework',
    'rest_framework_api_key',
    'drf_yasg',
    'django_filters',
    'django_crontab',
    'knox',  # 토큰 인증

    'api.apps.ApiConfig',
    'account.apps.AccountConfig',
    'schedule.apps.ScheduleConfig',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',  # 세션 관리
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.AllowAny',],
    'DEFAULT_FILTER_BACKENDS': 'django_filters.rest_framework.DjangoFilterBackend',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10
}

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

CORS_ALLOW_CREDENTIALS = True

CORS_ORIGIN_ALLOW_ALL = False

CORS_ORIGIN_WHITELIST = [
    'http://localhost:3000',  # React
    'http://localhost:80',  # Nginx
    'http://localhost:8000',  # Djgango
]


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': default_db.dbname,
        'USER': default_db.user,
        'PASSWORD': default_db.password,
        'HOST': default_db.host,
        'PORT': 5432,
    },
    'lightsail_db': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': lightsail_db.dbname,
        'USER': lightsail_db.user,
        'PASSWORD': lightsail_db.password,
        'HOST': lightsail_db.host,
        'PORT': 5432,
    },
}

DATABASE_ROUTER = [
    'config.router.MultiDBRouter',
]

CRONJOBS = [
    ### 분 시 일 월 요일
    # 한국 기준금리
    ("0 9 * * *", "schedule.scheduler.crontab_daily.kr_base_rate_restore",
     '>> ' + os.path.join(BASE_DIR, 'config/log/cron_daily.log' + ' 2>&1 ')),
    # 휴장일
    ("0 8 * * 1-5", "schedule.scheduler.crontab_daily.holiday",
     '>> ' + os.path.join(BASE_DIR, 'config/log/cron_daily.log' + ' 2>&1 ')),
    # 주가 > 종목코드 > 이격도
    ("0 16 * * 1-5", "schedule.scheduler.crontab_daily.run_flows",
     '>> ' + os.path.join(BASE_DIR, 'config/log/cron_daily.log' + ' 2>&1 ')),
    # 밸류에이션
    ("0 16 * * 1-5", "schedule.scheduler.crontab_daily.valuation",
     '>> ' + os.path.join(BASE_DIR, 'config/log/cron_daily.log' + ' 2>&1 ')),
    ## INDEX
    # KOSPI
    ("0 16 * * 1-5", "schedule.scheduler.crontab_daily.index_kospi",
     '>> ' + os.path.join(BASE_DIR, 'config/log/cron_daily.log' + ' 2>&1 ')),
    # KOSDAQ
    ("0 16 * * 1-5", "schedule.scheduler.crontab_daily.index_kosdaq",
     '>> ' + os.path.join(BASE_DIR, 'config/log/cron_daily.log' + ' 2>&1 ')),

    ###
    # 16:00 이후 수행해야함
    # per 전략
    ("5 16 * * 1-5", "schedule.scheduler.strategy_per.strategy_per_crontab",
     '>> ' + os.path.join(BASE_DIR, 'config/log/cron_daily.log' + ' 2>&1 ')),
    
    ### valuation 수익률
    # 16:05 이후 수행해야함
    ("10 16 * * 1-5", "schedule.scheduler.crontab_daily.valuation_returns",
     '>> ' + os.path.join(BASE_DIR, 'config/log/cron_daily.log' + ' 2>&1 ')),
    
    # categoryKeywords
    ("5 */3 * * *", "schedule.scheduler.crontab_hourly.category_keywords",
     '>> ' + os.path.join(BASE_DIR, 'config/log/cron_hourly.log' + ' 2>&1 ')),
    # calculate_yields
    # ("* * * * *", "schedule.scheduler.crontab_daily.calculate_yields",
    #  '>> ' + os.path.join(BASE_DIR, 'config/log/cron_daily.log' + ' 2>&1 ')),
]

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

# manage.py collectstatic 실행시 저장되는 static 경로
# STATIC_ROOT = BASE_DIR / "static"
STATIC_ROOT = PARENT_DIR / "react_quantmagnet/public/static"

# manage.py collectstatic 실행시 해당 경로 파일도 복사?
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'



DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# 로그인 성공후 이동하는 URL
LOGIN_REDIRECT_URL = '/'


# 로그아웃시 이동하는 URL
LOGOUT_REDIRECT_URL = '/'

# 세션 타임 아웃
SESSION_COOKIE_AGE = 1200  # 20분
SESSION_SAVE_EVERY_REQUEST = True