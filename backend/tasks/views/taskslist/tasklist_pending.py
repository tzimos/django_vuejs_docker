"""
.. module:: tasks.views.tasklist_pending.
   :synopsis: TaskList View ordered by pending tasks.

.. moduleauthor:: Panos Tzimos<tzimoss@gmail.com>
"""

from tasks.models import Task
from tasks.views.taskslist.base_tasklist import BaseTaskListView


class TaskListPendingView(BaseTaskListView):

    def get_queryset(self):
        return Task.objects.filter(done=False).order_by('due_date')
