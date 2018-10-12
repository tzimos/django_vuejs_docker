"""
.. module:: tasks.views.tasklist
   :synopsis: View to get the list of the tasks.

.. moduleauthor:: Panos Tzimos<tzimoss@gmail.com>
"""
from abc import ABC, abstractmethod

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.views import View


class BaseTaskListView(LoginRequiredMixin, View):
    __metaclass__ = ABC

    def get(self, request, *args, **kwargs):
        task_list = self.get_queryset()
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

    @abstractmethod
    def get_queryset(self):
        raise NotImplementedError()
