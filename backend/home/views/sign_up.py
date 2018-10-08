from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render_to_response, render
from django.urls import reverse
from django.views import View
from django.views.generic import FormView

from authentication.forms.sign_up_form import SignUpForm


class SignUpView(FormView):
    form_class = SignUpForm
    template_name = 'home/sign_up.html'


    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            login(request,form.user)
            return HttpResponseRedirect(reverse('tasks:tasklist'))
        return render(request,context={'form':form},template_name=self.template_name)