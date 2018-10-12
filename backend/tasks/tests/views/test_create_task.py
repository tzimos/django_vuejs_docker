"""
.. module:: home.tests.views.test_create_task
   :synopsis: Tasks Views Tests package.

.. moduleauthor:: Panos Tzimos<tzimoss@gmail.com>
"""
from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.utils import timezone

from tasks.models import Task
from tasks.views.create_task import TaskCreateView

User = get_user_model()


class TaskCreateViewTestCase(TestCase):

    def setUp(self):
        super(TaskCreateViewTestCase, self).setUp()
        self.request = RequestFactory()
        self.view = TaskCreateView()

    def test_get(self):
        """
        Tests if get method returns the form in the content of
        the response
        """
        req = self.request.get('/')
        response = self.view.get(req)
        html = response.content.decode('utf-8')
        self.assertIn(
            'id_details',
            html
        )
        self.assertIn(
            'id_title',
            html
        )
        self.assertIn(
            'id_due_date',
            html
        )

    def test_post_valid(self):
        """
        Tests when we provide correct credentials at the post
        method if there is a task object created and is linked to
        the user that created it.In addition we check if the
        successful post method redirects to the tasklist.
        :return:
        """
        user = User.create(
            email='email@gmail.com',
            password='aadsasd2@22d'
        )
        redirect_url = reverse('tasks:tasklist')
        params = {
            'title': 'title',
            'details': 'details',
            'due_date': timezone.now().date()
        }
        req = self.request.post(
            '/',
            data=params,
        )
        req.user = user
        response = self.view.post(req)
        self.assertEqual(
            response.status_code,
            302
        )
        task = Task.objects.get(title='title')
        self.assertEqual(
            task.details,
            'details'
        )
        self.assertEqual(
            response.url,
            redirect_url
        )
        self.assertEqual(
            user,
            task.author
        )
        Task.objects.all().delete()
        User.objects.all().delete()

    def test_post_invalid(self):
        """
        Tests wheb the params that we feed the post
        method if the response contains generic errors.
        """
        params = {}
        user = User.create(
            email='email@gmail.com',
            password='aadsasd2@22d'
        )
        req = self.request.post(
            '/',
            data=params,
        )
        req.user = user
        response = self.view.post(req)
        self.assertIn(
            'Please correct the errors below',
            response.content.decode('utf-8')
        )
