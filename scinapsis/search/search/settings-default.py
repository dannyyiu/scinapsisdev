"""
Django settings for search project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
PROJECT_DIR = os.path.dirname(__file__)
BASE_DIR = os.path.dirname(PROJECT_DIR)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'guu*(e65ph=nzgc4%g7e@hy5yv%=71h9gl(cfe6^+nlzxwsal3'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.sites',
    'grappelli.dashboard',
    'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social.apps.django_app.default',
    'userprofile',
    'search',
    'bootstrapform',
    'bootstrap3',
    'debug_toolbar',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',

)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware'
)

TEMPLATE_CONTEXT_PROCESSORS = [
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
    'allauth.account.context_processors.account',
    'allauth.socialaccount.context_processors.socialaccount'
]

AUTHENTICATION_BACKENDS = (
   # 'social.backends.facebook.FacebookOAuth2',
   # 'social.backends.google.GoogleOAuth2',
   # 'social.backends.twitter.TwitterOAuth',
   'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend'
)

ACCOUNT_EMAIL_REQUIRED = True

ROOT_URLCONF = 'search.urls'

WSGI_APPLICATION = 'search.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME' : 'scp_users',
        'USER': 'root',
        'PASSWORD': 'harahara'
    },
    'search_db': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME' : 'scinapsis',
        'USER': 'root',
        'PASSWORD': 'harahara'
    }
}

DATABASE_ROUTERS = ['search.routers.SearchDbRouter']


# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',

]

STATIC_URL = '/static/'

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    MEDIA_URL = '/media/'
    STATIC_ROOT = ''
    MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "media")
    STATICFILES_DIRS = (
       os.path.join(os.path.dirname(BASE_DIR), "static"),
    )

else:
    STATIC_ROOT = '/Users/sinkpoint/dev/scinapsis/scinapsis/static'


#Template location
TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(PROJECT_DIR), "templates"),
)


SOCIAL_AUTH_URL_NAMESPACE = 'social'
LOGIN_REDIRECT_URL = '/'

SOCIAL_AUTH_FACEBOOK_KEY='1379985962300126'
SOCIAL_AUTH_FACEBOOK_SECRET='b99684d153286079f2e15eeb5f6d3506'

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '454383567577-ufug19j75ga7s84tntant8utfhmre2dr.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'H2x7jiAUWXPjGVe1XB8k4oqI'

LOGIN_URL = '/accounts/login/'
SITE_ID = 1


GRAPPELLI_INDEX_DASHBOARD = 'search.dashboard.CustomIndexDashboard'

