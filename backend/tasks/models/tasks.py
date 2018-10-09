"""
.. module:: tasks.models.tasks
   :synopsis: Task Model module.

.. moduleauthor:: Panos Tzimos<tzimoss@gmail.com>
"""

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Task(models.Model):
    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        app_label = 'tasks'

    title = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    author = models.ForeignKey(
        to=get_user_model(),
        related_name='tasks',
        # We want to keep the task at the db
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    details = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    created = models.DateTimeField(
        verbose_name=_('Creation date/time'),
        editable=False,
        auto_now_add=True,
    )
    modified = models.DateTimeField(
        verbose_name=_('Modified date/time'),
        editable=False,
        auto_now=True,
    )

    done = models.BooleanField(default=False)

    done_by = models.ForeignKey(
        to=get_user_model(),
        related_name='tasks_completed',
        # We want to keep the task at the db
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    due_date = models.DateField(
        verbose_name=_('Due date/time'),
        editable=True,
        blank=True,
        null=True
    )

    def __str__(self):
        return 'Title: {title} || Author:{author}'.format(
            title=self.title,
            author=self.author
        )
