import random
import pdb
from django.db.models import signals
from django.dispatch import Signal
from django.contrib.auth import get_user_model
from allauth.account.signals import user_signed_up
# from .models import MobileNumber, MobileOtpConfirmation

# Setting the User model.
User = get_user_model()

# --- Commenting the Below signal, The mobile number save method is used in Serializer ---.
# def send_mobile_otp_after_registration(sender, instance, created, **kwargs):
#     if created:
#         # instance.mobile_number
#         otp = random.randint(111111, 999999)
#         obj = MobileNumber.objects.get(user=instance.user, mobile_number=instance.number)
#         p, c = MobileOtpConfirmation.objects.create(mobile_number=obj, key=)


# signals.post_save(send_mobile_otp_after_registration, sender=User)

# Provides the arguments "request", "confirmation", "mobile_numuber"
mobile_confirmed = Signal()

# Provides the arguments "request", "confirmation", "signup"
mobile_confirmation_sent = Signal()

# Provides the arguments "request", "user", "from_mobile_number"
# "to_mobile_number"
mobile_changed = Signal()

# Provides the arguments "request", "user", "mobile_number"
mobile_added = Signal()

# Provides the arguments "request", "user", "mobile_number"
mobile_removed = Signal()