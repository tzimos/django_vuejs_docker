"""
.. module:: project.settings.local
   :synopsis: Local settings.

.. moduleauthor:: Panos Tzimos<tzimoss@gmail.com>
"""
from .base import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'tasklist',
        'USER': 'localuser',
        'HOST': 'localhost',
        'PORT': 5432,
        'PASSWORD':'12345'
    }
}
