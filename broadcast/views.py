from django.http import HttpResponse
from django.shortcuts import render

from api.tasks import send_confirmation

# Create your views here.

# MESSAGE = "Dear Viren Patel,\nThankyou for registering with GreencurveSecurities\nWe are happy to have you onboard"


def test_celery(request):
    # send_confirmation.delay("Task Done", MESSAGE,
    #                         "vickyspatel@gmail.com",
    #                         ["9284270056"],
    #                         "1207163912231704631")
    return HttpResponse('<h1>Task Is Done!</h1>')
