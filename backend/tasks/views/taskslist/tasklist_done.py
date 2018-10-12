"""
.. module:: tasks.views.tasklist_done.
   :synopsis: TaskList View ordered by done.

.. moduleauthor:: Panos Tzimos<tzimoss@gmail.com>
"""

from tasks.models import Task
from tasks.views.taskslist.base_tasklist import BaseTaskListView


class TaskListDoneView(BaseTaskListView):

    def get_queryset(self):
        return Task.objects.filter(done=True).order_by('-due_date')
