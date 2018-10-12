"""
.. module:: home.tests.models.tasks
   :synopsis: Tasks Model Tests module.

.. moduleauthor:: Panos Tzimos<tzimoss@gmail.com>
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from tasks.models import Task

User = get_user_model()


class TaskModelTestCase(TestCase):

    def test_string_repr(self):
        """
        Tests the string representation of a task
        """
        tz = timezone.now()
        user = User.create(email='asn@gmail.com', password='123££Qsdd')
        params = {
            'title': 'title',
            'details': 'details',
            'due_date': tz,
            'author': user
        }
        task = Task.objects.create(**params)
        repr = task.__str__()
        self.assertEqual(
            repr,
            'Title: {title} || Author:{author}'.format(
                title=task.title,
                author=task.author
            )
        )
        Task.objects.all().delete()
        User.objects.all().delete()