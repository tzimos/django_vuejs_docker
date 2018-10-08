"""
.. module:: authentication.forms.login_form.
   :synopsis: Login Form.

.. moduleauthor:: Panos Tzimos<tzimoss@gmail.com>
"""
from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

User = get_user_model()


class UserLoginForm(forms.Form):
    """
    This is the class that we are going to use to validate the user
    credentials.
    """
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={'autofocus': True}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
        )
    )

    def __init__(self, request=None,*args, **kwargs):
        self.user = None
        self.request = request
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.sign_up_url = reverse('home:sign_up')
        self.error_dict = {
           "check_credentials" : _("Please check the provided credentials."
              "If you don't have an account please click "
              "<a href=\"{url}\">here</a>".format(
                url= self.sign_up_url
            )),
            "unknown_error":_("An error has occured, please <a href=\""
                              "{contact_url}\">click here </a>to "
                              "contact us".format(contact_url='#'))

        }


    def clean_password(self):
        """
        Clean password
        """
        password = self.cleaned_data.get('password')
        if not password:
            self.add_error(
                'password',
                _("This field is required")
            )
        try:
            validate_password(password)
        except ValidationError as err:
            self.add_error(
                'password',
                err.messages[0]
            )
        return password

    def clean(self):
        """
        In this method we have to make sure that the user has given the
        correct data.
        """
        clean_data = super(UserLoginForm, self).clean()
        email = clean_data.get('email')
        password = clean_data.get('password')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise ValidationError(
                self.error_dict['check_credentials']
            )
        except User.MultipleObjectsReturned:
            raise ValidationError(
                self.error_dict['unknown_error']
            )
        self.confirm_login_allowed(user)
        self.user = authenticate(
            self.request, username=email, password=password
        )
        if not self.user:
            raise ValidationError(
                self.error_dict['check_credentials']
            )

        return clean_data

    def confirm_login_allowed(self, user):
        """
        Controls whether the given User may log in. This is a policy setting,
        independent of end-user authentication. This default behavior is to
        allow login by active users, and reject login by inactive users.

        If the given user cannot log in, this method should raise a
        ``forms.ValidationError``.

        If the given user may log in, this method should return None.
        """
        if not user.is_active:
            raise forms.ValidationError(
                _("This account is inactive.")
            )
