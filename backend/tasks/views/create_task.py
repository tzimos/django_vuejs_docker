"""
.. module:: tasks.views.create_task
   :synopsis: Tasks Create View module.

.. moduleauthor:: Panos Tzimos<tzimoss@gmail.com>
"""

from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.urls import reverse
from django.views import View

from tasks.forms.create_task import TaskCreateForm


class TaskCreateView(View):
    template_name = 'create_task.html'

    def get(self, request, *args, **kwargs):
        form = TaskCreateForm()
        context = {'task_create_form':form}
        return render(request,context=context,template_name=self.template_name)

    def post(self, request, *args, **kwargs):
        form = TaskCreateForm(data=request.POST,request=request)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('tasks:tasklist'))
        context = {'task_create_form':form}
        return render_to_response(
            self.template_name,
            context=context
        )

