"""
.. module:: home.tests.views.tasklist.test_tasklist_pending
   :synopsis: TaskListPendingView Tests module.

.. moduleauthor:: Panos Tzimos<tzimoss@gmail.com>
"""

from django.contrib.auth import get_user_model
from django.test import RequestFactory

from tasks.models import Task
from tasks.tests.views.tasklist.base_tasklist_tastcase import \
    BaseTaskListHelperTestCase
from tasks.views.taskslist import TaskListPendingView

User = get_user_model()


class TaskListPendingViewTestCase(BaseTaskListHelperTestCase):

    def setUp(self):
        super(TaskListPendingViewTestCase, self).setUp()
        task = Task.objects.first()
        task.done = False
        task.save()
        self.request = RequestFactory()
        self.view = TaskListPendingView()

    def test_get_page_not_integer(self):
        """
        Tests when we pass no integer as page if get method
        returns us in the first page. But in this occasion we
        have only one page. It is just as a simple page without
        pagination.
        """
        data = {'page': "no_int"}
        req = self.request.get('/', data=data)
        response = self.view.get(req)
        html = response.content.decode('utf-8')
        self.assertNotIn(
            'pagination',
            html
        )

    def test_get_page_empty_page(self):
        """
        Tests when we pass a page that is not in the
        current range of pages if it returns us at
        the same page, as we haven't pagination
        with only 1 element in the page.
        """
        data = {'page': 1231}
        req = self.request.get('/', data=data)
        response = self.view.get(req)
        html = response.content.decode('utf-8')
        self.assertNotIn(
            'pagination',
            html
        )

    def test_get_filter_by_pending(self):
        """
        Tests if get method fetches only the data that
        are not done in the queryset.
        """
        done_qs = Task.objects.filter(done=True)
        data = {'page': 1}
        req = self.request.get('/', data=data)
        response = self.view.get(req)
        html = response.content.decode('utf-8')

        self.assertIn(
            Task.objects.filter(done=False).first().title,
            html
        )

        for task in range(4):
            self.assertNotIn(
                done_qs[task].title,
                html
            )
