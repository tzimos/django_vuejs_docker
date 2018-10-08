from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.urls import reverse
from django.views import View

from tasks.models import Task


class MarkAsDoneView(LoginRequiredMixin,View):

    def post(self,request,*args,**kwargs):
        task_id = kwargs.get('task_id')
        if not task_id:
            return HttpResponseBadRequest()
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return HttpResponseBadRequest()
        except Task.MultipleObjectsReturned:
            return HttpResponseBadRequest()
        task.done = True
        task.done_by = self.request.user
        task.save()
        return HttpResponseRedirect(reverse('tasks:tasklist'))