import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from ..models import MobileNumber, CustomUser
from ..serializers import CustomRegisterSerializer 

# initializing the APIClient App.
client = Client()




