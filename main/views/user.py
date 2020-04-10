import logging

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpResponseBadRequest
from django.shortcuts import render

from main.models.user import User

logger = logging.getLogger(__name__)

from sesame import utils
from django.core.mail import send_mail


def signup_magiclink(request):
    if request.method == "POST":
        email = request.POST.get("email")
        user, created = User.objects.get_or_create(email=email)
        login_token = utils.get_query_string(user)
        login_link = "http://127.0.0.1:8000/{}".format(login_token)

        html_message = """
        <p>Hi there,</p>
        <p>Here is your <a href="{}">magic link</a> </p>
        <p>Thanks,</p>
        <p>Django Admin</p>
        """.format(login_link)

        send_mail(
            'Django Magic Link',
            html_message,
            'admin@domain.com',
            [email],
            fail_silently=False,
            html_message=html_message
        )
        return render(request, "magiclink_sent.html", context={"email": email})

    return HttpResponseBadRequest()
