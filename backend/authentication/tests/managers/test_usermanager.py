"""
.. module:: authentication.tests.managers.test_usermanager
   :synopsis: Tests for UserManager.

.. moduleauthor:: Panos Tzimos<tzimoss@gmail.com>
"""

from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()

class UserManagerTestCase(TestCase):

    def setUp(self):
        super(UserManagerTestCase, self).setUp()
        self.manager = User.objects
        self.params = {
            'email':'test@email.com',
            'password':'password'
        }

    def tearDown(self):
        users = User.objects.all()
        if users.exists():
            users.delete()
        super(UserManagerTestCase, self).tearDown()

    def test__create_user_error(self):
        """
        Tests when we don't provide email at _create_user method
        if ValueError is raised.
        :return:
        """
        with self.assertRaises(ValueError):
            self.manager._create_user('','')

    def test__create_user_create(self):
        """
        Tests if a user is created if we provide email and password.
        """
        user = self.manager._create_user(**self.params)
        expected_user = User.objects.last()
        self.assertEqual(
            user.pk,
            expected_user.pk
        )

    def test__create_user(self):
        """
        Test when we use create_user method if a non superuser user
        is created
        """
        user = self.manager._create_user(**self.params)
        expected_user = User.objects.last()
        self.assertEqual(
            user.pk,
            expected_user.pk
        )
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)

    def test_create_user(self):
        """
        Tests if create user creates a non superuser and non staff
        user when we dont provide these extra params or they are both
        False.
        """
        user = self.manager.create_user(**self.params)
        expected_user = User.objects.last()
        self.assertEqual(
            user.pk,
            expected_user.pk
        )
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)

    def test_create_superuser_is_staff_false(self):
        """
        Tests when we provide a is_staff=False param if
        create_superuser method raises Error.
        """
        self.params['is_staff']= False
        with self.assertRaises(ValueError):
            self.manager.create_superuser(**self.params)

    def test_create_superuser_is_superuser_false(self):
        """
        Tests when we provide a is_superuser=False param if
        create_superuser method raises Error.
        """
        self.params['is_staff']= True
        self.params['is_superuser']= False
        with self.assertRaises(ValueError):
            self.manager.create_superuser(**self.params)

    def test_create_superuser_return_superuser(self):
        """
        Tests when we provide is_superuser=True and is_staff=True params if
        create_superuser method returns a superuser.
        """
        self.params['is_staff']= True
        self.params['is_superuser']= True
        user = self.manager.create_superuser(**self.params)
        expected_user = User.objects.get(email=self.params['email'])
        self.assertEqual(
            user.pk,
            expected_user.pk
        )
        self.assertTrue(user.is_superuser)