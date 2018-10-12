"""
.. module:: tasks.forms.edit_task
   :synopsis: Form to edit tasks.

.. moduleauthor:: Panos Tzimos<tzimoss@gmail.com>
"""

from django import forms
from django.http import Http404
from django.utils.translation import ugettext_lazy as _
from tasks.models import Task


class TaskEditForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = (
            'title',
            'details',
            'due_date'
        )

        widgets = {
            'title': forms.TextInput(
                attrs={
                    'placeholder': _('Title'),
                    'required': True
                }
            ),
            'details': forms.Textarea(
                attrs={
                    'placeholder': _('Details'),
                    'required': True
                }
            ),
            'due_date': forms.SelectDateWidget(
                attrs={
                    'required':True
                }
            )
        }

    def __init__(self,task_id=None,*args,**kwargs):
        self.task_id = task_id
        super(TaskEditForm, self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].required = True

    def save(self,commit=False):
        try:
            task = Task.objects.get(id=self.task_id)
        except Task.DoesNotExist:
            raise Http404()
        task.title = self.cleaned_data.get('title')
        task.details = self.cleaned_data.get('details')
        task.due_date = self.cleaned_data.get('due_date')
        task.save()

        return task
