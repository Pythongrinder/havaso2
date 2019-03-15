"""
Django settings for havasoweb project.

Generated by 'django-admin startproject' using Django 2.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""
from havasoweb.settings_general import *

ALLOWED_HOSTS = ['0.0.0.0', '127.0.0.1']

website = "0.0.0.0:8989"

CELERY_BROKER_URL = "amqp://localhost//"

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

SITE_ID = 5