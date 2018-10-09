"""
.. module:: authentication.forms.sign_up_form
   :synopsis: SignUp Form.

.. moduleauthor:: Panos Tzimos<tzimoss@gmail.com>
"""

from django import forms
from django.contrib.auth import password_validation, get_user_model
from django.conf import settings
from django.http import Http404
from django.utils.translation import ugettext_lazy as _

User = get_user_model()

class SignUpForm(forms.ModelForm):

    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
        'user_exists':_('A user with this email already exists')
    }
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html(),
    )
    confirm_password = forms.CharField(
        label=_("Confirm password"),
        widget=forms.PasswordInput,
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    superuser = forms.BooleanField(
        label=_('Are you a superuser ?'),
        required=False
    )

    class Meta:
        model = User
        fields = (
            'email',
        )

    def __init__(self,*args,**kwargs):
        super(SignUpForm, self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class':'form-control'}
        self.user = None

    def clean_confirm_password(self):
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("confirm_password")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def _post_clean(self):
        password = self.cleaned_data.get('confirm_password')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error('confirm_password', error)

    def clean(self):
        cleaned_data = self.cleaned_data
        email = cleaned_data.get('email')
        user = None
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            pass
        except User.MultipleObjectsReturned:
            raise Http404()
        if user:
            raise forms.ValidationError(
                self.error_messages['user_exists'],
                code='user_exists'
            )
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email')
        user.set_password(self.cleaned_data["password"])
        if settings.DEBUG and self.cleaned_data.get('superuser') == True:
            user.is_staff = True
            user.is_superuser = True
        if commit:
            user.save()
        self.user = user
        return user