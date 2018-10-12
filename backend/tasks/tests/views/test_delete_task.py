"""
.. module:: home.tests.views.test_create_task
   :synopsis: TasksDeleteView Tests module.

.. moduleauthor:: Panos Tzimos<tzimoss@gmail.com>
"""
from django.contrib.auth import get_user_model
from django.http import Http404

from django.test import TestCase, RequestFactory
from django.urls import reverse

from tasks.models import Task
from tasks.views.delete_task import TaskDeleteView

User = get_user_model()


class TaskDeleteViewTestCase(TestCase):

    def setUp(self):
        super(TaskDeleteViewTestCase, self).setUp()
        self.user = User.create(
            email='email@gmail.com',
            password='asd@23fsffidmS'
        )
        self.request = RequestFactory()
        self.task = Task.objects.create(author=self.user, title='title')
        self.view = TaskDeleteView()

    def tearDown(self):
        self.task.delete()
        self.user.delete()
        super(TaskDeleteViewTestCase, self).tearDown()

    def test_post_http404(self):
        """
        Tests when we don't provide at kwargs a task_id
        if the post method raises a Http404 error.
        """
        req = self.request.post('/')
        with self.assertRaises(Http404):
            self.view.post(req)

    def test_post_no_match(self):
        """
        Tests when the task_id we provide doesn't match
        with a task object if post method raises a Http404 error.
        """
        kwargs = {'task_id': 123124124}
        req = self.request.post('/')
        with self.assertRaises(Http404):
            self.view.post(req, **kwargs)

    def test_post_user_not_the_author(self):
        """
        Tests when the requested task from the user has a different
        author than the user itself.
        """
        user2 = User.create(
            email='user2@gmail.com',
            password='asd@2dwW'
        )
        kwargs = {'task_id': self.task.pk}
        req = self.request.post('/')
        req.user = user2

        response = self.view.post(req, **kwargs)
        self.assertEqual(
            response.status_code,
            403
        )
        self.assertEqual(
            response.reason_phrase,
            'Forbidden'
        )
        user2.delete()

    def test_post_deleted_successfully(self):
        """
        Tests if the post method deletes successfully the
        requested task.
        """
        redirect_url = reverse('tasks:tasklist')
        kwargs = {'task_id': self.task.id}
        req = self.request.post('/')
        req.user = self.user

        response = self.view.post(req, **kwargs)
        self.assertEqual(
            response.status_code,
            302
        )
        self.assertEqual(
            response.url,
            redirect_url
        )
        self.assertEqual(
            Task.objects.count(),
            0
        )
