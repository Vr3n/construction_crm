"""
Custom Validations for Serializers and Models.
"""

import re
from rest_framework.serializers import ValidationError
from .models import MobileNumber

def unique_mobile_validator(mobile_number):
    ret = True
    try:
        MobileNumber.objects.get(mobile_number=mobile_number)
    except MobileNumber.DoesNotExist:
        return ret

    raise ValidationError("A user is already registered with this mobile number")

def digits_only_validator(value):
    reg_pattern = re.compile(r'^[0-9]*$')
    if not bool(re.search(reg_pattern, value)):
        raise ValidationError(
            "Should consist only Digits"
        )

def character_only_validator(value):
    reg_pattern = re.compile(r'^[A-Za-z]*$')
    if not bool(re.search(reg_pattern, value)):
        raise ValidationError(
            "Value should consist only characters"
        )
