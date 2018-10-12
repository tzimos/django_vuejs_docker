"""
.. module:: home.tests.forms.test_edit_task
   :synopsis: TaskEditForm Tests module.

.. moduleauthor:: Panos Tzimos<tzimoss@gmail.com>
"""
from django.http import Http404
from django.test import TestCase
from django.utils import timezone

from tasks.forms.edit_task import TaskEditForm
from tasks.models import Task


class TaskEditFormTestCase(TestCase):

    def setUp(self):
        super(TaskEditFormTestCase, self).setUp()
        self.form_params = {
            'title': 'title',
            'details': 'details',
            'due_date': timezone.now(),
        }

    def test_save_no_task_id(self):
        """
        Tests when we don't provide a task id if Http404 error
        is raised.
        """
        form = TaskEditForm()
        form.cleaned_data = self.form_params
        with self.assertRaises(Http404):
            form.save()

    def test_save(self):
        """
        Tests when the save method is called if the new data
        that are passed through the fields are store at the
        current task.
        """
        task = Task.objects.create(**self.form_params)
        initial_title = task.title
        initial_pk = task.pk
        form = TaskEditForm(task_id=task.id)

        alternative_title = 'Other better title'
        form.title = alternative_title
        form.cleaned_data = {'title': alternative_title}
        edited_task = form.save()

        task.refresh_from_db()
        self.assertEqual(
            initial_pk,
            edited_task.pk
        )
        self.assertNotEqual(
            initial_pk,
            alternative_title
        )
        self.assertNotEqual(
            initial_title,
            alternative_title
        )
        Task.objects.all().delete()