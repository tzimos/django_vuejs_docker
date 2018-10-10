"""
.. module:: project.settings.testing
   :synopsis: Settings for testing container.

.. moduleauthor:: Panos Tzimos<tzimoss@gmail.com>
"""

from .base import *

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}
