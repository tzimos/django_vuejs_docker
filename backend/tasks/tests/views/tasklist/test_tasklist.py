"""
.. module:: home.tests.views.test_tasklist
   :synopsis: TaskListView Tests module.

.. moduleauthor:: Panos Tzimos<tzimoss@gmail.com>
"""
from random import randint
import uuid

from django.contrib.auth import get_user_model

from tasks.models import Task
from tasks.tests.views.tasklist.base_tasklist_tastcase import \
    BaseTaskListHelperTestCase
from tasks.views.taskslist import TaskListView

User = get_user_model()


class TaskListViewTestCase(BaseTaskListHelperTestCase):

    def setUp(self):
        super(TaskListViewTestCase, self).setUp()
        task = Task.objects.first()
        task.done = False
        task.save()
        self.view = TaskListView()


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

    def test_get_descending(self):
        """
        Tests if we have paginated the objects at
        a descending order.
        """
        qs = Task.objects.order_by('-created')
        # 1st page.
        data1 = {'page': 1}
        req1 = self.request.get('/', data=data1)
        response1 = self.view.get(req1)
        html1 = response1.content.decode('utf-8')

        self.assertIn(
            qs[0].title,
            html1
        )
        self.assertIn(
            qs[1].title,
            html1
        )
        for task in range(2, 5):
            self.assertNotIn(
                qs[task].title,
                html1
            )

        # 2nd page.
        data2 = {'page': 2}
        req2 = self.request.get('/', data=data2)
        response2 = self.view.get(req2)
        html2 = response2.content.decode('utf-8')

        self.assertIn(
            qs[2].title,
            html2
        )
        self.assertIn(
            qs[3].title,
            html2
        )

        self.assertNotIn(
            qs[0].title,
            html2
        )
        self.assertNotIn(
            qs[1].title,
            html2
        )
        self.assertNotIn(
            qs[4].title,
            html2
        )

        # Last page
        data3 = {'page': 3}
        req3 = self.request.get('/', data=data3)
        response3 = self.view.get(req3)
        html3 = response3.content.decode('utf-8')

        self.assertIn(
            qs[4].title,
            html3
        )

        for task in range(4):
            self.assertNotIn(
                qs[task].title,
                html3
            )
