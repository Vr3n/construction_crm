from django.forms import Form, ModelForm
from django.forms.widgets import Select
from django.contrib.auth.mixins import LoginRequiredMixin


class BootStrapForm(Form):
    """
    Extends  form and integrates bootstrap input class names.
    """

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
