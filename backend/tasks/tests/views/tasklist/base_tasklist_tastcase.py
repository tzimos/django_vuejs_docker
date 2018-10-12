"""
.. module:: tasks.tests.views.tasklist.base_tasklist_testcase
   :synopsis: Tasklist helper class.

.. moduleauthor:: Panos Tzimos<tzimoss@gmail.com>
"""
import uuid
from random import randint

from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory
from django.utils import timezone

from tasks.models import Task

User = get_user_model()


class BaseTaskListHelperTestCase(TestCase):

    def setUp(self):
        super(BaseTaskListHelperTestCase, self).setUp()
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
                    days=randint(1, 31)),
                done=True
            )
        self.request = RequestFactory()

    def tearDown(self):
        Task.objects.all().delete()
        User.objects.all().delete()
        super(BaseTaskListHelperTestCase, self).tearDown()
