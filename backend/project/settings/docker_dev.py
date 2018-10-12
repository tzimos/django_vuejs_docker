"""
.. module:: project.settings.docker_dev
   :synopsis: Docker dev settings.

.. moduleauthor:: Panos Tzimos<tzimoss@gmail.com>
"""
from .base import *


ALLOWED_HOSTS = ['*',]

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"