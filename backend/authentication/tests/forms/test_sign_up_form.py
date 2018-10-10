"""
.. module:: authentication.tests.forms.test_signup_form
   :synopsis: Tests for Authentication SignUpForm package.

.. moduleauthor:: Panos Tzimos<tzimoss@gmail.com>
"""
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase, override_settings

from authentication.forms.sign_up_form import SignUpForm

User = get_user_model()


class SignUpFormTestCase(TestCase):

    def setUp(self):
        super(SignUpFormTestCase, self).setUp()
        self.form = SignUpForm()
        self.params = {
            'email': 'test@email',
            'password': 't1st@psadS',
            'confirm_password': 't1st@psadS',
            'superuser': True
        }

    def tearDown(self):
        users = User.objects.all()
        if users.exists():
            users.delete()
        super(SignUpFormTestCase, self).tearDown()

    def test_clean_confirm_password_validation_error(self):
        """
        Tests when there is a password mismatch if a ValidationError
        is raised.
        """
        self.params['password'] = 'sadadf'
        self.form.cleaned_data = self.params

        with self.assertRaises(ValidationError) as err:
            self.form.clean_confirm_password()
        self.assertEqual(
            err.exception.message,
            'The two password fields didn\'t match.'
        )

    def test_clean_confirm_password_no_error(self):
        """
        Tests when passwords are matching each other if
        this validation step is passed without error.
        """
        self.form.cleaned_data = self.params
        result = self.form.clean_confirm_password()

        self.assertEqual(
            result,
            self.params['confirm_password']
        )

    def test__post_clean_password_validator_triggered(self):
        """
        Checks when we provide an invalid confirm_password if
        there are any errors stored at the form.
        """
        self.params['password'] = '12'
        self.params['confirm_password'] = '12'
        self.form.cleaned_data = self.params

        # with self.assertRaises(ValidationError) as err:
        self.form._post_clean()
        self.assertIn(
            'This password is too short.',
            self.form.errors['confirm_password'][0]
        )

    def test_clean_no_errors(self):
        """
        Tests when there is not an Error if clean method
        returns the given params.
        """
        self.form.cleaned_data = self.params
        result = self.form.clean()
        self.assertEqual(
            result,
            self.params
        )

    def test_clean_user_exists(self):
        """
        Tests when the user exists already if a validation error
        is raised.
        """
        User.create(
            email=self.params['email'],
            password=self.params['password']
        )
        self.form.cleaned_data = self.params
        with self.assertRaises(ValidationError) as err:
            self.form.clean()

        expected_msg = 'A user with this email already exists'
        self.assertEqual(
            err.exception.message,
            expected_msg
        )

    @override_settings(DEBUG=True)
    def test_save_superuser_debug_true(self):
        """
        Tests when the field superuser is True under DEBUG mode
        if the user becomes a superuser.
        """
        self.form.cleaned_data = self.params
        user = self.form.save()
        expected_user = User.objects.last()
        self.assertEqual(
            user.pk,
            expected_user.pk
        )
        self.assertTrue(user.is_superuser)

    @override_settings(DEBUG=False)
    def test_save_superuser_debug_false(self):
        """
                Tests when the field superuser is True under DEBUG mode
                if the user becomes a superuser.
                """
        self.form.cleaned_data = self.params
        user = self.form.save()
        expected_user = User.objects.last()
        self.assertEqual(
            user.pk,
            expected_user.pk
        )
        self.assertFalse(user.is_superuser)
