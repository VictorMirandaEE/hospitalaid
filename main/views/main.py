import structlog
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, FormView, UpdateView
from django_filters.views import FilterView

from main import forms, models

logger = structlog.get_logger(__name__)


### Hospital views


class AidRequestCreateView(LoginRequiredMixin, CreateView):
    model = models.main.AidRequest
    form_class = forms.AidRequestCreateForm
    success_url = reverse_lazy("aidrequestforhospital_list")

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.hospital = self.request.user.hospital
        obj.save()
        logger.info(
            "AidRequest created", email=self.request.user.email, hospital=obj.hospital
        )
        return super().form_valid(form)


class AidRequestUpdateView(LoginRequiredMixin, UpdateView):
    model = models.main.AidRequest
    form_class = forms.AidRequestUpdateForm
    success_url = reverse_lazy("aidrequestforhospital_list")

    def get_queryset(self):
        return self.model.objects.filter(hospital=self.request.user.hospital)


class AidRequestDeleteView(LoginRequiredMixin, DeleteView):
    model = models.main.AidRequest
    success_url = reverse_lazy("aidrequestforhospital_list")

    def get_queryset(self):
        return self.model.objects.filter(hospital=self.request.user.hospital)


@login_required
def aidrequest_status(request, pk, value):
    aid = models.main.AidRequest.objects.filter(hospital=request.user.hospital).get(
        pk=pk
    )
    aid.status = value
    aid.save()
    logger.info(
        "AidRequest status change",
        new_status=value,
        email=request.user.email,
        aidrequest=aid,
    )
    return redirect("aidrequestforhospital_detail", pk=pk)


class AidRequestDetailForHospital(LoginRequiredMixin, DetailView):
    model = models.main.AidRequest
    template_name = "main/aidrequest_detail_hospital.html"


class AidRequestListForHospital(LoginRequiredMixin, FilterView):
    model = models.main.AidRequest
    template_name = "main/aidrequest_list_hospital.html"
    filterset_fields = ["type"]

    def get_queryset(self):
        return self.model.objects.filter(hospital=self.request.user.hospital)


class SignupStep2(LoginRequiredMixin, FormView):
    success_url = reverse_lazy("aidrequestforhospital_list")
    form_class = forms.SignupStep2Form
    template_name = "main/step2_form.html"

    def get_initial(self):
        initial = super().get_initial()
        initial["name"] = self.request.user.first_name
        initial["phone"] = self.request.user.phone
        try:
            h = self.request.user.hospital
            initial["hospital_name"] = h.name
            initial["hospital_address"] = h.address
            initial["hospital_city"] = h.city
            initial["hospital_postcode"] = h.postal_code
            initial["hospital_country"] = h.country
            initial["hospital_latitude"] = h.latitude
            initial["hospital_longitude"] = h.longitude
        except models.user.User.hospital.RelatedObjectDoesNotExist:
            pass
        return initial

    def form_valid(self, form):
        self.request.user.first_name = form.cleaned_data["name"]
        self.request.user.phone = form.cleaned_data["phone"]
        self.request.user.save()
        try:
            h = self.request.user.hospital
        except models.user.User.hospital.RelatedObjectDoesNotExist:
            h = models.main.Hospital(user=self.request.user)
        h.name = form.cleaned_data["hospital_name"]
        h.address = form.cleaned_data["hospital_address"]
        h.city = form.cleaned_data["hospital_city"]
        h.postal_code = form.cleaned_data["hospital_postcode"]
        h.country = form.cleaned_data["hospital_country"]
        h.latitude = form.cleaned_data["hospital_latitude"]
        h.longitude = form.cleaned_data["hospital_longitude"]
        h.save()
        logger.info("User completed step 2.", email=self.request.user.email, hospital=h)
        return super().form_valid(form)


### Donor views


class AidRequestDetailForDonor(DetailView):
    model = models.main.AidRequest


class AidRequestListForDonor(FilterView):
    model = models.main.AidRequest
    filterset_fields = ["hospital__city", "type"]

    def get_queryset(self):
        return self.model.objects.all().order_by("-updated_at")


class HospitalDetailForDonor(DetailView):
    model = models.main.Hospital


class HospitalMap(FilterView):
    model = models.main.Hospital
    filterset_fields = ["city"]

    def get_queryset(self):
        return self.model.objects.all()


#### Unspecific views


def home(request):
    if request.user.is_authenticated:
        if request.user.first_name == "":
            return redirect(reverse("signup_step2"))
        else:
            return redirect(reverse("aidrequestforhospital_list"))
    return render(request, "home.html")


def hamburger(request):
    return render(request, "hamburger.html")


def about(request):
    return render(request, "about.html")


def language(request):
    return render(request, "language.html")


def language_home(request):
    return render(request, "language_home.html")
