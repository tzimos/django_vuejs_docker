"""
.. module:: authentication.models.user
   :synopsis: We have to define a custom User model in order to handle
              properly the username_field.

.. moduleauthor:: Panos Tzimos<tzimoss@gmail.com>
"""
from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models, IntegrityError
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from authentication.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User Model.
    """
    USERNAME_FIELD = 'email'

    email = models.EmailField(
        _('email address'),
        null=False,
        max_length=255,
        unique=True,
        error_messages={
            'unique': _("A user with that username already exists."),
        }
    )

    password = models.CharField(
        _('password'),
        max_length=128,
        help_text=_('Please enter your password.')
    )

    first_name = models.CharField(_('first name'), max_length=30, blank=True)

    last_name = models.CharField(_('last name'), max_length=150, blank=True)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    @property
    def get_full_name(self):
        if not self.first_name or not self.last_name:
            return self.email
        return '{} {}'.format(self.first_name, self.last_name)

    def __str__(self):
        return self.get_full_name

    @classmethod
    def create(cls, **kwargs):
        """
        Utility function to create users.
        :return: user instance or None
        """
        user = None
        password = kwargs.get('password')
        email = kwargs.get('email')
        if not email or not password:
            return None

        # Check if user exists.
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            pass
        # If exists then return None.
        if user:
            return None

        # Else go on and create the user.
        user = User.objects.create(**kwargs)
        user.set_password(password)
        user.save()

        return user
