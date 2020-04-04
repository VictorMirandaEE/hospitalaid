import os

from django.conf import settings


def globals(request):
    data = {}
    data.update(
        {"VERSION": os.environ.get("GIT_REV", ""),}
    )
    return data
