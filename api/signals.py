from django.db.models.signals import post_save, pre_save
from django.contrib.auth import get_user_model
from .utils import send_notification, create_order_reference_id, send_sms
from .models import AdminNotifications, Order, UserBankDetail, UserFund, UserKYC

# Create your signals here.

User = get_user_model()


def assign_kyc_model_after_registration(sender, instance, created, **kwargs):
    if created:
        UserKYC.objects.create(user=instance)
        UserFund.objects.create(user=instance)

post_save.connect(assign_kyc_model_after_registration, sender=User)


def create_order_referenceid(sender, instance, **kwargs):
    """
    Creating the Reference Id for the Order, before save.
    """

    if not instance.order_id:
        ref_id = create_order_reference_id(instance.user)
        instance.order_id = ref_id


pre_save.connect(create_order_referenceid, sender=Order)


def order_notifications(sender, instance, created, **kwargs):
    """
    Sending Notifications after the Order is created.
    """

    admin_msg = None
    msg = None
    notification_type = 'order_notification'
    if created:

        msg = f"Your order is punched successfully, Order id: {instance.order_id}"

        admin_msg = f"{instance.user.get_full_name()} punched an order (Order Id: {instance.order_id})"

        send_notification('admin_notifications',msg=admin_msg)
        send_notification('order_updates', msg="Order Has been Created!")

        admin_notification_obj = AdminNotifications(msg=admin_msg, notification_type=notification_type)
        admin_notification_obj.save()
        # send_sms(instance.user.mobile_number, msg)

    else:
        msg = f"Your order was updated successfully, Order id: {instance.order_id}"
        admin_msg = f"{instance.user.get_full_name()} updated an order - {instance.order_id}"
        send_notification('admin_notifications', admin_msg)


post_save.connect(order_notifications, sender=Order)


def user_document_upload_notification(sender, instance, created, **kwargs):
    """
    Notification sent after user has uploaded an document.
    """

    admin_msg = None

    if created:
        admin_msg = f"{instance.user.get_full_name()} has uploaded {instance.document_name.name} for kyc verification."
        send_notification('admin_notifications', admin_msg)
    else:
        admin_msg = f"{instance.user.get_full_name()} has modified {instance.document_name.name} for kyc verification."
        send_notification('admin_notifications', admin_msg)
