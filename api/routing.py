from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    # re_path(r'ws/stocks/$',
    #         consumers.StockConsumer.as_asgi()),
    re_path(r'ws/admin_notifications/$',
            consumers.AdminNotificationsConsumer.as_asgi()),
    re_path(r'ws/order_updates/$',
            consumers.OrderUpdatesConsumer.as_asgi()),
    re_path(r'ws/admin_fund_updates/$',
            consumers.AdminFundsUpdateConsumer.as_asgi()),
]
