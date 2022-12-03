from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase, modify_settings, override_settings
from rest_framework.exceptions import ErrorDetail

from ..serializers import CustomRegisterSerializer

User = get_user_model()

