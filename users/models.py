import datetime
from unittest import signals
from django.conf import settings
from django.utils import timezone
from django.db import models, transaction
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from .utils import user_mobile
from .managers import CustomUserManager, MobileNumberManager

# Create your models here.


class MobileNumber(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             verbose_name=_("user"), on_delete=models.CASCADE)
    mobile_number = models.CharField(
        unique=True, max_length=10, null=True, blank=True)
    is_verified = models.BooleanField(
        verbose_name=_("is_verified"), default=False)
    is_primary = models.BooleanField(
        verbose_name=_("is_primary"), default=False)

    class Meta:
        verbose_name = _("mobile number")
        verbose_name_plural = _("mobile numbers")
        unique_together = [(
            "user",
            "mobile_number"
        )]

    objects = MobileNumberManager()

    def set_as_primary(self, conditional=False):
        old_primary = MobileNumber.objects.get_primary(self.user)
        if old_primary:
            if conditional:
                return False
            old_primary.is_primary = False
            old_primary.save()
        self.is_primary = True
        self.save()
        user_mobile(self.user, self.mobile_number)
        self.user.save()
        return True

    def change(self, request, new_mobile, confirm=True):
        """
        Given a new mobile address, change self and re-confirm.
        """
        with transaction.atomic():
            user_mobile(self.user, new_mobile)
            self.user.save()
            self.mobile_number = new_mobile
            self.is_verified = False
            self.save()

    def __str__(self) -> str:
        return f"{self.mobile_number} - {self.user.first_name}"

class MobileOtpConfirmation(models.Model):
    mobile_number = models.ForeignKey(MobileNumber, verbose_name=_("mobile number"), on_delete=models.CASCADE)
    created = models.DateTimeField(verbose_name=_("created"), default=timezone.now)
    sent = models.DateTimeField(verbose_name=_("sent"), null=True)
    key = models.CharField(verbose_name=_("key"), max_length=6, unique=True)

    class Meta:
        verbose_name = _("mobile otp confirmation")
        verbose_name_plural = _("mobile otp conformations")

    @classmethod
    def create(cls, mobile_number):
        import pyotp
        key = pyotp.TOTP('base32secret3232')
        return cls._default_manager.create(mobile_number=mobile_number, key=key)

    def key_expired(self):
        expiration_date = self.sent + datetime.timedelta(
            seconds=60*5
        )
        return expiration_date <= timezone.now()

    key_expired.boolean = True

    def confirm_mobile_number(self, request, mobile_number):
        """
        Marks the Mobile number as confirmed in db
        """
        mobile_number.is_verified = True
        mobile_number.set_as_primary(conditional=True)
        mobile_number.save()

    def confirm(self, request):
        if not self.key_expired() and not self.mobile_number.is_verified:
            mobile_number = self.mobile_number
            self.confirm_mobile_number(request, mobile_number)
            signals.mobile_confirmed.send(
                sender=self.__class__,
                request=request,
                mobile_number=self.mobile_number
            )
            return mobile_number

class MemberRole(models.Model):
    role = models.CharField(max_length=256)

    def __str__(self) -> str:
        return str(self.role)

class CustomUser(AbstractUser):
    mobile_number = models.CharField(max_length=10, null=True, blank=True)
    max_mobile_numbers = models.IntegerField(
        default=2, verbose_name=_('max mobile number'), null=True, blank=True)
    mobile_otp = models.CharField(max_length=6, null=True, blank=True)

    objects = CustomUserManager()

    def __str__(self) -> str:
        return f"{self.username} ({self.email})"


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_img = models.ImageField(
        upload_to="user/profile_img/", default='default_avatar.png')
    about = models.TextField(verbose_name=_("About you"))

    def __str__(self) -> str:
        return f"{self.user.first_name} - Profile"
