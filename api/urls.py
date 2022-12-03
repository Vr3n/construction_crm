from django.urls import path
from .views import (NseStockListView, NseStockCodeListView,
                    NseStockNameListView, PositionListView, UserFundListView, checkUserAuthenticated, WatchListView, WatchListCreateView, OrderListView,
                    OrderCreateView, OrderUpdateView, order_delete_view,
                    WatchListDeleteView, watchlist_item_delete_view, userLogout, UserKYCRetriveAPIView,
                    KYCDocumentNameListView,
                    UserBankDetailListView, UserBankDetailCreateView, UserBankDetailUpdateDeleteView,
                    )


urlpatterns = [

    path('positions/', PositionListView.as_view(), name="positions_list"),

    path("kyc/", UserKYCRetriveAPIView.as_view(), name="kyc_retrieve"),
    path("kyc_document_list/", KYCDocumentNameListView.as_view(),
         name="kyc_documents"),

    path('funds/', UserFundListView.as_view(), name="user_funds"),

    path("user/banks/", UserBankDetailListView.as_view(), name="user_banks"),
    path("user/bank/<int:pk>/", UserBankDetailUpdateDeleteView.as_view(), name="user_bank_detail_update_delete"),
    path("user/bank/create/", UserBankDetailCreateView.as_view(), name="user_bank_create"),

    path('orders/delete/<int:pk>/', order_delete_view, name="order_delete"),
    path('orders/update/<int:pk>/', OrderUpdateView.as_view(), name="order_update"),
    path('orders/create/', OrderCreateView.as_view(), name="order_create"),
    path('orders/', OrderListView.as_view(), name="order_list"),

    path('watchlist/item/delete/<str:code>/',
         watchlist_item_delete_view, name="watchlist_item_delete"),
    path('watchlist/delete/<int:pk>/',
         WatchListDeleteView.as_view(), name="watchlist_delete"),
    path('watchlist/create/', WatchListCreateView.as_view(),
         name="watch_list_create"),
    path('watchlist/', WatchListView.as_view(), name="watch_list"),

    path('stock/list/names/', NseStockNameListView.as_view(), name="stock_name_list"),
    path('stock/list/codes/', NseStockCodeListView.as_view(), name="stock_code_list"),
    path('stock/list/', NseStockListView.as_view(), name="stock_list"),
    path('user_authenticated/', checkUserAuthenticated,
         name="is_user_authenticated"),
    path("users/logout/", userLogout, name="userLogout")
]
