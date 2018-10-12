"""
.. module:: tasks.views.tasklist_created.
   :synopsis: TaskList View ordered by created.

.. moduleauthor:: Panos Tzimos<tzimoss@gmail.com>
"""
from tasks.models import Task
from tasks.views.taskslist.base_tasklist import BaseTaskListView


class TaskListCreatedAtView(BaseTaskListView):

    def get_queryset(self):
        return Task.objects.all().order_by('created')
