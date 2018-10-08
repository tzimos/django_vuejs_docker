from django.contrib.auth import login
from django.contrib.auth.views import LoginView as LoginBaseView
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.urls import reverse
from django.middleware.csrf import get_token
from django.utils.decorators import method_decorator
from django.utils.http import is_safe_url
from django.views import View
from django.views.decorators.csrf import ensure_csrf_cookie

from authentication.forms.login_form import UserLoginForm


class LoginView(LoginBaseView):

    def get(self, request, *args, **kwargs):
        """
        We have to send manually the csrf token at the frontend, because
        the template fragments are rendered dynamically and we cannot pass it
        as usual.
        """
        context = {
            'login_url': reverse('home:login'),
            'csrf_token': get_token(request)
        }
        return render_to_response('home/login.html',context=context)

    def post(self, request, *args, **kwargs):
        """
        The usual post method
        """
        login_form = UserLoginForm(data=request.POST,request=request)
        if login_form.is_valid():
            user = login_form.user
            login(request,user)

            return JsonResponse(
                {'redirect_to':self.get_redirect_url()}
            )

        err = {}
        for error in login_form.errors:
            if error == '__all__':
                err['non_field_error'] = login_form.errors[error]
                continue
            err[error] = login_form.errors[error]

        context = {'form_errors':err}
        return JsonResponse(context,status=200)

    def get_redirect_url(self):
        """
        This method returns the redirection url if it is safe.
        If it is safe and we don't have any url then we redirect
        the user at the tasklist view.
        """
        redirect_to = super(LoginView, self).get_redirect_url()

        if not redirect_to:
            return reverse('tasks:tasklist')

        return redirect_to