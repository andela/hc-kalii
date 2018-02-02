from django import forms
from hc.api.models import Channel, Department


class NameTagsForm(forms.Form):
    name = forms.CharField(max_length=100, required=False)
    tags = forms.CharField(max_length=500, required=False)
    department = forms.ModelChoiceField(queryset=Department.objects.all(), \
            widget=forms.Select(), required=False)

    def clean_tags(self):
        l = []

        for part in self.cleaned_data["tags"].split(" "):
            part = part.strip()
            if part != "":
                l.append(part)

        return " ".join(l)


class TimeoutForm(forms.Form):
    """
    User can set desired timeout and grace values
    Minimun: 60 seconds (1 minute)
    Maximum: 7776000 seconds (90 days)
    """

    timeout = forms.IntegerField(min_value=60, max_value=7776000)
    grace = forms.IntegerField(min_value=60, max_value=7776000)
    interval = forms.IntegerField(min_value=60, max_value=2592000)

class AddChannelForm(forms.ModelForm):

    class Meta:
        model = Channel
        fields = ['kind', 'value']

    def clean_value(self):
        value = self.cleaned_data["value"]
        return value.strip()


class AddWebhookForm(forms.Form):
    error_css_class = "has-error"

    value_down = forms.URLField(max_length=1000, required=False)
    value_up = forms.URLField(max_length=1000, required=False)

    def get_value(self):
        return "{value_down}\n{value_up}".format(**self.cleaned_data)

class DepartmentForm(forms.ModelForm):
    """ Form for creating/updating a department """

    class Meta:
        model = Department
        fields = ['name']

    def clean_name(self):
        name = self.cleaned_data["name"]
        return name.strip()
