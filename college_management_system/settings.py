"""
Django settings for college_management_system project.

Generated by 'django-admin startproject' using Django 3.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'huc-dnxw$$b#y6=#$ctf-d!5n7*$h&ebt!%j0wqz$brgw@c!4@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

#HEROKU LIVE PROJECT LINK
#ALLOWED_HOSTS = ["collegemanagementsystem.herokuapp.com"]
ALLOWED_HOSTS = ["*"]

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR,"media")

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR,"static")


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'rest_framework',
    'college_management_app',
]

MIDDLEWARE = [
    # ===Enable Only Making Project Live on Heroku==
    # 'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'college_management_app.LoginCheckMiddleWare.LoginCheckMiddleWare',
]

ROOT_URLCONF = 'college_management_system.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['college_management_app/templates'],
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

WSGI_APPLICATION = 'college_management_system.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': BASE_DIR / 'db.sqlite3',
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'college_management_system',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '3306'
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

# custom user model
AUTH_USER_MODEL = 'college_management_app.CustomUser'
AUTHENTICATION_BACKENDS = ['college_management_app.EmailBackEnd.EmailBackEnd']


# In the real-world you would integrate with an email service like MailGun or SendGrid. For development purposes Django lets us store emails either in the console or as a file. We'll choose the latter and store all sent emails in a folder called sent_emails in our project directory.
# EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
# EMAIL_FILE_PATH = os.path.join(BASE_DIR,"sent_mails")


#send email code
EMAIL_HOST = "smtp.gmail.com"
EMAIl_PORT = 587
EMAIL_HOST_USER = "userakram09@gmail.com"
EMAIL_HOST_PASSWORD = "password00###"
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = "College management System <userakram09@gmail.com>"
