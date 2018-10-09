"""
.. module:: tasks.views.edit_task
   :synopsis: View to edit tasks.

.. moduleauthor:: Panos Tzimos<tzimoss@gmail.com>
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, render_to_response
from django.urls import reverse
from django.views import View

from tasks.forms.edit_task import TaskEditForm
from tasks.models import Task


class TaskEditView(LoginRequiredMixin, View):
    template_name = 'edit_task.html'

    def get(self, request, *args, **kwargs):
        task_id = kwargs.get('task_id')
        if not task_id:
            raise Http404()
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            raise Http404()
        except Task.MultipleObjectsReturned:
            raise Http404()
        data = {
            'title': task.title,
            'details': task.details,
            'due_date': task.due_date
        }
        form = TaskEditForm(initial=data)
        context = {'task_edit_form': form}
        return render(request, context=context,
                      template_name=self.template_name)

    def post(self, request, *args, **kwargs):
        task_id = kwargs.get('task_id')
        if not task_id:
            raise Http404()
        form = TaskEditForm(data=request.POST, task_id=task_id)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('tasks:tasklist'))
        context = {'task_edit_form': form}
        return render_to_response(
            request,
            context=context
        )
