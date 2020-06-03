from django import forms

from main import models


class AidRequestCreateForm(forms.ModelForm):
    class Meta:
        model = models.main.AidRequest
        fields = [
            "type",
            "title",
            "quantity",
            "manufacturer",
            "model",
            "serial_number",
            "comments",
        ]
        widgets = {
            "type": forms.HiddenInput,
            "comments": forms.Textarea(attrs={"rows": 4}),
        }


class AidRequestUpdateForm(forms.ModelForm):
    class Meta:
        model = models.main.AidRequest
        fields = [
            "type",
            "title",
            "quantity",
            "manufacturer",
            "model",
            "serial_number",
            "comments",
        ]
        widgets = {
            "type": forms.HiddenInput,
            "comments": forms.Textarea(attrs={"rows": 4}),
        }


class SignupStep2Form(forms.Form):
    name = forms.CharField(max_length=32)
    phone = forms.CharField(max_length=32)
    hospital_name = forms.CharField(max_length=32)
    hospital_address = forms.CharField(max_length=32)
    hospital_city = forms.CharField(max_length=32)
    hospital_postcode = forms.CharField(max_length=32)
    hospital_country = forms.CharField(max_length=32)
    hospital_latitude = forms.CharField(max_length=32, widget=forms.HiddenInput())
    hospital_longitude = forms.CharField(max_length=32, widget=forms.HiddenInput())
