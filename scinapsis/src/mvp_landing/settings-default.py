"""
Django settings for mvp_landing project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

PROJECT_DIR = os.path.dirname(__file__)
BASE_DIR = os.path.dirname(PROJECT_DIR)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'z39xhuj48ebi(789-_68$iq6uz63a1zqpff5zc706_0zqwp9&%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['*']

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025

# Application definition


TEMPLATE_CONTEXT_PROCESSORS = [
  'django.contrib.auth.context_processors.auth',
  'django.core.context_processors.i18n',
  'django.core.context_processors.request',
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
]


INSTALLED_APPS = (
  'django.contrib.auth',
  'django.contrib.admin',
  'django.contrib.sites',
  'django.contrib.sessions',
  'django.contrib.messages',
  'django.contrib.staticfiles',
  'django.contrib.contenttypes',
  'social.apps.django_app.default',
  'taggit',
  'blog',
  'tinymce',
  'bootstrapform',
  'debug_toolbar'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware'
)


ROOT_URLCONF = 'mvp_landing.urls'

WSGI_APPLICATION = 'mvp_landing.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Chicago'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SITE_ID=1

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

STATIC_URL = '/static/'

#Template location
TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(PROJECT_DIR), "templates"),
)

STATIC_ROOT = ''
if DEBUG:
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "media")
    STATICFILES_DIRS = (
       os.path.join(os.path.dirname(BASE_DIR), "static"),
    )

else:
    STATIC_ROOT = '/Users/sinkpoint/dev/scinapsisdev/scinapsis/static'

TINYMCE_JS_ROOT = os.path.join(STATIC_URL,'tiny_mce')
TINYMCE_JS_URL = os.path.join(STATIC_URL, "tiny_mce/tiny_mce_src.js")
TINYMCE_DEFAULT_CONFIG = {
    'plugins': "table,spellchecker,contextmenu,paste,searchreplace,save,youtube",
    'theme': "advanced",
    'remove_trailing_brs': 'false',
    'theme_advanced_font_sizes': "10px,12px,13px,14px,16px,18px,20px",
    'font_size_style_values': "12px,13px,14px,16px,18px,20px",
    'theme_advanced_buttons1':"bold,italic,underline,strikethrough,sub,sup,separator,justifyleft,justifycenter,justifyright,justifyfull,separator,formatselect,fontselect,fontsizeselect",
    'theme_advanced_buttons2':"bullist,numlist,outdent,indent,ltr,rtl,separator,link,unlink,anchor,image,separator,table,insertdate,inserttime,advhr,emotions,media,youtube,charmap,code,separator,pasteword,separator,undo,redo",
}
TINYMCE_SPELLCHECKER = True

# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'mysite.log',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers':['file'],
            'propagate': True,
            'level':'DEBUG',
        },
        'MYAPP': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
    }
}
