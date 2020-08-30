from .base import *
from dotenv import load_dotenv

load_dotenv()

DEBUG = False

ALLOWED_HOSTS = ['178.154.226.7', '0.0.0.0', 'mathcrib.space']

SECRET_KEY = os.getenv('SECRET_KEY')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
