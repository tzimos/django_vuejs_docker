"""
.. module:: home.tests.views.login
   :synopsis: LoginView Tests.

.. moduleauthor:: Panos Tzimos<tzimoss@gmail.com>
"""
import uuid
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django_dynamic_fixture import G

from home.views.login import LoginView

User = get_user_model()

class LoginViewTestCase(TestCase):

    def setUp(self):
        super(LoginViewTestCase, self).setUp()
        self.request = RequestFactory()
        self.view = LoginView()
        self.user = G(
            User,
            fill_nullable_fields=False
        )

    def tearDown(self):
        self.user.delete()
        super(LoginViewTestCase, self).tearDown()

    @patch('home.views.login.get_token')
    def test_get(self, mocked_csrf_token):
        """
        Tests if get method returns the correct context too the template.
        """
        req = self.request.get('/')
        req.user = self.user
        csrf_token_value = str(uuid.uuid4())
        login_url = reverse('home:login')
        mocked_csrf_token.return_value = csrf_token_value

        response = self.view.get(req)

        self.assertIn(
            csrf_token_value,
            response.content.decode('utf-8')
        )
        self.assertIn(
            login_url,
            response.content.decode('utf-8')
        )
