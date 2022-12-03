"""
Utility function for apis.

"""
import os
import requests
from nsetools import Nse
from urllib.error import URLError, HTTPError
import channels.layers
from asgiref.sync import async_to_sync
import uuid
import random
import pdb

from .models import NseStock, GeneratedUUIDS

# Initializing the NSE driver object.
nse = Nse()


def get_stock_quote(stock_code: str) -> dict:
    """Listing the quote for the selected Stock.

    Takes in stock_code and returns quote related to
    that stock.

    Parameters
    ----------
    stock_code: str
        The code of the stock you want to fetch quote for.

    Raises
    ---------

    URLError

    HTTPError

    """

    try:
        is_valid_code = nse.is_valid_code(stock_code)

        if is_valid_code:
            quote = nse.get_quote(stock_code)
            return quote

        return {
            "message": "Please check your stock code and try again!"
        }
    except URLError as e:
        print(e.__dict__)
        return {
            "message": "Please check URL or Internet Connection"
        }
    except HTTPError as e:
        print(e.__dict__)
        return {
            "message": "Please check URL or Internet Connection"
        }


def get_stock_names() -> dict:
    return nse.get_stock_codes()


def get_stock_names_save_to_db():
    """
    Get the stock names and code,
    save them the NseStocks model.
    """

    stock_codes = get_stock_names()
    for k, v in stock_codes.items():
        if k.lower() != "symbol":
            obj, created = NseStock.objects.get_or_create(
                name=v,
                code=k
            )
            if created:
                print(f"Adding -> {k}: {v}")
                print(f"New Code added -> {k}: {v}")


def send_notification(room_name: str, msg: str):
    """
    Utility function to Send Custom notifications,
    to the Channels.

    room_name: str -> Channel room name you want to send notification.
    msg: str -> notification message to channel room.
    """

    channel_layer = channels.layers.get_channel_layer()
    async_to_sync(channel_layer.group_send)(room_name, {
        'type': 'notification',
        'message': msg
    })


def send_sms(receiver_mobile_number: list, message: str, template_id: str):
    # SMS_ENDPOINT = "http://login.swarajinfotech.com/domestic/sendsms/jsonapi.php"

    if isinstance(receiver_mobile_number, str):
        receiver_mobile_number = [receiver_mobile_number]

    SMS_URL = f"http://login.swarajinfotech.com/domestic/sendsms/bulksms_v2.php?apikey={os.environ.get('SMS_APIKEY')}&templateId={template_id}&type=TEXT&sender={os.environ.get( 'SMS_SENDER' )}&mobile={','.join([str(x) for x in receiver_mobile_number])}&message={message}"

    # HEADERS = {
    #     'apiKey': SMS_APIKEY
    # }
    # BODY = {
    #     "data": [{
    #         "destination": receiver_mobile_number[0],
    #         "source": SMS_SENDER,
    #         "type": "0",
    #         "content": message,
    #     }]
    # }

    # res = requests.post(SMS_ENDPOINT, headers=HEADERS, json=BODY)
    res = requests.post(SMS_URL)
    print("Post request sent!")
    print(res)
    if res.status_code == 200:
        print("Successfull")

    print(res.content)


def get_unique_number(number: int) -> bool:
    num = GeneratedUUIDS.objects.filter(name=number)
    if num.exists():
        number = random.randint(100000, 999999)
        get_unique_number(number)
    GeneratedUUIDS.objects.create(name=number)
    return number


def create_order_reference_id(user) -> str:
    user_initials = f"{user.first_name[:2]}_{user.last_name[:2]}"
    random_number = get_unique_number(random.randint(100000, 999999))
    ref_id = 'ORD' + user_initials + str(random_number)
    return ref_id