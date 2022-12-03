from django.forms import ModelForm
from django.forms.widgets import Select
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

# TODO: Add the Login required for admin.


class BootStrapModelForm(ModelForm):
    """
    Extends model form and integrates bootstrap input class names.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fields_required = getattr(self.Meta, "fields_required", None)

        for field in self.fields:
            new_data = {
                "placeholder": f"{field}",
                "class": "form-control"
            }
            if not isinstance(self.fields[str(field)].widget, Select):
                self.fields[str(field)].widget.attrs.update(new_data)

            # Check if the field is required and add "required_css_class" to it.
            if fields_required:
                if field in fields_required:
                    new_data["class"] = f"form-control {required_css_class}"

                    self.fields[str(field)].widget.attrs.update(new_data)


class BootStrapMaxLengthModelForm(BootStrapModelForm):
    """
    Extends BootstrapModel for to add `max-length` class.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            new_data = {
                "placeholder": f"{field}",
                "class": "form-control max-length"
            }
            self.fields[str(field)].widget.attrs.update(new_data)


class StaffPermissionRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Check if user is authenticated and staff or not,
    if not logged in then the user will be redirected to login_url
    """

    login_url = reverse_lazy('login')

    def test_func(self):
        return self.request.user.is_staff
