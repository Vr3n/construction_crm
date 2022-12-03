from django.urls import path
from .views import (BackOfficeHome, LeadFormView, OrderStatusFormView,
                    OrderActionFormView, OrderTypeFormView, OrderDetailView, OrderTypeDetailView, OrderStatusDetailView, OrderActionDetailView, UserBankDetailListView, UserBankDetailUpdateView,
                    UsersTemplateView, EmailsTemplateView,
                    MobilesTemplateView, KYCTemplateView,
                    KYCDetailView,
                    KYCDocumentFormView, HxUserKYCFormView, HxUserDocumentFormView, HxKycDetailTableView,
                    UserDocumentFormView, UserFundListView, UserFundUpdateView, hx_resend_email_view, hx_order_delete_view,
                    admin_notifications_list,
                    order_list, user_funds_list
                    )

# Create your urls here.
urlpatterns = [
    path("", BackOfficeHome.as_view(), name="home"),

    # Resend Confirmation Views.
    path("hx/resend/email_confirm/", hx_resend_email_view,
         name="hx_resend_email_view"),

    # Users Urls.
    path('users/', UsersTemplateView.as_view(), name="backoffice_users"),
    path('users/emails/', EmailsTemplateView.as_view(),
         name="backoffice_user_emails"),
    path('users/mobile_numbers/', MobilesTemplateView.as_view(),
         name="backoffice_user_mobiles"),

    # Funds
    path('users/funds/', UserFundListView.as_view(),
         name="backoffice_user_funds"),
    path('funds/list/', user_funds_list,
         name="backoffice_user_funds_list"),
    path("users/fund/<int:pk>/", UserFundUpdateView.as_view(),
         name="backoffice_user_fund_update"),

    # Bank details
    path('users/bank/', UserBankDetailListView.as_view(),
         name="backoffice_user_bank_detail"),
    path("users/bank/detail/<int:pk>/", UserBankDetailUpdateView.as_view(),
         name="backoffice_user_bank_detail_update"),

    path('notifications/admin/', admin_notifications_list,
         name="admin_notifications"),

    # KYC URLS.
    path('kyc/', KYCTemplateView.as_view(), name="backoffice_kyc"),
    path('kyc/detail/<int:pk>/', KYCDetailView.as_view(),
         name="backoffice_kyc_detail"),
    path('kyc_document_master/', KYCDocumentFormView.as_view(),
         name="backoffice_document_master"),
    path('kyc/hx/kyc_form/<int:pk>/', HxUserKYCFormView.as_view(),
         name="hx_backoffice_user_kyc_form"),
    path('kyc/hx/user_document_form/<int:pk>/',
         HxUserDocumentFormView.as_view(), name="hx_backoffice_user_document_form"),
    path('kyc/hx/user_document_form/', HxUserDocumentFormView.as_view(),
         name="hx_backoffice_user_document_form"),
    path('kyc/user/user_document_form/',
         UserDocumentFormView.as_view(), name="user_document_form"),
    #     path('kyc_document_form/', KYCDocumentFormView.as_view(), name="backoffice_document_form"),
    path('kyc/hx_kyc_table/<int:pk>/',
         HxKycDetailTableView.as_view(), name="hx_kyc_table"),

    # Orders Urls.
    path("leads/", LeadFormView.as_view(), name="leads_form"),
    path("orders/list/", order_list, name="backoffice_order_list"),
    path("orders/update/<int:pk>/", OrderDetailView.as_view(),
         name="backoffice_order_detail"),
    path("orders/delete/<int:pk>/", hx_order_delete_view,
         name="backoffice_order_delete"),

    # Order Types Urls.
    path("order/types/<int:pk>/", OrderTypeDetailView.as_view(),
         name="backoffice_ordertype_detail"),
    path("order/types/", OrderTypeFormView.as_view(),
         name="backoffice_ordertype"),

    # Order Status Urls.
    path("order/status/<int:pk>/", OrderStatusDetailView.as_view(),
         name="backoffice_orderstatus_detail"),
    path("order/status/", OrderStatusFormView.as_view(),
         name="backoffice_orderstatus"),

    # Order Action Urls.
    path("order/action/<int:pk>/", OrderActionDetailView.as_view(),
         name="backoffice_orderaction_detail"),
    path("order/action/", OrderActionFormView.as_view(),
         name="backoffice_orderaction"),
]
