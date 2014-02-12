"""
Django settings for project project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'c-8@ya@%_cx&uldt2@&lys$&!pqb*g^l7ala*@&17ve^jp^7qw'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'photoalbum',
	'social.apps.django_app.default',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
)

ROOT_URLCONF = 'project.urls'

WSGI_APPLICATION = 'project.wsgi.application'

TEMPLATE_DIRS = (
   os.path.join(BASE_DIR, 'templates'),
)

STATICFILES_DIRS = (
os.path.join(BASE_DIR, 'static'),
)

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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

#E-mail configuration

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'petyalovei@gmail.com'
EMAIL_HOST_PASSWORD = 'llmvxqvwrasgnvnl'
EMAIL_PORT = 587



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, 'static'))

STATIC_URL = '/static/'

#Social configuration
SOCIAL_AUTH_AUTHENTICATION_BACKENDS = (
	'social.backends.facebook.FacebookAppOAuth2'
)

AUTHENTICATION_BACKENDS = (
	'social.backends.facebook.FacebookOAuth2',
	'django.contrib.auth.backends.ModelBackend',
	'social.backends.google.GoogleOAuth2',
)

SOCIAL_AUTH_FACEBOOK_KEY = '1461694107375507'
SOCIAL_AUTH_FACEBOOK_SECRET = 'a6161d36516d24600a4965310775bda3'

SOCIAL_AUTH_GOOGLE_KEY = 'AIzaSyCZbjStQ1-0Lx0KBtKaRAlhjAuKW_rDUSA'
SOCIAL_AUTH_GOOGLE_CLIENT_ID = '585540646570-oj5c755ait17qe64oqsrpbcl69i0qn2m.apps.googleusercontent.com'


SOCIAL_AUTH_LOGIN_URL = '/login/'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/albums/'


