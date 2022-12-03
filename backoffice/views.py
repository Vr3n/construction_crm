import pdb
from datetime import datetime
from typing import Any, Dict
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, FormView, UpdateView, DetailView, DeleteView, ListView
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.db.models.functions import TruncMonth
from allauth.account.models import EmailAddress
from allauth.account.utils import send_email_confirmation

from api.models import AdminNotifications, Order, OrderAction, OrderType, OrderStatus, KYCDocumentName, UserBankDetail, UserKYC, UserDocument, UserFund
from backoffice.models import LeadMaster

from users.models import MobileNumber

from .forms import LeadMasterForm, OrderForm, OrderTypeForm, OrderStatusForm, OrderActionForm, KYCDocumentForm, ResendEmailForm, UserBankDetailForm, UserKYCForm, UserDocumentForm, UserFundForm
from .mixins import StaffPermissionRequiredMixin

# Create your views here.

User = get_user_model()


class BackOfficeHome(StaffPermissionRequiredMixin, TemplateView):
    template_name = "backoffice/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["lead_data"] = LeadMaster.objects.filter(
            is_deleted=False).order_by('-updated_at')

        context["unverified_mobilenumbers"] = MobileNumber.objects.unverified()
        context["unverified_email"] = EmailAddress.objects.filter(
            verified=False, primary=True)

        context["user_count"] = User.objects.count()
        context["order_count"] = Order.objects.filter(is_deleted=False).count()

        return context


class LeadFormView(StaffPermissionRequiredMixin, FormView):
    template_name = "backoffice/forms/order_form.html"
    form_class = LeadMasterForm
    model = LeadMaster
    success_url = reverse_lazy("leads_form")

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["lead_data"] = LeadMaster.objects.filter(
            is_deleted=False).order_by('-updated_at')

        context["total_lead_count"] = LeadMaster.objects.filter(
            is_deleted=False).count()

        context["today_lead_count"] = LeadMaster.objects.annotate(
            created_at__month=TruncMonth('created_at')).count()

        context["members"] = User.objects.all()

        return context

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Order Created Successfully!",
                         extra_tags="alert alert-success alert-dismissible")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors,
                       extra_tags="alert alert-error alert-dismissible")

        return super().form_invalid(form)


def order_list(request):
    """
    Generates list of orders for updates.
    """

    order_data = Order.objects.filter(is_deleted=False).order_by('-updated_on')

    context = {
        "order_data": order_data,
        "update": True,
    }

    return render(request, 'backoffice/tables/orders/order_table.html', context=context)


class OrderDetailView(StaffPermissionRequiredMixin, UpdateView):
    """
    Update View for Order.
    """

    model = Order
    template_name = "backoffice/forms/order_detail.html"
    form_class = OrderForm

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy("backoffice_order_detail", kwargs={"pk": pk})

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Order Updated Successfully!",
                         extra_tags="alert alert-success alert-dismissible")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors,
                       extra_tags="alert alert-error alert-dismissible")

        return super().form_invalid(form)


@require_http_methods(["POST"])
def order_delete_view(request, pk):
    # Intializing Context for Templates.
    context = {}

    # fetch the Related object.
    obj = LeadMaster.object.get(id=pk)

    obj.is_deleted = True

    messages.success("Lead Deleted Successfully")

    return reverse_lazy("leads_from")


class OrderTypeFormView(StaffPermissionRequiredMixin, FormView):
    template_name = "backoffice/forms/ordertype_form.html"
    model = OrderType
    form_class = OrderTypeForm
    success_url = reverse_lazy('backoffice_ordertype')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["data"] = OrderType.objects.all()
        return context

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Order Type Created Successfully!",
                         extra_tags="alert alert-success alert-dismissible")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors,
                       extra_tags="alert alert-error alert-dismissible")
        return super().form_invalid(form)


class OrderTypeDetailView(StaffPermissionRequiredMixin, UpdateView):
    """
    Update View for Order.
    """

    model = OrderType
    template_name = "backoffice/forms/ordertype_detail.html"
    form_class = OrderTypeForm

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy("backoffice_ordertype_detail", kwargs={"pk": pk})

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Order Type Updated Successfully!",
                         extra_tags="alert alert-success alert-dismissible")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors,
                       extra_tags="alert alert-error alert-dismissible")

        return super().form_invalid(form)


class OrderStatusFormView(StaffPermissionRequiredMixin, FormView):
    template_name = "backoffice/forms/orderstatus_form.html"
    model = OrderStatus
    form_class = OrderStatusForm
    success_url = reverse_lazy('backoffice_orderstatus')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["data"] = OrderStatus.objects.all()
        return context

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Order Status Created Successfully!",
                         extra_tags="alert alert-success alert-dismissible")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors,
                       extra_tags="alert alert-error alert-dismissible")
        return super().form_invalid(form)


class OrderStatusDetailView(StaffPermissionRequiredMixin, UpdateView):
    """
    Update View for Order.
    """

    model = OrderStatus
    template_name = "backoffice/forms/orderstatus_detail.html"
    form_class = OrderStatusForm

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy("backoffice_orderstatus_detail", kwargs={"pk": pk})

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Order Status Updated Successfully!",
                         extra_tags="alert alert-success alert-dismissible")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors,
                       extra_tags="alert alert-error alert-dismissible")

        return super().form_invalid(form)


class OrderActionFormView(StaffPermissionRequiredMixin, FormView):
    template_name = "backoffice/forms/orderaction_form.html"
    form_class = OrderActionForm
    model = OrderAction
    success_url = reverse_lazy('backoffice_orderaction')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["data"] = OrderAction.objects.all()
        return context

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Order Action Created Successfully!",
                         extra_tags="alert alert-success alert-dismissible")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors,
                       extra_tags="alert alert-error alert-dismissible")
        return super().form_invalid(form)


class OrderActionDetailView(StaffPermissionRequiredMixin, UpdateView):
    """
    Update View for Order.
    """

    model = OrderAction
    template_name = "backoffice/forms/orderaction_detail.html"
    form_class = OrderActionForm

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy("backoffice_orderaction_detail", kwargs={"pk": pk})

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Order Action Updated Successfully!",
                         extra_tags="alert alert-success alert-dismissible")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors,
                       extra_tags="alert alert-error alert-dismissible")
        return super().form_invalid(form)


class UsersTemplateView(StaffPermissionRequiredMixin, TemplateView):
    template_name = "backoffice/users.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["users"] = User.objects.all()
        context["unverified_mobilenumbers"] = MobileNumber.objects.unverified()
        context["unverified_email"] = EmailAddress.objects.filter(
            verified=False, primary=True)

        return context


class EmailsTemplateView(StaffPermissionRequiredMixin, TemplateView):
    template_name = "backoffice/emails.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["emails"] = EmailAddress.objects.all()
        context["unverified_email"] = EmailAddress.objects.filter(
            verified=False, primary=True)
        return context


class MobilesTemplateView(StaffPermissionRequiredMixin, TemplateView):
    template_name = "backoffice/mobiles.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["mobile_numbers"] = MobileNumber.objects.all()
        context["unverified_mobilenumbers"] = MobileNumber.objects.unverified()
        return context


class KYCTemplateView(StaffPermissionRequiredMixin, TemplateView):
    template_name = "backoffice/user_kyc.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_kycs"] = UserKYC.objects.filter(is_kyc_verified=True)
        context["unverified_kycs"] = UserKYC.objects.filter(
            is_kyc_verified=False)
        return context


class KYCDetailView(StaffPermissionRequiredMixin, DetailView):
    template_name = "backoffice/kyc_detail.html"
    model = UserKYC

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["kyc_form"] = UserKYCForm()
        context["userdocument_form"] = UserDocumentForm()
        context["document_names"] = KYCDocumentName.objects.all()
        return context


# class KYCDocumentNameTemplateView(TemplateView):
#     template_name = "backoffice/kyc_document_master.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["document_form"] = KYCDocumentForm()
#         return context

class KYCDocumentFormView(StaffPermissionRequiredMixin, FormView):
    template_name = "backoffice/kyc_document_master.html"
    form_class = KYCDocumentForm
    model = KYCDocumentName
    success_url = reverse_lazy('backoffice_document_master')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["documents"] = KYCDocumentName.objects.filter()
        return context

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Order Action Updated Successfully!",
                         extra_tags="alert alert-success alert-dismissible")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors,
                       extra_tags="alert alert-error alert-dismissible")
        return super().form_invalid(form)


class HxUserKYCFormView(StaffPermissionRequiredMixin, UpdateView):
    template_name = "backoffice/forms/kyc/userkyc_form.html"
    form_class = UserKYCForm
    model = UserKYC

    def get_success_url(self):
        return reverse_lazy('backoffice_kyc_detail', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Kyc Updated Successfully",
                         extra_tags="alert alert-success alert-dismissible")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors,
                       extra_tags="alert alert-error alert-dismissible")
        return super().form_invalid(form)


class HxUserDocumentFormView(StaffPermissionRequiredMixin, FormView):
    """
    HTMX Partial view for form upload from Admin Dashboard,
    returns Response with custom htmx header.
    """

    template_name = "backoffice/forms/kyc/userdocument_form.html"
    form_class = UserDocumentForm
    model = UserDocument

    def get_success_url(self):
        return reverse_lazy('backoffice_kyc_detail', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # check if pk is passed in kwargs.
        if 'pk' in self.kwargs:
            context['object'] = get_object_or_404(
                UserKYC, pk=self.kwargs['pk'])

        context["document_names"] = KYCDocumentName.objects.all()
        return context

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Document Uploaded Successfully",
                         extra_tags="alert alert-success alert-dismissible")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors,
                       extra_tags="alert alert-error alert-dismissible")
        return super().form_invalid(form)


class UserDocumentFormView(LoginRequiredMixin, FormView):
    """
    Formview for User Document Uploads. From the User login.
    """

    template_name = "backoffice/forms/kyc/userdocument_form.html"
    form_class = UserDocumentForm
    model = UserDocument

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # check if pk is passed in kwargs.
        if 'pk' in self.kwargs:
            context['object'] = get_object_or_404(
                UserKYC, pk=self.kwargs['pk'])

        context["document_names"] = KYCDocumentName.objects.all()
        return context

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Document Uploaded Successfully",
                         extra_tags="alert alert-success alert-dismissible")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors,
                       extra_tags="alert alert-error alert-dismissible")
        return super().form_invalid(form)


class HxKycDetailTableView(StaffPermissionRequiredMixin, DetailView):
    template_name = "backoffice/tables/kyc/kyc_detail_table.html"
    model = UserKYC


class UserFundListView(StaffPermissionRequiredMixin, ListView):
    """
    List all the user funds.
    """

    template_name = "backoffice/user_funds.html"
    queryset = UserFund.objects.filter().order_by('-updated_on')
    context_object_name = "user_funds"


class UserFundUpdateView(StaffPermissionRequiredMixin, UpdateView):
    """
    List all the user funds.
    """

    template_name = "backoffice/forms/users/user_fund.html"
    model = UserFund
    form_class = UserFundForm

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Funds Updated Successfully",
                         extra_tags="alert alert-success alert-dismissible")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors,
                       extra_tags="alert alert-error alert-dismissible")
        return super().form_invalid(form)


class UserBankDetailListView(StaffPermissionRequiredMixin, ListView):
    """
    List all the User banks.
    """

    template_name = "backoffice/user_banks.html"
    queryset = UserBankDetail.objects.all()
    context_object_name = "user_banks"


class UserBankDetailUpdateView(StaffPermissionRequiredMixin, UpdateView):
    """
    Update the user BankDetails.
    """

    template_name = "backoffice/forms/users/user_bank.html"
    model = UserBankDetail
    form_class = UserBankDetailForm

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "BankDetails Updated Successfully",
                         extra_tags="alert alert-success alert-dismissible")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors,
                       extra_tags="alert alert-error alert-dismissible")
        return super().form_invalid(form)


def hx_resend_email_view(request):
    if request.method == "POST":
        form = ResendEmailForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            user_obj = get_object_or_404(
                UserKYC, pk=user)
            if user_obj.emailaddress_set.filter(primary=True).first().verified:
                messages.success(request, "User Already Verified")

            send_email_confirmation(request, user_obj)
            messages.success(request, "Email confirmation sent successfully!")

    return HttpResponse("OK", status=204)


@require_http_methods(['POST'])
def hx_order_delete_view(request, pk):
    obj = get_object_or_404(Order, pk=pk)
    obj.is_deleted = True
    obj.save()
    messages.success(request, "Order Deleted Successfully")

    order_data = Order.objects.filter(is_deleted=False)

    return render(request, 'backoffice/tables/orders/order_table.html', context={
        "order_data": order_data
    })


def admin_notifications_list(request):
    notifications = AdminNotifications.objects.filter().order_by(
        '-created_at')[:3]

    return render(request, 'backoffice/notifications.html', context={
        'notifications': notifications
    })


def user_funds_list(request):
    user_funds = UserFund.objects.filter().order_by('-updated_on')

    return render(request, 'backoffice/tables/users/user_funds.html', context={
        'user_funds': user_funds,
    })
