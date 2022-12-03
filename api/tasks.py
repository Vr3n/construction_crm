"""
Celery tasks for API applicaiton.
"""

import queue
import time
import json
import asyncio
from django.core.mail import send_mail
from pprint import pprint
from threading import Thread
from celery import shared_task
from celery.utils.log import get_task_logger
from .utils import get_stock_quote, get_stock_names
from channels.layers import get_channel_layer
from pix_apidata import *

from .utils import send_sms

logger = get_task_logger(__name__)


# @shared_task(name="fetch_stock_quote_every_2_seconds")
# def task_fetch_stock_quote_every_2_seconds():
#     """
#     Fetches stock_quote every 2 seconds
#     """
#     quote = get_stock_quote('infy')
#     return quote


api = apidata_lib.ApiData()


# @shared_task
# def send_email_task():
#     send_mail('Celery Task Worked!', 'This is a proof that task worked!',
#               'noreply@greencurvesecurities.com', ["vickyspatel@gmail.com"])


@shared_task
def send_confirmation(subject: str, message: str, email_id: list, mobile_number: str, template_id: str):
    """
    Task to send confirmation when user punches an order.
    """

    send_mail(subject, message,
              'noreply@greencurvesecurities.com', [email_id])

    send_sms(mobile_number, message=message,
             template_id=template_id)


@shared_task(bind=True)
async def update_stock_prices(self, watch_list):
    # data = {}
    # available_stocks = get_stock_names()
    # for i in watch_list:
    #     if i in available_stocks.keys():
    #         pass
    #     else:
    #         watch_list.remove(i)

    # n_threads = len(watch_list)
    # thread_list = []
    # que = queue.Queue()
    # for i in range(n_threads):
    #     thread = Thread(target=lambda q, arg1: q.put({watch_list[i]: json.loads(
    #         json.dumps(get_stock_quote(arg1)))}), args=(que, watch_list[i]))
    #     thread_list.append(thread)
    #     thread_list[i].start()

    # for thread in thread_list:
    #     thread.join()

    # while not que.empty():
    #     result = que.get()
    #     data.update(result)

    api.on_connection_started(connection_started)
    api.on_connection_stopped(connection_stopped)
    key = "/745y8A+XPshmfCGilWWDfgzrJo="
    host = "apidata.accelpix.in"
    scheme = "http"
    api.on_trade_update(on_trade)
    api.on_best_update(on_best)
    api.on_refs_update(on_refs)
    api.on_srefs_update(on_srefs)
    s = await api.initialize(key, host, scheme)
    print(s)

    await api.subscribeAll(watch_list)
    print("Subscribe Done", "\n")

    # send data to channels group
    # channel_layer = get_channel_layer()

    # loop = asyncio.new_event_loop()

    # asyncio.set_event_loop(loop)

    # loop.run_until_complete(channel_layer.group_send("stock_update", {
    #     'type': 'send_stock_update',
    #     'message': data,
    # }))

    return "Task Completed"
