"""
.. module:: home.tests.forms.test_create_task
   :synopsis: TaskCreateForm Tests module.

.. moduleauthor:: Panos Tzimos<tzimoss@gmail.com>
"""
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from tasks.forms.create_task import TaskCreateForm

User = get_user_model()


class MockRequest():

    def __init__(self, user):
        self.user = user


class TaskCreateFormTestCase(TestCase):

    def test_save(self):
        params = {
            'email': 'test@email.com',
            'password': 'test@2pasworD'
        }
        user = User.create(**params)
        request = MockRequest(user)
        form_params = {
            'title': 'title',
            'details': 'details',
            'due_date': timezone.now(),
        }
        form = TaskCreateForm(
            request=request,
        )
        form.cleaned_data = form_params
        task = form.save()
        self.assertEqual(
            task.author,
            user
        )

        task.delete()
        user.delete()

    def test_clean(self):
        """
        Tests when we don't provide at least in one field
        data if a ValidationError is raised.
        """
        params = {
            'email': 'test@email.com',
            'password': 'test@2pasworD'
        }
        user = User.create(**params)
        request = MockRequest(user)
        form_params = {
            'title': 'title',
            'details': '',
            'due_date': timezone.now()
        }
        form = TaskCreateForm(
            request=request,
        )
        form.cleaned_data = form_params
        with self.assertRaises(ValidationError) as err:
            form.clean()
        self.assertEqual(
            err.exception.message,
            'Please correct the errors below'
        )