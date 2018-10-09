"""
.. module:: project.wsgi
   :synopsis: Project wsgi module.

.. moduleauthor:: Panos Tzimos<tzimoss@gmail.com>
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings.docker_prod')

application = get_wsgi_application()
