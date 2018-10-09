"""
.. module:: tasks.urls
   :synopsis: Task urls module.

.. moduleauthor:: Panos Tzimos<tzimoss@gmail.com>
"""

from django.urls import path

from tasks.views.create_task import TaskCreateView
from tasks.views.delete_task import TaskDeleteView
from tasks.views.edit_task import TaskEditView
from tasks.views.mark_as_done import MarkAsDoneView
from tasks.views.tasklist import TaskListView
from tasks.views.tasklist_created import TaskListCreatedAtView
from tasks.views.tasklist_done import TaskListDoneView
from tasks.views.tasklist_pending import TaskListPendingView

app_name = 'tasks'

urlpatterns = [
    path('task_list/', TaskListView.as_view(), name='tasklist'),
    path(
        'mark_as_done/<task_id>/',
        MarkAsDoneView.as_view(),
        name='mark_as_done'
    ),
    path(
        'task_list/created_at',
        TaskListCreatedAtView.as_view(),
        name='created_at'
    ),
    path(
        'task_list/done',
        TaskListDoneView.as_view(),
        name='done'
    ),
    path(
        'task_list/pending',
        TaskListPendingView.as_view(),
        name='pending'
    ),
    path(
        'task_create/',
        TaskCreateView.as_view(),
        name='task_create'
    ),
    path(
        'task_edit/<task_id>/',
        TaskEditView.as_view(),
        name='edit_task'
    ),
    path(
        'task_delete/<task_id>/',
        TaskDeleteView.as_view(),
        name='delete_task'
    )

]
