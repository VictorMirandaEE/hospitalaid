import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import (CreateView, DeleteView, FormView,
                                       UpdateView)
from django.views.generic.list import ListView
from django_filters.views import FilterView
from django_tables2.views import SingleTableView

from main import models

logger = logging.getLogger(__name__)


class HospitalCreateView(LoginRequiredMixin, CreateView):
    model = models.main.Hospital
    fields = [
        "name",
        "phone",
        "address",
        "city",
        "postal_code",
        "state",
        "country",
    ]
    success_url = reverse_lazy("hospital_list")

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return super().form_valid(form)


class HospitalUpdateView(LoginRequiredMixin, UpdateView):
    model = models.main.Hospital
    fields = [
        "name",
        "phone",
        "address",
        "city",
        "postal_code",
        "state",
        "country",
    ]
    success_url = reverse_lazy("hospital_list")

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class HospitalDeleteView(LoginRequiredMixin, DeleteView):
    model = models.main.Hospital
    success_url = reverse_lazy("hospital_list")

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class HospitalListView(LoginRequiredMixin, FilterView):
    model = models.main.Hospital
    filterset_fields = ["city", "country"]

    def get_queryset(self):
        return self.model.objects.all()


####


class AidRequestCreateView(LoginRequiredMixin, CreateView):
    model = models.main.AidRequest
    fields = [
        "type",
        "details",
        "equipment_brand",
        "equipment_model",
        "equipment_serialno",
    ]
    success_url = reverse_lazy("aidrequest_list")

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.hospital_id = self.request.GET.get("hospital")
        obj.save()
        return super().form_valid(form)


class AidRequestUpdateView(LoginRequiredMixin, UpdateView):
    model = models.main.AidRequest
    fields = [
        "type",
        "details",
        "assigned_to",
        "status",
    ]
    success_url = reverse_lazy("aidrequest_list")

    def get_queryset(self):
        hospitals = models.main.Hospital.objects.filter(user=self.request.user)
        return self.model.objects.filter(hospital__in=hospitals)


class AidRequestDeleteView(LoginRequiredMixin, DeleteView):
    model = models.main.AidRequest
    success_url = reverse_lazy("aidrequest_list")

    def get_queryset(self):
        hospitals = models.main.Hospital.objects.filter(user=self.request.user)
        return self.model.objects.filter(hospital__in=hospitals)


class AidRequestListView(FilterView):
    model = models.main.AidRequest
    filterset_fields = ["hospital", "status"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            hospitals = models.main.Hospital.objects.filter(user=self.request.user)
            context["hospitals_managed"] = hospitals
        return context

    def get_queryset(self):
        return self.model.objects.all().order_by("-updated_at")


###


class AidResponseForMeListView(LoginRequiredMixin, FilterView):
    model = models.main.AidResponse
    filterset_fields = ["aid_request"]

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user).order_by("-created_at")


class AidResponseCreateView(LoginRequiredMixin, CreateView):
    model = models.main.AidResponse
    fields = [
        "comment",
    ]
    success_url = reverse_lazy("aidrequest_list")

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.aid_request_id = self.request.GET.get("aidrequest")
        obj.user = self.request.user
        obj.save()
        return super().form_valid(form)
