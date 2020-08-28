import django_heroku

from .base import *
from dotenv import load_dotenv

load_dotenv()

DEBUG = True

SECRET_KEY = os.getenv('SECRET_KEY')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

django_heroku.settings(locals())
