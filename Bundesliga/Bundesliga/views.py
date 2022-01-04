from datetime import datetime

from django.http import HttpResponse, HttpRequest

from .settings import start_time


def is_up(_: HttpRequest):
    return HttpResponse(f"{datetime.now() - start_time}")