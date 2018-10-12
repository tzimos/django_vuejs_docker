"""
.. module:: home.tests.views.test_mark_as_done
   :synopsis: MarkAsDoneView Tests module.

.. moduleauthor:: Panos Tzimos<tzimoss@gmail.com>
"""
from django.http import Http404
from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.utils import timezone

from tasks.models import Task
from tasks.views.mark_as_done import MarkAsDoneView

User = get_user_model()


class MarkAsDoneViewTestCase(TestCase):

    def setUp(self):
        super(MarkAsDoneViewTestCase, self).setUp()
        self.tz = timezone.now()
        self.user = User.create(
            email='email@gmail.com',
            password='asd@23fsffidmS'
        )
        self.task = Task.objects.create(
            title='title',
            details='details',
            due_date=self.tz,
            author=self.user
        )
        self.request = RequestFactory()
        self.view = MarkAsDoneView()

    def tearDown(self):
        self.user.delete()
        super(MarkAsDoneViewTestCase, self).tearDown()

    def test_post_no_task_id(self):
        """
        Tests when we don't provide a task id
        if an Http404 error is raised.
        """
        req = self.request.post('/')
        with self.assertRaises(Http404):
            self.view.post(req)

    def test_post_no_task(self):
        """
        Tests when we don't provide a correct task_id
        if Http404 error is raised.
        """
        kwargs = {'task_id': 123123123}
        req = self.request.post('/')
        with self.assertRaises(Http404):
            self.view.post(req, **kwargs)

    def test_post_user_not_author(self):
        """
        Tests when the user that requests a task object
        if he is not the author if a HttpResponseForbidden
        response is returned.
        """
        user2 = User.create(
            email='user2@gmail.com',
            password='apsso2@dwwW'
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

    def test_post_success(self):
        """
        Tests if a task is mark as done if it saved
        and if we redirected at the TaskListView
        """
        initial_state = self.task.done
        initial_done_by = self.task.done_by
        redirect_url = reverse('tasks:tasklist')

        kwargs = {'task_id': self.task.pk}
        req = self.request.post('/')
        req.user = self.user

        response = self.view.post(req, **kwargs)

        self.assertEqual(
            response.url,
            redirect_url
        )
        self.assertEqual(
            response.status_code,
            302
        )
        self.task.refresh_from_db()

        self.assertTrue(self.task.done)
        self.assertEqual(
            self.task.done_by,
            req.user
        )
