"""
.. module:: home.tests.views.test_login
   :synopsis: LoginView Tests.

.. moduleauthor:: Panos Tzimos<tzimoss@gmail.com>
"""
import json
import uuid
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import TestCase, RequestFactory
from django.urls import reverse

from authentication.forms.login_form import UserLoginForm
from home.views.login import LoginView

User = get_user_model()


class LoginViewTestCase(TestCase):

    def setUp(self):
        super(LoginViewTestCase, self).setUp()
        self.request = RequestFactory()
        self.view = LoginView()
        self.params = {
            'email': 'email@test.com',
            'password': '122£wdSsda'
        }
        self.user = User.create(**self.params)

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

    def test_post_invalid_form(self):
        """
        Tests when the form is invalid if we receive
        errors through JsonResponse.
        """
        params = {
            'data': {
                'email': '',
                'password': ''
            }
        }
        self.view.form_class = UserLoginForm
        req = self.request.post('/')
        req.user = self.user

        response = self.view.post(req)
        response_data = json.loads(response.content)

        # We can prove  that post returns erros by only one error that
        # is included.
        expected_error = 'This field is required.'
        error = response_data['form_errors']['email'][0]
        self.assertEqual(
            expected_error,
            error
        )

    def test_post_valid_form(self):
        """
        Tests if the login view when we provide correct
        credentials, redirects us to the next url.
        """
        params = {
            'data': {
                'email': self.user.email,
                'password': self.params['password']
            }
        }

        redirect_url = reverse('tasks:tasklist')
        self.view.form_class = UserLoginForm
        req = self.request.post('/', data=params['data'])
        req.user = self.user

        middleware = SessionMiddleware()
        middleware.process_request(req)
        req.session.save()
        self.view.request = req

        response = self.view.post(req)
        response_data = json.loads(response.content)

        self.assertEqual(
            response_data['redirect_to'],
            redirect_url
        )

    def test_get_redirect_url(self):
        """
        Tests the get_redirect_url method when
        we provide at post data the next url if
        it returns it after validation.
        """
        redirect_url = 'next_url/'
        params = {
            'data': {
                'email': self.user.email,
                'password': self.params['password'],
                'next': redirect_url
            }
        }

        self.view.form_class = UserLoginForm
        req = self.request.post('/', data=params['data'])
        req.user = self.user

        middleware = SessionMiddleware()
        middleware.process_request(req)
        req.session.save()

        self.view.request = req

        response = self.view.post(req)
        response_data = json.loads(response.content)

        self.assertEqual(
            response_data['redirect_to'],
            redirect_url
        )
