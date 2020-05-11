import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import (CreateView, DeleteView, FormView,
                                       UpdateView)
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django_filters.views import FilterView
from django import forms

from main import models

logger = logging.getLogger(__name__)


####

class AidRequestForm(forms.ModelForm):
    class Meta:
        model = models.main.AidRequest
        fields = [
            "type",
            "status",
            "comments",
            "manufacturer",
            "model",
            "serial_number",
        ]
        #widgets = {'type': forms.HiddenInput}

class AidRequestCreateView(LoginRequiredMixin, CreateView):
    model = models.main.AidRequest
    form_class = AidRequestForm
    success_url = reverse_lazy("aidrequestforhospital_list")

    def form_valid(self, form):
        obj = form.save(commit=False)
        hospital = self.request.user.hospital_set.all().first()
        obj.hospital = hospital
        obj.save()
        return super().form_valid(form)


class AidRequestUpdateView(LoginRequiredMixin, UpdateView):
    model = models.main.AidRequest
    form_class = AidRequestForm
    success_url = reverse_lazy("aidrequestforhospital_list")

    def get_queryset(self):
        hospitals = models.main.Hospital.objects.filter(user=self.request.user)
        return self.model.objects.filter(hospital__in=hospitals)


class AidRequestDeleteView(LoginRequiredMixin, DeleteView):
    model = models.main.AidRequest
    success_url = reverse_lazy("aidrequestforhospital_list")

    def get_queryset(self):
        hospitals = models.main.Hospital.objects.filter(user=self.request.user)
        return self.model.objects.filter(hospital__in=hospitals)


@login_required
def aidrequest_close(request, pk):
    hospitals = models.main.Hospital.objects.filter(user=request.user)
    aid = models.main.AidRequest.objects.filter(hospital__in=hospitals).get(pk=pk)
    aid.closed = True
    aid.save()
    return redirect("aidrequestforhospital_list")

class AidRequestDetailForHospital(DetailView):
    model = models.main.AidRequest
    template_name = "main/aidrequest_detail_hospital.html"


class AidRequestListForHospital(FilterView):
    model = models.main.AidRequest
    template_name = "main/aidrequest_list_hospital.html"
    filterset_fields = ["type"]

    def get_queryset(self):
        hospitals = models.main.Hospital.objects.filter(user=self.request.user)
        return self.model.objects.filter(hospital__in=hospitals)


class SignupStep2Form(forms.Form):
    name = forms.CharField(max_length=32)
    phone = forms.CharField(max_length=32)
    hospital_name = forms.CharField(max_length=32)
    hospital_address = forms.CharField(max_length=32)
    hospital_city = forms.CharField(max_length=32)
    hospital_postcode = forms.CharField(max_length=32)
    hospital_country = forms.CharField(max_length=32)
    

class SignupStep2(LoginRequiredMixin, FormView):
    success_url = reverse_lazy("aidrequestforhospital_list")
    form_class = SignupStep2Form
    template_name = "main/step2_form.html"

    def get_initial(self):
        initial = super().get_initial()
        initial['name'] = self.request.user.first_name
        initial['phone'] = self.request.user.phone
        h = models.main.Hospital.objects.filter(user=self.request.user).first()
        initial['hospital_name'] = h.name
        initial['hospital_address'] = h.address
        initial['hospital_city'] = h.city
        initial['hospital_postcode'] = h.postal_code
        initial['hospital_country'] = h.country
        return initial

    def form_valid(self, form):
        self.request.user.first_name = form.cleaned_data['name']
        self.request.user.phone = form.cleaned_data['phone']
        self.request.user.save()
        h, _ = models.main.Hospital.objects.get_or_create(name=form.cleaned_data['hospital_name'])
        h.address = form.cleaned_data['hospital_address']
        h.city = form.cleaned_data['hospital_city']
        h.postal_code = form.cleaned_data['hospital_postcode']
        h.country = form.cleaned_data['hospital_country']
        h.user = self.request.user
        h.save()
        return super().form_valid(form)

###
class AidRequestDetailForDonor(DetailView):
    model = models.main.AidRequest


class HospitalDetailForDonor(DetailView):
    model = models.main.Hospital


class HospitalListForDonor(FilterView):
    model = models.main.Hospital
    filterset_fields = ["city"]

    def get_queryset(self):
        return self.model.objects.all()


class AidRequestListForDonor(FilterView):
    model = models.main.AidRequest
    filterset_fields = ["hospital__city", "type"]

    def get_queryset(self):
        return self.model.objects.all().order_by("-updated_at")

def home(request):
    if request.user.is_authenticated:
        if request.user.first_name == "":
            return redirect(reverse("signup_step2"))
        else:
            return redirect(reverse("aidrequestforhospital_list"))
    return render(request, "home.html")
