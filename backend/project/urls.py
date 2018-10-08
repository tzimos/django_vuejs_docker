"""
.. module:: project.urls
   :synopsis: Project wide urls.

.. moduleauthor:: Panos Tzimos<tzimoss@gmail.com>
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('home.urls',namespace='home')),
    path('tasks/',include('tasks.urls',namespace='tasks')),
    path('help/',TemplateView.as_view(template_name='a.html'))
]
