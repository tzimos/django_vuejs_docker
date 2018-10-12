"""
.. module:: home.tests.views.test_tasklist_created
   :synopsis: TaskListCreatedView Tests module.

.. moduleauthor:: Panos Tzimos<tzimoss@gmail.com>
"""
from random import randint
import uuid

from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory
from django.utils import timezone

from tasks.models import Task
from tasks.views.tasklist_created import TaskListCreatedAtView

User = get_user_model()


class TaskListCreatedAtViewTestCase(TestCase):

    def setUp(self):
        super(TaskListCreatedAtViewTestCase, self).setUp()
        self.user = User.create(
            email='email@gmail.com',
            password='asd@23fsffidmS'
        )
        for _ in range(5):
            Task.objects.create(
                author=self.user,
                title=str(uuid.uuid4()),
                details=str(uuid.uuid4()),
                due_date=timezone.now() + timezone.timedelta(
                    days=randint(1, 31))
            )
        self.request = RequestFactory()
        self.view = TaskListCreatedAtView()

    def tearDown(self):
        Task.objects.all().delete()
        User.objects.all().delete()
        super(TaskListCreatedAtViewTestCase, self).tearDown()

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
