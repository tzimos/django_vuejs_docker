"""
.. module:: tasks.views.delete_task
   :synopsis: Delete View for tasks.

.. moduleauthor:: Panos Tzimos<tzimoss@gmail.com>
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.views import View

from tasks.models import Task


class TaskDeleteView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        task_id = kwargs.get('task_id')
        if not task_id:
            raise Http404()
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            raise Http404()
        except Task.MultipleObjectsReturned:
            raise Http404()
        task.delete()
        return HttpResponseRedirect(reverse('tasks:tasklist'))
