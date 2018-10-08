from django import forms
from django.utils.translation import ugettext_lazy as _
from tasks.models import Task


class TaskCreateForm(forms.ModelForm):
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

    def __init__(self,request=None,*args,**kwargs):
        self.request = request
        super(TaskCreateForm, self).__init__(*args,**kwargs)

    def save(self, commit=False):
        instance = super(TaskCreateForm, self).save(commit=True)
        instance.author = self.request.user
        instance.save()
        return instance
