"""
.. module:: home.urls
   :synopsis: Home urls module.

.. moduleauthor:: Panos Tzimos<tzimoss@gmail.com>
"""

from django.contrib.auth.views import LogoutView
from django.urls import path
from django.conf import settings

from home.views.login import LoginView
from home.views.sign_up import SignUpView

app_name = 'home'

urlpatterns = [
    path('sign_up/', SignUpView.as_view(), name='sign_up'),
    path('', LoginView.as_view(), name='login'),
    path(
        'logout/',
        LogoutView.as_view(),
        {'next_page': settings.LOGOUT_REDIRECT_URL},
        name='logout'
    )
]
