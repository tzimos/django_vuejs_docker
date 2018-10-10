"""
.. module:: authentication.tests.models.test_user
   :synopsis: Tests for User Model.

.. moduleauthor:: Panos Tzimos<tzimoss@gmail.com>
"""
import uuid

from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class UserModelTestCase(TestCase):

    def setUp(self):
        super(UserModelTestCase, self).setUp()
        self.generator = str(uuid.uuid4()).split('-')
        self.password = self.generator[-2]

    def tearDown(self):
        users = User.objects.all()
        if users.exists():
            users.delete()
        super(UserModelTestCase, self).tearDown()

    def test_get_full_name_only_email(self):
        """
        Tests if the get_full_name method returns only
        the email when no first_name and last_name is
        provided.
        """
        user = User.objects.create(
            email='{}@gmail.com'.format(str(uuid.uuid4()).split('-')[-1]),
            password=self.password
        )
        expected_result = user.email
        result = user.get_full_name
        self.assertEqual(
            expected_result,
            result
        )

    def test_get_full_name_first_and_last_name(self):
        """
        Tests if the get_full_name method returns only
        the first and last name of the user when they both are
        provided.
        """
        user = User.objects.create(
            first_name='Panos',
            last_name='Tzimos',
            email='{}@gmail.com'.format(str(uuid.uuid4()).split('-')[-1]),
            password=self.password
        )
        expected_result = 'Panos Tzimos'
        result = user.get_full_name
        self.assertEqual(
            expected_result,
            result
        )

    def test_get_full_name_first_or_last_name(self):
        """
        If we provide only first or only last name
        get_full name should return the email.
        """
        user1 = User.objects.create(
            first_name='Panos',
            email='{}@gmail.com'.format(str(uuid.uuid4()).split('-')[-1]),
            password=self.password
        )

        user2 = User.objects.create(
            last_name='Tzimos',
            email='{}@gmail.com'.format(str(uuid.uuid4()).split('-')[-1]),
            password=self.password
        )

        expected_result1 = user1.email
        result1 = user1.get_full_name

        expected_result2 = user2.email
        result2 = user2.get_full_name

        self.assertEqual(
            expected_result1,
            result1
        )
        self.assertEqual(
            expected_result2,
            result2
        )

    def test_string_representation(self):
        user1 = User.objects.create(
            email='{}@gmail.com'.format(str(uuid.uuid4()).split('-')[-1]),
            password=self.password
        )

        self.assertEqual(
            user1.__str__(),
            user1.email
        )

    def test_create_user_already_exists(self):
        """
        Tests when the user to be created has an email already stored
        in the database if create method returns None.
        """
        credentials = {
            'email': 'example@gmail.com',
            'password': 'example_pass'
        }
        user = User.create(**credentials)
        user1 = User.create(**credentials)
        self.assertIsNone(user1)

    def test_create_not_password_or_email_provided(self):
        """
        If we don't provide password or email then create
        method should create None.
        """
        user1 = User.create(password='12345678')
        user2 = User.create(email='test@email')
        self.assertIsNone(user1)
        self.assertIsNone(user2)
