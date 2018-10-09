"""
.. module:: tasks.admin.tasks
   :synopsis: Tasks Admin module.

.. moduleauthor:: Panos Tzimos<tzimoss@gmail.com>
"""

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from tasks.models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('__str__','created','modified','done')
    readonly_fields = ('done_by','created','modified')
    fieldsets = (
        (_('Task Details'),{'fields':(
            'title',
            'details',
            'author',
        )}),
        (_('Task Status'),{'fields':(
            'done',
            'done_by'
        )}),
        (_('Important Dates'),{'fields':(
            'created',
            'modified'
        )})
    )