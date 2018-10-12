"""
.. module:: tasks.forms.create_task
   :synopsis: Form to create tasks.

.. moduleauthor:: Panos Tzimos<tzimoss@gmail.com>
"""

from django import forms
from django.utils.translation import ugettext_lazy as _
from tasks.models import Task


class TaskCreateForm(forms.ModelForm):
    """
    Form to create tasks.
    """

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
                    'required': True
                }
            )
        }

    def clean(self):
        clean_data = self.cleaned_data
        fields = [
            clean_data.get('title'),
            clean_data.get('details'),
            clean_data.get('due_date')
        ]
        if not all(fields):
            raise forms.ValidationError(
                _('Please correct the errors below')
            )
        return clean_data

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super(TaskCreateForm, self).__init__(*args, **kwargs)

    def save(self, commit=False):
        instance = super(TaskCreateForm, self).save(commit=True)
        instance.author = self.request.user
        instance.save()
        return instance
