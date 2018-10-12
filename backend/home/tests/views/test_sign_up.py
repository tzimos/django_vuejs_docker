"""
.. module:: home.tests.views.test_sign_up
   :synopsis: LoginView Tests.

.. moduleauthor:: Panos Tzimos<tzimoss@gmail.com>
"""

from django.contrib.auth import get_user_model
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import TestCase, RequestFactory
from django.urls import reverse

from home.views.sign_up import SignUpView

User = get_user_model()


class SignUpViewTestCase(TestCase):

    def setUp(self):
        super(SignUpViewTestCase, self).setUp()
        self.params = {
            'email': 'email@gmail.com',
            'password': '12@asScx3rf',
            'confirm_password': '12@asScx3rf'
        }
        self.request = RequestFactory()
        self.view = SignUpView()

    def tearDown(self):
        users = User.objects.all()
        if users:
            users.delete()
        super(SignUpViewTestCase, self).tearDown()

    def test_post_invalid(self):
        """
        Tests when we provide false credentials if
        the post method returns the form with the errors.
        :return:
        """
        self.params['email'] = ''
        self.params['password'] = ''

        req = self.request.post('/', data=self.params)
        response = self.view.post(req)

        self.assertIn(
            'This field is required.',
            response.content.decode('utf-8')
        )

    def test_post_valid(self):
        """
        Tests if the post method redirects to the taskslist and
        creates a user instance when the provided credentials are
        correct.
        """
        redirect_url = reverse('tasks:tasklist')
        self.assertEqual(
            User.objects.count(),
            0
        )

        req = self.request.post('/', data=self.params)
        middleware = SessionMiddleware()
        middleware.process_request(req)
        req.session.save()

        response = self.view.post(req)
        self.assertTrue(
            User.objects.filter(
                email=self.params['email']
            ).exists())
        self.assertEqual(
            response.url,
            redirect_url
        )
