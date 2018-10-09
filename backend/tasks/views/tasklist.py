"""
.. module:: tasks.views.tasklist
   :synopsis: View to get the list of the tasks.

.. moduleauthor:: Panos Tzimos<tzimoss@gmail.com>
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.views import View

from tasks.models import Task


class TaskListView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        task_list = Task.objects.order_by('-created')
        page = request.GET.get('page', 1)
        paginator = Paginator(task_list, 2)
        try:
            tasks = paginator.page(page)
        except PageNotAnInteger:
            tasks = paginator.page(1)
        except EmptyPage:
            tasks = paginator.page(paginator.num_pages)
        context = {'tasks': tasks}

        return render(request, template_name='tasklist.html', context=context)
