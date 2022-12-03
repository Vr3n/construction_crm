import datetime
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


# Create your models here.


class ChannelPartnerOwner(models.Model):
    name = models.CharField(max_length=256)
    mobile_number = models.CharField(max_length=10)
    whatsapp_no = models.CharField(max_length=10, null=True, blank=True)
    email_id = models.EmailField(null=True, blank=True)
    pan_no = models.CharField(max_length=256, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.name)


class ChannelPartnerMaster(models.Model):
    owner = models.ForeignKey(ChannelPartnerOwner, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.company_name)


class ChannelPartnerAddressMaster(models.Model):
    channel_partner = models.ForeignKey(
        ChannelPartnerMaster, on_delete=models.CASCADE)
    address_line1 = models.TextField()
    city = models.ForeignKey("CityMaster", null=True,
                             blank=True, on_delete=models.CASCADE)
    taluka = models.ForeignKey(
        "TalukaMaster", null=True, blank=True, on_delete=models.CASCADE)
    district = models.ForeignKey(
        "DistrictMaster", null=True, blank=True, on_delete=models.CASCADE)
    state = models.ForeignKey("StateMaster", null=True,
                              blank=True, on_delete=models.CASCADE)
    country = models.ForeignKey(
        "CountryMaster", null=True, blank=True, on_delete=models.CASCADE)
    pincode = models.ForeignKey(
        "PinCodeMaster", null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{str(self.channel_partner)} Address"


class LeadMaster(models.Model):
    title = models.CharField(max_length=256, blank=True, null=True)
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256, null=True, blank=True)
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(
        max_length=10, unique=True, null=True, blank=True)
    interested_in = models.TextField(null=True, blank=True)
    lead_manager = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="lead_manager", null=True, blank=True, on_delete=models.CASCADE)
    attended_lead_manager = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="attended_lead_manager", null=True, blank=True, on_delete=models.CASCADE)
    budget = models.CharField(max_length=256, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    source = models.CharField(max_length=256, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'


class LeadSiteVisitDetailMaster(models.Model):
    lead = models.ForeignKey("LeadMaster", on_delete=models.CASCADE)
    detail = models.TextField()
    visited_on = models.DateTimeField(default=datetime.datetime)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{str(lead)} {self.visited_on.date()}'


class CountryMaster(models.Model):
    country = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.country)


class StateMaster(models.Model):
    state = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.state)


class DistrictMaster(models.Model):
    district = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.district)


class TalukaMaster(models.Model):
    taluka = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.taluka)


class CityMaster(models.Model):
    city = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.city)


class PinCodeMaster(models.Model):
    pincode = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.pincode)


class LeadAddressMaster(models.Model):
    lead = models.ForeignKey("LeadMaster", on_delete=models.CASCADE)
    address_line1 = models.TextField()
    city = models.ForeignKey("CityMaster", on_delete=models.CASCADE)
    taluka = models.ForeignKey("TalukaMaster", on_delete=models.CASCADE)
    district = models.ForeignKey("DistrictMaster", on_delete=models.CASCADE)
    state = models.ForeignKey("StateMaster", on_delete=models.CASCADE)
    country = models.ForeignKey("CountryMaster", on_delete=models.CASCADE)
    pincode = models.ForeignKey("PinCodeMaster", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{str(self.lead)} Address"


class MobileNumberPrefix(models.Model):
    prefix = models.CharField(max_length=256, default="91")
    country_abbr = models.CharField(max_length=256, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.prefix)


class LeadMobileNumberMaster(models.Model):
    lead = models.ForeignKey("LeadMaster", on_delete=models.CASCADE)
    mobile_number = models.CharField(max_length=10, unique=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{str(self.lead)} ({self.mobile_number})"


class DeveloperMaster(models.Model):
    developer = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.developer)


class ProjectAmenities(models.Model):
    amenities = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.amenities)


class ProjectMaster(models.Model):
    project = models.CharField(max_length=256)
    area = models.CharField(max_length=256)
    amenities = models.ForeignKey(
        "ProjectAmenities", null=True, blank=True, on_delete=models.CASCADE)
    market_value = models.BigIntegerField(
        verbose_name=_("Market Value"), null=True, blank=True)
    admin_rate = models.BigIntegerField(
        verbose_name=_("Admin Rate"), null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.project)


class BuildingMaster(models.Model):
    project = models.ForeignKey("ProjectMaster", on_delete=models.CASCADE)
    building = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.building}"


class WingMaster(models.Model):
    building = models.ForeignKey("BuildingMaster", on_delete=models.CASCADE)
    wing = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.wing} ({str(self.building)})"


class FlatTypeMaster(models.Model):
    flat_type = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.flat_type)


class FlatMaster(models.Model):
    wing = models.ForeignKey("WingMaster", on_delete=models.CASCADE)
    flat_no = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{str(self.wing)} {self.flat_no}"
