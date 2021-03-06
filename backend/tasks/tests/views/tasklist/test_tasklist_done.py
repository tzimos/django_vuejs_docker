"""
.. module:: home.tests.views.tasklist.test_tasklist_done
   :synopsis: TaskListDoneView Tests module.

.. moduleauthor:: Panos Tzimos<tzimoss@gmail.com>
"""
from django.contrib.auth import get_user_model

from tasks.models import Task
from tasks.tests.views.tasklist.base_tasklist_tastcase import \
    BaseTaskListHelperTestCase
from tasks.views.taskslist import TaskListDoneView

User = get_user_model()


class TaskListDoneViewTestCase(BaseTaskListHelperTestCase):

    def setUp(self):
        super(TaskListDoneViewTestCase, self).setUp()
        for task in Task.objects.all():
            task.done = False
            task.save()
        self.view = TaskListDoneView()

    def tearDown(self):
        Task.objects.all().delete()
        User.objects.all().delete()
        super(TaskListDoneViewTestCase, self).tearDown()

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
        the last page
        """
        data = {'page': 1231}
        req = self.request.get('/', data=data)
        response = self.view.get(req)
        html = response.content.decode('utf-8')
        self.assertNotIn(
            'pagination',
            html
        )

    def test_get_filter_by_done(self):
        """
        Tests if get method fetches only the data that
        are done in the queryset.
        """
        task = Task.objects.first()
        task.done = True
        task.save()
        not_done_qs = Task.objects.filter(done=False)
        data = {'page': 1}
        req = self.request.get('/', data=data)
        response = self.view.get(req)
        html = response.content.decode('utf-8')

        self.assertIn(
            Task.objects.filter(done=True).first().title,
            html
        )

        for task in range(4):
            self.assertNotIn(
                not_done_qs[task].title,
                html
            )
