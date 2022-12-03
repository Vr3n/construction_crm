from django import forms
from api.models import Order, OrderType, OrderStatus, OrderAction, NseStock, UserBankDetail, WatchList, KYCDocumentName, UserKYC, UserDocument, UserFund
from backoffice.models import LeadMaster
from django.contrib.auth import authenticate
from .mixins import BootStrapModelForm


class LeadMasterForm(BootStrapModelForm):

    class Meta:
        model = LeadMaster
        fields = [
            "title",
            "first_name",
            "last_name",
            "email",
            "mobile_number",
            "interested_in",
            "lead_manager",
            "attended_lead_manager",
            "budget",
            "source",
        ]
        exclude = ["is_deleted"]


class OrderForm(BootStrapModelForm):

    class Meta:
        model = Order
        fields = "__all__"
        exclude = ["is_deleted"]


class OrderTypeForm(BootStrapModelForm):

    class Meta:
        model = OrderType
        fields = "__all__"


class OrderStatusForm(BootStrapModelForm):

    class Meta:
        model = OrderStatus
        fields = "__all__"


class OrderActionForm(BootStrapModelForm):

    class Meta:
        model = OrderAction
        fields = "__all__"


class NseStockForm(BootStrapModelForm):

    class Meta:
        model = NseStock
        fields = "__all__"


class WatchListForm(BootStrapModelForm):

    class Meta:
        model = WatchList
        fields = "__all__"


class KYCDocumentForm(BootStrapModelForm):
    class Meta:
        model = KYCDocumentName
        fields = "__all__"


class UserKYCForm(BootStrapModelForm):
    class Meta:
        model = UserKYC
        fields = "__all__"


class UserDocumentForm(BootStrapModelForm):
    class Meta:
        model = UserDocument
        fields = [
            "user",
            "kyc",
            "number",
            "document_name",
            "document",
        ]


class UserFundForm(BootStrapModelForm):
    class Meta:
        model = UserFund
        fields = "__all__"


class UserBankDetailForm(BootStrapModelForm):
    class Meta:
        model = UserBankDetail
        fields = "__all__"


class ResendEmailForm(forms.Form):
    """
    Getting the User from the backoffice user table.
    """
    user = forms.IntegerField()
