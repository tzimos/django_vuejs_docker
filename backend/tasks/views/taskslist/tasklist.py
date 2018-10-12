"""
.. module:: tasks.views.tasklist
   :synopsis: View to get the list of the tasks.

.. moduleauthor:: Panos Tzimos<tzimoss@gmail.com>
"""

from tasks.models import Task
from tasks.views.taskslist.base_tasklist import BaseTaskListView


class TaskListView(BaseTaskListView):

    def get_queryset(self):
        return Task.objects.all().order_by('-created')
