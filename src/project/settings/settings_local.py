SECRET_KEY = 'z@g9tm#4^v$(p5+&%uvd#$@p=fpuwms=^81-(9-=fcgu#96+zc'

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'zakupki_notifier',
        'HOST': '127.0.0.1',
        'PORT': 5432,
        'USER': 'artem',
        'PASSWORD': '405b9c'
    }
}
