"""
.. module:: tasks.views.mark_as_done
   :synopsis: View to mark a task as done.

.. moduleauthor:: Panos Tzimos<tzimoss@gmail.com>
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, Http404, HttpResponseForbidden
from django.urls import reverse
from django.views import View

from tasks.models import Task


class MarkAsDoneView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        task_id = kwargs.get('task_id')
        if not task_id:
            raise Http404()
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            raise Http404()
        if task.author != request.user:
            return HttpResponseForbidden()
        task.done = True
        task.done_by = request.user
        task.save()
        return HttpResponseRedirect(reverse('tasks:tasklist'))
