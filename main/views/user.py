import logging

from django import forms
from django.core.mail import send_mail
from django.views.generic.edit import FormView
from django.urls import reverse, reverse_lazy
from sesame import utils

from main.models.user import User

logger = logging.getLogger(__name__)


class EmailForm(forms.Form):
    email = forms.EmailField()


class Signup(FormView):
    form_class = EmailForm
    template_name = "signup.html"

    def get_success_url(self):
        return reverse("signup") + "?sent=1"

    def form_valid(self, form):
        email = form.cleaned_data['email']
        user, created = User.objects.get_or_create(email=email)
        login_token = utils.get_query_string(user)
        login_link = "http://{}/{}".format(self.request.get_host(), login_token)

        html_message = """
        <p>Hi there,</p>
        <p>Here is your <a href="{}">login link</a> </p>
        <p>Thanks,</p>
        <p>HospitalAid Admin</p>
        """.format(login_link)

        send_mail(
            'Hospital Aid Login Link',
            html_message,
            'admin@domain.com',
            [email],
            fail_silently=False,
            html_message=html_message
        )
        return super().form_valid(form)

