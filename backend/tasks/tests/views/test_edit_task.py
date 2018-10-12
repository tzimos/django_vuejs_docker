"""
.. module:: home.tests.views.test_edit_task
   :synopsis: TaskEditView Tests module.

.. moduleauthor:: Panos Tzimos<tzimoss@gmail.com>
"""
from django.contrib.auth import get_user_model
from django.http import Http404
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.utils import timezone

from tasks.models import Task
from tasks.views.edit_task import TaskEditView

User = get_user_model()


class TaskEditViewTestCase(TestCase):

    def setUp(self):
        super(TaskEditViewTestCase, self).setUp()
        self.user = User.create(
            email='email@gmail.com',
            password='asd@23fsffidmS'
        )
        self.request = RequestFactory()
        self.view = TaskEditView()
        self.tz = timezone.now().date()
        self.task = Task.objects.create(
            title='title_tit',
            details='details_det',
            author=self.user,
            due_date=self.tz
        )

    def tearDown(self):
        self.task.delete()
        self.user.delete()
        super(TaskEditViewTestCase, self).tearDown()

    def test_get_no_task_id(self):
        """
        Tests when we don't provide task_id
        if Http404 error is raised.
        """
        req = self.request.get('/')
        with self.assertRaises(Http404):
            self.view.get(req)

    def test_get_invalid_task_id(self):
        """
        Tests when we don't provide a correct task_id
        if Http404 error is raised.
        """
        kwargs = {'task_id': 123123123}
        req = self.request.get('/')
        with self.assertRaises(Http404):
            self.view.get(req, **kwargs)

    def test_get_user_not_the_author(self):
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
        req = self.request.get('/')
        req.user = user2

        response = self.view.get(req, **kwargs)

        self.assertEqual(
            response.status_code,
            403
        )
        self.assertEqual(
            response.reason_phrase,
            'Forbidden'
        )

        user2.delete()

    def test_get_success(self):
        """
        Tests if the initial data of the task
        are rendered at the response if we provide
        all the correct credentials and pass the above checks.
        """
        kwargs = {'task_id': self.task.pk}
        req = self.request.get('/')
        req.user = self.user
        response = self.view.get(req, **kwargs)

        html = response.content.decode('utf-8')

        self.assertIn(
            self.task.title,
            html
        )
        self.assertIn(
            self.task.details,
            html
        )
        selected_day = 'selected>'+str(self.task.due_date.day)
        selected_month = 'selected>'+str(self.task.due_date.strftime('%B'))
        selected_year = 'selected>'+str(self.task.due_date.year)
        self.assertIn(
            self.task.title,
            html
        )
        self.assertIn(
            self.task.details,
            html
        )
        self.assertIn(
            selected_day,
            html
        )
        self.assertIn(
            selected_month,
            html
        )
        self.assertIn(
            selected_year,
            html
        )

    def test_post_no_task_id(self):
        """
        Tests when we don't provide task_id
        if Http404 error is raised.
        """
        req = self.request.post('/')
        with self.assertRaises(Http404):
            self.view.post(req)

    def test_post_invalid_task_id(self):
        """
        Tests when we don't provide task_id
        if Http404 error is raised.
        """
        kwargs = {'task_id': 123123123}
        req = self.request.post('/')
        with self.assertRaises(Http404):
            self.view.post(req, **kwargs)

    def test_post_user_not_the_author(self):
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
        Tests if the task is editted after a successful
        post request from the user.
        """
        initial_title= self.task.title
        redirect_url = reverse('tasks:tasklist')
        kwargs = {'task_id': self.task.pk}
        new_tz = timezone.now() + timezone.timedelta(days=1)
        data = {
            'title': 'changed title',
            'details': 'changed details',
            'due_date': new_tz.date()
        }

        req = self.request.post('/',data=data)
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
        editted_title = self.task.title

        self.assertNotEqual(
            initial_title,
            editted_title
        )

    def test_post_failure(self):
        """
        If we don't every required data then
        the post method fails.
        """
        initial_title = self.task.title
        initial_details = self.task.details
        initial_due_date = self.task.due_date

        kwargs = {'task_id': self.task.pk}

        # 1st try
        data1 ={
            'title':'changed title'
        }

        req = self.request.post('/',data=data1)

        req.user = self.user
        self.view.post(req, **kwargs)

        self.task.refresh_from_db()
        self.assertEqual(
            self.task.title,
            initial_title
        )

        # 2nd try
        data2 = {
            'details': 'changed details'
        }
        req = self.request.post('/', data=data2)

        req.user = self.user
        self.view.post(req, **kwargs)

        self.task.refresh_from_db()
        self.assertEqual(
            self.task.details,
            initial_details
        )

        # 3rd try
        data3 = {
            'due_date': timezone.now() + timezone.timedelta(days=10)
        }
        req = self.request.post('/', data=data3)

        req.user = self.user
        self.view.post(req, **kwargs)

        self.task.refresh_from_db()
        self.assertEqual(
            self.task.due_date,
            initial_due_date
        )