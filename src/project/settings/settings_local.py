import os
from project.settings.settings import BASE_DIR

SECRET_KEY = 'z@g9tm#4^v$(p5+&%uvd#$@p=fpuwms=^81-(9-=fcgu#96+zc'

DEBUG = False

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
