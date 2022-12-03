from attr import has
from django.db import models
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.urls import reverse
from django_lifecycle import LifecycleModelMixin, hook, AFTER_UPDATE, AFTER_CREATE
from simple_history.models import HistoricalRecords

from api.hook_utils import update_available_margin, send_notification

# Create your models here.
User = get_user_model()


class NseStock(models.Model):
    name = models.CharField(max_length=250)
    code = models.CharField(max_length=250)

    class Meta:
        ordering = ["id"]

    def __str__(self) -> str:
        return f"{self.name} ({self.code})"


class WatchList(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    stocks = models.ManyToManyField(NseStock)

    class Meta:
        ordering = ["id"]

    def __str__(self) -> str:
        return f"{self.user.first_name}'s watchlist."


class OrderStatus(models.Model):
    status = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)
    message = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ["id"]

    def __str__(self) -> str:
        return f"{self.status}"

    def get_absolute_url(self):
        return reverse("backoffice_orderstatus_detail", kwargs={"pk": self.pk})


class OrderType(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ["id"]

    def __str__(self) -> str:
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse("backoffice_ordertype_detail", kwargs={"pk": self.pk})


class OrderAction(models.Model):
    action = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ["id"]

    def __str__(self) -> str:
        return f"{self.action}"

    def get_absolute_url(self):
        return reverse("backoffice_orderaction_detail", kwargs={"pk": self.pk})


class OrderProduct(models.Model):
    product = models.CharField(max_length=250)
    abbr = models.CharField(max_length=250, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self) -> str:
        return f"{self.product} - {self.description}"


class Position(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.PROTECT, blank=True, null=True)
    order = models.OneToOneField("Order", on_delete=models.PROTECT)
    is_exited = models.BooleanField(default=False)
    pl = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    ltp = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    history = HistoricalRecords()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        get_latest_by = ['-created_on', '-updated_on']
        ordering = ["-created_on", "-updated_on"]

    @hook(AFTER_UPDATE, when='is_exited', has_changed=True, is_now=True)
    def position_exited_stoploss_order_cancellation(self):
        print("Hook Called")
        if Position.objects.filter(order=self.order).exists():
            order_obj = get_object_or_404(Order, pk=self.order.id)
            cancelled_status_obj = OrderStatus.objects.get(status="Cancelled")
            order_obj.status = cancelled_status_obj
            order_obj.save()
            print("Order Changes Saved!")

    def __str__(self) -> str:
        return f"{self.order.order_id} - {self.is_exited}"


class Order(LifecycleModelMixin, models.Model):

    user = models.ForeignKey(User, on_delete=models.PROTECT)
    order_id = models.CharField(max_length=250, null=True, blank=True)
    stock = models.ForeignKey(NseStock, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(decimal_places=2, max_digits=8)
    stop_loss = models.DecimalField(decimal_places=2, max_digits=8)
    margin = models.CharField(max_length=250, blank=True, null=True)
    order_type = models.ForeignKey(
        OrderType, on_delete=models.PROTECT, default=1, null=True, blank=True)
    action = models.ForeignKey(
        OrderAction, on_delete=models.PROTECT, null=True, blank=True)
    status = models.ForeignKey(
        OrderStatus, on_delete=models.PROTECT, default=1, null=True, blank=True)
    product = models.ForeignKey(
        OrderProduct, on_delete=models.PROTECT, null=True, blank=True)
    leverage = models.CharField(
        max_length=250, blank=True, null=True, default="2x")
    history = HistoricalRecords()
    is_deleted = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        get_latest_by = ['-created_on', '-updated_on']
        ordering = ["-created_on", "-updated_on"]

    @hook(AFTER_CREATE)
    @hook(AFTER_UPDATE, when='margin', has_changed=True)
    def available_margin_update(self):
        user = self.user
        fund_obj = UserFund.objects.filter(user=user)
        if fund_obj.exists():
            update_available_margin(
                fund_obj=fund_obj.first(), margin=self.margin)

    @hook(AFTER_UPDATE)
    def order_update_notification(self):
        admin_msg = f"{self.user.get_full_name()} has updated their order {self.order_id}"
        notification_type = "order_notification"

        if self.is_deleted:
            admin_msg = f"{self.user.get_full_name()} has deleted the order ({self.order_id})"


        send_notification('admin_notifications', admin_msg)
        send_notification('order_updates', "Order Updated!")

        admin_notification_obj = AdminNotifications(msg=admin_msg, notification_type=notification_type)
        admin_notification_obj.save()

    @hook(AFTER_UPDATE, when='status.status', has_changed=True, is_now="Executed")
    def create_order_position(self):
        print("Hook Called")
        if not Position.objects.filter(order=self).exists():
            print("Creating Order Position")
            Position.objects.create(order=self, user=self.user)
            print("Creating Order Position")

    def __str__(self) -> str:
        return f"{self.user.first_name} {self.stock.name} - ({self.created_on})"

    def get_absolute_url(self):
        return reverse("backoffice_order_detail", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse("backoffice_order_delete", kwargs={"pk": self.pk})


class GeneratedUUIDS(models.Model):
    name = models.IntegerField(blank=True, null=True)

    def __str__(self) -> str:
        return str(self.name)


def kyc_user_directory_path(instance, filename: str) -> str:
    """
    Defining the user directory when user uploads an file.

    instance: model instance (must contain user).
    filename: name of the file.
    """

    return 'user_{0}/{1}'.format(instance.user.id, filename)


class KYCDocumentName(models.Model):
    name = models.CharField(max_length=250)
    rule = models.CharField(max_length=250, blank=True, null=True)
    description = models.TextField(max_length=250, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.name} - {self.rule}"


class UserKYC(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_kyc_verified = models.BooleanField(default=False)
    history = HistoricalRecords()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse("backoffice_kyc_detail", kwargs={"pk": self.pk})

    def __str__(self) -> str:
        return f"{self.user.email} (KYC) - {'Verified' if self.is_kyc_verified else 'Not Verified'}"


class UserDocument(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    kyc = models.ForeignKey(UserKYC, related_name='userkycdocuments',
                            on_delete=models.CASCADE, blank=True, null=True)
    number = models.CharField(
        max_length=250, blank=True, null=True, unique=True)
    document_name = models.ForeignKey(KYCDocumentName,
                                      on_delete=models.CASCADE,
                                      blank=True, null=True)
    document = models.FileField(upload_to=kyc_user_directory_path)
    remarks = models.TextField(null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    history = HistoricalRecords()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"({self.user.email}) - {self.document_name}"


class UserFund(LifecycleModelMixin, models.Model):
    user = models.OneToOneField(
        User, related_name="userfunds", on_delete=models.CASCADE)
    available_margin = models.CharField(max_length=250, default=0.00)
    used_margin = models.CharField(max_length=250, default=0.00)
    available_cash = models.CharField(max_length=250, default=0.00)
    opening_balance = models.CharField(max_length=250, default=0.00)
    pay_in = models.CharField(max_length=250, default=0.00)
    pay_out = models.CharField(max_length=250, default=0.00)
    span = models.CharField(max_length=250, default=0.00)
    delivery_margin = models.CharField(max_length=250, default=0.00)
    exposure = models.CharField(max_length=250, default=0.00)
    options_premium = models.CharField(max_length=250, default=0.00)
    history = HistoricalRecords()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    @hook(AFTER_UPDATE)
    def notify_fund_change(self):
        send_notification('admin_fund_updates', "fund updated")

    class Meta:
        verbose_name = "User Fund"
        verbose_name_plural = "User Funds"

    def __str__(self) -> str:
        return f"{self.user.get_full_name()} ({self.user.email}) funds"

    def get_absolute_url(self):
        return reverse("backoffice_user_fund_update", kwargs={"pk": self.pk})


class UserBankDetail(models.Model):
    user = models.ForeignKey(
        User, related_name="userbank", on_delete=models.CASCADE)
    bank_name = models.CharField(max_length=250, blank=True, null=True)
    account_number = models.CharField(
        max_length=250, blank=True, null=True, unique=True)
    ifsc_code = models.CharField(max_length=250, null=True, blank=True)
    history = HistoricalRecords()
    created_at = models.DateTimeField(auto_now_add=timezone.now)
    updated_at = models.DateTimeField(auto_now=timezone.now)

    def __str__(self) -> str:
        return f"{self.user.get_full_name()} Bank Detail"

    def get_absolute_url(self):
        return reverse("backoffice_user_bank_detail_update", kwargs={"pk": self.pk})


def user_bank_documents_path(instance):
    return 'user_{0}'.format(instance.bank.id)

class UserBankDocuments(models.Model):
    bank = models.ForeignKey(UserBankDetail, related_name="bank_documents", on_delete=models.CASCADE)
    document = models.FileField(user_bank_documents_path)
    is_approved = models.BooleanField(default=False)
    remarks = models.TextField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=timezone.now)
    updated_on = models.DateTimeField(auto_now=timezone.now)
    history = HistoricalRecords()

    def __str__(self) -> str:
        return f"{self.bank.bank_name} - document"


class UserNotifications(models.Model):
    user = models.ForeignKey(
        User, related_name="usernotifications", on_delete=models.CASCADE)
    msg = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=timezone.now)
    updated_at = models.DateTimeField(auto_now=timezone.now)

    def __str__(self) -> str:
        return f"{self.user.get_full_name()} - {self.msg}"


class AdminNotifications(models.Model):
    msg = models.TextField(blank=True, null=True)
    notification_type = models.CharField(max_length=250, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=timezone.now)
    updated_at = models.DateTimeField(auto_now=timezone.now)

    # @hook(AFTER_CREATE)
    # def send_admin_notification(self):
    #     """
    #     Hook to send Admin notification after the object is created.
    #     """
    #     send_notification('admin_notifications', self.msg)

    def __str__(self) -> str:
        return str(self.msg)