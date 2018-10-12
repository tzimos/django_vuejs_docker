"""
.. module:: home.tests.views.tasklist.test_tasklist_created
   :synopsis: TaskListCreatedView Tests module.

.. moduleauthor:: Panos Tzimos<tzimoss@gmail.com>
"""
from random import randint
import uuid

from django.contrib.auth import get_user_model

from tasks.models import Task
from tasks.tests.views.tasklist.base_tasklist_tastcase import \
    BaseTaskListHelperTestCase
from tasks.views.taskslist import TaskListCreatedAtView

User = get_user_model()


class TaskListCreatedAtViewTestCase(BaseTaskListHelperTestCase):

    def setUp(self):
        super(TaskListCreatedAtViewTestCase, self).setUp()
        task = Task.objects.first()
        task.done = False
        task.save()
        self.view = TaskListCreatedAtView()

    def test_get_page_not_integer(self):
        """
        Tests when we pass no integer as page if get method
        returns us in the first page.
        """
        data = {'page': "no_int"}
        req = self.request.get('/', data=data)
        response = self.view.get(req)
        html = response.content.decode('utf-8')
        self.assertIn(
            'chosen">1</a>',
            html
        )

    def test_get_page_empty_page(self):
        """
        Tests when we pass a page that is not in the
        current range of pages if it returns us at
        the last page
        """
        data = {'page': 1231}
        req = self.request.get('/', data=data)
        response = self.view.get(req)
        html = response.content.decode('utf-8')
        self.assertIn(
            'chosen">3</a>',
            html
        )
