"""
.. module:: project.settings.docker_prod
   :synopsis: Docker production settings.

.. moduleauthor:: Panos Tzimos<tzimoss@gmail.com>
"""
from .base import *


ALLOWED_HOSTS = ['*',]
DEBUG = False

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"