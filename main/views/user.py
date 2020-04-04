import logging

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import FormView

from main.forms.user import UserCreationForm

logger = logging.getLogger(__name__)


class SignupView(FormView):
    template_name = "registration/signup.html"
    form_class = UserCreationForm

    def get_success_url(self):
        redirect_to = self.request.GET.get("next", "/")
        return redirect_to

    def get_success_url_hospital(self):
        redirect_to = reverse("hospital_create")
        return redirect_to

    def form_valid(self, form):
        form.save()

        email = form.cleaned_data.get("email")
        raw_password = form.cleaned_data.get("password1")
        logger.info("New signup for email=%s through SignupView", email)

        user = authenticate(email=email, password=raw_password)
        login(self.request, user)

        messages.info(self.request, "You signed up successfully.")

        if form.cleaned_data["role"] == UserCreationForm.ROLE_AID_MANAGER:
            return HttpResponseRedirect(self.get_success_url_hospital())

        return super().form_valid(form)
