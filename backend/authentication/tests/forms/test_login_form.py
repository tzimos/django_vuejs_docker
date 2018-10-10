"""
.. module:: authentication.tests.forms.test_login_form
   :synopsis: Tests for Authentication UserLoginForms package.

.. moduleauthor:: Panos Tzimos<tzimoss@gmail.com>
"""
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from authentication.forms.login_form import UserLoginForm

User = get_user_model()


class UserLoginFormTestCase(TestCase):

    def setUp(self):
        super(UserLoginFormTestCase, self).setUp()
        self.form = UserLoginForm()
        self.params = {
            'email': 'test@email',
            'password': 't1st@psadS'
        }

    def test_clean_no_password(self):
        """
        Tests when we don't provide a password to the
        form if there are errors in the form.
        """
        self.params['password'] = ''
        self.form.cleaned_data = self.params
        result = self.form.clean_password()

        # self.assertFalse(is_valid)
        expected_errors = [
            "This field is required",
            "This password is too short. "
            "It must contain at least 8 characters."
        ]
        self.assertEqual(
            expected_errors,
            self.form.errors['password']
        )

    def test_clean_no_user(self):
        """
        Tests if ValidationError is raised when
        user with the provided email does not exist.
        """
        self.form.cleaned_data = self.params
        expected_msg = 'Please check the provided credentials.If you ' \
                       'don\'t have an account please click ' \
                       '<a href="/sign_up/">here</a>'
        with self.assertRaises(ValidationError) as err:
            self.form.clean()
        self.assertEqual(
            err.exception.message,
            expected_msg
        )

    def test_clean_no_authentication(self):
        """
        Tests when the user cannot authenticate
        if ValidationError is raised.
        """
        User.create(**self.params)
        self.form.cleaned_data = self.params
        self.params['password'] = 'asdkonfvsi@@134'

        expected_msg = 'Please check the provided credentials.If you ' \
                       'don\'t have an account please click ' \
                       '<a href="/sign_up/">here</a>'
        with self.assertRaises(ValidationError) as err:
            self.form.clean()
        self.assertEqual(
            err.exception.message,
            expected_msg
        )
        User.objects.all().delete()

    def test_clean_no_errors(self):
        """
        Tests when we provide the correct credentials if
        there is not an error in the form.
        """
        User.create(**self.params)
        self.form.cleaned_data = self.params
        self.form.clean()

        self.assertEqual(self.form.errors, {})
        User.objects.all().delete()

    def test_confirm_login_allowed_not_active_user(self):
        """
        Tests when the user is not activated if it is raised
        a ValidationError.
        """
        user = User.create(**self.params)
        user.is_active = False
        user.save()

        with self.assertRaises(ValidationError) as err:
            self.form.confirm_login_allowed(user)
        self.assertEqual(
            err.exception.message,
            "This account is inactive."
        )
        User.objects.all().delete()
