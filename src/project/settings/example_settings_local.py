SECRET_KEY = 'z@g9tm#4^v$(p5+&%uvd#$@p=fpuwms=^81-(9-=fcgu#96+zc'

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'DB_NAME',
        'HOST': '127.0.0.1',
        'PORT': 5432,
        'USER': 'django',
        'PASSWORD': 'django'
    }
}

RQ_QUEUES = {
    'default': {
        'HOST': 'localhost',
        'PORT': 6379,
        'ASYNC': False,
        'DB': 3,
        'DEFAULT_TIMEOUT': 360,
    }
}
