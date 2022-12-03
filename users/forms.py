from django import forms
from allauth.account.forms import SignupForm, LoginForm
from django.forms.widgets import Select
from django.utils.translation import gettext_lazy as _

from .mixins import BootStrapForm


class AdminLoginForm(LoginForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # fields_required = getattr(self.Meta, "fields_required", None)

        for field in self.fields:
            new_data = {
                "placeholder": f"{field}",
                "class": "form-control"
            }
            if not isinstance(self.fields[str(field)].widget, Select):
                self.fields[str(field)].widget.attrs.update(new_data)

            # Check if the field is required and add "required_css_class" to it.
            # if fields_required:
                # if field in fields_required:
                # new_data["class"] = f"form-control {required_css_class}"

                # self.fields[str(field)].widget.attrs.update(new_data)

    password = forms.CharField(
        label=_("Password"), required=True, widget=forms.PasswordInput())
    remember = forms.BooleanField(label=_("Remember Me"), required=False)


class UserRegisterForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # fields_required = getattr(self.Meta, "fields_required", None)

        for field in self.fields:
            new_data = {
                "placeholder": f"{field}",
                "class": "form-control"
            }
            if not isinstance(self.fields[str(field)].widget, Select):
                self.fields[str(field)].widget.attrs.update(new_data)

            # Check if the field is required and add "required_css_class" to it.
            # if fields_required:
                # if field in fields_required:
                # new_data["class"] = f"form-control {required_css_class}"

                # self.fields[str(field)].widget.attrs.update(new_data)