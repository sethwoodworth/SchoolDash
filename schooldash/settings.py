# Django settings for schooldash project.
import os.path

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Seth Woodworth', 'seth@sethish.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'local.sqlite3',
    }
}

TIME_ZONE = 'America/Detroit'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = False
USE_L10N = True

# Filesystem root for user-uploaded files
MEDIA_ROOT = os.path.join(os.path.dirname(__file__), '../media/')
# Web root for displaying user-uploaded files
MEDIA_URL = 'media/'

# Compiled static files in a single dest folder
# DO NOT STORE THINGS IN THIS FILE
STATIC_ROOT = os.path.join(os.path.dirname(__file__), './static/')
# URL prefix for static files.
STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/admin_media/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put static files in the partent directory ../static
    os.path.join(os.path.dirname(__file__), '../static'),
)

# List of finder classes that know how to find static files in various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Make this unique, and don't share it with anybody.
# This is obviously not the SECRET_KEY we use in production override with local_settings
SECRET_KEY = ')#q(2^+jazd&=!mpu&5$$be$o&smq6f9(&1!+y9*$(lus8_i&d'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'schooldash.urls'

TEMPLATE_DIRS = (
    # Wherever you go, there you are
    os.path.join(os.path.dirname(__file__), 'templates'),
)

## ---- start: Userena ---- ##

AUTH_PROFILE_MODULE = 'userinfo.UserProfile'
ANONYMOUS_USER_ID   = -1
LOGIN_REDIRECT_URL  = '/dash/'
USERENA_SIGNIN_REDIRECT_URL = '/dash/'
LOGIN_URL           = '/accounts/signin/'
LOGOUT_URL          = '/accounts/signout/'
USERENA_DEFAULT_PRIVACY = 'closed'

AUTHENTICATION_BACKENDS = (
    'userena.backends.UserenaAuthenticationBackend',
    'guardian.backends.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
)

## ---- end: Userena   ---- ##

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',

    # Userena required
    'guardian',
    'easy_thumbnails',
    'userena',

    # Our apps
    'dataload',
    'datashow',
    'userinfo',
)

# Folder location of the csv files of student data
DATA_DIR = os.path.join(os.path.dirname(__file__), '../data/')

try:
    from local_settings import *
except:
    pass
